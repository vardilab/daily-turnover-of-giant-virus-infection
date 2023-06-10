#!/bin/python3

import sys
import os
from argparse import ArgumentParser
import pandas as pd

def main():
    args = get_args()
    print('Loading batch data')
    batch_data = load_batch_data(args.batch_data)
    batches = list(batch_data['Amp.Batch.ID'])
    data_list = []
    metadata_list = []
    for batch in batches:
        print(batch)
        temp_data = load_data(args.data_dir, batch, args.file_type) 
        data_list.append(temp_data)
        metadata_list.append(pd.Series(index=temp_data.index, data=[batch]*len(temp_data), name='Amp.Batch.ID'))
    print('Merging data')
    data = pd.concat(data_list)
    metadata = pd.concat(metadata_list).to_frame()
    print('Removing empty cells/features')
    data = data[data.sum(axis=1) > 0]
    data = data.T[data.sum() > 0].T
    metadata = metadata.loc[metadata.index.isin(data.index)]
    metadata = metadata.reset_index().rename(columns={'index':'Cell.ID'})
    print('Data shape (cells, features)', data.shape)
    print('Creating metadata file')
    metadata = metadata.merge(batch_data, on='Amp.Batch.ID', how='left')
    print('Saving raw data files')
    metadata.to_pickle(args.metadata_outfile)
    data.to_pickle(args.data_outfile)

def get_args():
    parser = ArgumentParser(description="Generate raw UMI counts complied by batch for MARS-seq single-cell data")
    parser.add_argument("--data_dir", help="Path to direcory with MARS-Seq UMI tables)", required=True)
    parser.add_argument("--batch_data", help="Path to batch data, a tab seperated file that should contain at least the header 'Amp.Batch.ID')", required=True)
    parser.add_argument("--file_type", help="Whether the delimiter is tab or comma: txt, csv (default: txt)", default='txt')
    parser.add_argument("--data_outfile", help="Path to file for saving count data (saving compressed pickle.gz file)", required=True)
    parser.add_argument("--metadata_outfile", help="Path to file for saving metadata (saving compressed pickle.gz file)", required=True)
    return parser.parse_args()

def load_batch_data(batch_data_file):
    """
    The batch data file is a tab seperated file and should contain at least the header 'Amp.Batch.ID' 
    """
    return pd.read_csv(batch_data_file, sep='\t')

def load_data(datadir, amp_batch, filetype):
    """
    :type datadir: object
    """
    filetypes = ['txt', 'csv']
    assert (filetype in filetypes), "Please enter file format from the following {}".format(filetypes)

    if filetype == 'txt':
        data = pd.read_csv(os.path.join(datadir, '{}.txt'.format(amp_batch)), sep='\t').T

    elif filetype == 'csv':
        data = pd.read_csv(os.path.join(datadir, '{}.csv'.format(amp_batch))).T

    return data

if __name__ == '__main__':
    main()
