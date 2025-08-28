""" test Device models"""

import unittest
import warnings

from aind_data_schema_models.coordinates import AnatomicalRelative
from aind_data_schema_models.devices import DaqChannelType
from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.organizations import Organization

from aind_data_schema.components.coordinates import CoordinateSystemLibrary, Translation
from aind_data_schema.components.devices import Filter, FilterType
from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    DAQChannel,
    DataInterface,
    Detector,
    DetectorType,
    Device,
    DevicePosition,
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

    def test_position_device(self):
        """Test that the DevicePosition validator gets raised properly"""

        # Test with both transform and coordinate_system set
        valid_positioned = DevicePosition(
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
        valid_positioned_unset = DevicePosition(
            relative_position=[AnatomicalRelative.SUPERIOR],
        )
        self.assertIsNone(valid_positioned_unset.transform)
        self.assertIsNone(valid_positioned_unset.coordinate_system)

        # Test with transform set but coordinate_system unset
        with self.assertRaises(ValueError) as e1:
            DevicePosition(
                relative_position=[AnatomicalRelative.SUPERIOR],
                transform=[
                    Translation(
                        translation=[1, 1, 1],
                    )
                ],
            )
        self.assertIn(
            "DevicePosition.transform and DevicePosition.coordinate_system must either both be set or both be unset",
            str(e1.exception),
        )

        # Test with coordinate_system set but transform unset
        with self.assertRaises(ValueError) as e2:
            DevicePosition(
                relative_position=[AnatomicalRelative.SUPERIOR],
                coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            )
        self.assertIn(
            "DevicePosition.transform and DevicePosition.coordinate_system must either both be set or both be unset",
            str(e2.exception),
        )


class FilterTests(unittest.TestCase):
    """tests filter schemas"""

    def test_filter(self):
        """tests the filter validator"""

        # Test valid single center wavelength
        valid_filter_single = Filter(
            name="test_filter",
            filter_type=FilterType.BANDPASS,
            manufacturer=Organization.CHROMA,
            center_wavelength=500,
        )
        self.assertEqual(valid_filter_single.center_wavelength, 500)

        # Test valid multiple center wavelengths
        valid_filter_multi = Filter(
            name="test_filter_multi",
            filter_type=FilterType.MULTI_NOTCH,
            manufacturer=Organization.CHROMA,
            center_wavelength=[450, 550, 650],
        )
        self.assertEqual(valid_filter_multi.center_wavelength, [450, 550, 650])

        # Test error for multi-band filter with single center wavelength
        with self.assertRaises(ValueError) as e1:
            Filter(
                name="test_filter_multi_single",
                filter_type=FilterType.MULTIBAND,
                manufacturer=Organization.CHROMA,
                center_wavelength=500,
            )
        self.assertIn("center_wavelength must be a list of wavelengths", str(e1.exception))

        # Test error for single-band filter with multiple center wavelengths
        with self.assertRaises(ValueError) as e2:
            Filter(
                name="test_filter_single_multi",
                filter_type=FilterType.BANDPASS,
                manufacturer=Organization.CHROMA,
                center_wavelength=[450, 550],
            )
        self.assertIn("center_wavelength must be a single wavelength", str(e2.exception))

        # Test with MULTI_NOTCH filter type and single wavelength (should fail)
        with self.assertRaises(ValueError) as e3:
            Filter(
                name="test_filter_notch_single",
                filter_type=FilterType.MULTI_NOTCH,
                manufacturer=Organization.CHROMA,
                center_wavelength=500,
            )
        self.assertIn("center_wavelength must be a list of wavelengths", str(e3.exception))


class DAQChannelTests(unittest.TestCase):
    """tests DAQChannel schemas"""

    def test_deprecated_channel_index(self):
        """Test that using channel_index raises a deprecation warning"""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            DAQChannel(channel_name="test_channel", channel_type=DaqChannelType.DI, channel_index=1)

            # Check that a deprecation warning was raised
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("DAQChannel.channel_index is deprecated", str(w[0].message))
            self.assertIn("Use DAQChannel.port instead", str(w[0].message))


if __name__ == "__main__":
    unittest.main()
