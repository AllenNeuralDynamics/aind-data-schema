""" test Device models"""

import re
import unittest

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.organizations import Organization
from pydantic import __version__ as pyd_version

from aind_data_schema.components.devices import (
    AdditionalImagingDevice,
    DataInterface,
    Detector,
    DetectorType,
    Device,
    HarpDevice,
    ImagingDeviceType,
    ImmersionMedium,
    Objective,
    RewardSpout,
    SpoutSide,
)

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


class DeviceTests(unittest.TestCase):
    """tests device schemas"""

    def test_other_validators(self):
        """tests validators which require notes when an instance of 'other' is used"""

        with self.assertRaises(ValueError) as e1:
            RewardSpout(
                name="test_reward_spout",
                spout_diameter=0.5,
                solenoid_valve=Device(
                    device_type="solenoid",
                    name="test_solenoid",
                ),
                lick_sensor=Device(
                    device_type="Lick sensor",
                    name="Sensor_test",
                ),
                side=SpoutSide.OTHER,
            )

        expected_e1 = (
            "1 validation error for RewardSpout\n"
            "  Value error, Notes cannot be empty if spout side is Other."
            " Describe the spout side in the notes field."
            " [type=value_error, input_value={'name': 'test_reward_spo...outSide.OTHER: 'Other'>}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )

        self.assertEqual(repr(e1.exception), expected_e1)

        with self.assertRaises(ValueError) as e2:
            Detector(
                name="test_detector",
                manufacturer=Organization.HAMAMATSU,
                detector_type=DetectorType.OTHER,
                immersion=ImmersionMedium.OTHER,
                data_interface=DataInterface.OTHER,
            )

        expected_e2 = (
            "1 validation error for Detector\n"
            "  Value error, Notes cannot be empty while any of the following fields"
            " are set to 'other': ['immersion', 'detector_type', 'data_interface']"
            " [type=value_error, input_value={'name': 'test_detector',...terface.OTHER: 'Other'>}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )

        self.assertEqual(repr(e2.exception), expected_e2)

        with self.assertRaises(ValueError) as e3:
            HarpDevice(
                name="test_harp",
                computer_name="test_harp_computer",
                harp_device_type=HarpDeviceType.BEHAVIOR,
                data_interface=DataInterface.OTHER,
                is_clock_generator=False,
            )

        expected_e3 = (
            "1 validation error for HarpDevice\n"
            "data_interface\n"
            "  Value error, Notes cannot be empty if data_interface is Other."
            " Describe the data interface in the notes field."
            " [type=value_error, input_value=<DataInterface.OTHER: 'Other'>, input_type=DataInterface]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )

        self.assertEqual(repr(e3.exception), expected_e3)

        HarpDevice(
            name="test_harp",
            computer_name="test_harp_computer",
            harp_device_type=HarpDeviceType.BEHAVIOR,
            data_interface=DataInterface.USB,
            is_clock_generator=False,
        )

        with self.assertRaises(ValueError) as e4:
            Objective(name="test_objective", numerical_aperture=0.5, magnification=10, immersion=ImmersionMedium.OTHER)

        expected_e4 = (
            "1 validation error for Objective\n"
            "immersion\n"
            "  Value error, Notes cannot be empty if immersion is Other. Describe the immersion in the notes field."
            " [type=value_error, input_value=<ImmersionMedium.OTHER: 'other'>, input_type=ImmersionMedium]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )

        self.assertEqual(repr(e4.exception), expected_e4)

        with self.assertRaises(ValueError) as e5:
            AdditionalImagingDevice(name="test_additional_imaging", imaging_device_type=ImagingDeviceType.OTHER)

        expected_e5 = (
            "1 validation error for AdditionalImagingDevice\n"
            "imaging_device_type\n"
            "  Value error, Notes cannot be empty if imaging_device_type is Other. "
            "Describe the imaging device type in the notes field."
            " [type=value_error, input_value=<ImagingDeviceType.OTHER: 'Other'>, input_type=ImagingDeviceType]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/value_error"
        )

        self.assertEqual(repr(e5.exception), expected_e5)
