""" Tests for the configs module """

import unittest
from decimal import Decimal

from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.units import AngleUnit, FrequencyUnit, SizeUnit, TimeUnit, VolumeUnit
from pydantic import ValidationError

from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    ImageSPIM,
    ImagingConfig,
    LaserConfig,
    LickSpoutConfig,
    Liquid,
    MRIScan,
    PlanarImage,
    Plane,
    SamplingStrategy,
    Scale,
    Valence,
)
from aind_data_schema.components.coordinates import Affine, CoordinateSystemLibrary, Translation


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
            echo_time_unit=TimeUnit.MS,
            repetition_time=Decimal("2000.0"),
            repetition_time_unit=TimeUnit.MS,
            subject_position="Prone",
            additional_scan_parameters={},
            scan_affine_transform=[
                Affine(
                    affine_transform=[[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]],
                ),
                Translation(
                    translation=[1, 2, 3],
                ),
            ],
            resolution=Scale(
                scale=[0.5, 0.4375, 0.52],
            ),
            resolution_unit=SizeUnit.MM,
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

    def test_validate_primary_missing_fields(self):
        """Test that missing fields raise ValidationError"""

        with self.assertRaises(ValidationError) as context:
            MRIScan(
                device_name="MRI Scanner",
                scan_index=1,
                scan_type="3D Scan",
                primary_scan=True,
                scan_sequence_type="RARE",
                echo_time=Decimal("10.0"),
                echo_time_unit=TimeUnit.MS,
                repetition_time=Decimal("2000.0"),
                repetition_time_unit=TimeUnit.MS,
                subject_position="Prone",
                additional_scan_parameters={},
                resolution_unit=SizeUnit.MM,
            )

        self.assertIn("Primary scan must have scan_affine_transform and resolution fields", str(context.exception))


class TestLickSpoutConfig(unittest.TestCase):
    """Tests for the LickSpoutConfig class"""

    def test_validate_other_success(self):
        """Test validate_other method with valid data"""
        lick_spout = LickSpoutConfig(
            device_name="Spout1",
            solution=Liquid.WATER,
            solution_valence=Valence.POSITIVE,
            volume=1.0,
            volume_unit=VolumeUnit.ML,
            relative_position=[],
        )
        self.assertIsNotNone(lick_spout)

    def test_validate_other_failure(self):
        """Test validate_other method with invalid data"""
        with self.assertRaises(ValueError) as context:
            LickSpoutConfig(
                device_name="Spout1",
                solution=Liquid.OTHER,
                solution_valence=Valence.POSITIVE,
                volume=1.0,
                volume_unit=VolumeUnit.ML,
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
        self.coordinate_system = CoordinateSystemLibrary.SPIM_IJK
        self.sampling_strategy = SamplingStrategy(
            frame_rate=30.0,
            frame_rate_unit=FrequencyUnit.HZ,
        )

    def test_check_image_channels_success(self):
        """Test check_image_channels validator with valid data"""
        imaging_config = ImagingConfig(
            device_name="ImagingDevice",
            channels=[self.channel1, self.channel2],
            images=[
                PlanarImage(
                    channel_name="Channel1",
                    image_to_acquisition_transform=[
                        Translation(
                            translation=[0, 0],
                        ),
                    ],
                    dimensions=Scale(
                        scale=[512, 512],
                    ),
                    planes=[
                        Plane(
                            depth=150,
                            depth_unit="micrometer",
                            targeted_structure=CCFv3.HPF,
                            power=10,
                            power_unit="milliwatt",
                        ),
                    ],
                ),
            ],
            sampling_strategy=self.sampling_strategy,
            coordinate_system=self.coordinate_system,
        )
        self.assertIsNotNone(imaging_config)

    def test_check_image_channels_failure(self):
        """Test check_image_channels validator with invalid data"""
        with self.assertRaises(ValidationError) as context:
            ImagingConfig(
                device_name="ImagingDevice",
                channels=[self.channel1],
                images=[
                    PlanarImage(
                        channel_name="InvalidChannel",
                        image_to_acquisition_transform=[
                            Translation(
                                translation=[0, 0],
                            ),
                        ],
                        dimensions=Scale(
                            scale=[512, 512],
                        ),
                        planes=[
                            Plane(
                                depth=150,
                                depth_unit="micrometer",
                                targeted_structure=CCFv3.HPF,
                                power=10,
                                power_unit="milliwatt",
                            ),
                        ],
                    )
                ],
                sampling_strategy=self.sampling_strategy,
                coordinate_system=self.coordinate_system,
            )
        self.assertIn(
            "Channel InvalidChannel must be defined in the ImagingConfig.channels list",
            str(context.exception),
        )

    def test_require_cs_images_success(self):
        """Test require_cs_images validator with valid data"""
        imaging_config = ImagingConfig(
            device_name="ImagingDevice",
            channels=[self.channel1],
            images=[
                ImageSPIM(
                    channel_name="Channel1",
                    file_name="test_image.tiff",
                    image_to_acquisition_transform=[
                        Affine(affine_transform=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [0, 0, 0, 1]]),
                    ],
                    imaging_angle=45,
                    imaging_angle_unit=AngleUnit.DEG,
                ),
            ],
            coordinate_system=self.coordinate_system,
        )
        self.assertIsNotNone(imaging_config)

    def test_require_cs_images_failure(self):
        """Test require_cs_images validator with missing coordinate system"""
        with self.assertRaises(ValidationError) as context:
            ImagingConfig(
                device_name="ImagingDevice",
                channels=[self.channel1],
                images=[
                    ImageSPIM(
                        channel_name="Channel1",
                        file_name="test_image.tiff",
                        image_to_acquisition_transform=[
                            Affine(affine_transform=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [0, 0, 0, 1]]),
                        ],
                        imaging_angle=45,
                        imaging_angle_unit=AngleUnit.DEG,
                    ),
                ],
                coordinate_system=None,
            )
        self.assertIn(
            "ImagingConfig.coordinate_system is required when ImagingConfig.images are ImageSPIM objects",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
