""" Unit tests for compatibility_check."""

import unittest
from unittest.mock import MagicMock

from aind_data_schema.components.devices import Device
from aind_data_schema.core.acquisition import Acquisition, StimulusEpoch
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.utils.compatibility_check import InstrumentAcquisitionCompatibility


class TestInstrumentAcquisitionCompatibility(unittest.TestCase):
    """Unit tests for InstrumentAcquisitionCompatibility class."""

    def setUp(self):
        """Set up mock instrument and acquisition objects for testing."""
        self.mock_instrument = MagicMock(spec=Instrument)
        self.mock_acquisition = MagicMock(spec=Acquisition)

        # Mock instrument attributes
        self.mock_instrument.instrument_id = "instrument_1"

        device0 = MagicMock(spec=Device)
        device0.name = "component_1"
        device1 = MagicMock(spec=Device)
        device1.name = "component_2"

        self.mock_instrument.components = [device0, device1]
        # Mock the get_component_names method to return the expected component names
        self.mock_instrument.get_component_names.return_value = ["component_1", "component_2"]

        # Mock acquisition attributes
        self.mock_acquisition.instrument_id = "instrument_1"
        self.mock_acquisition.data_streams = [MagicMock(active_devices=["component_1"])]
        self.mock_acquisition.stimulus_epochs = [MagicMock(active_devices=["component_2"])]

    def test_compare_instrument_id_success(self):
        """Test that instrument IDs match."""
        checker = InstrumentAcquisitionCompatibility(self.mock_instrument, self.mock_acquisition)
        self.assertIsNone(checker._compare_instrument_id())

    def test_compare_instrument_id_failure(self):
        """Test that instrument IDs mismatch raises ValueError."""
        self.mock_acquisition.instrument_id = "instrument_2"
        checker = InstrumentAcquisitionCompatibility(self.mock_instrument, self.mock_acquisition)
        error = checker._compare_instrument_id()
        self.assertIsInstance(error, ValueError)
        self.assertIn("Instrument ID in acquisition", str(error))

    def test_compare_stimulus_devices_success(self):
        """Test that stimulus devices in acquisition match instrument components."""
        checker = InstrumentAcquisitionCompatibility(self.mock_instrument, self.mock_acquisition)
        self.assertIsNone(checker._compare_stimulus_devices())

    def test_compare_stimulus_devices_failure(self):
        """Test that mismatched stimulus devices raise ValueError."""
        epoch = MagicMock(spec=StimulusEpoch)
        epoch.active_devices = ["unknown_device"]
        self.mock_acquisition.stimulus_epochs = [epoch]
        checker = InstrumentAcquisitionCompatibility(self.mock_instrument, self.mock_acquisition)
        error = checker._compare_stimulus_devices()
        self.assertIsInstance(error, ValueError)
        self.assertIn("Stimulus epoch device names in acquisition", str(error))

    def test_run_compatibility_check_success(self):
        """Test that compatibility check passes when all comparisons succeed."""
        checker = InstrumentAcquisitionCompatibility(self.mock_instrument, self.mock_acquisition)
        self.assertIsNone(checker.run_compatibility_check())

    def test_run_compatibility_check_failure(self):
        """Test that compatibility check raises ValueError when comparisons fail."""
        self.mock_acquisition.instrument_id = "instrument_2"
        checker = InstrumentAcquisitionCompatibility(self.mock_instrument, self.mock_acquisition)
        with self.assertRaises(ValueError) as context:
            checker.run_compatibility_check()
        self.assertIn("Instrument ID in acquisition", str(context.exception))


if __name__ == "__main__":
    unittest.main()
