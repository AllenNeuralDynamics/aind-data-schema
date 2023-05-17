""" example fiber photometry session """

import datetime

from aind_data_schema.ophys.ophys_session import Coupling, Detector, FiberPhotometrySession, Laser, Patch

t = datetime.datetime(2022, 7, 12, 7, 00, 00)

s = FiberPhotometrySession(
    experimenter_full_name=["John Doe"],
    session_start_time=t,
    session_end_time=t,
    subject_id="652567",
    session_type="Parameter Testing",
    iacuc_protocol="2115",
    rig_id="ophys_rig",
    light_sources=[
        Laser(
            name="Laser A",
            wavelength=405,
            wavelength_unit="nanometer",
            excitation_power=10,
            excitation_power_unit="milliwatt",
        ),
        Laser(
            name="Laser B",
            wavelength=473,
            wavelength_unit="nanometer",
            excitation_power=7,
            excitation_power_unit="milliwatt",
        ),
    ],
    detectors=[Detector(name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal")],
    patch_cords=[
        Patch(name="Patch Cord A", output_power=40, output_power_unit="microwatt"),
        Patch(name="Patch Cord B", output_power=43, output_power_unit="microwatt"),
    ],
    coupling_array=[
        Coupling(fiber_name="Fiber A", patch_cord_name="Patch Cord A"),
        Coupling(fiber_name="Fiber B", patch_cord_name="Patch Cord B"),
    ],
    notes="Internal trigger. GRAB-DA2m shows signal. Unclear about GRAB-rAC",
)

s.write_standard_file()
