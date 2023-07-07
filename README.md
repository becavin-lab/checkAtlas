
# CheckAtlas

[![codecov](https://codecov.io/gh/becavin-lab/checkatlas/branch/main/graph/badge.svg?token=checkatlas_token_here)](https://codecov.io/gh/becavin-lab/checkatlas)
[![CI](https://github.com/becavin-lab/checkatlas/actions/workflows/tests.yml/badge.svg)](https://github.com/becavin-lab/checkatlas/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/checkatlas/badge/?version=latest)](https://checkatlas.readthedocs.io/en/latest/?badge=latest)
[![Gitter](https://badges.gitter.im/checkatlas/checkatlas.svg)](https://matrix.to/#/#checkatlas:gitter.im)

CheckAtlas is a one liner tool to check the quality of your single-cell atlases. For every atlas, it produces the
quality control tables and figures which can be then processed by multiqc. CheckAtlas is able to load Scanpy, Seurat,
and CellRanger files.


## Summary

### Parse Scanpy, Seurat and CellRanger objects

The checkatlas pipeline start with a fast crawl through your working directory. It detects Seurat (.rds), Scanpy (.h5ad) or cellranger (.h5) atlas files.


### Create checkatlas summary files

Go through all atlas files and produce summary information:

- All basic QC (nRNA, nFeature, ratio_mito)
- General information (nbcells, nbgenes, nblayers)
- All elements in atlas files (obs, obsm, uns, var, varm)
- Reductions (pca, umap, tsne)
- All metrics (clustering, annotation, dimreduction, specificity)

### Parse checkatlas files in MultiQC

   Update MultiQC project to add checkatlas parsing. Dev project in: https://github.com/becavin-lab/MultiQC/tree/checkatlas

https://checkatlas.readthedocs.io/en/latest/

## Examples

1. Evaluate and compare different atlases: https://github.com/becavin-lab/checkatlas/blob/3a4f88e94716c09a3b9c86010f570743a5855461/examples/Atlas_comparison.ipynb

https://checkatlas.readthedocs.io/en/stable/CheckAtlas_example_1/CheckAtlas_example_1.html

2. Evaluate different version of your atlas: https://github.com/becavin-lab/checkatlas/blob/3a4f88e94716c09a3b9c86010f570743a5855461/examples/Version_comparison.ipynb

https://checkatlas.readthedocs.io/en/stable/CheckAtlas_example_2/CheckAtlas_example_2.html

3. Explore Scanpy, Seurat and CellRanger objects in your folder: https://github.com/becavin-lab/checkatlas/blob/main/examples/AtlasType_comparison.ipynb

https://checkatlas.readthedocs.io/en/stable/CheckAtlas_example_3/CheckAtlas_example_3.html

## Installation

CheckAtlas can be downloaded from PyPI. However, the project is in an early development phase. We strongly recommend to use the developmental version.

### Install checkatlas development version

```bash
git clone git@github.com:becavin-lab/checkatlas.git
pip install checkatlas/.
```

Install MultiQC with checkatlas file management. This version of MultiQC is available at checkatlas branch of github.com:becavin-lab/MultiQC.

```bash
git clone git@github.com:becavin-lab/MultiQC.git
cd MultiQC/
git checkout checkatlas
pip install .
```

### Install it from PyPI

```bash
pip install checkatlas
```

### Install Seurat

To be able to manage seurat file, rpy2 should have Seurat installed. The easiest way is to put all checkatlas requirements in a conda environment and add r-seurat.

```bash
conda create -n checkatlas python=3.9
pip install checkatlas
conda install -c bioconda r-seurat
```

Or, open R in checkatlas environment (the one where you ran 'pip install') and install Seurat.

```bash
% R
> install.packages('Seurat')
> library(Seurat)
```


## Usage

The one liner way to run checkatlas is the following: 

```bash
$ cd your_search_folder/
$ python -m checkatlas .
#or
$ checkatlas .
```

Or run it inside your python workflow.

```py
from checkatlas import checkatlas
checkatlas.run(path, atlas_list, multithread, n_cpus)
```


## Development

Read the [CONTRIBUTING.md](docs/contributing.md) file.

Project developed thanks to the project template : (https://github.com/rochacbruno/python-project-template/)

