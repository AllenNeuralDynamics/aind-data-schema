""" ephys procedure mouse 625100 """
import datetime

from aind_data_schema import Procedures
from aind_data_schema.procedures import Anaesthetic, Craniotomy, InjectionMaterial, NanojectInjection

t = datetime.datetime(2022, 7, 12, 7, 00, 00)

p = Procedures(
    subject_id="625100",
    subject_procedures=[
        Craniotomy(
            start_date=t.date(),
            end_date=t.date(),
            experimenter_full_name="n/a",
            craniotomy_type="Visual Cortex",
            protocol_id="null",
            iacuc_protocol="2109",
            animal_weight_prior=22.6,
            animal_weight_post=22.3,
            anaesthesia=Anaesthetic(type="Isoflurane", duration=1, level=1.5),
            bregma_to_lambda_distance=4.1,
            craniotomy_coordinates_reference="Lambda",
            craniotomy_size=5,
            workstation_id="SWS 3",
        ),
        NanojectInjection(
            start_date=t.date(),
            end_date=t.date(),
            experimenter_full_name="n/a",
            protocol_id="null",
            iacuc_protocol="2109",
            animal_weight_prior=22.6,
            animal_weight_post=22.7,
            anaesthesia=Anaesthetic(type="Isoflurane", duration=1, level=1.5),
            injection_materials=[InjectionMaterial(name="AAV2-Flex-ChrimsonR")],
            recovery_time=0,
            workstation_id="SWS 3",
            instrument_id=None,
            injection_hemisphere="Left",
            injection_coordinate_ml=-0.87,
            injection_coordinate_ap=-3.8,
            injection_coordinate_depth=-3.3,
            injection_coordinate_reference="Lambda",
            bregma_to_lambda_distance=4.1,
            injection_angle=10,
            injection_volume=200,
            targeted_structure="VISp",
        ),
    ],
)

p.write_standard_file()
