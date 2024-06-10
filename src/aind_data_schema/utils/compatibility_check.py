"""Utility methods to check compatibility"""
from typing import Optional

from aind_data_schema.core.rig import Rig
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

    def run_compatibility_check(self) -> None:
        """Runs compatibility check.Creates a dictionary of fields and whether it matches in rig and session."""
        comparisons = [self._compare_rig_id(), self._compare_mouse_platform_name()]
        error_messages = [str(error) for error in comparisons if error]
        if error_messages:
            raise ValueError(error_messages)
        return None
