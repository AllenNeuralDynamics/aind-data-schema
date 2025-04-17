""" Tests for the configs module """

import unittest
from decimal import Decimal
from pydantic import ValidationError
from aind_data_schema.components.acquisition_configs import (
    MRIScan,
    Scale,
    ManipulatorConfig,
    LickSpoutConfig,
    Liquid,
    Valence,
    ImagingConfig,
    Channel,
    Image,
    FieldOfView,
    DetectorConfig,
    LaserConfig,
)
from aind_data_schema.components.coordinates import (
    Coordinate,
    CoordinateSystemLibrary,
    Transform,
    Affine,
    Translation,
    CoordinateTransform,
)
from aind_data_schema_models.brain_atlas import CCFStructure
from aind_data_schema_models.units import AngleUnit


class TestMRIScan(unittest.TestCase):
    """Tests for the MRIScan class"""

    def test_validate_primary_scan_success(self):
        """Test validate_primary_scan method with valid primary scan data"""
        scan = MRIScan(
            device_name="MRI Scanner",
            scan_index=1,
            scan_type="3D Scan",
            primary_scan=True,
            scan_sequence_type="RARE",
            echo_time=Decimal("10.0"),
            repetition_time=Decimal("2000.0"),
            subject_position="Prone",
            additional_scan_parameters={},
            vc_transform=Transform(
                system_name=CoordinateSystemLibrary.MRI_LPS.name,
                transforms=[
                    Affine(
                        affine_transform=[[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]],
                    ),
                    Translation(
                        translation=[1, 2, 3],
                    ),
                ],
            ),
            voxel_sizes=Scale(
                scale=[0.5, 0.4375, 0.52],
            ),
            processing_steps=[],
        )
        self.assertIsNotNone(scan)

    def test_validate_primary_scan_failure(self):
        """Test validate_primary_scan method with invalid primary scan data"""
        invalid_data = {
            "device_name": "MRI Scanner",
            "scan_index": 1,
            "scan_type": "3D Scan",
            "primary_scan": True,
            "scan_sequence_type": "RARE",
            "echo_time": Decimal("10.0"),
            "repetition_time": Decimal("2000.0"),
            "subject_position": "Prone",
            "additional_scan_parameters": {},
        }
        with self.assertRaises(ValidationError):
            MRIScan(**invalid_data)


class TestManipulatorConfig(unittest.TestCase):
    """Tests for the ManipulatorConfig class"""

    def test_validate_len_coordinates_success(self):
        """Test validate_len_coordinates method with valid coordinate lengths"""
        coordinate1 = Coordinate(
            system_name=CoordinateSystemLibrary.BREGMA_ARI.name,
            position=[1, 2, 3],
        )
        coordinate2 = Coordinate(
            system_name=CoordinateSystemLibrary.BREGMA_ARI.name,
            position=[4, 5, 6],
        )
        coordinate1_surface = Coordinate(
            system_name=CoordinateSystemLibrary.BREGMA_ARID.name,
            position=[1, 2, 3, 1],
        )
        coordinate2_surface = Coordinate(
            system_name=CoordinateSystemLibrary.BREGMA_ARID.name,
            position=[4, 5, 6, 2],
        )
        config = ManipulatorConfig(
            device_name="Manipulator",
            arc_angle=Decimal("45.0"),
            module_angle=Decimal("30.0"),
            angle_unit=AngleUnit.DEG,
            primary_targeted_structure=CCFStructure.HPF,
            atlas_coordinates=[coordinate1, coordinate2],
            manipulator_coordinates=[coordinate1_surface, coordinate2_surface],
            manipulator_axis_positions=[coordinate1, coordinate2],
        )
        self.assertIsInstance(config, ManipulatorConfig)

    def test_validate_len_coordinates_failure(self):
        """Test validate_len_coordinates method with invalid coordinate lengths"""

        with self.assertRaises(ValueError) as context:
            ManipulatorConfig(
                device_name="Manipulator",
                arc_angle=Decimal("45.0"),
                module_angle=Decimal("30.0"),
                angle_unit=AngleUnit.DEG,
                primary_targeted_structure=CCFStructure.HPF,
                atlas_coordinates=[
                    Coordinate(
                        system_name=CoordinateSystemLibrary.BREGMA_ARI.name,
                        position=[1, 2, 3],
                    ),
                ],
                manipulator_coordinates=[
                    Coordinate(
                        system_name=CoordinateSystemLibrary.PROBE_ARID.name,
                        position=[1, 2, 3, 1],
                    ),
                    Coordinate(
                        system_name=CoordinateSystemLibrary.PROBE_ARID.name,
                        position=[4, 5, 6, 2],
                    ),
                ],
                manipulator_axis_positions=[
                    Coordinate(
                        system_name=CoordinateSystemLibrary.BREGMA_ARI.name,
                        position=[1, 2, 3],
                    ),
                    Coordinate(
                        system_name=CoordinateSystemLibrary.BREGMA_ARI.name,
                        position=[4, 5, 6],
                    ),
                ],
            )

        self.assertIn(
            "Length of atlas_coordinates, manipulator_coordinates, and manipulator_axis_positions must be the same",
            str(context.exception),
        )


class TestLickSpoutConfig(unittest.TestCase):
    """Tests for the LickSpoutConfig class"""

    def test_validate_other_success(self):
        """Test validate_other method with valid data"""
        lick_spout = LickSpoutConfig(
            solution=Liquid.WATER,
            solution_valence=Valence.POSITIVE,
            relative_position=[],
        )
        self.assertIsNotNone(lick_spout)

    def test_validate_other_failure(self):
        """Test validate_other method with invalid data"""
        with self.assertRaises(ValueError) as context:
            LickSpoutConfig(
                solution=Liquid.OTHER,
                solution_valence=Valence.POSITIVE,
                relative_position=[],
            )
        self.assertIn(
            "Notes cannot be empty if LickSpoutConfig.solution is Other." "Describe the solution in the notes field.",
            str(context.exception),
        )


class TestImagingConfig(unittest.TestCase):
    """Tests for the ImagingConfig class"""

    def setUp(self):
        """Set up common test data"""
        self.channel1 = Channel(
            channel_name="Channel1",
            detector=DetectorConfig(
                device_name="Detector1",
                exposure_time=Decimal("10.0"),
                trigger_type="Internal",
            ),
            light_sources=[
                LaserConfig(
                    device_name="Laser1",
                    wavelength=488,
                )
            ],
        )
        self.channel2 = Channel(
            channel_name="Channel2",
            detector=DetectorConfig(
                device_name="Detector2",
                exposure_time=Decimal("20.0"),
                trigger_type="External",
            ),
            light_sources=[
                LaserConfig(
                    device_name="Laser2",
                    wavelength=561,
                )
            ],
        )
        self.coordinate_system = CoordinateSystemLibrary.BREGMA_ARI

    def test_check_image_channels_success(self):
        """Test check_image_channels validator with valid data"""
        imaging_config = ImagingConfig(
            channels=[self.channel1, self.channel2],
            images=[
                FieldOfView(
                    channel_name="Channel1",
                    targeted_structure=CCFStructure.HPF,
                    center_coordinate=Coordinate(
                        system_name=self.coordinate_system.name,
                        position=[0, 0, 0],
                    ),
                    fov_width=512,
                    fov_height=512,
                    fov_scale_factor=Decimal("0.5"),
                    frame_rate=Decimal("30.0"),
                    planes=[],
                )
            ],
            coordinate_system=self.coordinate_system,
        )
        self.assertIsNotNone(imaging_config)

    def test_check_image_channels_failure(self):
        """Test check_image_channels validator with invalid data"""
        with self.assertRaises(ValidationError) as context:
            ImagingConfig(
                channels=[self.channel1],
                images=[
                    FieldOfView(
                        channel_name="InvalidChannel",
                        targeted_structure=CCFStructure.HPF,
                        center_coordinate=Coordinate(
                            system_name=self.coordinate_system.name,
                            position=[0, 0, 0],
                        ),
                        fov_width=512,
                        fov_height=512,
                        fov_scale_factor=Decimal("0.5"),
                        frame_rate=Decimal("30.0"),
                        planes=[],
                    )
                ],
                coordinate_system=self.coordinate_system,
            )
        self.assertIn(
            "Channel InvalidChannel must be defined in the ImagingConfig.channels list",
            str(context.exception),
        )

    def test_require_cs_images_success(self):
        """Test require_cs_images validator with valid data"""
        imaging_config = ImagingConfig(
            channels=[self.channel1],
            images=[
                Image(
                    channel_name="Channel1",
                    coordinate_transform=CoordinateTransform(
                        input="SPIM_IJK",
                        output="BREGMA_ARI",
                        transforms=[
                            Affine(affine_transform=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [0, 0, 0, 1]]),
                        ],
                    ),
                ),
            ],
            coordinate_system=self.coordinate_system,
        )
        self.assertIsNotNone(imaging_config)

    def test_require_cs_images_failure(self):
        """Test require_cs_images validator with missing coordinate system"""
        with self.assertRaises(ValidationError) as context:
            ImagingConfig(
                channels=[self.channel1],
                images=[
                    Image(
                        channel_name="Channel1",
                        coordinate_transform=CoordinateTransform(
                            input="SPIM_IJK",
                            output="BREGMA_ARI",
                            transforms=[
                                Affine(affine_transform=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [0, 0, 0, 1]]),
                            ],
                        ),
                    ),
                ],
                coordinate_system=None,
            )
        self.assertIn(
            "Coordinate system is required if any images are Image",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
