import pytest
import scanpy as sc

import checkatlas.atlas as atlas

given = pytest.mark.parametrize


# @given("path_input,expected", [("/home/checkatlas_data/",
#                                os.path.join("/home/checkatlas_data/",
#                                              "checkatlas_files"))])
""" def test_atlas_object():
    adata = sc.datasets.pbmc68k_reduced()
    atlas_info = ["PBMC68k", "Scanpy", ".h5ad", "Scanpy module"]
    assert atlas.clean_scanpy_atlas(adata, )
 """

# test_atlas_object()
# @given("fn", [atlas(), list_atlases()])
# def test_parameterized(fn):
#     assert "hello from" in fn()
#
#
# def test_list_atlases():
#     assert list_atlases(".") == "hello from base function"
#
#
# def test_atlas():
#     assert atlas() == "hello from BaseClass"
