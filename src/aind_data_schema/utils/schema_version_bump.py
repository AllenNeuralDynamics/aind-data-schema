"""Utility script for bumping schema versions"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Type

import dictdiffer
import semver

from aind_data_schema.base import AindCoreModel
from aind_data_schema.utils.json_writer import SchemaWriter

CURRENT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = CURRENT_DIR.parents[2]
OLD_SCHEMA_DIR = ROOT_DIR / "schemas"
CORE_SCHEMA_DIR = ROOT_DIR / "src"


class SchemaVersionHandler:
    """Class that manages semantic versioning of the schemas"""

    def __init__(
            self,
            commit_message: str = '',
            json_schemas_location: Path = Path(OLD_SCHEMA_DIR)
    ):
        """
        Class constructor
        Parameters
        ----------
        commit_message : str
          We can parse the commit message to manage which version to
          bump. For now, we will just bump the patch.
        json_schemas_location : Path
          Directory location of main branch schemas
        """
        self.commit_message = commit_message
        self.json_schemas_location = json_schemas_location

    def get_list_of_models_that_changed(self) -> List[AindCoreModel]:
        """Get a list of core models that have been updated."""
        schemas_that_need_updating = []
        for core_model in SchemaWriter.get_schemas():
            core_model_json = core_model.model_json_schema()
            default_filename = core_model.default_filename()
            main_branch_schema_path = (
                    self.json_schemas_location / default_filename
            )
            with open(main_branch_schema_path, "r") as f:
                main_branch_schema_contents = json.load(f)
            diff = dictdiffer.diff(main_branch_schema_contents, core_model_json)
            if len(list(diff)) > 0:
                schemas_that_need_updating.append(core_model)
        return schemas_that_need_updating

    @staticmethod
    def get_incremented_versions_map(models_that_changed: List[AindCoreModel]) -> Dict[AindCoreModel, str]:
        version_bump_map = {}
        # TODO: Use commit message to determine version number to bump?
        for model in models_that_changed:
            old_v = semver.Version.parse(model.model_fields["schema_version"].default)
            new_v = old_v.bump_patch()
            version_bump_map[model] = str(new_v)
        return version_bump_map

    @staticmethod
    def get_updated_file(python_file_path, new_ver: str) -> list:
        new_file_contents = []
        with open(python_file_path, "rb") as f:
            file_lines = f.readlines()
        for line in file_lines:
            if "schema_version: Literal[" in str(line):
                new_line_str = f'    schema_version: Literal["{new_ver}"] = Field("{new_ver}")\n'
                new_line = new_line_str.encode()
            else:
                new_line = line
            new_file_contents.append(new_line)
        return new_file_contents

    @staticmethod
    def write_new_file(new_file_contents: list, python_file_path) -> None:
        with open(python_file_path, 'wb') as f:
            for line in new_file_contents:
                f.write(line)

    def update_files(self, version_bump_map: Dict[AindCoreModel, str]) -> None:
        for model, new_ver in version_bump_map.items():
            python_file_path = os.path.join(CORE_SCHEMA_DIR,
                                            *model.__module__.split(
                                                ".")) + ".py"
            new_file_contents = self.get_updated_file(python_file_path, new_ver)
            self.write_new_file(new_file_contents, python_file_path)

    def run_job(self):
        list_of_models_that_changed = self.get_list_of_models_that_changed()
        list_of_inceremented_versions = self.get_incremented_versions_map(list_of_models_that_changed)
        self.update_files(list_of_inceremented_versions)





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
