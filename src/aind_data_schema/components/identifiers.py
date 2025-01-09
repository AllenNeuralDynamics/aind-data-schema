""" Schema for identifiers """

from typing import Optional
from pydantic import BaseModel, Field, model_validator
from aind_data_schema_models.registries import Registry


class Experimenter(BaseModel):
    """Experimenter identifier"""

    first_name: Optional[str] = Field(default=None, title="Experimenter first name")
    last_name: Optional[str] = Field(default=None, title="Experimenter last name")
    registry: Registry.ORCID = Field(default=Registry.ORCID, title="Registry")
    registry_identifier: Optional[str] = Field(default=None, title="ORCID ID")
    anonymous_id: Optional[str] = Field(default=None, title="Anonymous ID")

    @model_validator(mode="before")
    def validate_name(cls, v):
        """Ensure that either the first/last name or anonymous ID is provided"""
        if not (v.get("first_name") and v.get("last_name")) and not v.get("anonymous_id"):
            raise ValueError("Either first/last name or anonymous ID must be provided")
        return v
