# Daily turnover of active giant virus infection during algal blooms revealed by single-cell transcriptomics

Code reoisitory the manuscript Hevroni et al. (2023) Daily turnover of active giant virus infection during algal blooms revealed by single-cell transcriptomics. Science Advances.

Below is a list of arguments and usage examples of the Python scripts included in this reository:

### Aggregating raw UMI counts from MARS-Seq data by a batch list
```
usage: 01_raw_UMI_counts_MARSseq_data.py [-h] --data_dir DATA_DIR
                                            --batch_data BATCH_DATA
                                            [--file_type FILE_TYPE]
                                            --data_outfile DATA_OUTFILE
                                            --metadata_outfile
                                            METADATA_OUTFILE

Generate raw UMI counts complied by batch for MARS-seq single-cell data

optional arguments:
  -h, --help            show this help message and exit
  --data_dir DATA_DIR   Path to direcory with MARS-Seq UMI tables)
  --batch_data BATCH_DATA
                        Path to batch data, a tab seperated file that should
                        contain at least the header 'Amp.Batch.ID')
  --file_type FILE_TYPE
                        Whether the delimiter is tab or comma: txt, csv
                        (default: txt)
  --data_outfile DATA_OUTFILE
                        Path to file for saving count data (saving compressed
                        pickle.gz file)
  --metadata_outfile METADATA_OUTFILE
                        Path to file for saving metadata (saving compressed
                        pickle.gz file)

example: python3 01_raw_UMI_counts_MARSseq_data.py --data_dir ./ --batch_data MARS_Batches.txt --data_outfile data.pickle.gz --metadata_outfile metadata.pickle.gz
```

### Preprocessing: filter, normalize, scale
```
usage: 02_filter_normalize_scale_single_cell_data.py [-h] --data_dir DATA_DIR
                                                     [--file_type FILE_TYPE]
                                                     [--data_file DATA_FILE]
                                                     [--libsize_perc LIBSIZE_PERC]
                                                     [--mit_cutoff MIT_CUTOFF]
                                                     [--min_cells MIN_CELLS]

Preprocess Single-Cell Data: Filter, Normalize, Scale.

optional arguments:
  -h, --help            show this help message and exit
  --data_dir DATA_DIR   path to direcory with input files
  --file_type FILE_TYPE
                        Data file type. E.g. pickle.gz, mtx, csv, or tsv
                        (default: pickle.gz)
  --data_file DATA_FILE
                        Name of data file (default: data.pickle.gz)
  --libsize_perc LIBSIZE_PERC
                        int or tuple of ints, above or below which to retain a
                        cell. Must be an integer between 0 and 100 (default:
                        (5,95))
  --mit_cutoff MIT_CUTOFF
                        Remove cells with total expression of a mitochondrial
                        genes above or below a threshold (default: 200)
  --min_cells MIN_CELLS
                        Filter all genes with negligible counts in all but a
                        few cells (default: 5)

example: python3 02_filter_normalize_scale_single_cell_data.py --data_dir ./
```

### Dimentionality reduction
```
usage: 03_dimensionality_reduction_single_cell_data.py [-h] --data_dir
                                                       DATA_DIR
                                                       [--data_file DATA_FILE]
                                                       [--metadata_file METADATA_FILE]
                                                       [--pca_components PCA_COMPONENTS]
                                                       [--tsne_perplexity TSNE_PERPLEXITY]

Dimentionality reduction for single-cell data.

optional arguments:
  -h, --help            show this help message and exit
  --data_dir DATA_DIR   path to direcory with preprocessed single-cell data,
                        including file names: data.scaled.pickle.gz and
                        metadata.scaled.pickle.gz
  --data_file DATA_FILE
                        name of data file as appear in data_dir (default:
                        data.scaled.pickle.gz)
  --metadata_file METADATA_FILE
                        name of metadata file as appear in data_dir (default:
                        metadata.scaled.pickle.gz)
  --pca_components PCA_COMPONENTS
                        Number of components to calculate for the PCA
                        (default: 50)
  --tsne_perplexity TSNE_PERPLEXITY
                        float. The perplexity is related to the number of
                        nearest neighbors that is used in other manifold
                        learning algorithms. Larger datasets usually require a
                        larger perplexity. Consider selecting a value between
                        5 and 50. Different values can result in significantly
                        different results (default: 30)

example: python3 03_dimentionality_reduction_single_cell_data.py --data_dir ./
```

### Clustering
```
usage: 04_clustering_single_cell_data.py [-h] --data_dir DATA_DIR
                                         [--data_pca DATA_PCA]
                                         [--metadata_file METADATA_FILE]

Clustering single-cell data.

optional arguments:
  -h, --help            show this help message and exit
  --data_dir DATA_DIR   path to direcory with single-cell PCA data, including
                        file names: data.scaled.pca.pickle.gz and
                        metadata.scaled.dim_reduction.pickle.gz
  --data_pca DATA_PCA   name of data file as appear in data_dir (default:
                        data.scaled.pca.pickle.gz)
  --metadata_file METADATA_FILE
                        name of metadata file as appear in data_dir (default:
                        metadata.scaled.dim_reduction.pickle.gz)

example: python3 00.03.clustering_single_cell_data.py --data_dir ./
```

