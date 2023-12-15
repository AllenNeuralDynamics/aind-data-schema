""" ephys procedure mouse 625100 """
import datetime

from aind_data_schema.core.procedures import (
    Anaesthetic,
    Craniotomy,
    ViralMaterial,
    NanojectInjection,
    Perfusion,
    Procedures,
)

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
            injection_materials=[
                ViralMaterial(
                    material_type="Virus",
                    name="AAV2-Flex-ChrimsonR",
                    virus_TARS_id="AiV222",
                    plasmid_TARS_alias="AiP222",
                    prep_lot_number="VT222",
                    titer=2300000000,
                )
            ],
            recovery_time=0,
            workstation_id="SWS 3",
            instrument_id=None,
            injection_hemisphere="Left",
            injection_coordinate_ml=-0.87,
            injection_coordinate_ap=-3.8,
            injection_coordinate_depth=[-3.3],
            injection_coordinate_reference="Lambda",
            bregma_to_lambda_distance=4.1,
            injection_angle=10,
            injection_volume=[200],
            targeted_structure="VISp",
        ),
        Perfusion(
            start_date=t.date(),
            end_date=t.date(),
            experimenter_full_name="n/a",
            protocol_id="null",
            output_specimen_ids=["1"],
        ),
    ],
)

p.write_standard_file()
