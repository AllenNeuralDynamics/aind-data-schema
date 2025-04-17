""" test Device models"""

import unittest

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.organizations import Organization

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


if __name__ == "__main__":
    unittest.main()
