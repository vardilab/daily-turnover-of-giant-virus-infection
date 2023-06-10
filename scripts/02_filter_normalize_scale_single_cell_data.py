#!/bin/python3

import os
from argparse import ArgumentParser
import pandas as pd
import scprep

def main():
    args = get_args()
    print('Loading data')
    data = load_data(args.data_dir, args.file_type, args.data_file)
    # remove clutter from gene names
    new_columns = pd.Series(data.columns).str.split('\t', expand=True)[0]
    data.columns = new_columns.to_list()
    # remove ERCC (spike in)
    print('Removing spike-in')
    data = filter_ercc(data)
    print('Removing empty cells/features')
    data = data[data.sum(axis=1) > 0]
    data = data.T[data.sum() > 0].T
    print('Data shape (cells, features)', data.shape)
    # create metadata
    metadata = create_metadata(data)
    print('Filter library size by percentile {}'.format(args.libsize_perc))
    data, metadata = filter_library_size(data, metadata, args.libsize_perc)
    print('Filter cells with high mitochondrial expression')
    try:
        data, metadata = filter_mitochondrial_high_expression(data, metadata, args.mit_cutoff)
    except:
        print('Mitochondrial expression filtering step finished with error')
        print('Skiping this step')
        pass
    print('Filter cells rare genes')
    data = filter_low_expressing_genes(data, args.min_cells)
    print('Normalize data by library size')
    data, metadata['library_size'] = normalize_libsize(data, metadata)
    print('Scale data')
    data = scale_data(data)
    print('Saving preprocessed data file')
    data.to_pickle(os.path.join(args.data_dir, "data.scaled.pickle.gz"))
    metadata.to_pickle(os.path.join(args.data_dir, "metadata.scaled.pickle.gz"))

def get_args():
    parser = ArgumentParser(description="Preprocess Single-Cell Data: Filter, Normalize, Scale.")
    parser.add_argument("--data_dir", help="path to direcory with input files", required=True)
    parser.add_argument("--file_type", help="Data file type.  E.g. pickle.gz,  mtx, csv, or tsv (default: pickle.gz)", default='pickle.gz')
    parser.add_argument("--data_file", help="Name of data file (default: data.pickle.gz)", default='data.pickle.gz')
    parser.add_argument("--libsize_perc", help="int or tuple of ints, above or below which to retain a cell. Must be an integer between 0 and 100 (default: (5,95))", default=(5,95))
    parser.add_argument("--mit_cutoff", help="Remove cells with total expression of a mitochondrial genes above or below a threshold (default: 200)", default=200)
    parser.add_argument("--min_cells", help="Filter all genes with negligible counts in all but a few cells (default: 5)", default=5)

    return parser.parse_args()

def load_data(datadir, filetype, data_file):
    """

    :type datadir: object
    """
    filetypes = ['10X', '10X_HDF5', '10X_zip', 'csv', 'fcs', 'mtx', 'tsv', 'pickle.gz']
    assert (filetype in filetypes), "Please enter file format from the following {}".format(filetypes)

    if filetype == 'pickle.gz':
        data = pd.read_pickle(os.path.join(datadir, data_file))

    elif filetype == 'csv':
        data = scprep.io.load_csv(os.path.join(datadir, 'data.csv'))

    elif filetype == 'tsv':
        data = scprep.io.load_csv(os.path.join(datadir, 'data.tsv'))
    
    elif filetype == 'mtx':
        data = scprep.io.load_mtx(os.path.join(datadir, 'matrix.mtx.gz'),
                                  gene_names=os.path.join(datadir, 'features.tsv.gz'),
                                  cell_names=os.path.join(datadir, 'barcodes.tsv.gz'),
                                  cell_axis="column")


    return data

def filter_ercc(data):
    """Remove UMIs from internal standards (old version)
    """
    return data[[x for x in data.columns if 'ERCC' not in x]]

def create_metadata(data):
    """Create metadata file
    """
    return pd.DataFrame(index = data.index)

def filter_library_size(data, metadata, percentile):
    data, metadata = scprep.filter.filter_library_size(data, metadata, percentile=percentile)
    return data, metadata

def filter_mitochondrial_high_expression(data, metadata, cutoff):
    """Remove cells with high mitochondrial gene expression
    """
    mit_genes = ['rps8','cox1','cob','cox3','rps3','nad4',
             'rpl16','nad4L','nad2','nad3','cox2',
             'atp4','atp6','orf 104','nad5','atp9',
             'nad1','rps14','nad6','dam','rps12',
             'rps8_m','rps3_m','rpl16_m','rps14_m',
             'rps12_m']
    ## filter for genes that are expressed in the data
    mit_genes = pd.Series(data.columns)[pd.Series(data.columns).isin(mit_genes)].to_list()
    data, metadata = scprep.filter.filter_gene_set_expression(
        data, metadata, genes=mit_genes,
        cutoff=cutoff, keep_cells='below', library_size_normalize=True
        )

    return data, metadata

def filter_low_expressing_genes(data, cutoff):
    """ Remove cells with low number of UMIs
    """
    return scprep.filter.filter_rare_genes(data, min_cells=cutoff)

def normalize_libsize(data, metadata):
    data, metadata['library_size'] = scprep.normalize.library_size_normalize(data, return_library_size=True)
    return data, metadata

def scale_data(data):
    """Scale the UMI expression data with square-root transformation
    """
    return scprep.transform.sqrt(data)

if __name__ == '__main__':
    main()
