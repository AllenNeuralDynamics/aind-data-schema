"""Utility script for bumping schema versions"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

import dictdiffer
import semver


def bump_version(old_ver: Optional[str]) -> str:
    """
    Bumps an old version to a new version .
    Parameters
    ----------

    old_ver : str
      Like "0.1.3"

    Returns
    -------
    str

    """

    try:
        old_v = semver.Version.parse(old_ver)
    except (TypeError, ValueError):
        return f"Malformed version: {old_ver}"

    new_v = old_v.bump_patch()
    new_ver = f"{new_v.major}.{new_v.minor}.{new_v.patch}"

    return new_ver


def run_job(new_schema_folder: str, old_schema_folder: str, core_schemas_folder: str) -> None:
    """
    Loops through files in folders and creates a list of common files.
    For each common file, if they are equal, nothing happens. If they are
    different, the old schema version will be bumped and replaced with a
    new version in the corresponding core model.
    ----------
    new_schema_folder : str
    old_schema_folder : str
    core_schemas_folder: str

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
    for file in common_files:
        old_model = open_json_file(Path(old_schema_folder) / file)
        new_model = open_json_file(Path(new_schema_folder) / file)
        diff = dictdiffer.diff(old_model, new_model)
        is_equal = len(list(diff)) == 0
        if not is_equal:
            old_schema_version_dict = old_model["properties"].get("schema_version")
            old_schema_version = (
                None
                if old_schema_version_dict is None or not isinstance(old_schema_version_dict, dict)
                else old_schema_version_dict.get("const")
            )
            new_schema_version = bump_version(old_schema_version)
            core_schema_file = Path(core_schemas_folder) / file.replace("_schema.json", ".py")
            sed_command = f'sed -i \'/^schema_version:/s/"[^\"]*"/"{new_schema_version}"/g\' {core_schema_file}'
            try:
                subprocess.run(sed_command, shell=True, check=True)
                print(f"Schema version in {file.replace('_schema.json', '')} have been bumped to {new_schema_version}")
            except subprocess.CalledProcessError:
                print("Error while bumping schema version. Please check the file structure or permissions.")

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
    parser.add_argument(
        "-c",
        "--core-schemas-folder",
        required=True,
    )
    folder_args = parser.parse_args(sys_args)
    run_job(
        new_schema_folder=folder_args.new_schema_folder,
        old_schema_folder=folder_args.old_schema_folder,
        core_schemas_folder=folder_args.core_schemas_folder
    )
