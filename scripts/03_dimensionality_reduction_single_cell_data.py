#!/bin/python3

from argparse import ArgumentParser
import pandas as pd
import phate
import umap
import scprep
import os
import tasklogger
from sklearn.manifold import TSNE

def main():
    args = get_args()
    print('Loading data')
    data = pd.read_pickle(os.path.join(args.data_dir, args.data_file))
    metadata = pd.read_pickle(os.path.join(args.data_dir, args.metadata_file))
    data_pca, metadata = calc_pca(data, metadata, int(args.pca_components))
    metadata = calc_tsne(data_pca, metadata, int(args.tsne_perplexity), int(args.pca_components))
    metadata = calc_umap(data_pca, metadata, int(args.pca_components))
    metadata = calc_phate(data_pca, metadata, int(args.pca_components))
    print('Saving dimentionality reduction data')
    metadata.to_pickle(os.path.join(args.data_dir, str(args.metadata_file).replace(".pickle.gz",".dim_reduction.pickle.gz")))
    data_pca.to_pickle(os.path.join(args.data_dir, str(args.data_file).replace(".pickle.gz",".pca.pickle.gz")))

def get_args():
    parser = ArgumentParser(description="Dimentionality reduction for single-cell data.")
    parser.add_argument("--data_dir", help="path to direcory with preprocessed single-cell data, including file names: data.scaled.pickle.gz and metadata.scaled.pickle.gz", required=True)
    parser.add_argument("--data_file", help="name of data file as appear in data_dir (default: data.scaled.pickle.gz)", default='data.scaled.pickle.gz')
    parser.add_argument("--metadata_file", help="name of metadata file as appear in data_dir (default: metadata.scaled.pickle.gz)", default='metadata.scaled.pickle.gz')
    parser.add_argument("--pca_components", help="Number of components to calculate for the PCA (default: 50)", default=50)
    parser.add_argument("--tsne_perplexity", help="float. The perplexity is related to the number of nearest neighbors that is used in other manifold learning algorithms. Larger datasets usually require a larger perplexity. Consider selecting a value between 5 and 50. Different values can result in significantly different results (default: 30)", default=30)
    return parser.parse_args()

def calc_pca(data, metadata, pca_components):
    data_pca = scprep.reduce.pca(data, n_components=pca_components, method='dense')
    try:
        metadata = metadata.join(data_pca[['PC1','PC2','PC3']])
    except:
        metadata = metadata.join(data_pca[['PC1','PC2','PC3']], rsuffix='.scprep')
    return data_pca, metadata

def calc_tsne(data_pca, metadata, tsne_perplexity, pca_components):
    with tasklogger.log_task('t-SNE on {} cells'.format(data_pca.shape[0])):
        # Fitting tSNE. Change the perplexity here.
        tsne_op = TSNE(n_components=3, perplexity=tsne_perplexity)
        data_tsne = tsne_op.fit_transform(data_pca.iloc[:,:pca_components])
        # Put output into a dataframe
        data_tsne = pd.DataFrame(data_tsne, index=data_pca.index)
        data_tsne.columns = ['TSNE1', 'TSNE2', 'TSNE3']
        try:
            metadata = metadata.join(data_tsne)
        except:
            metadata = metadata.join(data_tsne, rsuffix='.scprep')
        return metadata

def calc_umap(data_pca, metadata, pca_components):
    with tasklogger.log_task('UMAP on {} cells'.format(data_pca.shape[0])):
        ## Calculate UMAP and add results to metadata file
        data_umap = umap.UMAP(n_components=3).fit_transform(data_pca.iloc[:,:pca_components])
        data_umap = pd.DataFrame(data_umap, index=data_pca.index)
        data_umap.columns = ['UMAP1', 'UMAP2', 'UMAP3']
        try:
            metadata = metadata.join(data_umap)
        except:
            metadata = metadata.join(data_umap, rsuffix='.scprep')
        return metadata

def calc_phate(data_pca, metadata, pca_components):
    with tasklogger.log_task('PHATE on {} cells'.format(data_pca.shape[0])):
        ## Calculate PHATE and add results to metadata file
        phate_op = phate.PHATE(n_components=3)
        data_phate = phate_op.fit_transform(data_pca.iloc[:,:pca_components])
        data_phate = pd.DataFrame(data_phate, index=data_pca.index)
        data_phate.columns = ['PHATE1', 'PHATE2', 'PHATE3']
        try:
            metadata = metadata.join(data_phate)
        except:
            metadata = metadata.join(data_phate, rsuffix='.scprep')
        return metadata

if __name__ == '__main__':
    main()
