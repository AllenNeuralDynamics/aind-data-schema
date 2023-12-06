""" generic base class with supporting validators and fields for basic AIND schema """

import re
from pathlib import Path
from typing import Optional, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic.json_schema import SkipJsonSchema

# Custom type to handle Optionals. We want Optionals in the schema to render
# the way they did in pydantic version 1 for the time being while the UIs that
# create fillable forms from the schema are being updated.
T = TypeVar("T")
OptionalType = Union[T, SkipJsonSchema[None]]


def OptionalField(**kwargs):
    """Returns a custom Field for Optionals"""
    return Field(default=None, json_schema_extra=lambda x: x.pop("default"), **kwargs)


class AindModel(BaseModel):
    """BaseModel that disallows extra fields"""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class AindCoreModel(AindModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    _FILE_EXTENSION = PrivateAttr(default=".json")
    _DESCRIBED_BY_BASE_URL = PrivateAttr(
        default="https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/"
    )

    describedBy: str = Field(..., json_schema_extra={"const": True})
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

    def write_standard_file(self, output_directory: Optional[Path] = None, prefix=None, suffix=None):
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
