""" Test for the acquisition.json """

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
from aind_data_schema.components.identifiers import Person
from aind_data_schema.components.configs import (
    DomeModule,
    ManipulatorModule,
    MRIScan,
    RewardDeliveryConfig,
)
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    SubjectDetails,
)
from aind_data_schema_models.brain_atlas import CCFStructure

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


class AcquisitionTest(unittest.TestCase):
    """Group of tests for the Acquisition class"""

    def test_constructors(self):
        """Test constructing acquisition files"""

        with self.assertRaises(pydantic.ValidationError):
            acquisition = Acquisition()

        acquisition = Acquisition(
            experimenters=[Person(name="Mam Moth")],
            acquisition_start_time=datetime.now(),
            acquisition_end_time=datetime.now(),
            subject_id="1234",
            experiment_type="Test",
            instrument_id="1234",
            subject_details=SubjectDetails(
                mouse_platform_name="Running wheel",
            ),
            data_streams=[
                DataStream(
                    stream_start_time=datetime.now(),
                    stream_end_time=datetime.now(),
                    modalities=[Modality.ECEPHYS],
                    active_devices=["Stick_assembly", "Ephys_assemblyA"],
                    configurations=[
                        DomeModule(
                            device_name="Stick_assembly",
                            arc_angle=24,
                            module_angle=10,
                        ),
                        ManipulatorModule(
                            device_name="Ephys_assemblyA",
                            arc_angle=0,
                            module_angle=10,
                            primary_targeted_structure=CCFStructure.VISL,
                            targeted_ccf_coordinates=[CcfCoords(ml="1", ap="1", dv="1")],
                            manipulator_coordinates=Coordinates3d(x="1", y="1", z="1"),
                        ),
                    ],
                )
            ],
        )

        self.assertIsNotNone(acquisition)

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

        # mri_scanner=Scanner(
        #     name="Scanner 72",
        #     scanner_location="Fred Hutch",
        #     magnetic_strength="7",
        # )

        stream = DataStream(
            stream_start_time="2024-03-12T16:27:55.584892Z",
            stream_end_time="2024-03-12T16:27:55.584892Z",
            active_devices=["Scanner 72"],
            configurations=[
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
                    device_name="Scanner 72",
                )
            ],
            modalities=[Modality.MRI],
        )

        mri = Acquisition(
            experimenters=[Person(name="Mam Moth")],
            subject_id="123456",
            acquisition_start_time=datetime.now(tz=timezone.utc),
            acquisition_end_time=datetime.now(tz=timezone.utc),
            protocol_id=["doi_path"],
            ethics_review_id="1234",
            experiment_type="3D MRI Volume",
            instrument_id="NA",
            subject_details=SubjectDetails(
                animal_weight_prior=22.1,
                animal_weight_post=21.9,
                mouse_platform_name="NA",
            ),
            data_streams=[stream],
        )

        assert mri is not None

    def test_subject_details_if_not_specimen(self):
        """Test that subject details are required if no specimen ID"""
        with self.assertRaises(ValueError):
            Acquisition(
                experimenters=[Person(name="Mam Moth")],
                acquisition_start_time=datetime.now(),
                acquisition_end_time=datetime.now(),
                subject_id="1234",
                experiment_type="Test",
                instrument_id="1234",
                data_streams=[
                    DataStream(
                        stream_start_time=datetime.now(),
                        stream_end_time=datetime.now(),
                        modalities=[Modality.ECEPHYS],
                        active_devices=["Stick_assembly", "Ephys_assemblyA"],
                        configurations=[
                            DomeModule(
                                device_name="Stick_assembly",
                                arc_angle=24,
                                module_angle=10,
                            ),
                            ManipulatorModule(
                                device_name="Ephys_assemblyA",
                                arc_angle=0,
                                module_angle=10,
                                primary_targeted_structure=CCFStructure.VISL,
                                targeted_ccf_coordinates=[CcfCoords(ml="1", ap="1", dv="1")],
                                manipulator_coordinates=Coordinates3d(x="1", y="1", z="1"),
                            ),
                        ],
                    )
                ],
            )

    def test_check_subject_specimen_id(self):
        """Test that subject and specimen IDs match"""
        with self.assertRaises(ValueError):
            Acquisition(
                experimenters=[Person(name="Mam Moth")],
                acquisition_start_time=datetime.now(),
                acquisition_end_time=datetime.now(),
                subject_id="123456",
                specimen_id="654321",
                experiment_type="Test",
                instrument_id="1234",
                subject_details=SubjectDetails(
                    mouse_platform_name="Running wheel",
                ),
                data_streams=[
                    DataStream(
                        stream_start_time=datetime.now(),
                        stream_end_time=datetime.now(),
                        modalities=[Modality.ECEPHYS],
                        active_devices=["Stick_assembly", "Ephys_assemblyA"],
                        configurations=[
                            DomeModule(
                                device_name="Stick_assembly",
                                arc_angle=24,
                                module_angle=10,
                            ),
                            ManipulatorModule(
                                device_name="Ephys_assemblyA",
                                arc_angle=0,
                                module_angle=10,
                                primary_targeted_structure=CCFStructure.VISL,
                                targeted_ccf_coordinates=[CcfCoords(ml="1", ap="1", dv="1")],
                                manipulator_coordinates=Coordinates3d(x="1", y="1", z="1"),
                            ),
                        ],
                    )
                ],
            )

    def test_specimen_required(self):
        """Test that specimen ID is required for in vitro imaging modalities"""
        with self.assertRaises(ValueError):
            Acquisition(
                experimenters=[Person(name="Mam Moth")],
                acquisition_start_time=datetime.now(),
                acquisition_end_time=datetime.now(),
                subject_id="123456",
                experiment_type="Test",
                instrument_id="1234",
                subject_details=SubjectDetails(
                    mouse_platform_name="Running wheel",
                ),
                data_streams=[
                    DataStream(
                        stream_start_time=datetime.now(),
                        stream_end_time=datetime.now(),
                        modalities=[Modality.SPIM],
                        active_devices=["Stick_assembly", "Ephys_assemblyA"],
                        configurations=[
                            DomeModule(
                                device_name="Stick_assembly",
                                arc_angle=24,
                                module_angle=10,
                            ),
                            ManipulatorModule(
                                device_name="Ephys_assemblyA",
                                arc_angle=0,
                                module_angle=10,
                                primary_targeted_structure=CCFStructure.VISL,
                                targeted_ccf_coordinates=[CcfCoords(ml="1", ap="1", dv="1")],
                                manipulator_coordinates=Coordinates3d(x="1", y="1", z="1"),
                            ),
                        ],
                    )
                ],
            )

    def test_check_modality_config_requirements(self):
        """Test that modality configuration requirements are enforced"""

        # Test missing required devices for ECEPHYS modality
        with self.assertRaises(ValueError):
            DataStream(
                stream_start_time=datetime.now(),
                stream_end_time=datetime.now(),
                modalities=[Modality.ECEPHYS],
                active_devices=[],
                configurations=[],
            )

        # Test valid configuration for ECEPHYS modality
        stream = DataStream(
            stream_start_time=datetime.now(),
            stream_end_time=datetime.now(),
            modalities=[Modality.ECEPHYS],
            active_devices=["Stick_assembly", "Ephys_assemblyA"],
            configurations=[
                DomeModule(
                    device_name="Stick_assembly",
                    arc_angle=24,
                    module_angle=10,
                ),
                ManipulatorModule(
                    device_name="Ephys_assemblyA",
                    arc_angle=0,
                    module_angle=10,
                    primary_targeted_structure=CCFStructure.VISL,
                    targeted_ccf_coordinates=[CcfCoords(ml="1", ap="1", dv="1")],
                    manipulator_coordinates=Coordinates3d(x="1", y="1", z="1"),
                ),
            ],
        )
        self.assertIsNotNone(stream)


if __name__ == "__main__":
    unittest.main()
