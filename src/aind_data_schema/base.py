from pydantic import BaseModel, validator
from pydantic.fields import ModelField

import urllib.parse
import aind_data_schema
import os
import inspect

DESCRIBED_BY_BASE_URL = "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/"


def build_described_by(cls, base_url=DESCRIBED_BY_BASE_URL):
    """construct a pydantic Field that refers to a specific file"""

    # find the root path of this package
    path = os.path.dirname(aind_data_schema.__file__)

    # get the filename of the class
    filename = inspect.getfile(cls)

    # remove package prefix from class filename
    filename = filename.replace(path + os.sep, "")

    # forward slashes
    filename = filename.replace(os.sep, "/")

    return urllib.parse.urljoin(base_url, filename)


class AindSchema(BaseModel):
    """Generic base class to hold common fields/validators/etc for all basic AIND schema"""

    describedBy: str

    def __init_subclass__(cls, optional_fields=None, **kwargs):
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
