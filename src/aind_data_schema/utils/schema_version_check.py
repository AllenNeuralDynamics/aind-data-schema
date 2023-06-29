"""Utility script to check if schemas are version bumped"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

# TODO: Put this in the base model class to perform validation on instance
#   creation
VERSION_REGEX = r"(\d+).(\d+).(\d+)"


def compare_versions(new_ver: str, old_ver: Optional[str]) -> (bool, Optional[str]):
    """
    Compares an old version with a new version.
    Parameters
    ----------
    new_ver : str
      Like "0.2.0"
    old_ver : str
      Like "0.1.3

    Returns
    -------
    (bool, Union[str, None])
      If the version is bumped correctly, returns (True, None). Otherwise,
      returns (False, an error message)

    """

    new_v_match = re.search(VERSION_REGEX, new_ver)
    old_v_match = None if old_ver is None else re.search(VERSION_REGEX, old_ver)
    if new_v_match is None:
        v_check = (False, f"Malformed version: {new_ver}")
    elif old_v_match is None:
        v_check = (True, None)
    else:
        new_ver_major = int(new_v_match.groups()[0])
        new_ver_minor = int(new_v_match.groups()[1])
        new_ver_patch = int(new_v_match.groups()[2])
        old_ver_major = int(old_v_match.groups()[0])
        old_ver_minor = int(old_v_match.groups()[1])
        old_ver_patch = int(old_v_match.groups()[2])
        major_bump = True if new_ver_major == old_ver_major + 1 and new_ver_minor == 0 and new_ver_patch == 0 else False
        minor_bump = (
            True
            if new_ver_major == old_ver_major and new_ver_minor == old_ver_minor + 1 and new_ver_patch == 0
            else False
        )
        patch_bump = (
            True
            if new_ver_major == old_ver_major and new_ver_minor == old_ver_minor and new_ver_patch == old_ver_patch + 1
            else False
        )

        if major_bump or minor_bump or patch_bump:
            v_check = (True, None)
        else:
            v_check = (False, f"Version not bumped correctly. New Version: {new_ver}. Old Version: {old_ver}")
    return v_check


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

    def sorting(item):
        """Helper method to sort items in a dictionary to make comparisons
        easier."""
        if isinstance(item, dict):
            return sorted((key, sorting(values)) for key, values in item.items())
        if isinstance(item, list):
            return sorted(sorting(x) for x in item)
        if item is None:
            return "null"
        else:
            return item

    files_in_old_schema_folder = os.listdir(Path(old_schema_folder))
    files_in_new_schema_folder = os.listdir(Path(new_schema_folder))
    common_files: list = list(set(files_in_old_schema_folder).intersection(set(files_in_new_schema_folder)))
    comparison_issues = []
    for file in common_files:
        old_model = open_json_file(Path(old_schema_folder) / file)
        new_model = open_json_file(Path(new_schema_folder) / file)
        is_equal = sorting(old_model) == sorting(new_model)
        if not is_equal:
            new_schema_version = new_model["properties"]["schema_version"]["const"]
            old_schema_version_dict = old_model["properties"].get("schema_version")
            old_schema_version = (
                None
                if old_schema_version_dict is None or type(old_schema_version_dict) != dict
                else old_schema_version_dict.get("const")
            )
            v_check = compare_versions(new_schema_version, old_schema_version)
            if v_check[0] is False:
                comparison_issues.append(f"{file} - {v_check[1]}")
    if len(comparison_issues) > 0:
        comparison_issues.sort()
        raise AssertionError(f"There were issues checking the schema versions: {comparison_issues}")
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
    run_job(new_schema_folder=folder_args.new_schema_folder, old_schema_folder=folder_args.old_schema_folder)
