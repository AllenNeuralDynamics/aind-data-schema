""" test Device models"""

import unittest

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.organizations import Organization
from aind_data_schema.components.coordinates import CoordinateSystem, Scale
from aind_data_schema.components.devices import PositionedDevice
from aind_data_schema_models.coordinates import AnatomicalRelative

from aind_data_schema.components.devices import (
    Device,
    AdditionalImagingDevice,
    DataInterface,
    Detector,
    DetectorType,
    HarpDevice,
    ImagingDeviceType,
    ImmersionMedium,
    Objective,
)
from aind_data_schema.components.coordinates import CoordinateSystemLibrary, Translation


class DeviceTests(unittest.TestCase):
    """tests device schemas"""

    def test_other_validators(self):
        """tests validators which require notes when an instance of 'other' is used"""

        with self.assertRaises(ValueError) as e1:
            Device(name="test_device", manufacturer=Organization.OTHER, notes="")

        self.assertIn("Device.notes cannot be empty if manufacturer is 'other'", str(e1.exception))

        with self.assertRaises(ValueError) as e2:
            Detector(
                name="test_detector",
                manufacturer=Organization.HAMAMATSU,
                detector_type=DetectorType.OTHER,
                immersion=ImmersionMedium.OTHER,
                data_interface=DataInterface.OTHER,
            )

        self.assertIn("Value error, Notes cannot be empty", str(e2.exception))
        self.assertIn("'immersion', 'detector_type', 'data_interface'", str(e2.exception))

        with self.assertRaises(ValueError) as e3:
            HarpDevice(
                name="test_harp",
                harp_device_type=HarpDeviceType.BEHAVIOR,
                data_interface=DataInterface.OTHER,
                is_clock_generator=False,
            )

        self.assertIn("Value error, Notes cannot be empty", str(e3.exception))
        self.assertIn("data_interface", str(e3.exception))

        HarpDevice(
            name="test_harp",
            harp_device_type=HarpDeviceType.BEHAVIOR,
            data_interface=DataInterface.USB,
            is_clock_generator=False,
        )

        with self.assertRaises(ValueError) as e4:
            Objective(name="test_objective", numerical_aperture=0.5, magnification=10, immersion=ImmersionMedium.OTHER)

        self.assertIn("Value error, Notes cannot be empty if immersion is Other", str(e4.exception))

    def test_additional_imaging_device(self):
        """tests the additional imaging device validator"""
        with self.assertRaises(ValueError) as e5:
            AdditionalImagingDevice(name="test_additional_imaging", imaging_device_type=ImagingDeviceType.OTHER)

        self.assertIn("Notes cannot be empty if imaging_device_type", str(e5.exception))

        valid = AdditionalImagingDevice(
            name="test_additional_imaging",
            imaging_device_type=ImagingDeviceType.OTHER,
            notes="test notes",
        )
        self.assertEqual(valid.name, "test_additional_imaging")

    def test_position_device(self):
        """Test that the PositionDevice validator gets raised properly"""

        # Test with both transform and coordinate_system set
        valid_positioned = PositionedDevice(
            relative_position=[AnatomicalRelative.SUPERIOR],
            transform=[
                Translation(
                    translation=[1, 1, 1],
                )
            ],
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
        )
        self.assertIsNotNone(valid_positioned.transform)
        self.assertIsNotNone(valid_positioned.coordinate_system)

        # Test with both transform and coordinate_system unset
        valid_positioned_unset = PositionedDevice(
            relative_position=[AnatomicalRelative.SUPERIOR],
        )
        self.assertIsNone(valid_positioned_unset.transform)
        self.assertIsNone(valid_positioned_unset.coordinate_system)

        # Test with transform set but coordinate_system unset
        with self.assertRaises(ValueError) as e1:
            PositionedDevice(
                relative_position=[AnatomicalRelative.SUPERIOR],
                transform=[
                    Translation(
                        translation=[1, 1, 1],
                    )
                ]
            )
        self.assertIn("PositionDevice.transform and PositionedDevice.coordinate_system must either both be set or both be unset", str(e1.exception))

        # Test with coordinate_system set but transform unset
        with self.assertRaises(ValueError) as e2:
            PositionedDevice(
                relative_position=[AnatomicalRelative.SUPERIOR],
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            )
        self.assertIn("PositionDevice.transform and PositionedDevice.coordinate_system must either both be set or both be unset", str(e2.exception))


if __name__ == "__main__":
    unittest.main()
