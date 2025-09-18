"""schema for various Procedures"""

from typing import List, Literal, Optional

from pydantic import Field, SkipValidation, field_validator, model_validator

from aind_data_schema.base import DataCoreModel, DiscriminatedList
from aind_data_schema.components.coordinates import CoordinateSystem
from aind_data_schema.components.injection_procedures import Injection
from aind_data_schema.components.specimen_procedures import SpecimenProcedure
from aind_data_schema.components.subject_procedures import (
    GenericSubjectProcedure,
    Surgery,
    TrainingProtocol,
    WaterRestriction,
)
from aind_data_schema.utils.merge import merge_notes
from aind_data_schema.utils.validators import subject_specimen_id_compatibility


class Procedures(DataCoreModel):
    """Description of all procedures performed on a subject, including surgeries, injections, and tissue processing"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/procedures.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})

    schema_version: SkipValidation[Literal["2.0.34"]] = Field(default="2.0.34")
    subject_id: str = Field(
        ...,
        description="Unique identifier for the subject of data acquisition",
        title="Subject ID",
    )
    subject_procedures: DiscriminatedList[
        Surgery | Injection | TrainingProtocol | WaterRestriction | GenericSubjectProcedure
    ] = Field(default=[], title="Subject Procedures", description="Procedures performed on a live subject")
    specimen_procedures: List[SpecimenProcedure] = Field(
        default=[], title="Specimen Procedures", description="Procedures performed on tissue extracted after perfusion"
    )

    # Coordinate system
    coordinate_system: Optional[CoordinateSystem] = Field(
        default=None,
        title="Coordinate System",
        description=(
            "Origin and axis definitions for determining the configured position of devices implanted during"
            " procedures. Required when coordinates are provided within the Procedures"
        ),
    )  # note: exact field name is used by a validator

    notes: Optional[str] = Field(default=None, title="Notes")

    def get_device_names(self) -> List[str]:
        """Get all device names for implanted devices in the procedures"""
        device_names = set()

        for procedure in self.subject_procedures:
            # These commented lines are left in case we added implanted_devices to a subject procedure
            # if hasattr(procedure, "implanted_device") and procedure.implanted_device is not None:
            #     device_names.add(procedure.implanted_device.name)
            if hasattr(procedure, "procedures"):
                for surgery_procedure in procedure.procedures:
                    if (
                        hasattr(surgery_procedure, "implanted_device")
                        and surgery_procedure.implanted_device is not None
                    ):
                        device_names.add(surgery_procedure.implanted_device.name)

        # These commented lines are left in case we added implanted_devices to a specimen procedure
        # for spec_proc in self.specimen_procedures:
        #     if hasattr(spec_proc, "implanted_device") and spec_proc.implanted_device is not None:
        #         device_names.add(spec_proc.implanted_device.name)

        return list(device_names)

    @field_validator("specimen_procedures", mode="after")
    def validate_identical_specimen_ids(cls, v, values):
        """Validate that all specimen_id fields are identical in the specimen_procedures"""

        if v:
            specimen_ids = [spec_proc.specimen_id for spec_proc in v]

            if any(spec_id != specimen_ids[0] for spec_id in specimen_ids):
                raise ValueError("All specimen_id must be identical in the specimen_procedures.")

        return v

    @model_validator(mode="after")
    def validate_subject_specimen_ids(values):
        """Validate that the subject_id and specimen_id match"""

        # Return if no specimen procedures
        if values.specimen_procedures:
            subject_id = values.subject_id
            specimen_ids = [spec_proc.specimen_id for spec_proc in values.specimen_procedures]

            if any(not subject_specimen_id_compatibility(subject_id, spec_id) for spec_id in specimen_ids):
                raise ValueError("specimen_id must be an extension of the subject_id.")

        return values

    def __add__(self, other: "Procedures") -> "Procedures":
        """Combine two Procedures objects"""

        if not self.schema_version == other.schema_version:
            raise ValueError("Schema versions must match to combine Procedures")

        if not self.subject_id == other.subject_id:
            raise ValueError("Subject IDs must match to combine Procedures objects.")

        # Check for incompatible coordinate systems
        if self.coordinate_system != other.coordinate_system:
            raise ValueError(
                "Cannot combine Procedures objects with different coordinate systems: "
                f"{self.coordinate_system} vs {other.coordinate_system}"
            )

        return Procedures(
            subject_id=self.subject_id,
            subject_procedures=self.subject_procedures + other.subject_procedures,
            specimen_procedures=self.specimen_procedures + other.specimen_procedures,
            coordinate_system=self.coordinate_system,
            notes=merge_notes(self.notes, other.notes),
        )
