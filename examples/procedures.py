""" ephys procedure mouse 625100 """

from datetime import datetime, timezone

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

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)
t2 = datetime(2022, 9, 23, 10, 22, 00, tzinfo=timezone.utc)

p = Procedures(
    subject_id="625100",
    subject_procedures=[
        Surgery(
            start_date=t.date(),
            protocol_id="doi",
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
            protocol_id="doi",
            procedures=[
                Perfusion(
                    protocol_id="doi_of_protocol",
                    output_specimen_ids=["2", "1"],
                )
            ],
        ),
    ],
)
serialized = p.model_dump_json()
deserialized = Procedures.model_validate_json(serialized)
deserialized.write_standard_file()
