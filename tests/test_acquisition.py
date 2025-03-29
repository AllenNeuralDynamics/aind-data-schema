""" Test for the acquisition.json """

import unittest
from datetime import datetime, timezone

import pydantic
from aind_data_schema_models.modalities import Modality
from pydantic import ValidationError

from aind_data_schema.components.coordinates import (
    Affine,
    Scale,
    Translation,
    Coordinate,
    Transform,
    CoordinateSystemLibrary,
)
from aind_data_schema.components.identifiers import Person
from aind_data_schema.components.acquisition_configs import (
    DomeModule,
    ManipulatorConfig,
    MRIScan,
)
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    AcquisitionSubjectDetails,
)
from aind_data_schema_models.brain_atlas import CCFStructure


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
            acquisition_type="Test",
            instrument_id="1234",
            subject_details=AcquisitionSubjectDetails(
                mouse_platform_name="Running wheel",
            ),
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
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
                        ManipulatorConfig(
                            device_name="Ephys_assemblyA",
                            arc_angle=0,
                            module_angle=10,
                            primary_targeted_structure=CCFStructure.VISL,
                            atlas_coordinates=[
                                Coordinate(
                                    system_name="BREGMA_ARID",
                                    position=[1, 1, 1, 0],
                                ),
                            ],
                            manipulator_coordinates=[
                                Coordinate(
                                    system_name="BREGMA_ARID",
                                    position=[1, 1, 1, 1],
                                )
                            ],
                            manipulator_axis_positions=[
                                Coordinate(
                                    system_name="BREGMA_ARID",
                                    position=[1, 1, 1, 0],
                                )
                            ],
                        ),
                    ],
                )
            ],
        )

        self.assertIsNotNone(acquisition)

        with self.assertRaises(ValidationError):
            MRIScan(
                scan_sequence_type="Other",
            )

        with self.assertRaises(ValidationError):
            MRIScan(scan_sequence_type="Other", notes="")

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
                    vc_transform=Transform(
                        system_name=CoordinateSystemLibrary.MRI_LPS.name,
                        transforms=[
                            Affine(
                                affine_transform=[[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]],
                            ),
                            Translation(
                                translation=[1, 1, 1],
                            ),
                        ],
                    ),
                    subject_position="Supine",
                    voxel_sizes=Scale(
                        scale=[0.5, 0.4375, 0.52],
                    ),
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
            acquisition_type="3D MRI Volume",
            instrument_id="NA",
            coordinate_system=CoordinateSystemLibrary.MRI_LPS,
            subject_details=AcquisitionSubjectDetails(
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
                acquisition_type="Test",
                instrument_id="1234",
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
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
                            ManipulatorConfig(
                                device_name="Ephys_assemblyA",
                                arc_angle=0,
                                module_angle=10,
                                primary_targeted_structure=CCFStructure.VISL,
                                atlas_coordinates=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 0],
                                    ),
                                ],
                                manipulator_coordinates=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 1],
                                    )
                                ],
                                manipulator_axis_positions=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 0],
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            )

    def test_check_subject_specimen_id(self):
        """Test that subject and specimen IDs match"""
        with self.assertRaises(ValueError) as context:
            Acquisition(
                experimenters=[Person(name="Mam Moth")],
                acquisition_start_time=datetime.now(),
                acquisition_end_time=datetime.now(),
                subject_id="123456",
                specimen_id="654321",
                acquisition_type="Test",
                instrument_id="1234",
                subject_details=AcquisitionSubjectDetails(
                    mouse_platform_name="Running wheel",
                ),
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
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
                            ManipulatorConfig(
                                device_name="Ephys_assemblyA",
                                arc_angle=0,
                                module_angle=10,
                                primary_targeted_structure=CCFStructure.VISL,
                                atlas_coordinates=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 0],
                                    ),
                                ],
                                manipulator_coordinates=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 1],
                                    )
                                ],
                                manipulator_axis_positions=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 0],
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            )

        self.assertIn("Expected 123456 to appear in 654321", str(context.exception))

    def test_specimen_required(self):
        """Test that specimen ID is required for in vitro imaging modalities"""
        with self.assertRaises(ValueError):
            Acquisition(
                experimenters=[Person(name="Mam Moth")],
                acquisition_start_time=datetime.now(),
                acquisition_end_time=datetime.now(),
                subject_id="123456",
                acquisition_type="Test",
                instrument_id="1234",
                subject_details=AcquisitionSubjectDetails(
                    mouse_platform_name="Running wheel",
                ),
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
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
                            ManipulatorConfig(
                                device_name="Ephys_assemblyA",
                                arc_angle=0,
                                module_angle=10,
                                primary_targeted_structure=CCFStructure.VISL,
                                atlas_coordinates=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 0],
                                    ),
                                ],
                                manipulator_coordinates=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 1],
                                    )
                                ],
                                manipulator_axis_positions=[
                                    Coordinate(
                                        system_name="BREGMA_ARID",
                                        position=[1, 1, 1, 0],
                                    )
                                ],
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
                ManipulatorConfig(
                    device_name="Ephys_assemblyA",
                    arc_angle=0,
                    module_angle=10,
                    primary_targeted_structure=CCFStructure.VISL,
                    atlas_coordinates=[
                        Coordinate(
                            system_name="BREGMA_ARI",
                            position=[1, 1, 1],
                        ),
                    ],
                    manipulator_coordinates=[
                        Coordinate(
                            system_name="BREGMA_ARID",
                            position=[1, 1, 1, 1],
                        )
                    ],
                    manipulator_axis_positions=[
                        Coordinate(
                            system_name="BREGMA_ARI",
                            position=[1, 1, 1],
                        )
                    ],
                ),
            ],
        )
        self.assertIsNotNone(stream)


if __name__ == "__main__":
    unittest.main()
