"""Utility methods to check compatibility"""

from typing import Optional

from aind_data_schema.core.acquisition import Acquisition
from aind_data_schema.core.instrument import Instrument


class InstrumentAcquisitionCompatibility:
    """Class of methods to check compatibility between instrument and acquisition"""

    def __init__(self, instrument: Instrument, acquisition: Acquisition) -> None:
        """Initiate InstrumentAcquisitionCompatibility class"""
        self.inst = instrument
        self.acquisition = acquisition

    def _compare_instrument_id(self) -> Optional[ValueError]:
        """Compares instrument_id"""
        if self.acquisition.instrument_id != self.inst.instrument_id:
            return ValueError(
                f"Instrument ID in acquisition {self.acquisition.instrument_id} "
                f"does not match the instrument's {self.inst.instrument_id}."
            )  # noqa: E501
        else:
            return None

    def _compare_stimulus_devices(self) -> Optional[ValueError]:
        """Compares stimulus device names"""
        acquisition_stimulus_devices = [
            stimulus_device_name
            for stimulus_epoch in getattr(self.acquisition, "stimulus_epochs", [])
            for stimulus_device_name in getattr(stimulus_epoch, "active_devices")
        ]
        instrument_component_names = self.inst.get_component_names()

        if any(device not in instrument_component_names for device in acquisition_stimulus_devices):
            return ValueError(
                f"Stimulus epoch device names in acquisition do not match stimulus device names in instrument."
                f"\nacquisition_stimulus_devices: {set(acquisition_stimulus_devices)} "
                f"\ninstrument_stimulus_devices: {set(instrument_component_names)}"
            )

    def run_compatibility_check(self) -> None:
        """Runs compatibility check.
        Creates a dictionary of fields and whether it matches in instrument and acquisition.
        """
        comparisons = [
            self._compare_instrument_id(),
            self._compare_stimulus_devices(),
        ]
        error_messages = [str(error) for error in comparisons if error]
        if error_messages:
            raise ValueError(error_messages)
        return None
