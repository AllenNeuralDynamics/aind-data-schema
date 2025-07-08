"""example MRIAcquisition and MRIScan"""

from decimal import Decimal

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.coordinates import Affine, Scale, Translation, CoordinateSystemLibrary
from aind_data_schema.components.devices import Scanner
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    AcquisitionSubjectDetails,
)
from aind_data_schema.components.configs import MRIScan, MriScanSequence, ScanType, SubjectPosition

from aind_data_schema_models.units import TimeUnit, SizeUnit


mri_scanner = Scanner(
    name="Scanner 72",
    magnetic_strength=7,
    magnetic_strength_unit="tesla",
)

scan1 = MRIScan(
    scan_index="1",
    device_name="Scanner 72",
    scan_type=ScanType.SETUP,
    primary_scan=False,
    scan_sequence_type=MriScanSequence.RARE,
    rare_factor=8,
    echo_time=Decimal("3.42"),
    echo_time_unit=TimeUnit.MS,
    repetition_time=Decimal("100.0"),
    repetition_time_unit=TimeUnit.MS,
    subject_position=SubjectPosition.SUPINE,
    resolution=Scale(scale=[0.5, 0.4375, 0.52]),
    resolution_unit=SizeUnit.MM,
    additional_scan_parameters={},
    notes="Set up scan for the 3D scan.",
)

scan2 = MRIScan(
    scan_index="2",
    device_name="Scanner 72",
    scan_type=ScanType.SCAN_3D,
    primary_scan=True,
    scan_sequence_type=MriScanSequence.RARE,
    rare_factor=4,
    echo_time=Decimal(5.33333333333333),
    echo_time_unit=TimeUnit.MS,
    effective_echo_time=Decimal("10.6666666666666998253276688046753406524658203125"),
    repetition_time=Decimal("500.0"),
    repetition_time_unit=TimeUnit.MS,
    scan_affine_transform=[
        Affine(
            affine_transform=[[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]],
        ),
        Translation(
            translation=[-6.1, 7.0, 7.9],
        ),
    ],
    subject_position=SubjectPosition.SUPINE,
    resolution=Scale(scale=[0.5, 0.4375, 0.52]),
    resolution_unit=SizeUnit.MM,
    additional_scan_parameters={},
    notes=None,
)

stream = DataStream(
    stream_start_time="2024-03-12T16:27:55.584892Z",
    stream_end_time="2024-03-12T16:27:55.584892Z",
    active_devices=["Scanner 72"],
    configurations=[scan1, scan2],
    modalities=[Modality.MRI],
)

acquisition = Acquisition(
    subject_id="123456",
    acquisition_start_time="2024-03-12T16:27:55.584892Z",
    acquisition_end_time="2024-03-12T16:27:55.584892Z",
    experimenters=["John Smith"],
    protocol_id=["dx.doi.org/10.57824/protocols.io.bh7kl4n6"],
    ethics_review_id=["1234"],
    acquisition_type="3D MRI Volume",
    instrument_id="NA",
    coordinate_system=CoordinateSystemLibrary.MRI_LPS,
    subject_details=AcquisitionSubjectDetails(
        mouse_platform_name="NA",
    ),
    data_streams=[stream],
    notes="There was some information about this scan acquisition",
)

if __name__ == "__main__":
    serialized = acquisition.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="mri")
