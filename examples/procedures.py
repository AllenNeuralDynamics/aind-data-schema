""" ephys procedure mouse 625100 """
import datetime

from aind_data_schema.core.procedures import (
    Anaesthetic,
    Craniotomy,
    NanojectInjection,
    Perfusion,
    Procedures,
    Surgery,
    TarsVirusIdentifiers,
    ViralMaterial,
)

t = datetime.datetime(2022, 7, 12, 7, 00, 00)
t2 = datetime.datetime(2022, 9, 23, 10, 22, 00)

p = Procedures(
    subject_id="625100",
    subject_procedures=[
        Surgery(
            start_date=t.date(),
            experimenter_full_name="John Apple",
            iacuc_protocol="2109",
            animal_weight_prior=22.6,
            animal_weight_post=22.3,
            anaesthesia=Anaesthetic(type="Isoflurane", duration=1, level=1.5),
            workstation_id="SWS 3",
            procedures=[
                Craniotomy(
                    craniotomy_type="Visual Cortex",
                    protocol_id="1234",
                    craniotomy_hemisphere="Left",
                    bregma_to_lambda_distance=4.1,
                    craniotomy_coordinates_reference="Lambda",
                    craniotomy_size=5,
                ),
                NanojectInjection(
                    protocol_id="5678",
                    injection_materials=[
                        ViralMaterial(
                            material_type="Virus",
                            name="AAV2-Flex-ChrimsonR",
                            tars_identifiers=TarsVirusIdentifiers(
                                virus_tars_id="AiV222",
                                plasmid_tars_alias="AiP222",
                                prep_lot_number="VT222",
                            ),
                            titer=2300000000,
                        )
                    ],
                    recovery_time=0,
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
            ],
        ),
        Surgery(
            start_date=t2.date(),
            experimenter_full_name="Frank Lee",
            iacuc_protocol="2109",
            procedures=[
                Perfusion(
                    protocol_id="doi_of_protocol",
                    output_specimen_ids=["1"],
                )
            ],
        ),
    ],
)

p.write_standard_file()
