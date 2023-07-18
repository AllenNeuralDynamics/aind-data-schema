""" generic base class with supporting validators and fields for basic AIND schema """

import inspect
import logging
import os
import re
import urllib.parse
from enum import Enum, EnumMeta
from pathlib import Path
from typing import Optional, Tuple

from pydantic import BaseModel, Extra, Field
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass

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


class BaseNameEnumMeta(EnumMeta):
    """Allows to create complicated enum based on attribute name."""

    def __call__(cls, value, *args, **kw):
        """Allow enum to be set by a string."""
        if isinstance(value, str):
            value = getattr(cls, value.upper())

        return super().__call__(value, *args, **kw)

    def __modify_schema__(cls, field_schema):
        """Adds enumNames to institution"""
        field_schema.update(
            enumNames=[e.value.name for e in cls],
        )


class BaseName(AindModel):
    """A simple model associating a name with an abbreviation"""

    name: str = Field(..., title="Name")
    abbreviation: Optional[str] = Field(None, title="Abbreviation")


class PIDName(BaseName):
    """
    Model for associate a name with a persistent identifier (PID),
    the registry for that PID, and abbreviation for that registry
    """

    registry: Optional[BaseName] = Field(None, title="Registry")
    registry_identifier: Optional[str] = Field(None, title="Registry identifier")


class AindCoreModel(AindModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    describedBy: str
    schema_version: str = Field(..., regex=r"^\d+.\d+.\d+$")

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

    def write_standard_file(self, output_directory: Optional[Path] = None, prefix=None):
        """
        Writes schema to standard json file
        Parameters
        ----------
        output_directory:
            optional Path object for output directory
        prefix:
            optional str for intended filepath with extra naming convention

        """
        if prefix is None:
            filename = self.default_filename()
        else:
            filename = str(prefix) + "_" + self.default_filename()

        if output_directory is not None:
            filename = output_directory / filename

        with open(filename, "w") as f:
            f.write(self.json(indent=3))


class _TypeEnumSubset(object):
    """Helper class useful for defining a custom pydantic data type"""

    @classmethod
    def __get_validators__(cls):
        """Method needs to be defined for pydantic"""
        yield cls.validate_allowable

    @classmethod
    def validate_allowable(cls, val):
        """This will check whether the input value is one of the enums from the enum_set"""
        enum_set = getattr(cls, "enum_set")
        enum_class = type(enum_set) if isinstance(enum_set, tuple) is False else type(enum_set[0])
        if isinstance(val, dict) or isinstance(val, str) or isinstance(type(val), ModelMetaclass):
            val = enum_class(val)
        if val not in enum_set:
            raise ValueError(f"Value not allowed! {val}")
        else:
            return val

    @classmethod
    def __modify_schema__(cls, field_schema):
        """To render the schema correctly, it needs an enum field and an enumNames field."""
        enum_set = getattr(cls, "enum_set")
        field_schema["enumNames"] = [e.name for e in enum_set]
        field_schema["enum"] = [e.value for e in enum_set]


class _EnumSubsetMeta(type):
    """Metaclass used to pass the enum set values"""

    def __getitem__(self, t):
        """Function needed for a user to define a class with square brackets"""

        # Convert to Tuple if only single value passed
        if not isinstance(t, Tuple):
            t = (t,)

        # Check that only enums of a specific class are being passed
        first_type = type(t[0])
        if not issubclass(first_type, Enum):
            raise TypeError(f"Only Enums are allowed. {first_type}")
        for enum_member in t[1:]:
            if type(enum_member) != first_type:
                raise ValueError("All enums must be of the same class.")
        return type("EnumSubset", (_TypeEnumSubset,), {"enum_set": t})


class EnumSubset(object, metaclass=_EnumSubsetMeta):
    """Special data type for fields that use a subset of enums"""
