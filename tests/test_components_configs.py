"""Test for configs"""

import unittest


from examples.bergamo_ophys_acquisition import a as bergamo_acquisition
from aind_data_schema.components.configs import ImagingConfig


class ImagingConfigTest(unittest.TestCase):
    """Test for ImagingConfig"""

    def test_image_channels_invalid(self):
        """ Test ValidationError raised if channels are missing"""

        acq = bergamo_acquisition.model_copy()

        imaging_config = acq.data_streams[0].configurations[0]
        imaging_config.channels = []

        with self.assertRaises(ValueError) as e:
            ImagingConfig.model_validate_json(imaging_config.model_dump_json())

        self.assertIn("must be defined in the ImagingConfig.channels", str(e.exception))


if __name__ == "__main__":
    unittest.main()
