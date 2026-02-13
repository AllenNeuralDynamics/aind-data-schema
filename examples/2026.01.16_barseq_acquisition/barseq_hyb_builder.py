"""Builder for BARseq Hybridization acquisition metadata."""

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

from constants import (
    HYB_DAPI_CONFIG,
    HYB_FLUOROPHORE_CONFIG,
    HYB_PROBE_MEASUREMENTS,
    HYB_PROBE_TO_FLUOROPHORE,
)
from utils import create_max_projection_image, create_tiling_description


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
    # Create hybridization channels
    channels = _create_hybridization_channels()

    # Create ImageSPIM objects only for saved max projections (1 per channel)
    images = []
    for channel_name in ["Hyb_XC2758", "Hyb_XC2759", "Hyb_XC2760", "Hyb_YS221", "DAPI"]:
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
        f"Fluorescent in situ hybridization with 4 probes (XC2758, XC2759, XC2760, YS221) for anatomical reference. "
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
        f"BARseq hybridization for anatomical reference and cell identification. "
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
        acquisition_type="BarcodeSequencing",  # All three phases use same type per SUMMARY.md
        protocol_id=protocol_id or ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"],
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        data_streams=[data_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_hybridization_channels() -> List[Channel]:
    """Create channels for hybridization (4 probes + DAPI)."""
    channels = []

    # Hybridization probes - uses assumed probe-to-fluorophore mapping
    for channel_name, measurement in HYB_PROBE_MEASUREMENTS.items():
        # Look up which fluorophore this probe uses (based on assumption)
        fluorophore = HYB_PROBE_TO_FLUOROPHORE[channel_name]
        # Get the config for that fluorophore
        fluor_config = HYB_FLUOROPHORE_CONFIG[fluorophore]

        detector = DetectorConfig(
            device_name="Camera-1",
            exposure_time=fluor_config["exposure_ms"],
            exposure_time_unit=TimeUnit.MS,
            trigger_type=TriggerType.INTERNAL,
        )
        channels.append(
            Channel(
                channel_name=channel_name,
                intended_measurement=measurement,
                light_sources=[
                    LaserConfig(
                        device_name=f"Lumencor Celesta {fluor_config['wavelength_nm']}nm",
                        wavelength=fluor_config["wavelength_nm"],
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
    dapi_detector = DetectorConfig(
        device_name="Camera-1",
        exposure_time=HYB_DAPI_CONFIG["exposure_ms"],
        exposure_time_unit=TimeUnit.MS,
        trigger_type=TriggerType.INTERNAL,
    )
    channels.append(
        Channel(
            channel_name="DAPI",
            intended_measurement="DAPI counterstain",
            light_sources=[
                LaserConfig(
                    device_name=f"Lumencor Celesta {HYB_DAPI_CONFIG['laser_wavelength_nm']}nm",
                    wavelength=HYB_DAPI_CONFIG["laser_wavelength_nm"],
                    wavelength_unit=SizeUnit.NM,
                ),
            ],
            emission_filters=[
                DeviceConfig(device_name=HYB_DAPI_CONFIG["filter_name"]),
            ],
            detector=dapi_detector,
        )
    )

    return channels
