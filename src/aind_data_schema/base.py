""" generic base class with supporting validators and fields for basic AIND schema """

import inspect
import logging
import os
import re
import urllib.parse

from pydantic import BaseModel, Extra
from pydantic.fields import ModelField

DESCRIBED_BY_BASE_URL = "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/"


def build_described_by(cls, base_url=DESCRIBED_BY_BASE_URL):
    """construct a pydantic Field that refers to a specific file"""

    # get the filename of the class
    filename = inspect.getfile(cls)

    # strip off local directories
    package_index = filename.rfind("aind_data_schema")
    filename = filename[package_index:]

    # forward slashes
    filename = filename.replace(os.sep, "/")

    described_by = urllib.parse.urljoin(base_url, filename)

    return described_by


class AindModel(BaseModel, extra=Extra.forbid):
    """BaseModel that disallows extra fields"""


class BaseName(AindModel):
    """A simple model associating a name with an abbreviation"""

    name: str
    abbreviation: str


class AindCoreModel(AindModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    describedBy: str
    schema_version: str

    def __init_subclass__(cls, optional_fields=None, **kwargs):
        """Add the describedby field to all subclasses"""
        super().__init_subclass__(**kwargs)

        value = build_described_by(cls)
        field = ModelField.infer(
            name="describedBy", value=value, annotation=str, class_validators=None, config=cls.__config__
        )
        field.field_info.const = True
        cls.__fields__.update({"describedBy": field})

    @staticmethod
    def _get_direct_subclass(pydantic_class):
        """
        Check superclasses for a direct subclass of AindCoreModel
        """
        try:
            new_cls = pydantic_class
            bases = new_cls.__bases__
            first_base = bases[0]
            while bases and AindCoreModel is not first_base:
                new_cls = bases[0]
                bases = new_cls.__bases__
                first_base = bases[0]
            return new_cls
        except IndexError:
            logging.error(f"Unable to find direct AindCoreModel subclass for {pydantic_class}")
            raise IndexError

    @classmethod
    def default_filename(cls):
        """
        Returns standard filename in snakecase
        """
        name = cls._get_direct_subclass(cls).__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + ".json"

    def write_standard_file(self, prefix=None):
        """
        Writes schema to standard json file
        Parameters
        ----------
        prefix:
            optional str for intended filepath with extra naming convention
        """
        if prefix is None:
            filename = self.default_filename()
        else:
            filename = str(prefix) + "_" + self.default_filename()
        with open(filename, "w") as f:
            f.write(self.json(indent=3))
