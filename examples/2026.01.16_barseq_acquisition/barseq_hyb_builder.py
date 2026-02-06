"""Builder for BARseq Hybridization acquisition metadata."""

from datetime import datetime
from typing import List, Optional

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import SizeUnit, TimeUnit

# Hardware configuration from MMConfig_Ti2E-xc2.1.txt and dogwood.json
# Tile dimensions (pixels)
TILE_WIDTH_PX = 3200
TILE_HEIGHT_PX = 3200
Z_PLANES_PER_TILE = 10

# Pixel size and z-step (micrometers)
PIXEL_SIZE_UM = 0.33
Z_STEP_UM = 1.5

# DAPI channel configuration (from MMConfig presets)
# Note: Other fluorophore configs (GFP, YFP, TxRed, Cy5) will be needed once
# probe-to-fluorophore mapping is determined
DAPI_CONFIG = {
    "laser_wavelength_nm": 365,
    "filter_name": "DAPI/GFP/TxRed-69401",
    "exposure_ms": 30.0,
}

from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    DeviceConfig,
    ImagingConfig,
    ImageSPIM,
    LaserConfig,
    TriggerType,
)
from aind_data_schema.components.coordinates import (
    CoordinateSystemLibrary,
    Scale,
    Translation,
)
from aind_data_schema.core.acquisition import Acquisition, DataStream


def _create_image_placeholder(channel_name: str) -> ImageSPIM:
    """Create placeholder ImageSPIM for a single channel."""
    return ImageSPIM(
        channel_name=channel_name,
        file_name="PLACEHOLDER_raw_data_path",
        dimensions_unit=SizeUnit.PX,
        dimensions=Scale(scale=[TILE_WIDTH_PX, TILE_HEIGHT_PX, Z_PLANES_PER_TILE]),
        image_to_acquisition_transform=[
            Translation(translation=[0, 0, 0]),  # PLACEHOLDER tile position in microns
            Scale(scale=[PIXEL_SIZE_UM, PIXEL_SIZE_UM, Z_STEP_UM]),
        ],
    )


def create_hyb_acquisition(
    subject_id: str,
    specimen_id: str,
    num_sections: int,
    ccf_start_plate: int,
    ccf_end_plate: int,
    experimenters: List[str],
    acquisition_start_time: datetime,
    acquisition_end_time: datetime,
    instrument_id: str = "Dogwood",
    protocol_id: Optional[List[str]] = None,
    notes: Optional[str] = None,
) -> Acquisition:
    """
    Create a BARseq Hybridization acquisition metadata object.

    Hybridization (1 cycle) uses fluorescent probes for anatomical reference
    and cell identification.

    Parameters
    ----------
    subject_id : str
        Subject ID (mouse from which specimen was derived)
    specimen_id : str
        Specimen ID for the brain section(s)
    num_sections : int
        Number of 20μm sections imaged
    ccf_start_plate : int
        Starting CCFv3 plate number
    ccf_end_plate : int
        Ending CCFv3 plate number
    experimenters : List[str]
        Names of experimenters
    acquisition_start_time : datetime
        Start time of hybridization acquisition
    acquisition_end_time : datetime
        End time of hybridization acquisition
    instrument_id : str, optional
        Instrument ID (default: "Dogwood")
    protocol_id : List[str], optional
        Protocol DOI(s)
    notes : str, optional
        Additional notes

    Returns
    -------
    Acquisition
        Hybridization acquisition metadata object
    """
    # Create hybridization channels (each with its own detector config)
    channels = _create_hybridization_channels()

    # Create ImagingConfig with placeholder images
    imaging_config = ImagingConfig(
        device_name=instrument_id,
        channels=channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=[
            _create_image_placeholder("Hyb_XC2758"),
            _create_image_placeholder("Hyb_XC2759"),
            _create_image_placeholder("Hyb_XC2760"),
            _create_image_placeholder("Hyb_YS221"),
            _create_image_placeholder("DAPI"),
        ],
    )

    # Create DataStream
    data_stream = DataStream(
        stream_start_time=acquisition_start_time,
        stream_end_time=acquisition_end_time,
        modalities=[Modality.BARSEQ],
        active_devices=[
            "Ti2-E__0",
            "20x Objective",
            "Camera-1",
            "XLIGHT Spinning Disk",
        ],
        configurations=[imaging_config],
        notes="Fluorescent in situ hybridization with 4 probes (XC2758, XC2759, XC2760, YS221) for anatomical reference",
    )

    # Build acquisition notes
    acq_notes = (
        f"BARseq hybridization for anatomical reference and cell identification. "
        f"Imaged {num_sections} × 20μm coronal sections (CCFv3 plates {ccf_start_plate}-{ccf_end_plate})."
    )
    if notes:
        acq_notes += f" {notes}"

    # Create acquisition
    acquisition = Acquisition(
        subject_id=subject_id,
        specimen_id=specimen_id,
        experimenters=experimenters,
        instrument_id=instrument_id,
        acquisition_start_time=acquisition_start_time,
        acquisition_end_time=acquisition_end_time,
        acquisition_type="FluorescentInSituHybridization",
        protocol_id=protocol_id or ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"],
        coordinate_system=None,
        data_streams=[data_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_hybridization_channels() -> List[Channel]:
    """Create channels for hybridization (4 probes + DAPI)."""
    channels = []

    # Hybridization probes - fluorophore mapping unknown, using placeholders
    # Available: GFP (488nm), YFP (514nm), TxRed (561nm), Cy5 (640nm)
    probe_names = ["Hyb_XC2758", "Hyb_XC2759", "Hyb_XC2760", "Hyb_YS221"]

    for channel_name in probe_names:
        # Using placeholders until probe-to-fluorophore mapping is known
        # Placeholder exposure time - will be updated when mapping is known
        detector = DetectorConfig(
            device_name="Camera-1",
            exposure_time=9999.0,  # PLACEHOLDER - actual exposure depends on fluorophore
            exposure_time_unit=TimeUnit.MS,
            trigger_type=TriggerType.INTERNAL,
        )
        channels.append(
            Channel(
                channel_name=channel_name,
                light_sources=[
                    LaserConfig(
                        device_name="PLACEHOLDER_LASER_HYB",
                        wavelength=9999,  # Could be 488, 514, 561, or 640nm
                        wavelength_unit=SizeUnit.NM,
                    ),
                ],
                emission_filters=[
                    DeviceConfig(device_name="PLACEHOLDER_FILTER_HYB"),
                ],
                detector=detector,
            )
        )

    # DAPI channel - configuration is known
    dapi_config = DAPI_CONFIG
    dapi_detector = DetectorConfig(
        device_name="Camera-1",
        exposure_time=dapi_config["exposure_ms"],
        exposure_time_unit=TimeUnit.MS,
        trigger_type=TriggerType.INTERNAL,
    )
    channels.append(
        Channel(
            channel_name="DAPI",
            light_sources=[
                LaserConfig(
                    device_name=f"Lumencor Celesta {dapi_config['laser_wavelength_nm']}nm",
                    wavelength=dapi_config["laser_wavelength_nm"],
                    wavelength_unit=SizeUnit.NM,
                ),
            ],
            emission_filters=[
                DeviceConfig(device_name=dapi_config["filter_name"]),
            ],
            detector=dapi_detector,
        )
    )

    return channels
