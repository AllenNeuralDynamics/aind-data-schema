"""Tests instrument acquisition compatibility check"""

import json
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit, SizeUnit, PowerUnit

from aind_data_schema.components.acquisition_configs import Channel
import aind_data_schema.components.devices as d
from aind_data_schema.components.identifiers import Person
from aind_data_schema.components.devices import (
    Camera,
    CameraAssembly,
    CameraTarget,
    DAQChannel,
    Device,
    Disc,
    EphysAssembly,
    EphysProbe,
    Filter,
    HarpDevice,
    Laser,
    LaserAssembly,
    Lens,
    Manipulator,
    NeuropixelsBasestation,
    FiberPatchCord,
    ProbePort,
    Computer,
)
from aind_data_schema.components.measurements import Calibration
from aind_data_schema.core.instrument import Instrument, Connection, ConnectionData, ConnectionDirection
from aind_data_schema.core.acquisition import (
    Acquisition,
    StimulusEpoch,
    DataStream,
    AcquisitionSubjectDetails,
)
from aind_data_schema.components.acquisition_configs import (
    DetectorConfig,
    DomeModule,
    PatchCordConfig,
    FiberAssemblyConfig,
    LaserConfig,
    ManipulatorConfig,
    StimulusModality,
)
from aind_data_schema.components.stimulus import VisualStimulation
from aind_data_schema.utils.compatibility_check import InstrumentAcquisitionCompatibility
from aind_data_schema_models.brain_atlas import CCFStructure
from aind_data_schema.components.identifiers import Code, Software
from aind_data_schema.components.coordinates import (
    Coordinate,
    CoordinateSystemLibrary,
)
from aind_data_schema_models.coordinates import AnatomicalRelative

from examples.ephys_instrument import inst as ephys_instrument
from examples.ephys_acquisition import acquisition as ephys_acquisition
from examples.ophys_acquisition import a as ophys_acquisition
from examples.fip_ophys_instrument import instrument as ophys_instrument


class TestInstrumentAcquisitionCompatibility(unittest.TestCase):
    """Tests InstrumentAcquisitionCompatibility class"""

    def setUp(self):
        """Set up test data"""
        self.ephys_instrument = ephys_instrument.model_copy()
        self.ephys_acquisition = ephys_acquisition.model_copy()
        self.ophys_instrument = ophys_instrument.model_copy()
        self.ophys_acquisition = ophys_acquisition.model_copy()

    def test_run_compatibility_check(self):
        """Tests compatibility check"""

        with self.assertRaises(ValueError):
            InstrumentAcquisitionCompatibility(
                instrument=self.ophys_instrument, acquisition=self.ophys_acquisition
            ).run_compatibility_check()

    def test_check_examples_compatibility(self):
        """Tests that examples are compatible"""
        # check that ephys acquisition and instrument are synced
        example_ephys_check = InstrumentAcquisitionCompatibility(
            instrument=self.ephys_instrument, acquisition=self.ephys_acquisition
        )
        self.assertIsNone(example_ephys_check.run_compatibility_check())

    def test_compare_instrument_id_error(self):
        """Tests that an error is raised when instrument ids do not match"""
        self.ophys_acquisition.instrument_id = "wrong_id"
        with self.assertRaises(ValueError):
            InstrumentAcquisitionCompatibility(
                instrument=self.ophys_instrument, acquisition=self.ophys_acquisition
            ).run_compatibility_check()

    def test_compare_mouse_platform_name_error(self):
        """Tests that an error is raised when mouse platform names do not match"""
        self.ophys_acquisition.subject_details.mouse_platform_name = "wrong_platform"
        with self.assertRaises(ValueError):
            InstrumentAcquisitionCompatibility(
                instrument=self.ophys_instrument, acquisition=self.ophys_acquisition
            ).run_compatibility_check()

    def test_compare_active_devices(self):
        """Tests that an error is raised when active_devices do not match"""
        self.ophys_acquisition.data_streams[0].active_devices = ["wrong_daq"]
        with self.assertRaises(ValueError):
            InstrumentAcquisitionCompatibility(
                instrument=self.ophys_instrument, acquisition=self.ophys_acquisition
            ).run_compatibility_check()

        self.ophys_acquisition.data_streams[0].active_devices = ["wrong_camera"]
        with self.assertRaises(ValueError):
            InstrumentAcquisitionCompatibility(
                instrument=self.ophys_instrument, acquisition=self.ophys_acquisition
            ).run_compatibility_check()

    def test_compare_configurations(self):
        """Tests that an error is raised when configuration names do not match"""
        self.ophys_acquisition.data_streams[0].configurations = [
            LaserConfig(
                device_name="wrong_laser", wavelength=488, excitation_power=10, excitation_power_unit="milliwatt"
            ),
        ]
        with self.assertRaises(ValueError):
            InstrumentAcquisitionCompatibility(
                instrument=self.ophys_instrument, acquisition=self.ophys_acquisition
            ).run_compatibility_check()


if __name__ == "__main__":
    unittest.main()
