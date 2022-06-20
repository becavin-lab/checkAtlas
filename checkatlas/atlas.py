import os
import re

import numpy as np
import pandas as pd
import scanpy as sc

from . import checkatlas, folders
from .metrics.cluster import clust_compute

# try:
#     from .metrics.cluster import clust_compute
# except ImportError:
#     from metrics.cluster import clust_compute
# try:
#     from .metrics.dim_red import dr_compute
# except ImportError:
#     from metrics.dim_red import dr_compute

# try:
#     from . import checkatlas, folders
# except ImportError:
#     import folders
#     import checkatlas


"""
Atlas module
All the function to screen the atlases
"""

OBS_CLUSTERS = [
    "cell_type",
    "CellType",
    "celltype",
    "ann_finest_level",
    "seurat_clusters",
    "louvain",
    "leiden",
    "orig.ident",
]


def list_atlases(path) -> list:
    """
    List all atlases files in the path
    Detect .rds, .h5, .h5ad
    :param path:
    :return: List of files
    """
    atlas_list = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            for extension in checkatlas.EXTENSIONS:
                if file.endswith(extension):
                    atlas_list.append(os.path.join(root, file))
    return atlas_list


def convert_atlas(atlas_path, atlas_name) -> None:
    """
    Convert a atlas to Scanpy
    :param atlas_path:
    :return:
    """
    print("Convert Seurat object to Scanpy: ", atlas_path)
    rscript_cmd = (
        "Rscript "
        + checkatlas.RSCRIPT
        + " "
        + os.path.dirname(atlas_path)
        + " "
        + atlas_name
    )
    print(rscript_cmd)
    os.system(rscript_cmd)


def clean_scanpy_atlas(adata, atlas_info) -> bool:
    """
    Clean the Scanpy object to be suyre to get all information out of it
    :param adata:
    :return:
    """
    print("Clean scanpy:" + atlas_info[0])
    # If OBS_CLUSTERS are present and in int32 -> be sure to
    # transform them in categorical
    for obs_key in adata.obs_keys():
        for obs_key_celltype in OBS_CLUSTERS:
            if obs_key_celltype in obs_key:
                if adata.obs[obs_key].dtype == np.int32:
                    adata.obs[obs_key] = pd.Categorical(adata.obs[obs_key])
    return adata


def get_viable_obs(adata):
    """
    Search in obs_keys a match to OBS_CLUSTERS values
    Extract sorted obs_keys in same order then OBS_CLUSTERS
    :param adata:
    :return:
    """
    obs_keys = list()
    for obs_key in adata.obs_keys():
        for obs_key_celltype in OBS_CLUSTERS:
            if obs_key_celltype in obs_key:
                if type(adata.obs[obs_key].dtype) == pd.CategoricalDtype:
                    obs_keys.append(obs_key)
    # ### obs are sorted to have cell_type first
    # (! Need to fix that accordingly)
    return sorted(obs_keys)


def create_summary_table(adata, atlas_path, atlas_info, path) -> None:
    """
    Create a table with all interesting variables
    :param adata:
    :param atlas_name:
    :param csv_path:
    :return:
    """
    atlas_name = atlas_info[0]
    atlas_file_type = atlas_info[1]
    atlas_extension = atlas_info[2]
    csv_path = os.path.join(
        folders.get_folder(path, folders.SUMMARY),
        atlas_name + checkatlas.SUMMARY_EXTENSION,
    )
    # Create summary table
    header = [
        "AtlasFileType",
        "NbCells",
        "NbGenes",
        "AnnData.raw",
        "AnnData.X",
        "File_extension",
        "File_path",
    ]
    print("Run summary")
    df_summary = pd.DataFrame(index=[atlas_name], columns=header)
    df_summary["AtlasFileType"][atlas_name] = atlas_file_type
    df_summary["NbCells"][atlas_name] = adata.n_obs
    df_summary["NbGenes"][atlas_name] = adata.n_vars
    df_summary["AnnData.raw"][atlas_name] = adata.raw is not None
    df_summary["AnnData.X"][atlas_name] = adata.X is not None
    df_summary["File_extension"][atlas_name] = atlas_extension
    df_summary["File_path"][atlas_name] = atlas_path.replace(path, "")
    df_summary.to_csv(csv_path, index=False)


def create_anndata_table(adata, atlas_path, atlas_info, path) -> None:
    """
    Create a table with all AnnData arguments
    :param adata:
    :param atlas_name:
    :param atlas_path:
    :return:
    """
    atlas_name = atlas_info[0]
    csv_path = os.path.join(
        folders.get_folder(path, folders.ANNDATA),
        atlas_name + checkatlas.ADATA_EXTENSION,
    )
    # Create AnnData table
    header = ["obs", "obsm", "var", "varm", "uns"]
    df_summary = pd.DataFrame(index=[atlas_name], columns=header)
    # html_element = "<span class=\"label label-primary\">"
    # new_line = ''
    # for value in list(adata.obs.columns):
    #     new_line += html_element + value + "</span><br>"
    #     print(new_line)
    df_summary["obs"][atlas_name] = (
        "<code>"
        + "</code><br><code>".join(list(adata.obs.columns))
        + "</code>"
    )
    df_summary["obsm"][atlas_name] = (
        "<code>"
        + "</code><br><code>".join(list(adata.obsm_keys()))
        + "</code>"
    )
    df_summary["var"][atlas_name] = (
        "<code>" + "</code><br><code>".join(list(adata.var_keys())) + "</code>"
    )
    df_summary["varm"][atlas_name] = (
        "<code>"
        + "</code><br><code>".join(list(adata.varm_keys()))
        + "</code>"
    )
    df_summary["uns"][atlas_name] = (
        "<code>" + "</code><br><code>".join(list(adata.uns_keys())) + "</code>"
    )
    df_summary.to_csv(csv_path, index=False, quoting=False)


def create_qc_plots(adata, atlas_path, atlas_info, path) -> None:
    """
    Display the atlas QC
    Search for the OBS variable which correspond to the toal_RNA, total_UMI,
     MT_ratio, RT_ratio
    :param path:
    :param adata:
    :param atlas_name:
    :param atlas_path:
    :return:
    """
    atlas_name = atlas_info[0]
    sc.settings.figdir = folders.get_workingdir(path)
    qc_path = os.sep + atlas_name + checkatlas.QC_EXTENSION
    print("Calc QC")
    # mitochondrial genes
    adata.var["mt"] = adata.var_names.str.startswith("MT-")
    # ribosomal genes
    adata.var["ribo"] = adata.var_names.str.startswith(("RPS", "RPL"))
    sc.pp.calculate_qc_metrics(
        adata,
        qc_vars=["mt", "ribo"],
        percent_top=None,
        log1p=False,
        inplace=True,
    )
    sc.pl.violin(
        adata,
        [
            "n_genes_by_counts",
            "total_counts",
            "pct_counts_mt",
            "pct_counts_ribo",
        ],
        jitter=0.4,
        multi_panel=True,
        show=False,
        save=qc_path,
    )


def create_umap_fig(adata, atlas_path, atlas_info, path) -> None:
    """
    Display the UMAP of celltypes
    Search for the OBS variable which correspond to the celltype annotation
    :param path:
    :param adata:
    :param atlas_name:
    :param atlas_path:
    :return:
    """
    atlas_name = atlas_info[0]
    # Search if tsne reduction exists
    r = re.compile(".*umap*.")
    print(len(list(filter(r.match, adata.obsm_keys()))))
    if len(list(filter(r.match, adata.obsm_keys()))) > 0:
        # Setting up figures directory
        sc.settings.figdir = folders.get_workingdir(path)
        umap_path = os.sep + atlas_name + checkatlas.UMAP_EXTENSION
        # Exporting umap
        obs_keys = get_viable_obs(adata)
        if len(obs_keys) != 0:
            sc.pl.umap(adata, color=obs_keys[0], show=False, save=umap_path)
        else:
            sc.pl.umap(adata, show=False, save=umap_path)


def create_tsne_fig(adata, atlas_path, atlas_info, path) -> None:
    """
    Display the TSNE of celltypes
    Search for the OBS variable which correspond to the celltype annotation
    :param path:
    :param adata:
    :param atlas_name:
    :param atlas_path:
    :return:
    """
    # Search if tsne reduction exists
    atlas_name = atlas_info[0]
    r = re.compile(".*tsne*.")
    if len(list(filter(r.match, adata.obsm_keys()))) > 0:
        # Setting up figures directory
        sc.settings.figdir = sc.settings.figdir = folders.get_workingdir(path)
        tsne_path = os.sep + atlas_name + checkatlas.TSNE_EXTENSION
        # Exporting tsne
        obs_keys = get_viable_obs(adata)
        if len(obs_keys) != 0:
            sc.pl.tsne(adata, color=obs_keys[0], show=False, save=tsne_path)
        else:
            sc.pl.tsne(adata, show=False, save=tsne_path)


def metric_cluster(adata, atlas_path, atlas_info, path) -> None:
    """
    Main function of checkatlas
    For every atlas create summary tables with all attributes of the atlas
    Calc UMAP, tSNE, andd all metrics
    :param atlas_path:
    :return:
    """
    atlas_name = atlas_info[0]
    csv_path = os.path.join(
        folders.get_folder(path, folders.CLUSTER),
        atlas_name + checkatlas.METRIC_CLUSTER_EXTENSION,
    )
    header = ["Sample", "obs", "Silhouette", "Davies-Bouldin"]
    df_cluster = pd.DataFrame(columns=header)
    obs_keys = get_viable_obs(adata)
    for obs_key in obs_keys:
        # Need more than one sample to calculate metric
        annotations = adata.obs[obs_key]
        if len(annotations.cat.categories) != 1:
            silhouette = 1
            print("Calc Silhouette for " + atlas_name, obs_key)
            silhouette = clust_compute.silhouette(adata, obs_key, "X_umap")
            daviesb = -1
            print("Calc Davies Bouldin for " + atlas_name, obs_key)
            daviesb = clust_compute.davies_bouldin(adata, obs_key, "X_umap")
            df_line = pd.DataFrame(
                {
                    "Sample": [atlas_name + "_" + obs_key],
                    "obs": [obs_key],
                    "Silhouette": [silhouette],
                    "Davies-Bouldin": [daviesb],
                }
            )
            df_cluster = pd.concat(
                [df_cluster, df_line], ignore_index=True, axis=0
            )
    if len(df_cluster) != 0:
        df_cluster.to_csv(csv_path, index=False)


def metric_annot(adata, atlas_path, atlas_info, path) -> None:
    """
    Main function of checkatlas
    For every atlas create summary tables with all attributes of the atlas
    Calc UMAP, tSNE, and all metrics
    :param atlas_path:
    :return:
    """
    atlas_name = atlas_info[0]
    csv_path = os.path.join(
        folders.get_folder(path, folders.ANNOTATION),
        atlas_name + checkatlas.METRIC_ANNOTATION_EXTENSION,
    )
    header = ["Sample", "obs", "Rand"]
    df_annot = pd.DataFrame(columns=header)
    obs_keys = get_viable_obs(adata)
    if len(obs_keys) != 0:
        ref_obs = obs_keys[0]
        for i in range(1, len(obs_keys)):
            obs_key = obs_keys[i]
            # Need more than one sample to calculate metric
            annotations = adata.obs[obs_key]
            if len(annotations.cat.categories) != 1:
                print(
                    "NOT WORKING YET - Calc Rand Index for " + atlas_name,
                    obs_key,
                )
                rand = -1
                # ##rand = clust_compute.rand(adata, obs_key, ref_obs)
                df_line = pd.DataFrame(
                    {
                        "Sample": [atlas_name + "_" + obs_key],
                        "Reference": [ref_obs],
                        "obs": [obs_key],
                        "Rand": [rand],
                    }
                )
                df_annot = pd.concat(
                    [df_annot, df_line], ignore_index=True, axis=0
                )
        if len(df_annot) != 0:
            df_annot.to_csv(csv_path, index=False)


def metric_dimred(adata, atlas_path, atlas_info, path) -> None:
    """
    Main function of checkatlas
    For every atlas create summary tables with all attributes of the atlas
    Calc UMAP, tSNE, andd all metrics
    :param atlas_path:
    :return:
    """
    atlas_name = atlas_info[0]
    csv_path = os.path.join(
        folders.get_folder(path, folders.DIMRED),
        atlas_name + checkatlas.METRIC_DIMRED_EXTENSION,
    )
    header = ["Sample", "obs", "Kruskal"]
    df_dimred = pd.DataFrame(columns=header)
    for obsm_key in adata.obsm_keys():
        print(
            "NOT WORKING YET - Calc Kruskal Stress for " + atlas_name, obsm_key
        )
        kruskal = -1
        # kruskal = dr_compute.kruskal_stress(adata, obsm_key)
        df_line = pd.DataFrame(
            {
                "Sample": [atlas_name + "_" + obsm_key],
                "obs": [obsm_key],
                "Kruskal": [kruskal],
            }
        )
        df_dimred = pd.concat([df_dimred, df_line], ignore_index=True, axis=0)
    if len(df_dimred) != 0:
        df_dimred.to_csv(csv_path, index=False)
