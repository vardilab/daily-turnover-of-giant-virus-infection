# Daily turnover of active giant virus infection during algal blooms revealed by single-cell transcriptomics

Code reoisitory the manuscript Hevroni et al. (2023) Daily turnover of active giant virus infection during algal blooms revealed by single-cell transcriptomics. Science Advances.

#### scripts
- `01_raw_UMI_counts_MARSseq_data.py` - aggregating raw UMI counts from MARS-Seq data by a batch list
- `02_filter_normalize_scale_single_cell_data.py` - preprocessing: filter, normalize, scale
- `03_dimentionality_reduction_single_cell_data.py` - dimentionality reduction
- `04_clustering_single_cell_data.py` - clustering

#### examples
- `MARS_Batches.txt` - metadata format of MARS-Seq batch information 
- `UMIs.txt` - tabular format of a raw UMI talbe; cell ids (columns); gene id (rows)
