"""Test for configs"""

import unittest

from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.units import PowerUnit, SizeUnit
from pydantic import ValidationError

from aind_data_schema.components.configs import CoupledPlane, ImagingConfig, PlanarImage, Plane
from aind_data_schema.components.coordinates import Scale, Translation
from examples.bergamo_ophys_acquisition import a as bergamo_acquisition
from examples.exaspim_acquisition import acq as exaspim_acquisition


class ImagingConfigTest(unittest.TestCase):
    """Test for ImagingConfig"""

    def test_image_channels_invalid(self):
        """Test ValidationError raised if channels are missing"""

        acq = bergamo_acquisition.model_copy()

        imaging_config = acq.data_streams[0].configurations[0]
        imaging_config.channels = []

        with self.assertRaises(ValueError) as e:
            ImagingConfig.model_validate_json(imaging_config.model_dump_json())

        self.assertIn("must be defined in the ImagingConfig.channels", str(e.exception))

        acq2 = exaspim_acquisition.model_copy()
        imaging_config2 = acq2.data_streams[0].configurations[0]
        imaging_config2.channels = []
        with self.assertRaises(ValueError) as e:
            ImagingConfig.model_validate_json(imaging_config2.model_dump_json())
        self.assertIn("must be defined in the ImagingConfig.channels", str(e.exception))


class TestPlanarImage(unittest.TestCase):
    """Test for PlanarImage class"""

    def setUp(self):
        """Set up common values for tests"""
        self.channel_name = "test_channel"
        self.dimensions = Scale(scale=[512, 512])
        self.dimensions_unit = SizeUnit.PX

        self.transform = [Translation(translation=[0, 0])]

        self.plane = Plane(
            depth=150, depth_unit=SizeUnit.UM, power=5.0, power_unit=PowerUnit.MW, targeted_structure=CCFv3.VISP
        )

        self.coupled_plane = CoupledPlane(
            plane_index=0,
            power=5.0,
            power_unit=PowerUnit.MW,
            targeted_structure=CCFv3.VISP,
            depth=100.0,
            depth_unit=SizeUnit.UM,
            coupled_plane_index=1,
            power_ratio=0.5,
        )

    def test_planar_image_with_single_plane(self):
        """Test PlanarImage with a single Plane object"""
        planar_image = PlanarImage(
            channel_name=self.channel_name,
            dimensions=self.dimensions,
            dimensions_unit=self.dimensions_unit,
            image_to_acquisition_transform=self.transform,
            planes=[self.plane],
        )
        self.assertEqual(len(planar_image.planes), 1)
        self.assertIsInstance(planar_image.planes[0], Plane)

    def test_planar_image_with_multiple_planes_raises_error(self):
        """Test PlanarImage with multiple Plane objects - should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            PlanarImage(
                channel_name=self.channel_name,
                dimensions=self.dimensions,
                dimensions_unit=self.dimensions_unit,
                image_to_acquisition_transform=self.transform,
                planes=[self.plane, self.plane],
            )

        self.assertIn(
            "For single-plane optical physiology only a single Plane should be in PlanarImage.planes",
            str(context.exception),
        )

    def test_planar_image_with_multiple_coupled_planes(self):
        """Test PlanarImage with multiple CoupledPlane objects"""
        planar_image = PlanarImage(
            channel_name=self.channel_name,
            dimensions=self.dimensions,
            dimensions_unit=self.dimensions_unit,
            image_to_acquisition_transform=self.transform,
            planes=[self.coupled_plane, self.coupled_plane],
        )
        self.assertEqual(len(planar_image.planes), 2)
        self.assertIsInstance(planar_image.planes[0], CoupledPlane)
        self.assertIsInstance(planar_image.planes[1], CoupledPlane)

    def test_planar_image_with_mixed_plane_types(self):
        """Test PlanarImage with mixed Plane and CoupledPlane objects - should raise ValueError"""
        with self.assertRaises(ValidationError) as context:
            PlanarImage(
                channel_name=self.channel_name,
                dimensions=self.dimensions,
                dimensions_unit=self.dimensions_unit,
                image_to_acquisition_transform=self.transform,
                planes=[self.plane, self.coupled_plane],
            )

        self.assertIn(
            "For single-plane optical physiology only a single Plane should be in PlanarImage.planes",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
