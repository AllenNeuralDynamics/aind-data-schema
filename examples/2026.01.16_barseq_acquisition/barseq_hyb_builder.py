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

# Tiling configuration (from Aixin's email + Dan's estimate)
TILE_OVERLAP_PERCENT = 0.23  # 23% overlap between tiles
TILE_STEP_PX = int(TILE_WIDTH_PX * (1 - TILE_OVERLAP_PERCENT))  # 2464 pixels
TILES_X = 14  # Estimated grid size
TILES_Y = 8
FIRST_TILE_OFFSET_PX = -736  # Starting position in pixels

# DAPI channel configuration (from Aixin's email + MMConfig presets)
# Note: Other fluorophore configs (GFP, YFP, TxRed, Cy5) will be needed once
# probe-to-fluorophore mapping is determined
DAPI_CONFIG = {
    "laser_wavelength_nm": 365,
    "filter_name": "DAPI/GFP/TxRed-69401",
    "exposure_ms": 20.0,  # Updated from 30 per Aixin
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


def _create_images_for_channel(channel_name: str) -> list[ImageSPIM]:
    """
    Create ImageSPIM objects for a channel: tiles + max projection.

    The acquisition uses a 14×8 grid of tiles with 23% overlap. Individual tiles
    are transient and deleted after stitching, but we document them in the acquisition
    metadata. The final stitched max projection is saved.

    Parameters
    ----------
    channel_name : str
        Name of the channel this image corresponds to

    Returns
    -------
    list[ImageSPIM]
        List of image objects: 112 tiles + 1 max projection
    """
    images = []
    
    # Create 112 tile ImageSPIM objects (14×8 grid)
    for y_idx in range(TILES_Y):
        for x_idx in range(TILES_X):
            # Calculate tile position in pixels
            x_pos_px = FIRST_TILE_OFFSET_PX + x_idx * TILE_STEP_PX
            y_pos_px = FIRST_TILE_OFFSET_PX + y_idx * TILE_STEP_PX
            
            # Convert to microns
            x_pos_um = x_pos_px * PIXEL_SIZE_UM
            y_pos_um = y_pos_px * PIXEL_SIZE_UM
            
            tile = ImageSPIM(
                channel_name=channel_name,
                file_name="not saved",  # Tiles are transient
                dimensions_unit=SizeUnit.PX,
                dimensions=Scale(scale=[TILE_WIDTH_PX, TILE_HEIGHT_PX, Z_PLANES_PER_TILE]),
                image_to_acquisition_transform=[
                    Translation(translation=[x_pos_um, y_pos_um, 0]),
                    Scale(scale=[PIXEL_SIZE_UM, PIXEL_SIZE_UM, Z_STEP_UM]),
                ],
            )
            images.append(tile)
    
    # Create max projection ImageSPIM (stitched result that is saved)
    total_width_px = abs(FIRST_TILE_OFFSET_PX) + (TILES_X - 1) * TILE_STEP_PX + TILE_WIDTH_PX
    total_height_px = abs(FIRST_TILE_OFFSET_PX) + (TILES_Y - 1) * TILE_STEP_PX + TILE_HEIGHT_PX
    
    max_proj = ImageSPIM(
        channel_name=channel_name,
        file_name="PLACEHOLDER_max_projection_path",
        dimensions_unit=SizeUnit.PX,
        dimensions=Scale(scale=[total_width_px, total_height_px, Z_PLANES_PER_TILE]),
        image_to_acquisition_transform=[
            Translation(translation=[0, 0, 0]),
            Scale(scale=[PIXEL_SIZE_UM, PIXEL_SIZE_UM, Z_STEP_UM]),
        ],
    )
    images.append(max_proj)
    
    return images


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
        Number of 20um sections imaged
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

    # Create ImagingConfig with tiles + max projections for each channel
    all_images = []
    for channel_name in ["Hyb_XC2758", "Hyb_XC2759", "Hyb_XC2760", "Hyb_YS221", "DAPI"]:
        all_images.extend(_create_images_for_channel(channel_name))
    
    imaging_config = ImagingConfig(
        device_name=instrument_id,
        channels=channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=all_images,
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

    # Build acquisition notes - single succinct sentence
    acq_notes = "BARseq hybridization for anatomical reference and cell identification."
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
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        data_streams=[data_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_hybridization_channels() -> List[Channel]:
    """Create channels for hybridization (4 probes + DAPI)."""
    channels = []

    # Hybridization probes - fluorophore mapping unknown, using placeholders
    # Available: GFP (488nm), YFP (514nm), TxRed (561nm), Cy5 (640nm)
    probe_measurements = {
        "Hyb_XC2758": "Probe XC2758",
        "Hyb_XC2759": "Probe XC2759",
        "Hyb_XC2760": "Probe XC2760",
        "Hyb_YS221": "Probe YS221",
    }

    for channel_name, measurement in probe_measurements.items():
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
                intended_measurement=measurement,
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
            intended_measurement="DAPI counterstain",
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
