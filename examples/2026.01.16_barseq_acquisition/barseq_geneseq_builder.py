"""Builder for BARseq Gene Sequencing acquisition metadata."""

from datetime import datetime, timezone
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

# Gene sequencing channel configuration (from MMConfig presets)
GENE_CHANNEL_CONFIG = {
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
    "DAPI": {
        "laser_wavelength_nm": 365,
        "filter_name": "DAPI/GFP/TxRed-69401",
        "exposure_ms": 30.0,
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
    """
    Create placeholder ImageSPIM for a single channel.

    Represents tiled imaging data for one channel. Once tile layout information
    is available from the BARseq team, this should be replaced with individual
    ImageSPIM objects for each tile with proper positions.

    Parameters
    ----------
    channel_name : str
        Name of the channel this image corresponds to

    Returns
    -------
    ImageSPIM
        Placeholder image object with known parameters filled in
    """
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


def create_geneseq_acquisition(
    subject_id: str,
    specimen_id: str,
    num_sections: int,
    ccf_start_plate: int,
    ccf_end_plate: int,
    experimenters: List[str],
    acquisition_start_time: datetime,
    acquisition_end_time: datetime,
    instrument_id: str = "Dogwood",
    exposure_time: float = 40.0,  # Average from channel configs (20-60ms range)
    exposure_time_unit: TimeUnit = TimeUnit.MS,
    protocol_id: Optional[List[str]] = None,
    notes: Optional[str] = None,
) -> Acquisition:
    """
    Create a BARseq Gene Sequencing acquisition metadata object.

    Gene sequencing (7 cycles) reads 7-base gene barcodes from a 109-gene codebook.

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
        Start time of gene sequencing acquisition
    acquisition_end_time : datetime
        End time of gene sequencing acquisition
    instrument_id : str, optional
        Instrument ID (default: "Dogwood")
    exposure_time : float, optional
        Camera exposure time (default: 9999.0 as placeholder)
    exposure_time_unit : TimeUnit, optional
        Unit for exposure time (default: milliseconds)
    protocol_id : List[str], optional
        Protocol DOI(s)
    notes : str, optional
        Additional notes

    Returns
    -------
    Acquisition
        Gene sequencing acquisition metadata object
    """
    # Create detector configuration
    detector = DetectorConfig(
        device_name="Camera-1",
        exposure_time=exposure_time,
        exposure_time_unit=exposure_time_unit,
        trigger_type=TriggerType.INTERNAL,
    )

    # Create gene sequencing channels
    channels = _create_gene_sequencing_channels(detector)

    # Create ImagingConfig with placeholder images
    imaging_config = ImagingConfig(
        device_name=instrument_id,
        channels=channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=[
            _create_image_placeholder("GeneSeq_G"),
            _create_image_placeholder("GeneSeq_T"),
            _create_image_placeholder("GeneSeq_A"),
            _create_image_placeholder("GeneSeq_C"),
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
        configurations=[imaging_config, detector],
        notes="Gene barcode sequencing (7 cycles) using sequential base incorporation imaging",
    )

    # Build acquisition notes
    acq_notes = (
        f"BARseq gene sequencing for neural projection mapping from Locus Coeruleus. "
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
        acquisition_type="BarcodeSequencing",
        protocol_id=protocol_id or ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"],
        coordinate_system=None,  # CCFv3 noted in acquisition notes
        data_streams=[data_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_gene_sequencing_channels(detector: DetectorConfig) -> List[Channel]:
    """Create channels for gene sequencing (G, T, A, C, DAPI)."""
    channels = []

    # Base names and descriptions
    base_info = [
        ("G", "Guanine"),
        ("T", "Thymine"),
        ("A", "Adenine"),
        ("C", "Cytosine"),
    ]

    # Bases G, T, A, C
    for base_code, base_name in base_info:
        config = GENE_CHANNEL_CONFIG[base_code]
        channels.append(
            Channel(
                channel_name=f"GeneSeq_{base_code}",
                intended_measurement=base_name,
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

    # DAPI channel
    dapi_config = GENE_CHANNEL_CONFIG["DAPI"]
    channels.append(
        Channel(
            channel_name="DAPI",
            intended_measurement="Nuclear counterstain",
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
            detector=detector,
        )
    )

    return channels
