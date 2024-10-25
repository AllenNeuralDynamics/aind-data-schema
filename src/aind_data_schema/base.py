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
from pydantic import model_validator
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

    @model_validator(mode="after")
    def unit_validator(cls, values):
        """Ensure that all fields matching the pattern variable_unit are set if
        they have a matching variable that is set (!= None)

        This also checks the multi-variable condition, i.e. variable_unit is set
        if any of variable_* are set
        """
        # Accumulate a dictionary mapping variable : unit/unit_value
        for unit_name, unit_value in values:
            if "_unit" in unit_name and not unit_value:
                var_name = unit_name.rsplit("_unit", 1)[0]
                root_name = unit_name.split("_")[0]

                # Go through all the values again, if any value matches the variable name
                # and is set, then the unit needs to be set as well
                for variable_name, variable_value in values:
                    if variable_name == var_name:
                        if variable_value:
                            raise ValueError(f"Unit {unit_name} is required when {variable_name} is set.")
                        # if we found our variable and it was None, we can move on
                        continue

                # One more time, now looking for the multi-variable condition
                for variable_name, variable_value in values:
                    # skip the unit itself
                    if variable_name is not unit_name:
                        if root_name in variable_name and variable_value:
                            raise ValueError(f"Unit {unit_name} is required when {variable_name} is set.")

        return values


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
