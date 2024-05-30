"""Utility methods to check compatibility"""
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session
import json


class RigSessionCompatibility:
    """Class of methods to check compatibility between rig and session"""

    def __init__(self, rig_filepath, session_filepath):
        """Initiate class"""
        rig_file = json.loads(rig_filepath)
        session_file = json.loads(session_filepath)
        self.rig = Rig(**rig_file)
        self.session = Session(**session_file)

    def check_rig_id(self):
        """"""
        return self.session.rig_id == self.rig.rig_id

    def check_mouse_platform_name(self):
        """"""
        return self.session.mouse_platform_name == self.rig.mouse_platform.name

    def check_stream(self):
        """

        """
        data_streams = self.session.data_streams
        for daq in self.rig.daqs:

        for stream in data_streams:
            stream.daq_names



