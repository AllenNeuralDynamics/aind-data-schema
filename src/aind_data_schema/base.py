""" generic base class with supporting validators and fields for basic AIND schema """

import inspect
import os
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

    pass


class AindCoreModel(AindModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    describedBy: str

    def __init_subclass__(cls, optional_fields=None, **kwargs):
        """add the describedby field to all subclasses"""
        super().__init_subclass__(**kwargs)

        value = build_described_by(cls)
        field = ModelField.infer(
            name="describedBy",
            value=value,
            annotation=str,
            class_validators=None,
            config=cls.__config__,
        )
        field.field_info.const = True
        cls.__fields__.update({"describedBy": field})

    def _get_default_filename(self):
        """
        returns standard filename (schema.json)
        """
        return self.__class__.__name__.lower() + ".json"

    def write_standard_file(self, prefix=None):
        """
        writes schema to standard json file
        parameters
        ----------
        prefix: 
            optional str for intended filepath with extra naming convention
        """
        if prefix is None:
            filename = self._get_default_filename()
        else:
            filename = str(prefix) + "_" + self._get_default_filename()
        with open(filename, "w") as f:
            f.write(self.json(indent=3))
