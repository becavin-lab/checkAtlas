import os

import pytest

import checkatlas.utils.folders as folders

given = pytest.mark.parametrize


@given(
    "path_input,expected",
    [
        (
            "/home/checkatlas_data/",
            os.path.join("/home/checkatlas_data/", "checkatlas_files"),
        )
    ],
)
def test_workingdir(path_input, expected):
    assert folders.get_workingdir(path_input) == expected


@given(
    "path_input,key_folder,expected",
    [
        (
            "/home/checkatlas_data/",
            "adata",
            os.path.join(
                "/home/checkatlas_data/", "checkatlas_files", "adata"
            ),
        ),
        (
            "/home/checkatlas_data/",
            "summary",
            os.path.join(
                "/home/checkatlas_data/", "checkatlas_files", "summary"
            ),
        ),
    ],
)
def test_getfolder(path_input, key_folder, expected):
    assert folders.get_folder(path_input, key_folder) == expected


def test_checkfolders():
    folders.checkatlas_folders(os.getcwd())
    path_summary_folder = os.path.join(
        os.getcwd(), "checkatlas_files", "summary"
    )
    assert os.path.exists(path_summary_folder)
