"""Builder function for BARseq acquisition metadata.

This module generates acquisition.json files for BARseq experiments using the
Dogwood microscope (Nikon Ti2-E with spinning disk confocal).

Device names match the instrument definition in aind-data-schema PR #1685.
"""

from datetime import datetime, timezone
from typing import List, Optional

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import PowerUnit, SizeUnit, TimeUnit

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
        dimensions=Scale(
            scale=[9999, 9999, 10]  # PLACEHOLDER width, height; Known: 10 z-planes
        ),
        image_to_acquisition_transform=[
            Translation(translation=[0, 0, 0]),  # PLACEHOLDER tile position in microns
            Scale(scale=[0.33, 0.33, 1.5])  # Known: pixel size (x,y) and z-step in microns
        ],
    )


def create_barseq_acquisition(
    subject_id: str,
    specimen_id: str,
    num_sections: int,
    ccf_start_plate: int,
    ccf_end_plate: int,
    experimenters: List[str],
    acquisition_date: datetime,
    instrument_id: str = "Dogwood",
    # Timing parameters
    gene_seq_start_time: Optional[datetime] = None,
    gene_seq_end_time: Optional[datetime] = None,
    barcode_seq_start_time: Optional[datetime] = None,
    barcode_seq_end_time: Optional[datetime] = None,
    hyb_start_time: Optional[datetime] = None,
    hyb_end_time: Optional[datetime] = None,
    # Hardware parameters (with placeholders as defaults)
    exposure_time: float = 9999.0,
    exposure_time_unit: TimeUnit = TimeUnit.MS,
    # Additional metadata
    protocol_id: Optional[List[str]] = None,
    notes: Optional[str] = None,
) -> Acquisition:
    """
    Create a BARseq acquisition metadata object.

    BARseq imaging workflow:
    1. Gene Sequencing (7 cycles) - Reads 7-base gene barcodes (109-gene codebook)
    2. Barcode Sequencing (15 cycles) - Reads 30-base Sindbis virus barcodes
    3. Hybridization (1 cycle) - Fluorescent probe visualization for anatomical reference

    Parameters
    ----------
    subject_id : str
        Subject ID (mouse from which specimen was derived)
    specimen_id : str
        Specimen ID for the brain section(s)
    num_sections : int
        Number of 20μm sections imaged
    ccf_start_plate : int
        Starting CCFv3 plate number (anterior-posterior coordinate)
    ccf_end_plate : int
        Ending CCFv3 plate number
    experimenters : List[str]
        Names of experimenters
    acquisition_date : datetime
        Date of acquisition
    instrument_id : str, optional
        Instrument ID (default: "Dogwood")
    gene_seq_start_time : datetime, optional
        Gene sequencing start time
    gene_seq_end_time : datetime, optional
        Gene sequencing end time
    barcode_seq_start_time : datetime, optional
        Barcode sequencing start time
    barcode_seq_end_time : datetime, optional
        Barcode sequencing end time
    hyb_start_time : datetime, optional
        Hybridization start time
    hyb_end_time : datetime, optional
        Hybridization end time
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
        Complete acquisition metadata object
    """

    # Use placeholder times if not provided
    placeholder_dt = datetime(2099, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    gene_seq_start_time = gene_seq_start_time or placeholder_dt
    gene_seq_end_time = gene_seq_end_time or placeholder_dt
    barcode_seq_start_time = barcode_seq_start_time or placeholder_dt
    barcode_seq_end_time = barcode_seq_end_time or placeholder_dt
    hyb_start_time = hyb_start_time or placeholder_dt
    hyb_end_time = hyb_end_time or placeholder_dt

    # Create detector config
    detector = DetectorConfig(
        device_name="Camera-1",
        exposure_time=exposure_time,
        exposure_time_unit=exposure_time_unit,
        trigger_type=TriggerType.INTERNAL,
    )

    # Gene sequencing channels (G, T, A, C, DAPI)
    # Based on instrument notes: geneseq cycles use G/T/A/C/DAPI channels
    gene_channels = _create_gene_sequencing_channels(detector)

    # Barcode sequencing channels (G, T, A, C)
    # Based on instrument notes: bcseq cycles use GTAC channels (no DAPI after first cycle)
    barcode_channels = _create_barcode_sequencing_channels(detector)

    # Hybridization channels (GFP, G, TxRed, Cy5, DAPI, DIC)
    # Based on instrument notes: hyb cycles use GFP/G/TxRed/Cy5/DAPI/DIC channels
    hyb_channels = _create_hybridization_channels(detector)

    # Create ImagingConfigs with placeholder images
    # Note: Once tile layout info is available, each channel should have one ImageSPIM per tile
    gene_imaging_config = ImagingConfig(
        device_name="Ti2-E__0",
        channels=gene_channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=[
            _create_image_placeholder("GeneSeq_G"),
            _create_image_placeholder("GeneSeq_T"),
            _create_image_placeholder("GeneSeq_A"),
            _create_image_placeholder("GeneSeq_C"),
            _create_image_placeholder("GeneSeq_DAPI"),
        ],
    )

    barcode_imaging_config = ImagingConfig(
        device_name="Ti2-E__0",
        channels=barcode_channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=[
            _create_image_placeholder("BarcodeSeq_G"),
            _create_image_placeholder("BarcodeSeq_T"),
            _create_image_placeholder("BarcodeSeq_A"),
            _create_image_placeholder("BarcodeSeq_C"),
        ],
    )

    hyb_imaging_config = ImagingConfig(
        device_name="Ti2-E__0",
        channels=hyb_channels,
        coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
        images=[
            _create_image_placeholder("Hyb_XC2758"),
            _create_image_placeholder("Hyb_XC2759"),
            _create_image_placeholder("Hyb_XC2760"),
            _create_image_placeholder("Hyb_YS221"),
            _create_image_placeholder("Hyb_DAPI"),
        ],
    )

    # DataStream 1: Gene Sequencing
    gene_stream = DataStream(
        stream_start_time=gene_seq_start_time,
        stream_end_time=gene_seq_end_time,
        modalities=[Modality.BARSEQ],
        active_devices=[
            "Ti2-E__0",
            "20x Objective",
            "Camera-1",
            "XLIGHT Spinning Disk",
            "PLACEHOLDER_LASER_G",
            "PLACEHOLDER_LASER_T",
            "PLACEHOLDER_LASER_A",
            "PLACEHOLDER_LASER_C",
            "PLACEHOLDER_LASER_DAPI",
            "PLACEHOLDER_FILTER_G",
            "PLACEHOLDER_FILTER_T",
            "PLACEHOLDER_FILTER_A",
            "PLACEHOLDER_FILTER_C",
            "PLACEHOLDER_FILTER_DAPI",
        ],
        configurations=[gene_imaging_config, detector],
        notes="Gene barcode sequencing (7 cycles) using sequential base incorporation imaging",
    )

    # DataStream 2: Barcode Sequencing
    barcode_stream = DataStream(
        stream_start_time=barcode_seq_start_time,
        stream_end_time=barcode_seq_end_time,
        modalities=[Modality.BARSEQ],
        active_devices=[
            "Ti2-E__0",
            "20x Objective",
            "Camera-1",
            "XLIGHT Spinning Disk",
            "PLACEHOLDER_LASER_G",
            "PLACEHOLDER_LASER_T",
            "PLACEHOLDER_LASER_A",
            "PLACEHOLDER_LASER_C",
            "PLACEHOLDER_FILTER_G",
            "PLACEHOLDER_FILTER_T",
            "PLACEHOLDER_FILTER_A",
            "PLACEHOLDER_FILTER_C",
        ],
        configurations=[barcode_imaging_config, detector],
        notes="Viral barcode sequencing (15 cycles) for neural projection tracing",
    )

    # DataStream 3: Hybridization
    hyb_stream = DataStream(
        stream_start_time=hyb_start_time,
        stream_end_time=hyb_end_time,
        modalities=[Modality.BARSEQ],
        active_devices=[
            "Ti2-E__0",
            "20x Objective",
            "Camera-1",
            "XLIGHT Spinning Disk",
            "PLACEHOLDER_LASER_HYB_1",
            "PLACEHOLDER_LASER_HYB_2",
            "PLACEHOLDER_LASER_HYB_3",
            "PLACEHOLDER_LASER_HYB_4",
            "PLACEHOLDER_LASER_DAPI",
            "PLACEHOLDER_FILTER_HYB_1",
            "PLACEHOLDER_FILTER_HYB_2",
            "PLACEHOLDER_FILTER_HYB_3",
            "PLACEHOLDER_FILTER_HYB_4",
            "PLACEHOLDER_FILTER_DAPI",
        ],
        configurations=[hyb_imaging_config, detector],
        notes="Fluorescent in situ hybridization with 4 probes (XC2758, XC2759, XC2760, YS221) for anatomical reference",
    )

    # Build acquisition notes
    acq_notes = (
        "BARseq in situ sequencing for neural projection mapping from Locus Coeruleus. "
        "Three sequential data streams: gene sequencing (7 cycles), viral barcode sequencing (15 cycles), "
        "and fluorescent in situ hybridization."
    )
    if notes:
        acq_notes += f" {notes}"

    # Create acquisition
    acquisition = Acquisition(
        subject_id=subject_id,
        specimen_id=specimen_id,
        experimenters=experimenters,
        instrument_id=instrument_id,
        acquisition_start_time=min(gene_seq_start_time, barcode_seq_start_time, hyb_start_time),
        acquisition_end_time=max(gene_seq_end_time, barcode_seq_end_time, hyb_end_time),
        acquisition_type="BarcodeSequencing",
        protocol_id=protocol_id or ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"],
        coordinate_system=None,  # CCFv3 not in predefined enum, noted in acquisition notes
        data_streams=[gene_stream, barcode_stream, hyb_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_gene_sequencing_channels(detector: DetectorConfig) -> List[Channel]:
    """Create channels for gene sequencing (G, T, A, C, DAPI)."""
    channels = []

    # Base names and descriptions
    base_info = [
        ("G", "guanine"),
        ("T", "thymine"),
        ("A", "adenine"),
        ("C", "cytosine"),
    ]

    # Bases G, T, A, C
    for base_code, base_name in base_info:
        channels.append(
            Channel(
                channel_name=f"GeneSeq_{base_code}",
                intended_measurement=f"Fluorescent signal from sequencing reaction indicating {base_name} incorporation",
                light_sources=[
                    LaserConfig(
                        device_name=f"PLACEHOLDER_LASER_{base_code}",
                        wavelength=9999,
                        wavelength_unit=SizeUnit.NM,
                        power=9999.0,
                        power_unit=PowerUnit.MW,
                    ),
                ],
                emission_filters=[
                    DeviceConfig(device_name=f"PLACEHOLDER_FILTER_{base_code}"),
                ],
                detector=detector,
                emission_wavelength=9999,
                emission_wavelength_unit=SizeUnit.NM,
            )
        )

    # DAPI channel
    channels.append(
        Channel(
            channel_name="GeneSeq_DAPI",
            intended_measurement="Nuclear DNA staining for anatomical reference (DAPI counterstain)",
            light_sources=[
                LaserConfig(
                    device_name="PLACEHOLDER_LASER_DAPI",
                    wavelength=9999,
                    wavelength_unit=SizeUnit.NM,
                    power=9999.0,
                    power_unit=PowerUnit.MW,
                ),
            ],
            emission_filters=[
                DeviceConfig(device_name="PLACEHOLDER_FILTER_DAPI"),
            ],
            detector=detector,
            emission_wavelength=9999,
            emission_wavelength_unit=SizeUnit.NM,
        )
    )

    return channels


def _create_barcode_sequencing_channels(detector: DetectorConfig) -> List[Channel]:
    """Create channels for barcode sequencing (G, T, A, C)."""
    channels = []

    # Base names and descriptions
    base_info = [
        ("G", "guanine"),
        ("T", "thymine"),
        ("A", "adenine"),
        ("C", "cytosine"),
    ]

    for base_code, base_name in base_info:
        channels.append(
            Channel(
                channel_name=f"BarcodeSeq_{base_code}",
                intended_measurement=f"Fluorescent signal from sequencing reaction indicating {base_name} incorporation",
                light_sources=[
                    LaserConfig(
                        device_name=f"PLACEHOLDER_LASER_{base_code}",
                        wavelength=9999,
                        wavelength_unit=SizeUnit.NM,
                        power=9999.0,
                        power_unit=PowerUnit.MW,
                    ),
                ],
                emission_filters=[
                    DeviceConfig(device_name=f"PLACEHOLDER_FILTER_{base_code}"),
                ],
                detector=detector,
                emission_wavelength=9999,
                emission_wavelength_unit=SizeUnit.NM,
            )
        )

    return channels


def _create_hybridization_channels(detector: DetectorConfig) -> List[Channel]:
    """Create channels for hybridization (4 probes + DAPI)."""
    channels = []

    # Hybridization probes with actual probe IDs from methods
    probe_info = [
        ("Hyb_XC2758", "Fluorescent in situ hybridization signal - probe XC2758", "HYB_1"),
        ("Hyb_XC2759", "Fluorescent in situ hybridization signal - probe XC2759", "HYB_2"),
        ("Hyb_XC2760", "Fluorescent in situ hybridization signal - probe XC2760", "HYB_3"),
        ("Hyb_YS221", "Fluorescent in situ hybridization signal - probe YS221", "HYB_4"),
    ]

    for channel_name, measurement, laser_suffix in probe_info:
        channels.append(
            Channel(
                channel_name=channel_name,
                intended_measurement=measurement,
                light_sources=[
                    LaserConfig(
                        device_name=f"PLACEHOLDER_LASER_{laser_suffix}",
                        wavelength=9999,
                        wavelength_unit=SizeUnit.NM,
                        power=9999.0,
                        power_unit=PowerUnit.MW,
                    ),
                ],
                emission_filters=[
                    DeviceConfig(device_name=f"PLACEHOLDER_FILTER_{laser_suffix}"),
                ],
                detector=detector,
                emission_wavelength=9999,
                emission_wavelength_unit=SizeUnit.NM,
            )
        )

    # DAPI channel
    channels.append(
        Channel(
            channel_name="Hyb_DAPI",
            intended_measurement="Nuclear DNA staining for cell identification (DAPI counterstain)",
            light_sources=[
                LaserConfig(
                    device_name="PLACEHOLDER_LASER_DAPI",
                    wavelength=9999,
                    wavelength_unit=SizeUnit.NM,
                    power=9999.0,
                    power_unit=PowerUnit.MW,
                ),
            ],
            emission_filters=[
                DeviceConfig(device_name="PLACEHOLDER_FILTER_DAPI"),
            ],
            detector=detector,
            emission_wavelength=9999,
            emission_wavelength_unit=SizeUnit.NM,
        )
    )

    # Note: DIC is transmitted light and wouldn't be in fluorescence channel list

    return channels
