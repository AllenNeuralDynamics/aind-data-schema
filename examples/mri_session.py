"""example MRISession and MRIScan"""

from decimal import Decimal

from aind_data_schema.core.mri_session import MRIScan, MriScanSequence, MriSession, ScanType, SubjectPosition
from aind_data_schema.models.coordinates import Rotation3dTransform, Scale3dTransform, Translation3dTransform
from aind_data_schema.models.devices import Scanner

scan1 = MRIScan(
    scan_index="1",
    scan_type=ScanType.SETUP,
    primary_scan=False,
    scan_sequence_type=MriScanSequence.RARE,
    rare_factor=8,
    echo_time=Decimal(3.42),
    repetition_time=Decimal(100.0),
    subject_position=SubjectPosition.SUPINE,
    voxel_sizes=Scale3dTransform(scale=[0.5, 0.4375, 0.52]),
    processing_steps=[],
    additional_scan_parameters={},
    notes="Set up scan for the 3D scan.",
)

scan2 = MRIScan(
    scan_index="2",
    scan_type=ScanType.SCAN_3D,
    primary_scan=True,
    scan_sequence_type=MriScanSequence.RARE,
    rare_factor=4,
    echo_time=Decimal(5.33333333333333),
    effective_echo_time=Decimal(10.6666666666666998253276688046753406524658203125),
    repetition_time=Decimal(500.0),
    vc_orientation=Rotation3dTransform(rotation=[1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0]),
    vc_position=Translation3dTransform(translation=[-6.1, -7.0, 7.9]),
    subject_position=SubjectPosition.SUPINE,
    voxel_sizes=Scale3dTransform(scale=[0.1, 0.1, 0.1]),
    processing_steps=[],
    additional_scan_parameters={},
    notes=None,
)

scans = [scan1, scan2]

sess = MriSession(
    subject_id="",
    session_start_time="2024-03-12T16:27:55.584892Z",
    session_end_time="2024-03-12T16:27:55.584892Z",
    experimenter_full_name=["Allen Brain"],
    protocol_id="dx.doi.org/10.57824/protocols.io.bh7kl4n6",
    iacuc_protocol="12345",
    mri_scanner=Scanner(
        name="Scanner 72",
        scanner_location="Fred Hutch",
        magnetic_strength="7",
    ),
    scans=scans,
    notes="There was some information about this scan session",
)
serialized = sess.model_dump_json()
deserialized = MriSession.model_validate_json(serialized)
deserialized.write_standard_file()
