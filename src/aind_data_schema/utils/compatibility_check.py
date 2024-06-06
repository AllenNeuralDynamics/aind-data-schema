"""Utility methods to check compatibility"""
from typing import Dict, Optional

from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session


class RigSessionCompatibility:
    """Class of methods to check compatibility between rig and session"""

    def __init__(self, rig: Rig, session: Session) -> None:
        """Initiate RigSessionCompatibility class"""
        self.rig = rig
        self.session = session

    def compare_rig_id(self) -> bool:
        """Compares rig_id"""
        return self.session.rig_id == self.rig.rig_id

    def compare_mouse_platform_name(self) -> bool:
        """Compares mouse_platform_name"""
        return self.session.mouse_platform_name == self.rig.mouse_platform.name

    def run_compatibility_check(self) -> Optional[Dict]:
        """Runs compatibility check.Creates a dictionary of fields and whether it matches in rig and session."""
        if self.compare_rig_id() is False:
            raise ValueError(f"Rig ID in session {self.session.rig_id} does not match the rig {self.rig.rig_id}.")
        else:
            comparison_data = {
                "rig_id": self.compare_rig_id(),
                "mouse_platform_name": self.compare_mouse_platform_name(),
            }
            return comparison_data
