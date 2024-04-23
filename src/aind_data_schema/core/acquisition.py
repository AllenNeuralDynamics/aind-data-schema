""" schema describing imaging acquisition """

from decimal import Decimal
from typing import List, Literal, Optional, Union

from pydantic import Field, field_validator

from aind_data_schema.base import AindCoreModel, AindModel, AwareDatetimeWithDefault
from aind_data_schema.imaging.tile import AcquisitionTile
from aind_data_schema.models.coordinates import AnatomicalDirection, AxisName, ImageAxis
from aind_data_schema.models.devices import Calibration, ImmersionMedium, Maintenance
from aind_data_schema.models.process_names import ProcessName


class Immersion(AindModel):
    """Description of immersion medium"""

    medium: ImmersionMedium = Field(..., title="Immersion medium")
    refractive_index: Decimal = Field(..., title="Index of refraction")


class ProcessingSteps(AindModel):
    """Description of downstream processing steps"""

    channel_name: str = Field(..., title="Channel name")
    process_name: List[
        Literal[
            ProcessName.IMAGE_ATLAS_ALIGNMENT,
            ProcessName.IMAGE_BACKGROUND_SUBTRACTION,
            ProcessName.IMAGE_CELL_SEGMENTATION,
            ProcessName.IMAGE_DESTRIPING,
            ProcessName.IMAGE_FLATFIELD_CORRECTION,
            ProcessName.IMAGE_IMPORTING,
            ProcessName.IMAGE_THRESHOLDING,
            ProcessName.IMAGE_TILE_ALIGNMENT,
            ProcessName.IMAGE_TILE_FUSING,
            ProcessName.IMAGE_TILE_PROJECTION,
            ProcessName.FILE_CONVERSION,
        ]
    ] = Field(...)


class Acquisition(AindCoreModel):
    """Description of an imaging acquisition session"""

    _DESCRIBED_BY_URL = AindCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/acquisition.py"
    describedBy: str = Field(_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: Literal["0.6.13"] = Field("0.6.13")
    protocol_id: List[str] = Field([], title="Protocol ID", description="DOI for protocols.io")
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    specimen_id: str = Field(..., title="Specimen ID")
    subject_id: Optional[str] = Field(None, title="Subject ID")
    instrument_id: str = Field(..., title="Instrument ID")
    calibrations: List[Calibration] = Field(
        default=[],
        title="Calibrations",
        description="List of calibration measurements taken prior to acquisition.",
    )
    maintenance: List[Maintenance] = Field(
        default=[], title="Maintenance", description="List of maintenance on rig prior to acquisition."
    )
    session_start_time: AwareDatetimeWithDefault = Field(..., title="Session start time")
    session_end_time: AwareDatetimeWithDefault = Field(..., title="Session end time")
    session_type: Optional[str] = Field(None, title="Session type")
    tiles: List[AcquisitionTile] = Field(..., title="Acquisition tiles")
    axes: List[ImageAxis] = Field(..., title="Acquisition axes")
    chamber_immersion: Immersion = Field(..., title="Acquisition chamber immersion data")
    sample_immersion: Optional[Immersion] = Field(None, title="Acquisition sample immersion data")
    active_objectives: Optional[List[str]] = Field(None, title="List of objectives used in this acquisition.")
    local_storage_directory: Optional[str] = Field(None, title="Local storage directory")
    external_storage_directory: Optional[str] = Field(None, title="External storage directory")
    processing_steps: List[ProcessingSteps] = Field(
        default=[],
        title="Processing steps",
        description="List of downstream processing steps planned for each channel",
    )
    notes: Optional[str] = Field(None, title="Notes")

    @field_validator("axes", mode="before")
    def from_direction_code(cls, v: Union[str, List[ImageAxis]]) -> List[ImageAxis]:
        """Map direction codes to Axis model"""
        if type(v) is str:
            direction_lookup = {
                "L": AnatomicalDirection.LR,
                "R": AnatomicalDirection.RL,
                "A": AnatomicalDirection.AP,
                "P": AnatomicalDirection.PA,
                "I": AnatomicalDirection.IS,
                "S": AnatomicalDirection.SI,
            }

            name_lookup = [AxisName.X, AxisName.Y, AxisName.Z]

            axes = []
            for i, c in enumerate(v):
                axis = ImageAxis(name=name_lookup[i], direction=direction_lookup[c], dimension=i)
                axes.append(axis)
            return axes
        else:
            return v
