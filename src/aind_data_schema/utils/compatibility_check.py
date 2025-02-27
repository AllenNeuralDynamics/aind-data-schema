"""Utility methods to check compatibility"""

from typing import Optional

from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.acquisition import Acquisition


class InstrumentAcquisitionCompatibility:
    """Class of methods to check compatibility between instrument and acquisition"""

    def __init__(self, instrument: Instrument, acquisition: Acquisition) -> None:
        """Initiate InstrumentSessionCompatibility class"""
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

    def _compare_stream_devices(self) -> Optional[ValueError]:
        """Compare acquisition active devices against instrument devices"""

        active_devices = []
        for stream in getattr(self.acquisition, "data_streams", []):
            active_devices.extend(getattr(stream, "active_devices", []))

        component_names = [comp.name for comp in self.inst.components if hasattr(comp, "name")]

        for device in active_devices:
            if device not in component_names:
                return ValueError(f"Active device {device} in acquisition does not match any device in the instrument.")

    # def _compare_mouse_platform_name(self) -> Optional[ValueError]:
    #     """Compares mouse_platform_name"""

    #     component_names = [comp.name for comp in self.inst.components if hasattr(comp, "name")]

    #     if self.acquisition.mouse_platform_name not in component_names:
    #         return ValueError(
    #             f"Mouse platform {self.acquisition.mouse_platform_name} can't be found in the instrument's components"
    #         )

    def _compare_stimulus_devices(self) -> Optional[ValueError]:
        """Compares stimulus device names"""
        acquisition_stimulus_devices = [
            stimulus_device_name
            for stimulus_epoch in getattr(self.acquisition, "stimulus_epochs", [])
            for stimulus_device_name in getattr(stimulus_epoch, "active_devices")
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]

        if not set(acquisition_stimulus_devices).issubset(set(instrument_component_names)):
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
            self._compare_stream_devices(),
            self._compare_stimulus_devices(),
        ]
        error_messages = [str(error) for error in comparisons if error]
        if error_messages:
            raise ValueError(error_messages)
        return None
