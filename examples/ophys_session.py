""" example fiber photometry session """

import datetime

from aind_data_schema.models.modalities import FIB
from aind_data_schema.models.device_configurations import DetectorConfigs, FiberConnectionConfigs, LaserConfigs
from aind_data_schema.session import Session, Stream

t = datetime.datetime(2022, 7, 12, 7, 00, 00)

s = Session(
    experimenter_full_name=["John Doe"],
    session_start_time=t,
    session_end_time=t,
    subject_id="652567",
    session_type="Parameter Testing",
    iacuc_protocol="2115",
    rig_id="ophys_rig",
    data_streams=[
        Stream(
            stream_start_time=t,
            stream_end_time=t,
            stream_modalities=[FIB],
            light_sources=[
                LaserConfigs(
                    name="Laser A",
                    wavelength=405,
                    wavelength_unit="nanometer",
                    excitation_power=10,
                    excitation_power_unit="milliwatt",
                ),
                LaserConfigs(
                    name="Laser B",
                    wavelength=473,
                    wavelength_unit="nanometer",
                    excitation_power=7,
                    excitation_power_unit="milliwatt",
                ),
            ],
            detectors=[DetectorConfigs(name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal")],
            fiber_connections=[
                FiberConnectionConfigs(
                    patch_cord_name="Patch Cord A",
                    patch_cord_output_power=40,
                    output_power_unit="microwatt",
                    fiber_name="Fiber A",
                ),
                FiberConnectionConfigs(
                    patch_cord_name="Patch Cord B",
                    patch_cord_output_power=43,
                    output_power_unit="microwatt",
                    fiber_name="Fiber B",
                ),
            ],
            mouse_platform_name="Disc",
            active_mouse_platform=False,
            notes="Internal trigger. GRAB-DA2m shows signal. Unclear about GRAB-rAC"
        )
    ],
)

s.write_standard_file(prefix="ophys")
