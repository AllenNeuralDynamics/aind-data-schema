"""Builder for BARseq Barcode Sequencing acquisition metadata."""

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

# Barcode sequencing channel configuration (from MMConfig presets)
# Uses same bases as gene sequencing (G, T, A, C)
BARCODE_CHANNEL_CONFIG = {
    "G": {
        "laser_wavelength_nm": 514,
        "filter_name": "565/24",
        "exposure_ms": 60.0,
    },
    "T": {
        "laser_wavelength_nm": 561,
        "filter_name": "441/511/593/684/817",
        "exposure_ms": 30.0,
    },
    "A": {
        "laser_wavelength_nm": 640,
        "filter_name": "676/29",
        "exposure_ms": 20.0,
    },
    "C": {
        "laser_wavelength_nm": 640,
        "filter_name": "775/140",
        "exposure_ms": 40.0,
    },
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


def create_barcodeseq_acquisition(
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
    Create a BARseq Barcode Sequencing acquisition metadata object.

    Barcode sequencing (15 cycles) reads 30-base Sindbis virus barcodes
    for neural projection tracing.

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
        Start time of barcode sequencing acquisition
    acquisition_end_time : datetime
        End time of barcode sequencing acquisition
    instrument_id : str, optional
        Instrument ID (default: "Dogwood")
    protocol_id : List[str], optional
        Protocol DOI(s)
    notes : str, optional
        Additional notes

    Returns
    -------
    Acquisition
        Barcode sequencing acquisition metadata object
    """
    # Create barcode sequencing channels (each with its own detector config)
    channels = _create_barcode_sequencing_channels()

    # Create ImagingConfig with placeholder images
    imaging_config = ImagingConfig(
        device_name=instrument_id,
        channels=channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=[
            _create_image_placeholder("BarcodeSeq_G"),
            _create_image_placeholder("BarcodeSeq_T"),
            _create_image_placeholder("BarcodeSeq_A"),
            _create_image_placeholder("BarcodeSeq_C"),
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
        notes="Viral barcode sequencing (15 cycles) for neural projection tracing",
    )

    # Build acquisition notes - single succinct sentence
    acq_notes = "BARseq viral barcode sequencing for neural projection mapping from Locus Coeruleus."
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
        acquisition_type="BarcodeSequencing",
        protocol_id=protocol_id or ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"],
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        data_streams=[data_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_barcode_sequencing_channels() -> List[Channel]:
    """Create channels for barcode sequencing (G, T, A, C)."""
    channels = []

    # Each channel gets its own detector config with the correct exposure time
    base_names = {"G": "Guanine", "T": "Thymine", "A": "Adenine", "C": "Cytosine"}

    for base_code in ["G", "T", "A", "C"]:
        config = BARCODE_CHANNEL_CONFIG[base_code]
        detector = DetectorConfig(
            device_name="Camera-1",
            exposure_time=config["exposure_ms"],
            exposure_time_unit=TimeUnit.MS,
            trigger_type=TriggerType.INTERNAL,
        )
        channels.append(
            Channel(
                channel_name=f"BarcodeSeq_{base_code}",
                intended_measurement=base_names[base_code],
                light_sources=[
                    LaserConfig(
                        device_name=f"Lumencor Celesta {config['laser_wavelength_nm']}nm",
                        wavelength=config["laser_wavelength_nm"],
                        wavelength_unit=SizeUnit.NM,
                    ),
                ],
                emission_filters=[
                    DeviceConfig(device_name=config["filter_name"]),
                ],
                detector=detector,
            )
        )

    return channels
