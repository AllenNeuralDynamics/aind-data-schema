"""Tests instrument acquisition compatibility check"""

import unittest

from aind_data_schema.utils.compatibility_check import InstrumentAcquisitionCompatibility
from examples.ephys_acquisition import acquisition as ephys_acquisition
from examples.ephys_instrument import inst as ephys_instrument
from examples.fip_ophys_instrument import instrument as ophys_instrument
from examples.ophys_acquisition import a as ophys_acquisition


class TestInstrumentAcquisitionCompatibility(unittest.TestCase):
    """Tests InstrumentAcquisitionCompatibility class"""

    def setUp(self):
        """Set up test data"""
        self.ephys_instrument = ephys_instrument.model_copy()
        self.ephys_acquisition = ephys_acquisition.model_copy()
        self.ophys_instrument = ophys_instrument.model_copy()
        self.ophys_acquisition = ophys_acquisition.model_copy()

    def test_check_examples_compatibility(self):
        """Tests that examples are compatible"""
        # check that ephys acquisition and instrument are synced
        example_ephys_check = InstrumentAcquisitionCompatibility(
            instrument=self.ephys_instrument, acquisition=self.ephys_acquisition
        )
        self.assertIsNone(example_ephys_check.run_compatibility_check())

        # check that ophys acquisition and instrument are synced
        example_ophys_check = InstrumentAcquisitionCompatibility(
            instrument=self.ophys_instrument, acquisition=self.ophys_acquisition
        ).run_compatibility_check()
        self.assertIsNone(example_ophys_check)

    def test_compare_instrument_id_error(self):
        """Tests that an error is raised when instrument ids do not match"""
        ophys_acquisition = self.ophys_acquisition.model_copy()
        ophys_acquisition.instrument_id = "wrong_id"
        with self.assertRaises(ValueError) as context:
            InstrumentAcquisitionCompatibility(
                instrument=self.ophys_instrument, acquisition=ophys_acquisition
            ).run_compatibility_check()
        self.assertIn(
            "Instrument ID in acquisition wrong_id does not match the instrument's",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
