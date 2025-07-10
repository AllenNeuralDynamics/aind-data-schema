""" Test for the acquisition.json """

import unittest
from datetime import datetime, timezone

import pydantic
from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import SizeUnit, TimeUnit
from pydantic import ValidationError

from aind_data_schema.components.configs import (
    EphysAssemblyConfig,
    ImagingConfig,
    Immersion,
    ManipulatorConfig,
    MISModuleConfig,
    MRIScan,
    SampleChamberConfig,
)
from aind_data_schema.components.coordinates import Affine, CoordinateSystemLibrary, Scale, Translation
from aind_data_schema.core.acquisition import Acquisition, AcquisitionSubjectDetails, DataStream
from aind_data_schema.components.connections import Connection
from examples.ephys_acquisition import acquisition as ephys_acquisition
from examples.exaspim_acquisition import acq as exaspim_acquisition


class AcquisitionTest(unittest.TestCase):
    """Group of tests for the Acquisition class"""

    def test_constructors(self):
        """Test constructing acquisition files"""

        with self.assertRaises(pydantic.ValidationError):
            Acquisition()

        acq = ephys_acquisition.model_copy()
        self.assertIsNotNone(Acquisition.model_validate_json(acq.model_dump_json()))

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
                    scan_affine_transform=[
                        Affine(
                            affine_transform=[[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]],
                        ),
                        Translation(
                            translation=[1, 1, 1],
                        ),
                    ],
                    subject_position="Supine",
                    resolution=Scale(
                        scale=[0.5, 0.4375, 0.52],
                    ),
                    resolution_unit=SizeUnit.MM,
                    echo_time=2.2,
                    echo_time_unit=TimeUnit.MS,
                    effective_echo_time=2.0,
                    repetition_time=1.2,
                    repetition_time_unit=TimeUnit.MS,
                    additional_scan_parameters={"number_averages": 3},
                    device_name="Scanner 72",
                )
            ],
            modalities=[Modality.MRI],
        )

        mri = Acquisition(
            experimenters=["Mam Moth"],
            subject_id="123456",
            acquisition_start_time=datetime.now(tz=timezone.utc),
            acquisition_end_time=datetime.now(tz=timezone.utc),
            protocol_id=["doi_path"],
            ethics_review_id=["1234"],
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
        with self.assertRaises(ValueError) as context:
            acq = ephys_acquisition.model_copy()

            acq.subject_details = None

            Acquisition.model_validate_json(acq.model_dump_json())

        self.assertIn("Subject details are required for in vivo experiments", str(context.exception))

    def test_check_subject_specimen_id(self):
        """Test that subject and specimen IDs match"""
        with self.assertRaises(ValueError) as context:
            acq = exaspim_acquisition.model_copy()
            acq.specimen_id = "654321"

            Acquisition.model_validate_json(acq.model_dump_json())

        self.assertIn("Expected 123456 to appear in 654321", str(context.exception))

    def test_specimen_required(self):
        """Test that specimen ID is required for in vitro imaging modalities"""
        with self.assertRaises(ValueError):
            Acquisition(
                experimenters=["Mam Moth"],
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
                            MISModuleConfig(
                                device_name="Stick_assembly",
                                arc_angle=24,
                                module_angle=10,
                            ),
                            ManipulatorConfig(
                                device_name="Ephys_assemblyA",
                                arc_angle=0,
                                module_angle=10,
                                primary_targeted_structure=CCFv3.VISL,
                                atlas_coordinates=[
                                    Translation(
                                        translation=[1, 1, 1, 0],
                                    ),
                                ],
                                manipulator_coordinates=[
                                    Translation(
                                        translation=[1, 1, 1, 1],
                                    )
                                ],
                                manipulator_axis_positions=[
                                    Translation(
                                        translation=[1, 1, 1, 0],
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
                EphysAssemblyConfig.model_construct(),
            ],
        )
        self.assertIsNotNone(stream)

    def test_specimen_required_for_in_vitro_modalities(self):
        """Test that specimen ID is required for in vitro imaging modalities"""

        # Test case where specimen ID is missing for in vitro modality
        with self.assertRaises(ValueError) as context:
            Acquisition(
                experimenters=["Mam Moth"],
                acquisition_start_time=datetime.now(),
                acquisition_end_time=datetime.now(),
                subject_id="123456",
                acquisition_type="Test",
                instrument_id="1234",
                subject_details=AcquisitionSubjectDetails(
                    mouse_platform_name="Running wheel",
                ),
                data_streams=[
                    DataStream(
                        stream_start_time=datetime.now(),
                        stream_end_time=datetime.now(),
                        modalities=[Modality.SPIM],
                        active_devices=["Device1"],
                        configurations=[
                            ImagingConfig(
                                device_name="Device1",
                                channels=[],
                                images=[],
                            ),
                            SampleChamberConfig(
                                device_name="Sample chamber",
                                chamber_immersion=Immersion(
                                    medium="PBS",
                                    refractive_index=1.33,
                                ),
                            ),
                        ],
                    )
                ],
            )
        self.assertIn("Specimen ID is required for modalities", str(context.exception))

        # Test case where specimen ID is provided for in vitro modality
        acquisition = Acquisition(
            experimenters=["Mam Moth"],
            acquisition_start_time=datetime.now(),
            acquisition_end_time=datetime.now(),
            subject_id="123456",
            specimen_id="SP123456",
            acquisition_type="Test",
            instrument_id="1234",
            subject_details=AcquisitionSubjectDetails(
                mouse_platform_name="Running wheel",
            ),
            data_streams=[
                DataStream(
                    stream_start_time=datetime.now(),
                    stream_end_time=datetime.now(),
                    modalities=[Modality.SPIM],
                    active_devices=["Device1"],
                    configurations=[
                        ImagingConfig(
                            device_name="Device1",
                            channels=[],
                            images=[],
                        ),
                        SampleChamberConfig(
                            device_name="Sample chamber",
                            chamber_immersion=Immersion(
                                medium="PBS",
                                refractive_index=1.33,
                            ),
                        ),
                    ],
                )
            ],
        )
        self.assertIsNotNone(acquisition)

    def test_check_connections(self):
        """Test that every device in a Connection is present in the active_devices list"""

        # Test valid connections
        stream = DataStream(
            stream_start_time=datetime.now(),
            stream_end_time=datetime.now(),
            modalities=[],
            active_devices=["DeviceA", "DeviceB", "SomeTarget"],
            configurations=[],
            connections=[
                Connection(source_device="DeviceA", target_device="SomeTarget"),
                Connection(source_device="DeviceB", target_device="SomeTarget"),
            ],
        )
        self.assertIsNotNone(stream)

        # Test invalid connections
        with self.assertRaises(ValueError) as context:
            DataStream(
                stream_start_time=datetime.now(),
                stream_end_time=datetime.now(),
                modalities=[],
                active_devices=["DeviceA"],
                configurations=[],
                connections=[
                    Connection(source_device="SomeTarget", target_device="DeviceA"),
                ],
            )
        self.assertIn("Missing devices in active_devices list for connection", str(context.exception))

        # Test invalid connections
        with self.assertRaises(ValueError) as context:
            DataStream(
                stream_start_time=datetime.now(),
                stream_end_time=datetime.now(),
                modalities=[],
                active_devices=["DeviceA"],
                configurations=[],
                connections=[
                    Connection(source_device="DeviceA", target_device="SomeTarget"),
                ],
            )
        self.assertIn("Missing devices in active_devices list for connection", str(context.exception))


if __name__ == "__main__":
    unittest.main()
