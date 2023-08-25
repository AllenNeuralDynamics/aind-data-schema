"""Utility script to check if schemas are version bumped"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

import dictdiffer
import semver


def compare_versions(new_ver: str, old_ver: Optional[str]) -> (bool, Optional[str]):
    """
    Compares an old version with a new version.
    Parameters
    ----------
    new_ver : str
      Like "0.2.0"
    old_ver : str
      Like "0.1.3"

    Returns
    -------
    (bool, Union[str, None])
      If the version is bumped correctly, returns (True, None). Otherwise,
      returns (False, an error message)

    """

    try:
        new_v = semver.Version.parse(new_ver)
    except (TypeError, ValueError):
        return (False, f"Malformed version: {new_ver}")

    try:
        old_v = semver.Version.parse(old_ver)
    except (TypeError, ValueError):
        return (True, None)

    major_bump = new_v == old_v.bump_major()
    minor_bump = new_v == old_v.bump_minor()
    patch_bump = new_v == old_v.bump_patch()

    if major_bump or minor_bump or patch_bump:
        return (True, None)
    else:
        return (
            False,
            f"Version not bumped correctly. New Version: {new_ver}. Old Version: {old_ver}",
        )


def run_job(new_schema_folder: str, old_schema_folder: str) -> None:
    """
    Loops through files in folders and creates a list of common files.
    For each common file, if they are equal, nothing happens. If they are
    different, the schema_version in the new file is checked against the old.
    An AssertionError is raised if the version is not bumped correctly.
    Parameters
    ----------
    new_schema_folder : str
    old_schema_folder : str

    Returns
    -------
    None

    """

    def open_json_file(path):
        """Helper method to read a json file"""
        with open(path, "r") as f:
            data = json.load(f)
        return data

    files_in_old_schema_folder = os.listdir(Path(old_schema_folder))
    files_in_new_schema_folder = os.listdir(Path(new_schema_folder))
    common_files: list = list(set(files_in_old_schema_folder).intersection(set(files_in_new_schema_folder)))
    version_comparison_issues = []
    for file in common_files:
        old_model = open_json_file(Path(old_schema_folder) / file)
        new_model = open_json_file(Path(new_schema_folder) / file)
        diff = dictdiffer.diff(old_model, new_model)
        is_equal = len(list(diff)) == 0
        if not is_equal:
            new_schema_version = new_model["properties"]["schema_version"]["const"]
            old_schema_version_dict = old_model["properties"].get("schema_version")
            old_schema_version = (
                None
                if old_schema_version_dict is None or not isinstance(old_schema_version_dict, dict)
                else old_schema_version_dict.get("const")
            )
            v_check = compare_versions(new_schema_version, old_schema_version)
            if v_check[0] is False:
                version_comparison_issues.append(f"{file} - {v_check[1]}")
    if len(version_comparison_issues) > 0:
        version_comparison_issues.sort()
        raise AssertionError(f"There were issues checking the schema versions: {version_comparison_issues}")
    return None


if __name__ == "__main__":
    sys_args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--old-schema-folder",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--new-schema-folder",
        required=True,
    )
    folder_args = parser.parse_args(sys_args)
    run_job(
        new_schema_folder=folder_args.new_schema_folder,
        old_schema_folder=folder_args.old_schema_folder,
    )
