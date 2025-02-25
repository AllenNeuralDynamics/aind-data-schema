"""example MRISession and MRIScan"""

from decimal import Decimal

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.coordinates import Rotation, Scaling, Translation
from aind_data_schema.components.devices import Scanner
from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.session import MRIScan, MriScanSequence, ScanType, Session, Stream, SubjectPosition

scan1 = MRIScan(
    scan_index="1",
    mri_scanner=Scanner(
        name="Scanner 72",
        scanner_location="Fred Hutch",
        magnetic_strength="7",
    ),
    scan_type=ScanType.SETUP,
    primary_scan=False,
    scan_sequence_type=MriScanSequence.RARE,
    rare_factor=8,
    echo_time=Decimal("3.42"),
    repetition_time=Decimal("100.0"),
    subject_position=SubjectPosition.SUPINE,
    voxel_sizes=Scaling(scale=[0.5, 0.4375, 0.52]),
    processing_steps=[],
    additional_scan_parameters={},
    notes="Set up scan for the 3D scan.",
)

scan2 = MRIScan(
    scan_index="2",
    mri_scanner=Scanner(
        name="Scanner 72",
        scanner_location="Fred Hutch",
        magnetic_strength="7",
    ),
    scan_type=ScanType.SCAN_3D,
    primary_scan=True,
    scan_sequence_type=MriScanSequence.RARE,
    rare_factor=4,
    echo_time=Decimal(5.33333333333333),
    effective_echo_time=Decimal("10.6666666666666998253276688046753406524658203125"),
    repetition_time=Decimal("500.0"),
    vc_orientation=Rotation(rotation=[1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0]),
    vc_position=Translation(translation=[-6.1, -7.0, 7.9]),
    subject_position=SubjectPosition.SUPINE,
    voxel_sizes=Scaling(scale=[0.1, 0.1, 0.1]),
    processing_steps=[],
    additional_scan_parameters={},
    notes=None,
)

stream = Stream(
    stream_start_time="2024-03-12T16:27:55.584892Z",
    stream_end_time="2024-03-12T16:27:55.584892Z",
    mri_scans=[scan1, scan2],
    stream_modalities=[Modality.MRI],
)

sess = Session(
    subject_id="123456",
    session_start_time="2024-03-12T16:27:55.584892Z",
    session_end_time="2024-03-12T16:27:55.584892Z",
    experimenters=[Person(name="John Smith")],
    protocol_id=["dx.doi.org/10.57824/protocols.io.bh7kl4n6"],
    ethics_review_id="1234",
    session_type="3D MRI Volume",
    instrument_id="NA",
    data_streams=[stream],
    mouse_platform_name="NA",
    active_mouse_platform=False,
    notes="There was some information about this scan session",
)
serialized = sess.model_dump_json()
deserialized = Session.model_validate_json(serialized)
deserialized.write_standard_file(prefix="mri")
