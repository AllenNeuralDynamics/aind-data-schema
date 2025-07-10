""" ephys procedure mouse 625100 """

from datetime import datetime, timezone

from aind_data_schema.components.injection_procedures import (
    InjectionDynamics,
    InjectionProfile,
    TarsVirusIdentifiers,
    ViralMaterial,
)
from aind_data_schema.components.surgery_procedures import (
    Anaesthetic,
    BrainInjection,
    Craniotomy,
    CraniotomyType,
    Perfusion,
    ProbeImplant,
)
from aind_data_schema.core.procedures import (
    Procedures,
    Surgery,
)
from aind_data_schema.components.devices import EphysProbe
from aind_data_schema.components.configs import ProbeConfig
from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.units import VolumeUnit, SizeUnit
from aind_data_schema.components.coordinates import (
    Translation,
    Rotation,
    Origin,
    CoordinateSystemLibrary,
)

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)
t2 = datetime(2022, 9, 23, 10, 22, 00, tzinfo=timezone.utc)

coordinate_system = CoordinateSystemLibrary.BREGMA_RASD
coordinate_system.name = "LAMBDA_RASD"
coordinate_system.origin = Origin.LAMBDA

probe = EphysProbe(
    name="Probe A",
    probe_model="Neuropixels UHD (Fixed)",
)

config = ProbeConfig(
    primary_targeted_structure=CCFv3.VTA,
    device_name="Probe A",
    coordinate_system=CoordinateSystemLibrary.MPM_MANIP_RFB,
    transform=[
        Translation(
            translation=[-600, -3050, 0, 4200],
        ),
    ],
)

surgery1 = Surgery(
    start_date=t.date(),
    protocol_id="doi",
    experimenters=["Scientist Smith"],
    ethics_review_id="2109",
    animal_weight_prior=22.6,
    animal_weight_post=22.3,
    anaesthesia=Anaesthetic(anaesthetic_type="Isoflurane", duration=1, level=1.5),
    coordinate_system=coordinate_system,
    workstation_id="SWS 3",
    procedures=[
        ProbeImplant(
            implanted_device=probe,
            device_config=config,
        ),
        Craniotomy(
            craniotomy_type=CraniotomyType.CIRCLE,
            protocol_id="1234",
            coordinate_system_name="LAMBDA_RASD",
            position=Translation(translation=[-2, 2, 0, 0]),
            size=1,
            size_unit=SizeUnit.MM,
        ),
        BrainInjection(
            protocol_id="5678",
            injection_materials=[
                ViralMaterial(
                    name="AAV2-Flex-ChrimsonR",
                    tars_identifiers=TarsVirusIdentifiers(
                        virus_tars_id="AiV222",
                        plasmid_tars_alias=["AiP222"],
                        prep_lot_number="VT222",
                    ),
                    titer=2300000000,
                )
            ],
            coordinate_system_name=coordinate_system.name,
            coordinates=[
                [
                    Translation(translation=[-0.85, -3.8, 0, 3.3]),
                    Rotation(
                        angles=[0, 10, 0],
                    ),
                ],
            ],
            dynamics=[
                InjectionDynamics(
                    volume=200,
                    volume_unit=VolumeUnit.NL,
                    profile=InjectionProfile.BOLUS,
                )
            ],
            targeted_structure=CCFv3.VISP,
        ),
    ],
)

p = Procedures(
    subject_id="625100",
    subject_procedures=[
        surgery1,
        Surgery(
            start_date=t2.date(),
            experimenters=["Scientist Smith"],
            ethics_review_id="2109",
            protocol_id="doi",
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
            procedures=[
                Perfusion(
                    protocol_id="doi_of_protocol",
                    output_specimen_ids=["2", "1"],
                )
            ],
        ),
    ],
)

if __name__ == "__main__":
    serialized = p.model_dump_json()
    deserialized = Procedures.model_validate_json(serialized)
    deserialized.write_standard_file()
