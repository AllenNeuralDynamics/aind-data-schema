""" example procedures """
import datetime

from aind_data_schema import Procedures
from aind_data_schema.procedures import (Craniotomy, FiberImplant, OphysProbe,
                                         TrainingProtocol)

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

p = Procedures(
    subject_id="12345",
    training_protocols=[
        TrainingProtocol(
            protocol_id="dx.doi.org/10.12345/protocols.io.12345",
            training_protocol_start_date=t.date(),
            training_protocol_end_date=t.date(),
        )
    ],
    craniotomies=[
        Craniotomy(
            experimenter_full_name="jane doe",
            protocol_id="dx.doi.org/10.12345/protocols.io.12345",
            craniotomy_coordinates_ap=0,
            craniotomy_coordinates_ml=1,
            craniotomy_size=2,
            protective_material="Duragel",
            animal_weight=10,
            start_date=t.date(),
            end_date=t.date(),
        )
    ],
    fiber_implants=[
        FiberImplant(
            experimenter_full_name="john doe",
            protocol_id="dx.doi.org/10.12345/protocols.io.12345",
            animal_weight=34,
            start_date=t.date(),
            end_date=t.date(),
            probes=[
                OphysProbe(
                    name="Probe A",
                    manufacturer="acmecorp",
                    part_number="12345",
                    core_diameter=10,
                    numerical_aperture=1,
                    targeted_structure="VISp",
                    stereotactic_coordinate_ap=0,
                    stereotactic_coordinate_ml=0,
                    stereotactic_coordinate_dv=0,
                    angle=0,
                )
            ],
        )
    ],
)

p.write_standard_file()
