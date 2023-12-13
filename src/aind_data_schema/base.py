""" generic base class with supporting validators and fields for basic AIND schema """

import re
import json
from os import PathLike
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr


class AindModel(BaseModel):
    """BaseModel that disallows extra fields"""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    @classmethod
    def write_standard_model(cls, filename: Optional[PathLike] = None) -> None:
        """
        Compiles and writes a model to a json-schema
        Parameters
        ----------
        filename:
            optional PathLike object for the filename
        """
        filename = cls.__name__ + '.json' if filename is None else filename
        with open(filename, "w") as f:
            f.write(json.dumps(cls.model_json_schema(), indent=3))


class AindCoreModel(AindModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    _FILE_EXTENSION = PrivateAttr(default=".json")
    _DESCRIBED_BY_BASE_URL = PrivateAttr(
        default="https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/"
    )

    describedBy: str = Field(...)
    schema_version: str = Field(
        ..., pattern=r"^\d+.\d+.\d+$", description="schema version", title="Version", frozen=True
    )

    @classmethod
    def default_filename(cls):
        """
        Returns standard filename in snakecase
        """
        name = cls.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + cls._FILE_EXTENSION.default

    def write_standard_file(self, output_directory: Optional[PathLike] = None, prefix=None, suffix=None):
        """
        Writes schema to standard json file
        Parameters
        ----------
        output_directory:
            optional Path object for output directory
        prefix:
            optional str for intended filepath with extra naming convention
        suffix:
            optional str for intended filepath with extra naming convention
        """
        filename = self.default_filename()
        if prefix:
            filename = str(prefix) + "_" + filename
        if suffix:
            filename = filename.replace(self._FILE_EXTENSION, suffix)

        if output_directory is not None:
            output_directory = Path(output_directory)
            filename = output_directory / filename

        with open(filename, "w") as f:
            f.write(self.model_dump_json(indent=3))
