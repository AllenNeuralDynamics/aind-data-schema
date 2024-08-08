"""Utility methods to check compatibility"""

from typing import Optional

from aind_data_schema.core.rig import RewardDelivery, Rig
from aind_data_schema.core.session import Session


class RigSessionCompatibility:
    """Class of methods to check compatibility between rig and session"""

    def __init__(self, rig: Rig, session: Session) -> None:
        """Initiate RigSessionCompatibility class"""
        self.rig = rig
        self.session = session

    def _compare_rig_id(self) -> Optional[ValueError]:
        """Compares rig_id"""
        if self.session.rig_id != self.rig.rig_id:
            return ValueError(f"Rig ID in session {self.session.rig_id} does not match the rig's {self.rig.rig_id}.")
        else:
            return None

    def _compare_mouse_platform_name(self) -> Optional[ValueError]:
        """Compares mouse_platform_name"""
        if self.session.mouse_platform_name != self.rig.mouse_platform.name:
            return ValueError(
                f"Mouse platform name in session {self.session.mouse_platform_name} "
                f"does not match the rig's {self.rig.mouse_platform.name}"
            )

    def _compare_daq_names(self) -> Optional[ValueError]:
        """Compares daq names"""
        session_daqs = [
            daq for stream in getattr(self.session, "data_streams", []) for daq in getattr(stream, "daq_names", [])
        ]
        rig_daqs = [getattr(daq, "name", None) for daq in getattr(self.rig, "daqs", [])]
        if not set(session_daqs).issubset(set(rig_daqs)):
            return ValueError(
                f"daq names in session do not match daq names in rig. "
                f"session_daqs: {set(session_daqs)} rig_daqs: {set(rig_daqs)}"
            )

    def _compare_camera_names(self) -> Optional[ValueError]:
        """Compares camera names"""
        session_cameras = [
            camera
            for stream in getattr(self.session, "data_streams", [])
            for camera in getattr(stream, "camera_names", [])
        ]
        rig_cameras = [
            name
            for camera_device in getattr(self.rig, "cameras", [])
            for name in (camera_device.camera.name, camera_device.name)
        ]
        if not set(session_cameras).issubset(set(rig_cameras)):
            return ValueError(
                f"camera names in session do not match camera names in rig. "
                f"session_cameras: {set(session_cameras)} rig_cameras: {set(rig_cameras)}"
            )

    def _compare_light_sources(self) -> Optional[ValueError]:
        """Compares light sources"""
        session_light_sources = [
            light_source.name
            for stream in getattr(self.session, "data_streams", [])
            for light_source in getattr(stream, "light_sources", [])
        ]
        rig_light_sources = [
            getattr(light_source, "name", None) for light_source in getattr(self.rig, "light_sources", [])
        ]
        if not set(session_light_sources).issubset(set(rig_light_sources)):
            return ValueError(
                f"light source names in session do not match light source names in rig. "
                f"session_light_sources: {set(session_light_sources)} rig_light_sources: {set(rig_light_sources)}"
            )

    def _compare_ephys_assemblies(self) -> Optional[ValueError]:
        """Compares ephys assemblies"""
        session_ephys_assemblies = [
            ephys_module.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for ephys_module in getattr(stream, "ephys_modules")
        ]
        rig_ephys_assemblies = [ephys_assembly.name for ephys_assembly in getattr(self.rig, "ephys_assemblies", [])]
        if not set(session_ephys_assemblies).issubset(set(rig_ephys_assemblies)):
            return ValueError(
                f"ephys assembly names in session do not match ephys assembly names in rig. "
                f"session_ephys_assemblies: {set(session_ephys_assemblies)}"
                f" rig_ephys_assemblies: {set(rig_ephys_assemblies)}"
            )

    def _compare_stick_microscopes(self) -> Optional[ValueError]:
        """Compares stick microscopes"""
        session_stick_microscopes = [
            stick_microscope.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for stick_microscope in getattr(stream, "stick_microscopes", [])
        ]
        rig_stick_microscopes = [
            name
            for camera_device in getattr(self.rig, "stick_microscopes", [])
            for name in (camera_device.camera.name, camera_device.name)
        ]
        if not set(session_stick_microscopes).issubset(set(rig_stick_microscopes)):
            return ValueError(
                f"stick microscope names in session do not match stick microscope names in rig. "
                f"session_stick_microscopes: {set(session_stick_microscopes)} "
                f"rig_stick_microscopes: {set(rig_stick_microscopes)}"
            )

    def _compare_manipulator_modules(self) -> Optional[ValueError]:
        """Compares manipulator modules"""
        session_manipulator_modules = [
            manipulator_module.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for manipulator_module in getattr(stream, "manipulator_modules", [])
        ]
        rig_manipulator_modules = [laser_assembly.name for laser_assembly in getattr(self.rig, "laser_assemblies", [])]
        if not set(session_manipulator_modules).issubset(set(rig_manipulator_modules)):
            return ValueError(
                f"manipulator module names in session do not match manipulator names (laser assemblies) in rig. "
                f"session_manipulators: {set(session_manipulator_modules)}"
                f" rig_manipulators: {set(rig_manipulator_modules)}"
            )

    def _compare_detectors(self) -> Optional[ValueError]:
        """Compares detectors"""
        session_detectors = [
            detector.name
            for stream in getattr(self.session, "data_streams", [])
            for detector in getattr(stream, "detectors", [])
        ]
        rig_detectors = [detector.name for detector in getattr(self.rig, "detectors", [])]
        if not set(session_detectors).issubset(set(rig_detectors)):
            return ValueError(
                f"detector names in session do not match detector names in rig. "
                f"session_detectors: {set(session_detectors)} rig_detectors: {set(rig_detectors)}"
            )

    def _compare_patch_cords(self) -> Optional[ValueError]:
        """Compares patch cords of fiber connections"""
        session_patch_cords = [
            fiber_connection.patch_cord_name
            for stream in getattr(self.session, "data_streams", [])
            for fiber_connection in getattr(stream, "fiber_connections", [])
        ]
        rig_patch_cords = [patch_cord.name for patch_cord in getattr(self.rig, "patch_cords", [])]
        if not set(session_patch_cords).issubset(set(rig_patch_cords)):
            return ValueError(
                f"patch cord names in session do not match patch cord names in rig. "
                f"session_patch_cords: {set(session_patch_cords)} rig_patch_cords: {set(rig_patch_cords)}"
            )

    def _compare_fiber_modules(self) -> Optional[ValueError]:
        """Compares fiber assembly names"""
        session_fiber_modules = [
            fiber_module.assembly_name
            for stream in getattr(self.session, "data_streams", [])
            for fiber_module in getattr(stream, "fiber_modules", [])
        ]
        rig_fiber_modules = [fiber_assembly.name for fiber_assembly in getattr(self.rig, "fiber_assemblies", [])]
        if not set(session_fiber_modules).issubset(set(rig_fiber_modules)):
            return ValueError(
                f"fiber module names in session do not match fiber assembly names in rig. "
                f"session_fiber_modules: {set(session_fiber_modules)} rig_fiber_assemblies: {set(rig_fiber_modules)}"
            )

    def _compare_stimulus_devices(self) -> Optional[ValueError]:
        """Compares stimulus device names"""
        session_stimulus_devices = [
            stimulus_device_name
            for stimulus_epoch in getattr(self.session, "stimulus_epochs", [])
            for stimulus_device_name in getattr(stimulus_epoch, "stimulus_device_names")
        ]
        rig_stimulus_devices = [
            stimulus_device.name
            for stimulus_device in getattr(self.rig, "stimulus_devices", [])
            if not isinstance(stimulus_device, RewardDelivery)
        ] + [
            reward_spout.name
            for stimulus_device in getattr(self.rig, "stimulus_devices", [])
            if isinstance(stimulus_device, RewardDelivery)
            for reward_spout in getattr(stimulus_device, "reward_spouts", [])
        ]
        if not set(session_stimulus_devices).issubset(set(rig_stimulus_devices)):
            return ValueError(
                f"stimulus device names in session do not match stimulus device names in rig. "
                f"session_stimulus_devices: {set(session_stimulus_devices)} "
                f"rig_stimulus_devices: {set(rig_stimulus_devices)}"
            )

    def run_compatibility_check(self) -> None:
        """Runs compatibility check.Creates a dictionary of fields and whether it matches in rig and session."""
        comparisons = [
            self._compare_rig_id(),
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
