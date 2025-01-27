"""Utility methods to check compatibility"""

from typing import Optional

from aind_data_schema.components.devices import CameraAssembly, EphysAssembly
from aind_data_schema.core.instrument import RewardDelivery, Instrument
from aind_data_schema.core.session import Session


class InstrumentSessionCompatibility:
    """Class of methods to check compatibility between instrument and session"""

    def __init__(self, instrument: Instrument, session: Session) -> None:
        """Initiate InstrumentSessionCompatibility class"""
        self.inst = instrument
        self.session = session

    def _compare_instrument_id(self) -> Optional[ValueError]:
        """Compares instrument_id"""
        if self.session.instrument_id != self.inst.instrument_id:
            return ValueError(
                f"Instrument ID in session {self.session.instrument_id} does not match the instrument's {self.inst.instrument_id}."
            )
        else:
            return None

    def _compare_mouse_platform_name(self) -> Optional[ValueError]:
        """Compares mouse_platform_name"""
        if self.session.mouse_platform_name != self.inst.mouse_platform.name:
            return ValueError(
                f"Mouse platform name in session {self.session.mouse_platform_name} "
                f"does not match the instrument's {self.inst.mouse_platform.name}"
            )

    def _compare_daq_names(self) -> Optional[ValueError]:
        """Compares daq names"""
        session_daqs = [
            daq for stream in getattr(self.session, "data_streams", []) for daq in getattr(stream, "daq_names", [])
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]
        if not set(session_daqs).issubset(set(instrument_component_names)):
            return ValueError(
                f"daq names in session do not match daq names in inst. "
                f"session_daqs: {set(session_daqs)} instrument components: {set(instrument_component_names)}"
            )

    def _compare_camera_names(self) -> Optional[ValueError]:
        """Compares camera names"""
        session_cameras = [
            camera
            for stream in getattr(self.session, "data_streams", [])
            for camera in getattr(stream, "camera_names", [])
        ]
        instrument_camera_names = [
            comp.camera.name if isinstance(comp, CameraAssembly) else None
            for comp in getattr(self.inst, "components", [])
        ]

        if not set(session_cameras).issubset(set(instrument_camera_names)):
            return ValueError(
                f"camera names in session do not match camera names in inst. "
                f"session_cameras: {set(session_cameras)} instrument_cameras: {set(instrument_camera_names)}"
            )

    def _compare_light_sources(self) -> Optional[ValueError]:
        """Compares light sources"""
        session_light_sources = [
            light_source.name
            for stream in getattr(self.session, "data_streams", [])
            for light_source in getattr(stream, "light_sources", [])
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]
        if not set(session_light_sources).issubset(set(instrument_component_names)):
            return ValueError(
                f"light source names in session do not match light source names in inst. "
                f"session_light_sources: {set(session_light_sources)} "
                f"instrument_light_sources: {set(instrument_component_names)}"
            )

    def _compare_ephys_assemblies(self) -> Optional[ValueError]:
        """Compares ephys assemblies"""
        session_ephys_assemblies = [
            ephys_module.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for ephys_module in getattr(stream, "ephys_modules")
        ]
        instrument_component_names = [
            comp.name if isinstance(comp, EphysAssembly) else None for comp in getattr(self.inst, "components", [])
        ]

        if not set(session_ephys_assemblies).issubset(set(instrument_component_names)):
            return ValueError(
                f"ephys assembly names in session do not match ephys assembly names in inst. "
                f"session_ephys_assemblies: {set(session_ephys_assemblies)}"
                f" instrument_ephys_assemblies: {set(instrument_component_names)}"
            )

    def _compare_stick_microscopes(self) -> Optional[ValueError]:
        """Compares stick microscopes"""
        session_stick_microscopes = [
            stick_microscope.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for stick_microscope in getattr(stream, "stick_microscopes", [])
        ]
        instrument_camera_names = [
            comp.camera.name if isinstance(comp, CameraAssembly) else None
            for comp in getattr(self.inst, "components", [])
        ]

        if not set(session_stick_microscopes).issubset(set(instrument_camera_names)):
            return ValueError(
                f"stick microscope names in session do not match stick microscope names in inst. "
                f"session_stick_microscopes: {set(session_stick_microscopes)} "
                f"instrument_stick_microscopes: {set(instrument_camera_names)}"
            )

    def _compare_manipulator_modules(self) -> Optional[ValueError]:
        """Compares manipulator modules"""
        session_manipulator_modules = [
            manipulator_module.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for manipulator_module in getattr(stream, "manipulator_modules", [])
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]

        if not set(session_manipulator_modules).issubset(set(instrument_component_names)):
            return ValueError(
                f"manipulator module names in session do not match manipulator names (laser assemblies) in inst. "
                f"session_manipulators: {set(session_manipulator_modules)}"
                f" instrument_manipulators: {set(instrument_component_names)}"
            )

    def _compare_detectors(self) -> Optional[ValueError]:
        """Compares detectors"""
        session_detectors = [
            detector.name
            for stream in getattr(self.session, "data_streams", [])
            for detector in getattr(stream, "detectors", [])
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]

        if not set(session_detectors).issubset(set(instrument_component_names)):
            return ValueError(
                f"detector names in session do not match detector names in inst. "
                f"session_detectors: {set(session_detectors)} instrument_detectors: {set(instrument_component_names)}"
            )

    def _compare_patch_cords(self) -> Optional[ValueError]:
        """Compares patch cords of fiber connections"""
        session_patch_cords = [
            fiber_connection.patch_cord_name
            for stream in getattr(self.session, "data_streams", [])
            for fiber_connection in getattr(stream, "fiber_connections", [])
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]

        if not set(session_patch_cords).issubset(set(instrument_component_names)):
            return ValueError(
                f"patch cord names in session do not match patch cord names in inst. "
                f"session_patch_cords: {set(session_patch_cords)} instrument_patch_cords: {set(instrument_component_names)}"
            )

    def _compare_fiber_modules(self) -> Optional[ValueError]:
        """Compares fiber assembly names"""
        session_fiber_modules = [
            fiber_module.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for fiber_module in getattr(stream, "fiber_modules", [])
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]

        if not set(session_fiber_modules).issubset(set(instrument_component_names)):
            return ValueError(
                f"fiber module names in session do not match fiber assembly names in inst. "
                f"session_fiber_modules: {set(session_fiber_modules)} "
                f"instrument_fiber_assemblies: {set(instrument_component_names)}"
            )

    def _compare_stimulus_devices(self) -> Optional[ValueError]:
        """Compares stimulus device names"""
        session_stimulus_devices = [
            stimulus_device_name
            for stimulus_epoch in getattr(self.session, "stimulus_epochs", [])
            for stimulus_device_name in getattr(stimulus_epoch, "stimulus_device_names")
        ]
        instrument_component_names = [getattr(comp, "name", None) for comp in getattr(self.inst, "components", [])]

        if not set(session_stimulus_devices).issubset(set(instrument_component_names)):
            return ValueError(
                f"stimulus device names in session do not match stimulus device names in inst. "
                f"session_stimulus_devices: {set(session_stimulus_devices)} "
                f"instrument_stimulus_devices: {set(instrument_component_names)}"
            )

    def run_compatibility_check(self) -> None:
        """Runs compatibility check.Creates a dictionary of fields and whether it matches in instrument and session."""
        comparisons = [
            self._compare_instrument_id(),
            self._compare_mouse_platform_name(),
            self._compare_daq_names(),
            self._compare_camera_names(),
            self._compare_light_sources(),
            self._compare_ephys_assemblies(),
            self._compare_manipulator_modules(),
            self._compare_stick_microscopes(),
            self._compare_detectors(),
            self._compare_fiber_modules(),
            self._compare_stimulus_devices(),
            self._compare_patch_cords(),
        ]
        error_messages = [str(error) for error in comparisons if error]
        if error_messages:
            raise ValueError(error_messages)
        return None
