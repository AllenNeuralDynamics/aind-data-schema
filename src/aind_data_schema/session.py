""" Schemas for Physiology and/or Behavior Sessions """

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import Field, root_validator
from pydantic.typing import Annotated, Literal

from aind_data_schema.base import AindCoreModel, AindModel
from aind_data_schema.coordinates import CcfCoords, Coordinates3d
from aind_data_schema.data_description import Modality
from aind_data_schema.device import Calibration, Maintenance, RelativePosition, SpoutSide
from aind_data_schema.imaging.tile import Channel
from aind_data_schema.stimulus import StimulusEpoch
from aind_data_schema.utils.units import AngleUnit, FrequencyUnit, MassUnit, PowerUnit, SizeUnit, TimeUnit


# Ophys components
class FiberName(Enum):
    """Fiber name"""

    FIBER_A = "Fiber A"
    FIBER_B = "Fiber B"
    FIBER_C = "Fiber C"
    FIBER_D = "Fiber D"
    FIBER_E = "Fiber E"


class PatchCordName(Enum):
    """Patch cord name"""

    PATCH_CORD_A = "Patch Cord A"
    PATCH_CORD_B = "Patch Cord B"
    PATCH_CORD_C = "Patch Cord C"
    PATCH_CORD_D = "Patch Cord D"


class FiberPhotometryAssembly(AindModel):
    """Description of a fiber photometry configuration"""

    patch_cord_name: PatchCordName = Field(..., title="Name")
    patch_cord_output_power: Decimal = Field(..., title="Output power (uW)")
    output_power_unit: PowerUnit = Field(PowerUnit.UW, title="Output power unit")
    fiber_name: FiberName = Field(..., title="Fiber name")


class TriggerType(Enum):
    """Types of detector triggers"""

    INTERNAL = "Internal"
    EXTERNAL = "External"


class Detector(AindModel):
    """Description of detector settings"""

    name: str = Field(..., title="Name")
    exposure_time: Decimal = Field(..., title="Exposure time (ms)")
    exposure_time_unit: TimeUnit = Field(TimeUnit.MS, title="Exposure time unit")
    trigger_type: TriggerType = Field(..., title="Trigger type")


class LightEmittingDiode(AindModel):
    """Description of LED settings"""

    device_type: Literal["LightEmittingDiode"] = Field("LightEmittingDiode", const=True, readOnly=True)
    name: str = Field(..., title="Name")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


class FieldOfView(AindModel):
    """Description of an imaging field of view"""

    index: int = Field(..., title="Index")
    imaging_depth: int = Field(..., title="Imaging depth (um)")
    imaging_depth_unit: SizeUnit = Field(SizeUnit.UM, title="Imaging depth unit")
    targeted_structure: str = Field(..., title="Targeted structure")
    fov_coordinate_ml: Decimal = Field(..., title="FOV coordinate ML")
    fov_coordinate_ap: Decimal = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(..., title="FOV reference", description="Reference for ML/AP coordinates")
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(SizeUnit.PX, title="FOV size unit")
    magnification: str = Field(..., title="Magnification")
    fov_scale_factor: Decimal = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field("um/pixel", title="FOV scale factor unit")
    frame_rate: Decimal = Field(..., title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")


class StackChannel(Channel):
    """Description of a Channel used in a Stack"""

    start_depth: int = Field(..., title="Starting depth (um)")
    end_depth: int = Field(..., title="Ending depth (um)")
    depth_unit: SizeUnit = Field(SizeUnit.UM, title="Depth unit")


class Stack(AindModel):
    """Description of a two photon stack"""

    channels: List[StackChannel] = Field(..., title="Channels")
    number_of_planes: int = Field(..., title="Number of planes")
    step_size: float = Field(..., title="Step size (um)")
    step_size_unit: SizeUnit = Field(SizeUnit.UM, title="Step size unit")
    number_of_plane_repeats_per_volume: int = Field(..., title="Number of repeats per volume")
    number_of_volume_repeats: int = Field(..., title="Number of volume repeats")
    fov_coordinate_ml: float = Field(..., title="FOV coordinate ML")
    fov_coordinate_ap: float = Field(..., title="FOV coordinate AP")
    fov_coordinate_unit: SizeUnit = Field(SizeUnit.UM, title="FOV coordinate unit")
    fov_reference: str = Field(..., title="FOV reference", description="Reference for ML/AP coordinates")
    fov_width: int = Field(..., title="FOV width (pixels)")
    fov_height: int = Field(..., title="FOV height (pixels)")
    fov_size_unit: SizeUnit = Field(SizeUnit.PX, title="FOV size unit")
    magnification: Optional[str] = Field(None, title="Magnification")
    fov_scale_factor: float = Field(..., title="FOV scale factor (um/pixel)")
    fov_scale_factor_unit: str = Field("um/pixel", title="FOV scale factor unit")
    frame_rate: float = Field(..., title="Frame rate (Hz)")
    frame_rate_unit: FrequencyUnit = Field(FrequencyUnit.HZ, title="Frame rate unit")
    targeted_structure: Optional[str] = Field(None, title="Targeted structure")


# Ephys Components
class DomeModule(AindModel):
    """Movable module that is mounted on the ephys dome insertion system"""

    assembly_name: str = Field(..., title="Assembly name")
    arc_angle: Decimal = Field(..., title="Arc Angle", units="degrees")
    module_angle: Decimal = Field(..., title="Module Angle", units="degrees")
    angle_unit: AngleUnit = Field(AngleUnit.DEG, title="Angle unit")
    rotation_angle: Optional[Decimal] = Field(0.0, title="Rotation Angle", units="degrees")
    coordinate_transform: Optional[str] = Field(
        None,
        title="Transform from local manipulator axes to rig",
        description="Path to coordinate transform",
    )
    calibration_date: Optional[datetime] = Field(None, title="Date on which coordinate transform was last calibrated")
    notes: Optional[str] = Field(None, title="Notes")


class ManipulatorModule(DomeModule):
    """A dome module connected to a 3-axis manipulator"""

    primary_targeted_structure: str = Field(..., title="Targeted structure")
    targeted_ccf_coordinates: Optional[List[CcfCoords]] = Field(
        None,
        title="Targeted CCF coordinates",
    )
    manipulator_coordinates: Coordinates3d = Field(
        ...,
        title="Manipulator coordinates",
    )


class EphysProbe(AindModel):
    """Probes in a EphysProbeModule"""

    name: str = Field(..., title="Ephys probe name (must match rig JSON)")
    other_targeted_structures: Optional[List[str]] = None


class EphysModule(ManipulatorModule):
    """Probe recorded in a Stream"""

    ephys_probes: List[EphysProbe] = Field(..., title="Ephys probes used in this module")


class Laser(AindModel):
    """Description of laser settings in a session"""

    device_type: Literal["Laser"] = Field("Laser", const=True, readOnly=True)
    name: str = Field(..., title="Name", description="Must match rig json")
    wavelength: int = Field(..., title="Wavelength (nm)")
    wavelength_unit: SizeUnit = Field(SizeUnit.NM, title="Wavelength unit")
    excitation_power: Optional[Decimal] = Field(None, title="Excitation power (mW)")
    excitation_power_unit: PowerUnit = Field(PowerUnit.MW, title="Excitation power unit")


# Behavior components
class RewardSolution(Enum):
    """Reward solution name"""

    WATER = "Water"
    OTHER = "Other"


class RewardSpout(AindModel):
    """Reward spout session information"""

    side: SpoutSide = Field(..., title="Spout side", description="Must match rig")
    starting_position: RelativePosition = Field(..., title="Starting position")
    variable_position: bool = Field(
        ..., title="Variable position", description="True if spout position changes during session as tracked in data"
    )


class RewardDelivery(AindModel):
    """Description of reward delivery configuration"""

    reward_solution: RewardSolution = Field(..., title="Reward solution", description="If Other use notes")
    reward_spouts: List[RewardSpout] = Field(..., title="Reward spouts", unique_items=True)
    notes: Optional[str] = Field(None, title="Notes")

    @root_validator
    def validate_other(cls, v):
        """Validator for other/notes"""

        if v.get("reward_solution") == RewardSolution.OTHER and not v.get("notes"):
            raise ValueError(
                "Notes cannot be empty if reward_solution is Other. Describe the reward_solution in the notes field."
            )
        return v


class Stream(AindModel):
    """Data streams with a start and stop time"""

    stream_start_time: datetime = Field(..., title="Stream start time")
    stream_end_time: datetime = Field(..., title="Stream stop time")
    stream_modalities: List[Modality] = Field(..., title="Modalities")
    daq_names: Optional[List[str]] = Field(None, title="DAQ devices", unique_items=True)
    camera_names: Optional[List[str]] = Field(None, title="Cameras", unique_items=True)
    light_sources: Optional[
        Annotated[
            List[Union[Laser, LightEmittingDiode]],
            Field(None, title="Light sources", unique_items=True, discriminator="device_type"),
        ]
    ]
    ephys_modules: Optional[List[EphysModule]] = Field(None, title="Ephys modules", unique_items=True)
    manipulator_modules: Optional[List[ManipulatorModule]] = Field(None, title="Manipulator modules", unique_items=True)
    detectors: Optional[List[Detector]] = Field(None, title="Detectors", unique_items=True)
    fiber_photometry_assemblies: Optional[List[FiberPhotometryAssembly]] = Field(None, title="Fiber photometry devices")
    ophys_fovs: Optional[List[FieldOfView]] = Field(None, title="Fields of view", unique_items=True)
    stack_parameters: Optional[Stack] = Field(None, title="Stack parameters")
    stimulus_device_names: Optional[List[str]] = Field(None, title="Stimulus devices")
    notes: Optional[str] = Field(None, title="Notes")


class Session(AindCoreModel):
    """Description of a physiology and/or behavior session"""

    schema_version: str = Field(
        "0.0.1",
        description="schema version",
        title="Schema Version",
        const=True,
    )
    experimenter_full_name: List[str] = Field(
        ...,
        description="First and last name of the experimenter(s).",
        title="Experimenter(s) full name",
    )
    session_start_time: datetime = Field(..., title="Session start time")
    session_end_time: Optional[datetime] = Field(None, title="Session end time")
    session_type: str = Field(..., title="Session type")
    iacuc_protocol: Optional[str] = Field(None, title="IACUC protocol")
    rig_id: str = Field(..., title="Rig ID")
    calibrations: Optional[List[Calibration]] = Field(
        None, title="Calibrations", description="Calibrations of rig devices prior to session"
    )
    maintenance: Optional[List[Maintenance]] = Field(
        None, title="Maintenance", description="Maintenance of rig devices prior to session"
    )
    subject_id: int = Field(..., title="Subject ID")
    animal_weight_prior: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight before procedure",
        units="g",
    )
    animal_weight_post: Optional[Decimal] = Field(
        None,
        title="Animal weight (g)",
        description="Animal weight after procedure",
        units="g",
    )
    weight_unit: MassUnit = Field(MassUnit.G, title="Weight unit")
    data_streams: List[Stream] = Field(
        ...,
        title="Data streams",
        description=(
            "A data stream is a collection of devices that are recorded simultaneously. Each session can include"
            " multiple streams (e.g., if the manipulators are moved to a new location)"
        ),
        unique_items=True,
    )
    stimulus_epochs: Optional[List[StimulusEpoch]] = Field(None, title="Stimulus")
    reward_delivery: Optional[RewardDelivery] = Field(None, title="Reward delivery")
    stick_microscopes: Optional[List[DomeModule]] = Field(
        None,
        title="Stick microscopes",
        description="Must match stick microscope assemblies in rig file",
    )
    notes: Optional[str] = Field(None, title="Notes")
