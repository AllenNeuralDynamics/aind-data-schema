"""Utility script for bumping schema versions"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

import dictdiffer
import semver

CURRENT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = CURRENT_DIR.parents[2]
OLD_SCHEMA_DIR = ROOT_DIR / "schemas"
CORE_SCHEMA_DIR = ROOT_DIR / "src" / "aind_data_schema" / "core"

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
    new_ver = str(new_v)

    return new_ver


def run_job(new_schema_folder: str) -> None:
    """
    Loops through files in folders and creates a list of common files.
    For each common file, if they are equal, nothing happens. If they are
    different, the old schema version will be bumped and replaced with a
    new version in the corresponding core model.
    ----------
    new_schema_folder : str

    Returns
    -------
    None

    """

    def open_json_file(path):
        """Helper method to read a json file"""
        with open(path, "r") as f:
            data = json.load(f)
        return data

    files_in_old_schema_folder = os.listdir(OLD_SCHEMA_DIR)
    files_in_new_schema_folder = os.listdir(Path(new_schema_folder))
    common_files: list = list(set(files_in_old_schema_folder).intersection(set(files_in_new_schema_folder)))
    for file_name in common_files:
        old_model = open_json_file(OLD_SCHEMA_DIR / file_name)
        new_model = open_json_file(Path(new_schema_folder) / file_name)
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
            core_schema_file = CORE_SCHEMA_DIR / file_name.replace("_schema.json", ".py")

            with open(core_schema_file, 'r') as file:
                for line in file:
                    if line.lstrip().startswith("schema"):
                        current_version_line = line
            with open(core_schema_file, 'r') as file:
                filedata = file.read()
            bumped_version_line = current_version_line.replace(old_schema_version, new_schema_version)
            filedata = filedata.replace(current_version_line, bumped_version_line)
            with open(core_schema_file, 'w') as file:
                file.write(filedata)
            print(f"Schema version in {file_name.replace('_schema.json', '')} have been bumped to {new_schema_version}")
    return None


if __name__ == "__main__":
    sys_args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--new-schema-folder",
        required=True,
    )
    folder_args = parser.parse_args(sys_args)
    run_job(
        new_schema_folder=folder_args.new_schema_folder,
    )
