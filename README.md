
# checkatlas

[![codecov](https://codecov.io/gh/becavin-lab/checkatlas/branch/main/graph/badge.svg?token=checkatlas_token_here)](https://codecov.io/gh/becavin-lab/checkatlas)
[![CI](https://github.com/becavin-lab/checkatlas/actions/workflows/main.yml/badge.svg)](https://github.com/becavin-lab/checkatlas/actions/workflows/main.yml)

Awesome checkatlas created by becavin-lab

## Summary

1. Parse Scanpy, Seurat and CellRanger objects
    
    CheckAtlas should be able to load : .rds, .h5 and .h5ad corresponding to single-cell experiment. Need to implement :
      - automatic conversion of Seurat object to Scanpy with SeuratDisk
      - Rapid check-up of files to see if a Seurat or Scanpy can be found
      - Automatic search in Scanpy files of key information = raw data, normalized data, integrated data, reductions, layers, assays, metadatas, etc...


2. Create checkatlas summary files
  
    Go through all Scanpy files and extract summary information. We won't to extract :

      - All basic QC (nRNA, nFeature, ratio_mito)
      - General information (nbcells, nbgenes, nblayers)
      - All elements in scanpy objects (obs, obsm, uns, var, varm)
      - Reductions (pca, umap, tsne)
      - All metrics (clustering, annotation, dimreduction, specificity)

3. Parse checkatlas files in MultiQC
  
    Update MultiQC project to add checkatlas parsing. Dev project in: https://github.com/becavin-lab/MultiQC/tree/checkatlas

## Use cases

1. Evaluate and compare different atlases
2. Evaluate different version of your atlas
3. Explore Scanpy, Seurat and CellRanger objects in your folder
4. 


## Install it from PyPI

```bash
pip install checkatlas
```

## Usage

```py
from checkatlas import checkatlas
checkatlas.run(path, atlas_list, multithread, n_cpus)
```

```bash
$ cd your_search_folder/
$ python -m checkatlas .
#or
$ checkatlas .
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

Project developed thanks to the project template : (https://github.com/rochacbruno/python-project-template/)

