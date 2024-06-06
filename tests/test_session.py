""" example unit test file """

import re
import unittest
from datetime import datetime, timezone

import pydantic
from aind_data_schema_models.modalities import Modality
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.components.coordinates import (
    CcfCoords,
    Coordinates3d,
    Rotation3dTransform,
    Scale3dTransform,
    Translation3dTransform,
)
from aind_data_schema.core.session import (
    DomeModule,
    ManipulatorModule,
    MRIScan,
    RewardDeliveryConfig,
    Scanner,
    Session,
    Stream,
)

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


class ExampleTest(unittest.TestCase):
    """an example test"""

    def test_constructors(self):
        """always returns true"""

        with self.assertRaises(pydantic.ValidationError):
            sess = Session()

        sess = Session(
            experimenter_full_name=["alice"],
            session_start_time=datetime.now(),
            session_end_time=datetime.now(),
            subject_id="1234",
            session_type="Test",
            rig_id="1234",
            mouse_platform_name="Running wheel",
            active_mouse_platform=False,
            data_streams=[
                Stream(
                    stream_start_time=datetime.now(),
                    stream_end_time=datetime.now(),
                    stream_modalities=[Modality.ECEPHYS],
                    stick_microscopes=[
                        DomeModule(
                            assembly_name="Stick_assembly",
                            arc_angle=24,
                            module_angle=10,
                        )
                    ],
                    ephys_modules=[
                        ManipulatorModule(
                            assembly_name="Ephys_assemblyA",
                            arc_angle=0,
                            module_angle=10,
                            primary_targeted_structure="VISlm",
                            targeted_ccf_coordinates=[CcfCoords(ml="1", ap="1", dv="1")],
                            manipulator_coordinates=Coordinates3d(x="1", y="1", z="1"),
                        ),
                    ],
                )
            ],
        )

        assert sess is not None

        with self.assertRaises(pydantic.ValidationError):
            RewardDeliveryConfig()

        with self.assertRaises(pydantic.ValidationError):
            RewardDeliveryConfig(reward_solution="Other")

        with self.assertRaises(ValidationError):
            MRIScan(
                scan_sequence_type="Other",
            )

        with self.assertRaises(ValidationError):
            MRIScan(scan_sequence_type="Other", notes="")

        stream = Stream(
            stream_start_time="2024-03-12T16:27:55.584892Z",
            stream_end_time="2024-03-12T16:27:55.584892Z",
            mri_scans=[
                MRIScan(
                    scan_index=1,
                    scan_type="3D Scan",
                    scan_sequence_type="RARE",
                    rare_factor=4,
                    primary_scan=True,
                    vc_orientation=Rotation3dTransform(rotation=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
                    vc_position=Translation3dTransform(translation=[1, 1, 1]),
                    subject_position="Supine",
                    voxel_sizes=Scale3dTransform(scale=[0.1, 0.1, 0.1]),
                    echo_time=2.2,
                    effective_echo_time=2.0,
                    repetition_time=1.2,
                    additional_scan_parameters={"number_averages": 3},
                    mri_scanner=Scanner(
                        name="Scanner 72",
                        scanner_location="Fred Hutch",
                        magnetic_strength="7",
                    ),
                )
            ],
            stream_modalities=[Modality.MRI],
        )

        mri = Session(
            experimenter_full_name=["Frank Frankson"],
            subject_id="123456",
            session_start_time=datetime.now(tz=timezone.utc),
            session_end_time=datetime.now(tz=timezone.utc),
            protocol_id=["doi_path"],
            iacuc_protocol="1234",
            session_type="3D MRI Volume",
            rig_id="NA",
            animal_weight_prior=22.1,
            animal_weight_post=21.9,
            data_streams=[stream],
            mouse_platform_name="NA",
            active_mouse_platform=False,
        )

        assert mri is not None

    def test_validators(self):
        """Test the session file validators"""

        with self.assertRaises(pydantic.ValidationError) as e:
            Stream(
                stream_start_time=datetime.now(),
                stream_end_time=datetime.now(),
                stream_modalities=[
                    Modality.ECEPHYS,
                    Modality.SLAP,
                    Modality.FIB,
                    Modality.BEHAVIOR_VIDEOS,
                    Modality.POPHYS,
                    Modality.BEHAVIOR,
                    Modality.MRI,
                ],
            )

        self.assertTrue("ephys_modules field must be utilized for Ecephys modality" in repr(e.exception))
        self.assertTrue("light_sources field must be utilized for FIB modality" in repr(e.exception))
        self.assertTrue(
            "ophys_fovs field OR stack_parameters field must be utilized for Pophys modality" in repr(e.exception)
        )
        self.assertTrue("camera_names field must be utilized for Behavior Videos modality" in repr(e.exception))
        self.assertTrue("mri_scans field must be utilized for MRI modality" in repr(e.exception))

        with self.assertRaises(ValueError) as e:
            MRIScan(
                scan_index=1,
                scan_type="3D Scan",
                scan_sequence_type="RARE",
                rare_factor=4,
                primary_scan=True,
                subject_position="Supine",
                voxel_sizes=Scale3dTransform(scale=[0.1, 0.1, 0.1]),
                echo_time=2.2,
                effective_echo_time=2.0,
                repetition_time=1.2,
                additional_scan_parameters={"number_averages": 3},
            )

        expected_exception = (
            "1 validation error for MRIScan\n"
            "  Value error, Primary scan must have vc_orientation, vc_position, and voxel_sizes fields "
            "[type=value_error, input_value={'scan_index': 1, 'scan_t... {'number_averages': 3}}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )
        self.assertEqual(expected_exception, repr(e.exception))


if __name__ == "__main__":
    unittest.main()
