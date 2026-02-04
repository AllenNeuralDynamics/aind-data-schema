"""Specimen procedures module for AIND data schema."""

import warnings
from datetime import date
from enum import Enum
from typing import Dict, List, Optional, Union

from aind_data_schema_models.brain_atlas import BrainStructureModel
from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.specimen_procedure_types import SpecimenProcedureType
from aind_data_schema_models.units import SizeUnit
from pydantic import Field, model_validator

from aind_data_schema.base import AwareDatetimeWithDefault, DataModel, DiscriminatedList
from aind_data_schema.components.coordinates import Atlas, CoordinateSystem, Translation
from aind_data_schema.components.reagent import (
    FluorescentStain,
    GeneProbeSet,
    ProbeReagent,
    Reagent,
)
from aind_data_schema.utils.exceptions import OneOfError


class SectionOrientation(str, Enum):
    """Orientation of sectioning"""

    CORONAL = "Coronal"
    SAGITTAL = "Sagittal"
    TRANSVERSE = "Transverse"


class Section(DataModel):
    """Description of a single section of brain tissue"""

    output_specimen_id: str = Field(..., title="Specimen ID")
    targeted_structure: Optional[BrainStructureModel] = Field(default=None, title="Targeted structure")
    includes_surrounding_tissue: Optional[bool] = Field(
        default=None,
        title="Includes surrounding tissue",
        description="Whether the section includes additional tissue surrounding the targeted structure.",
    )

    coordinate_system_name: Optional[str] = Field(
        default=None, title="Coordinate system name", deprecated="Use PlanarSection instead"
    )
    start_coordinate: Optional[Translation] = Field(
        default=None, title="Start coordinate", deprecated="Use PlanarSection instead"
    )
    end_coordinate: Optional[Translation] = Field(
        default=None, title="End coordinate", deprecated="Use PlanarSection instead"
    )
    thickness: Optional[float] = Field(default=None, title="Slice thickness", deprecated="Use PlanarSection instead")
    thickness_unit: Optional[SizeUnit] = Field(
        default=None, title="Slice thickness unit", deprecated="Use PlanarSection instead"
    )
    partial_slice: Optional[List[AnatomicalRelative]] = Field(
        default=None,
        title="Partial slice",
        description="If sectioning does not include the entire slice, indicate which part of the slice is retained.",
        deprecated="Use PlanarSection instead",
    )

    @model_validator(mode="after")
    def deprecated_coordinate_fields(self):
        """Warn if deprecated coordinate fields are used"""
        deprecated_fields = []
        if self.coordinate_system_name is not None:
            deprecated_fields.append("coordinate_system_name")
        if self.start_coordinate is not None:
            deprecated_fields.append("start_coordinate")
        if self.end_coordinate is not None:
            deprecated_fields.append("end_coordinate")
        if self.thickness is not None:
            deprecated_fields.append("thickness")
        if self.thickness_unit is not None:
            deprecated_fields.append("thickness_unit")
        if self.partial_slice is not None:
            deprecated_fields.append("partial_slice")

        if deprecated_fields:
            warnings.warn(
                (
                    f"Section fields {deprecated_fields} are deprecated. "
                    "Use PlanarSection for sections with coordinate data."
                ),
                DeprecationWarning,
            )

        if self.start_coordinate and not self.end_coordinate and not self.thickness:
            raise OneOfError(
                "Section",
                ["end_coordinate", "thickness"],
            )

        return self


class PlanarSection(Section):
    """Description of a single planar section of brain tissue"""

    # Coordinates
    coordinate_system_name: str = Field(..., title="Coordinate system name")
    start_coordinate: Translation = Field(..., title="Start coordinate")
    end_coordinate: Optional[Translation] = Field(default=None, title="End coordinate")
    thickness: Optional[float] = Field(default=None, title="Slice thickness")
    thickness_unit: Optional[SizeUnit] = Field(default=None, title="Slice thickness unit")

    partial_slice: Optional[List[AnatomicalRelative]] = Field(
        default=None,
        title="Partial slice",
        description="If sectioning does not include the entire slice, indicate which part of the slice is retained.",
    )

    @model_validator(mode="after")
    def check_one_of_end_thickness(self):
        """Ensure that either end_coordinate or thickness is provided"""

        if not self.end_coordinate and not self.thickness:
            raise OneOfError(
                "PlanarError",
                ["end_coordinate", "thickness"],
            )
        return self


class Sectioning(DataModel):
    """Description of a sectioning procedure targeting a specific structure"""

    sections: List[Section] = Field(..., title="Sections")


class PlanarSectioning(Sectioning):
    """Description of a sectioning procedure performed on the coronal, sagittal, or transverse/axial plane"""

    coordinate_system: Optional[CoordinateSystem | Atlas] = Field(
        default=None,
        title="Sectioning coordinate system",
        description="Only required if different from the Procedures.coordinate_system",
    )

    sections: List[Union[Section, PlanarSection]] = Field(
        ..., title="Planar sections", description="Use PlanarSection for new implementations"
    )

    section_orientation: SectionOrientation = Field(..., title="Sectioning orientation")


class HybridizationChainReaction(DataModel):
    """Description of an HCR staining round"""

    round_index: int = Field(..., title="Round index")
    start_time: AwareDatetimeWithDefault = Field(..., title="Round start time")
    end_time: AwareDatetimeWithDefault = Field(..., title="Round end time")
    stains: List[FluorescentStain] = Field(..., title="Stains")
    probe_concentration: float = Field(..., title="Probe concentration (M)")
    probe_concentration_unit: str = Field(default="M", title="Probe concentration unit")


class HCRSeries(DataModel):
    """Description of series of HCR staining rounds for mFISH"""

    codebook_name: str = Field(..., title="Codebook name")
    number_of_rounds: int = Field(..., title="Number of round")
    hcr_rounds: List[HybridizationChainReaction] = Field(..., title="Hybridization Chain Reaction rounds")
    strip_qc_compatible: bool = Field(..., title="Strip QC compatible")
    cell_id: Optional[str] = Field(default=None, title="Cell ID")


class SpecimenProcedure(DataModel):
    """Description of surgical or other procedure performed on a specimen"""

    procedure_type: SpecimenProcedureType = Field(..., title="Procedure type")
    procedure_name: Optional[str] = Field(default=None, title="Procedure name")
    specimen_id: Union[str, List[str]] = Field(..., title="Specimen ID(s)")
    start_date: date = Field(..., title="Start date")
    end_date: date = Field(..., title="End date")
    experimenters: List[str] = Field(
        default=[],
        title="experimenter(s)",
    )
    protocol_id: Optional[List[str]] = Field(default=None, title="Protocol ID", description="DOI for protocols.io")
    protocol_parameters: Optional[Dict[str, str]] = Field(
        default=None,
        title="Protocol parameters",
        description="Parameters defined in the protocol and their value during this procedure",
    )

    procedure_details: DiscriminatedList[
        HCRSeries | FluorescentStain | Sectioning | PlanarSectioning | ProbeReagent | Reagent | GeneProbeSet
    ] = Field(
        default=[],
        title="Procedure details",
        description="Details of the procedures, including reagents and sectioning information.",
    )

    notes: Optional[str] = Field(default=None, title="Notes")

    @model_validator(mode="after")
    def validate_procedure_type(self):
        """Adds a validation check on procedure_type"""

        has_hcr_series = any(isinstance(detail, HCRSeries) for detail in self.procedure_details)
        has_fluorescent_stain = any(isinstance(detail, FluorescentStain) for detail in self.procedure_details)
        has_protein_probe = any(isinstance(detail, ProbeReagent) for detail in self.procedure_details)
        has_sectioning = any(isinstance(detail, PlanarSectioning) for detail in self.procedure_details)
        has_geneprobeset = any(isinstance(detail, GeneProbeSet) for detail in self.procedure_details)

        if has_hcr_series + has_fluorescent_stain + has_sectioning + has_geneprobeset + has_protein_probe > 1:
            raise AssertionError("SpecimenProcedure.procedure_details should only contain one type of model.")

        if self.procedure_type == SpecimenProcedureType.OTHER and not self.notes:
            raise AssertionError(
                "notes cannot be empty if procedure_type is Other. Describe the procedure in the notes field."
            )
        elif self.procedure_type == SpecimenProcedureType.HYBRIDIZATION_CHAIN_REACTION and not has_hcr_series:
            raise AssertionError("HCRSeries required if procedure_type is HCR.")
        elif self.procedure_type == SpecimenProcedureType.IMMUNOLABELING and not (
            has_fluorescent_stain or has_protein_probe
        ):
            raise AssertionError("FluorescentStain or ProbeReagent required if procedure_type is Immunolabeling.")
        elif self.procedure_type == SpecimenProcedureType.SECTIONING and not has_sectioning:
            raise AssertionError("Sectioning required if procedure_type is Sectioning.")
        elif self.procedure_type == SpecimenProcedureType.BARSEQ and not has_geneprobeset:
            raise AssertionError("GeneProbeSet required if procedure_type is BarSEQ.")
        return self


def section_to_planar_section(section: Section) -> PlanarSection:
    """Convert a Section with coordinate data to a PlanarSection.

    This utility helps migrate from the deprecated Section coordinate fields
    to the new PlanarSection class.

    Parameters
    ----------
    section : Section
        A Section object with coordinate fields populated

    Returns
    -------
    PlanarSection
        A PlanarSection object with the same data

    Raises
    ------
    ValueError
        If the section lacks required coordinate data
    """
    if not section.coordinate_system_name or not section.start_coordinate:
        raise ValueError("Section must have coordinate_system_name and start_coordinate to convert to PlanarSection")

    return PlanarSection(
        output_specimen_id=section.output_specimen_id,
        targeted_structure=section.targeted_structure,
        includes_surrounding_tissue=section.includes_surrounding_tissue,
        coordinate_system_name=section.coordinate_system_name,
        start_coordinate=section.start_coordinate,
        end_coordinate=section.end_coordinate,
        thickness=section.thickness,
        thickness_unit=section.thickness_unit,
        partial_slice=section.partial_slice,
    )
