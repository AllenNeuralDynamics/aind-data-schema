import datetime

from aind_data_schema.ophys.ophys_session import (OphysSession, FiberPhotometrySession, Laser, 
                Detector, Patch, Coupling)

t = datetime.datetime(2022, 7, 12, 7, 00, 00)

s = FiberPhotometrySession(
    experimenter_full_name = "Smrithi Sunil",
    start_date = t.date(),
    end_date = t.date(),
    subject_id = "652567",
    session_type = "Parameter Testing",
    iacuc_protocol = "2115",
    rig_id = "ophys_rig",
    lasers = [
        Laser(
            name = "Laser A",
            wavelength = 405,
            wavelength_unit = "nm",
            excitation_power = 10,
            excitation_power_unit = "mW"
        ),
        Laser(
            name = "Laser B",
            wavelength = 473,
            wavelength_unit = "nm",
            excitation_power = 7,
            excitation_power_unit = "mW"
        )
    ],
    detectors = [
        Detector(
            name="Hamamatsu Camera",
            exposure_time = 10
        )
    ],
    patch_cords = [
        Patch(
            name="Patch Cord A",
            output_power = 40,
            output_power_unit = "uW"
        ),
        Patch(
            name="Patch Cord B",
            output_power = 43,
            output_power_unit = "uW"
        ),
    ],
    coupling_array = [
        Coupling(
            fiber_name = "Fiber 1",
            patch_cord_name = "Patch Cord A"
        ),
        Coupling(
            fiber_name = "Fiber 2",
            patch_cord_name = "Patch Cord B"
        )
    ], 
    notes = "Internal trigger. GRAB-DA2m shows signal. Unclear about GRAB-rAC"
)

s.write_standard_file()