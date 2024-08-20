"""Module to handle the schema_versions"""

import json
import os
from pathlib import Path
from typing import Dict, List

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

    def __init__(self, commit_message: str = "", json_schemas_location: Path = Path(OLD_SCHEMA_DIR)):
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

    def _get_list_of_models_that_changed(self) -> List[AindCoreModel]:
        """
        Get a list of core models that have been updated by comparing the json
        schema of the models to the json schema in the schemas folder.
        Returns
        -------
        List[AindCoreModel]
          A list of AindCoreModels that changed.
        """
        schemas_that_need_updating = []
        for core_model in SchemaWriter.get_schemas():
            core_model_json = core_model.model_json_schema()
            default_filename = core_model.default_filename()
            if default_filename.find(".") != -1:
                schema_filename = default_filename[: default_filename.find(".")] + "_schema.json"
            main_branch_schema_path = self.json_schemas_location / schema_filename
            if main_branch_schema_path.exists():
                with open(main_branch_schema_path, "r") as f:
                    main_branch_schema_contents = json.load(f)
                diff = dictdiffer.diff(main_branch_schema_contents, core_model_json)
                if len(list(diff)) > 0:
                    schemas_that_need_updating.append(core_model)
        return schemas_that_need_updating

    @staticmethod
    def _get_incremented_versions_map(models_that_changed: List[AindCoreModel]) -> Dict[AindCoreModel, str]:
        """

        Parameters
        ----------
        models_that_changed : List[AindCoreModel]
          A list of models that have been updated and need to have their version numbers incremented.

        Returns
        -------
        Dict[AindCoreModel, str]
          A mapping of the AindCoreModel to its new version number.

        """
        version_bump_map = {}
        # TODO: Use commit message to determine version number to bump?
        for model in models_that_changed:
            old_v = semver.Version.parse(model.model_fields["schema_version"].default)
            new_v = old_v.bump_patch()
            version_bump_map[model] = str(new_v)
        return version_bump_map

    @staticmethod
    def _get_updated_file(python_file_path: str, new_ver: str) -> list:
        """
        Will read the lines of the file at python_file_path and replaces
        the line with the old version number with the updated version.
        Parameters
        ----------
        python_file_path : str
          Path of the python file that will be updated
        new_ver : str
          The new version number

        Returns
        -------

        """
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
    def _write_new_file(new_file_contents: list, python_file_path: str) -> None:
        """
        Abstracting the write operation to its own method in case we want a
        different file writer.
        Parameters
        ----------
        new_file_contents : list
          A list of encoded strings
        python_file_path : str
          The Path of the python to overwrite

        Returns
        -------
        None
          Writes the contents to the file path

        """
        with open(python_file_path, "wb") as f:
            for line in new_file_contents:
                f.write(line)

    def _update_files(self, version_bump_map: Dict[AindCoreModel, str]) -> None:
        """
        Using the information in the version_bump_map, will update the python
        files in the core directory.
        Parameters
        ----------
        version_bump_map : Dict[AindCoreModel, str]
          The models that need updating are in the dictionary keys and the
          new version number is the dictionary value.

        Returns
        -------
        None
          Updates the files in the core directory.

        """
        for model, new_ver in version_bump_map.items():
            python_file_path = os.path.join(CORE_SCHEMA_DIR, *model.__module__.split(".")) + ".py"
            new_file_contents = self._get_updated_file(python_file_path, new_ver)
            self._write_new_file(new_file_contents, python_file_path)

    def run_job(self):
        """
        This method will compare the json schema generated by the core models to the json schema
        in the schemas folder, see which schemas have changed, increment the versions, and update
        the necessary files.
        """
        list_of_models_that_changed = self._get_list_of_models_that_changed()
        list_of_incremented_versions = self._get_incremented_versions_map(list_of_models_that_changed)
        self._update_files(list_of_incremented_versions)


if __name__ == "__main__":
    # TODO: Pass in the commit message as an argument
    schema_version_handler = SchemaVersionHandler()
    schema_version_handler.run_job()
