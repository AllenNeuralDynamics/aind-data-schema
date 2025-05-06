""" schema for mostly mouse metadata """

from typing import Literal, Optional

from pydantic import Field, SkipValidation

from aind_data_schema.base import DataCoreModel, Discriminated
from aind_data_schema.components.subjects import HumanSubject, MouseSubject


class Subject(DataCoreModel):
    """Description of a subject of data collection"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/subject.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.6"]] = Field(default="2.0.6")
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject. If this is not a Allen LAS ID, indicate this in the Notes.",
        title="Subject ID",
    )

    subject_details: Discriminated[MouseSubject | HumanSubject] = Field(..., title="Subject Details")

    notes: Optional[str] = Field(default=None, title="Notes")
