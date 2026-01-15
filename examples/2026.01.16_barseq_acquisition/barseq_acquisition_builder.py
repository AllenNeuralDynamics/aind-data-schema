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
    LaserConfig,
    TriggerType,
)
from aind_data_schema.core.acquisition import Acquisition, DataStream


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
    ethics_review_id: Optional[List[str]] = None,
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
    ethics_review_id : List[str], optional
        IACUC protocol number(s)
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

    # Create ImagingConfigs
    gene_imaging_config = ImagingConfig(
        device_name="Ti2-E__0",
        channels=gene_channels,
        images=[],
    )

    barcode_imaging_config = ImagingConfig(
        device_name="Ti2-E__0",
        channels=barcode_channels,
        images=[],
    )

    hyb_imaging_config = ImagingConfig(
        device_name="Ti2-E__0",
        channels=hyb_channels,
        images=[],
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
        notes=(
            f"Gene sequencing: 7 sequential cycles reading 7-base gene barcodes from "
            f"109-gene codebook. Each cycle images 4 DNA bases (G/T/A/C) plus DAPI. "
            f"Imaging: Z-stack of 10 images, 1.5μm step, 24% tile overlap, 0.33μm pixel size. "
            f"Sequencing: Illumina MiSeq Reagent Nano Kit v2, primer YS220."
        ),
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
        notes=(
            f"Barcode sequencing: 15 sequential cycles reading 30-base Sindbis virus barcodes "
            f"from HZ120 library (~8M diversity). Each cycle images 4 DNA bases (G/T/A/C). "
            f"Used for neural projection tracing. Sequencing primer: XCAI5."
        ),
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
        notes=(
            f"Hybridization: Single cycle with fluorescent probes (XC2758, XC2759, XC2760, YS221) "
            f"plus DAPI and DIC for anatomical reference and cell identification."
        ),
    )

    # Build acquisition notes
    acq_notes = (
        f"BARseq acquisition of Locus Coeruleus for noradrenergic neuron projection mapping. "
        f"Specimen: {num_sections} coronal sections (20μm) spanning CCF plates {ccf_start_plate}-{ccf_end_plate}. "
        f"Subject {subject_id} received Sindbis HZ120 virus injection 22-28h pre-harvest. "
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
        protocol_id=protocol_id
        or [
            "dx.doi.org/10.17504/protocols.io.n2bvj82q5gk5/v1",
            "dx.doi.org/10.17504/protocols.io.81wgbp4j3vpk/v2",
        ],
        ethics_review_id=ethics_review_id,
        coordinate_system=None,  # CCFv3 not in predefined enum, noted in acquisition notes
        data_streams=[gene_stream, barcode_stream, hyb_stream],
        notes=acq_notes,
    )

    return acquisition


def _create_gene_sequencing_channels(detector: DetectorConfig) -> List[Channel]:
    """Create channels for gene sequencing (G, T, A, C, DAPI)."""
    channels = []

    # Bases G, T, A, C
    for base in ["G", "T", "A", "C"]:
        channels.append(
            Channel(
                channel_name=f"Gene_{base}",
                intended_measurement=f"Gene sequencing - DNA base {base}",
                light_sources=[
                    LaserConfig(
                        device_name=f"PLACEHOLDER_LASER_{base}",
                        wavelength=9999,
                        wavelength_unit=SizeUnit.NM,
                        power=9999.0,
                        power_unit=PowerUnit.MW,
                    ),
                ],
                emission_filters=[
                    DeviceConfig(device_name=f"PLACEHOLDER_FILTER_{base}"),
                ],
                detector=detector,
                emission_wavelength=9999,
                emission_wavelength_unit=SizeUnit.NM,
            )
        )

    # DAPI channel
    channels.append(
        Channel(
            channel_name="Gene_DAPI",
            intended_measurement="DAPI nuclear counterstain",
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

    for base in ["G", "T", "A", "C"]:
        channels.append(
            Channel(
                channel_name=f"Barcode_{base}",
                intended_measurement=f"Barcode sequencing - DNA base {base}",
                light_sources=[
                    LaserConfig(
                        device_name=f"PLACEHOLDER_LASER_{base}",
                        wavelength=9999,
                        wavelength_unit=SizeUnit.NM,
                        power=9999.0,
                        power_unit=PowerUnit.MW,
                    ),
                ],
                emission_filters=[
                    DeviceConfig(device_name=f"PLACEHOLDER_FILTER_{base}"),
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

    # Hybridization probes - based on instrument notes mentioning GFP/G/TxRed/Cy5
    probe_info = [
        ("Hyb_Probe1_GFP", "Hybridization probe (likely GFP-like)", "HYB_1"),
        ("Hyb_Probe2", "Hybridization probe", "HYB_2"),
        ("Hyb_Probe3_TxRed", "Hybridization probe (likely Texas Red-like)", "HYB_3"),
        ("Hyb_Probe4_Cy5", "Hybridization probe (likely Cy5-like)", "HYB_4"),
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
            intended_measurement="DAPI nuclear counterstain",
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
