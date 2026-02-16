"""Builder for BARseq Barcode Sequencing acquisition metadata."""

from datetime import datetime
from typing import List, Optional

from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    DeviceConfig,
    ImagingConfig,
    LaserConfig,
    TriggerType,
)
from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.core.acquisition import Acquisition, DataStream
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import SizeUnit, TimeUnit

from constants import BARCODESEQ_CHANNEL_CONFIG
from utils import create_max_projection_image, create_tiling_description


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
    # Create barcode sequencing channels
    channels = _create_barcode_sequencing_channels()

    # Create ImageSPIM objects only for saved max projections (1 per channel)
    images = []
    for channel_name in ["BarcodeSeq_G", "BarcodeSeq_T", "BarcodeSeq_A", "BarcodeSeq_C"]:
        images.append(create_max_projection_image(channel_name))

    imaging_config = ImagingConfig(
        device_name=instrument_id,
        channels=channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=images,
    )

    # Generate tiling description for notes
    tiling_description = create_tiling_description()

    # Create DataStream with tiling details in notes
    stream_notes = (
        f"Viral barcode sequencing (15 cycles) for neural projection tracing. "
        f"{tiling_description}"
    )

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
        notes=stream_notes,
    )

    # Build acquisition notes
    acq_notes = (
        f"BARseq viral barcode sequencing for neural projection mapping from Locus Coeruleus. "
        f"Imaged {num_sections} sections (20μm coronal) covering CCF plates {ccf_start_plate}-{ccf_end_plate}."
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
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        data_streams=[data_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_barcode_sequencing_channels() -> List[Channel]:
    """Create channels for barcode sequencing (G, T, A, C)."""
    channels = []

    base_names = {"G": "Guanine", "T": "Thymine", "A": "Adenine", "C": "Cytosine"}

    for base_code in ["G", "T", "A", "C"]:
        config = BARCODESEQ_CHANNEL_CONFIG[base_code]
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
