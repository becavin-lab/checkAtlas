import os

working_dir = "checkatlas_files"
SUMMARY = "summary"
ANNDATA = "adata"
QC = "violin"
UMAP = "umap"
TSNE = "tsne"
CLUSTER = "cluster"
ANNOTATION = "annotation"
DIMRED = "dimred"
SPECI = "specificity"

dict_folder = {
    SUMMARY: SUMMARY,
    ANNDATA: ANNDATA,
    QC: QC,
    UMAP: UMAP,
    TSNE: TSNE,
    CLUSTER: CLUSTER,
    ANNOTATION: ANNOTATION,
    DIMRED: DIMRED,
    SPECI: SPECI,
}


def get_workingdir(path):
    return os.path.join(path, working_dir)


def get_folder(path, key_folder):
    return os.path.join(get_workingdir(path), dict_folder[key_folder])


def checkatlas_folders(path):
    print("Check if checkatlas folders exist")
    global_path = get_workingdir(path)
    if not os.path.exists(global_path):
        os.mkdir(global_path)

    for key_folder in dict_folder.keys():
        temp_path = os.path.join(global_path, key_folder)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
