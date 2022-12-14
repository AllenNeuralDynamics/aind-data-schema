""" ephys procedure mouse 625100 """
import datetime
from aind_data_schema import Procedures
from aind_data_schema.procedures import (
    Craniotomy,
    NanojectInjection,
    Anaesthetic,
    InjectionMaterial,
)

t = datetime.datetime(2022, 7, 12, 7, 00, 00)

p = Procedures(
    subject_id="625100",
    craniotomies=[
        Craniotomy(
            start_date=t.date(),
            end_date=t.date(),
            experimenter_full_name="n/a",
            protocol_id="null",
            iacuc_protocol="2109",
            animal_weight=22.6,
            anaesthesia=Anaesthetic(type="Isoflurane", duration=1, level=1.5),
            craniotomy_size=5,
            workstation_id="SWS 3",
        )
    ],
    injections=[
        NanojectInjection(
            start_date=t.date(),
            end_date=t.date(),
            experimenter_full_name="n/a",
            protocol_id="null",
            iacuc_protocol="2109",
            animal_weight=22.6,
            anaesthesia=Anaesthetic(type="Isoflurane", duration=1, level=1.5),
            injection_materials=[InjectionMaterial(name="AAV2-Flex-ChrimsonR")],
            recovery_time=0,
            workstation_id="SWS 3",
            instrument_id=None,
            injection_hemisphere="Left",
            injection_coordinate_ml=-0.87,
            injection_coordinate_ap=-3.8,
            injection_coordinate_depth=-3.3,
            injection_angle=10,
            injection_volume=200,
        ),
    ],
)

p.write_standard_file()
