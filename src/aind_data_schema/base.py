""" generic base class with supporting validators and fields for basic AIND schema """

import re
from pathlib import Path
from typing import Any, Generic, Optional, TypeVar

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    NaiveDatetime,
    PrivateAttr,
    ValidationError,
    ValidatorFunctionWrapHandler,
    create_model,
)
from pydantic.functional_validators import WrapValidator
from typing_extensions import Annotated


def _coerce_naive_datetime(v: Any, handler: ValidatorFunctionWrapHandler) -> AwareDatetime:
    """Validator to wrap around AwareDatetime to set a default timezone as user's locale"""
    try:
        return handler(v)
    except ValidationError:
        # Try to parse the input as a naive datetime object and attach timezone info
        return create_model("TempNaiveDatetimeModel", dt=(NaiveDatetime, ...)).model_validate({"dt": v}).dt.astimezone()


AwareDatetimeWithDefault = Annotated[AwareDatetime, WrapValidator(_coerce_naive_datetime)]


class AindGeneric(BaseModel, extra="allow"):
    """Base class for generic types that can be used in AIND schema"""

    # extra="allow" is needed because BaseModel by default drops extra parameters.
    # Alternatively, consider using 'SerializeAsAny' once this issue is resolved
    # https://github.com/pydantic/pydantic/issues/6423
    pass


AindGenericType = TypeVar("AindGenericType", bound=AindGeneric)


class AindModel(BaseModel, Generic[AindGenericType]):
    """BaseModel that disallows extra fields"""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)


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
        parent_classes = [base_class for base_class in cls.__bases__ if base_class.__name__ != AindCoreModel.__name__]

        name = cls.__name__

        if len(parent_classes):
            name = parent_classes[0].__name__

        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + cls._FILE_EXTENSION.default

    def write_standard_file(
        self,
        output_directory: Optional[Path] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ):
        """
        Writes schema to standard json file
        Parameters
        ----------
        output_directory: Optional[Path]
            optional Path object for output directory.
            Default: None

        prefix: Optional[str]
            optional str for intended filepath with extra naming convention
            Default: None

        suffix: Optional[str]
            optional str for intended filepath with extra naming convention
            Default: None

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
