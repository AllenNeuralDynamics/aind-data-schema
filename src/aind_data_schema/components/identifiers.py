""" Schema for identifiers """

from typing import Optional
from pydantic import BaseModel, Field
from aind_data_schema_models.registries import Registry, _Orcid


class Investigator(BaseModel):
    """Investigator identifier"""

    name: str = Field(..., title="Investigator name", description="Investigator first and last name OR anonmyous ID")

    registry: _Orcid = Field(default_factory=lambda: Registry.ORCID, title="Registry")
    registry_identifier: Optional[str] = Field(default=None, title="ORCID ID")
