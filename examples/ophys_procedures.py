""" 0phys procedure mouse 625100 """

import datetime

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.species import Species
from aind_data_schema_models.reagent import FluorophoreType, StainType

from aind_data_schema.components.injection_procedures import InjectionDynamics
from aind_data_schema.components.reagent import FluorescentStain, ProbeReagent, ProteinProbe, Fluorophore
from aind_data_schema.components.surgery_procedures import Anaesthetic, BrainInjection, Headframe, ProbeImplant
from aind_data_schema.core.procedures import (
    Procedures,
    SpecimenProcedure,
    Surgery,
    WaterRestriction,
)
from aind_data_schema.components.injection_procedures import ViralMaterial, InjectionProfile
from aind_data_schema.components.surgery_procedures import Perfusion
from aind_data_schema.components.configs import ProbeConfig
from aind_data_schema.components.devices import FiberProbe
from aind_data_schema_models.units import VolumeUnit
from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema.components.coordinates import CoordinateSystemLibrary, Translation

t = datetime.datetime(2022, 7, 12, 7, 00, 00)
t2 = datetime.datetime(2022, 9, 23, 10, 22, 00)

probe = FiberProbe(
    name="Probe A",
    core_diameter=200,
    numerical_aperture=0.37,
    ferrule_material="Ceramic",
    total_length=0.5,
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


p = Procedures(
    subject_id="625100",
    subject_procedures=[
        Surgery(
            start_date=t.date(),
            experimenters=["Scientist Smith"],
            ethics_review_id="2109",
            animal_weight_prior=22.6,
            animal_weight_post=22.3,
            anaesthesia=Anaesthetic(anaesthetic_type="Isoflurane", duration=180, level=1.5),
            workstation_id="SWS 3",
            protocol_id="doi",
            coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
            procedures=[
                Headframe(
                    protocol_id="2109",
                    headframe_type="AI straight",
                    headframe_part_number="TO ENTER",
                    headframe_material="Titanium",
                ),
                BrainInjection(
                    protocol_id="5678",
                    injection_materials=[
                        ViralMaterial(
                            name="AAV2/1-Syn-Flex-ChrimsonR-tdT",
                            addgene_id=PIDName(
                                registry=Registry.ADDGENE,
                                name="62723-AAV5",
                                registry_identifier="v122159",
                            ),
                            titer=20000000000000,
                        )
                    ],
                    coordinate_system_name=CoordinateSystemLibrary.BREGMA_ARID.name,
                    coordinates=[
                        [
                            Translation(
                                translation=[-600, -3050, 0, 4200],
                            ),
                        ],
                    ],
                    dynamics=[
                        InjectionDynamics(
                            volume=400,
                            volume_unit=VolumeUnit.NL,
                            profile=InjectionProfile.BOLUS,
                        )
                    ],
                    targeted_structure=CCFv3.VTA,
                ),
                ProbeImplant(
                    protocol_id="TO ENTER",
                    implanted_device=probe,
                    device_config=config,
                ),
            ],
        ),
        WaterRestriction(
            start_date="2023-05-15",
            ethics_review_id="1234",
            target_fraction_weight=25,
            minimum_water_per_day=1.5,
            baseline_weight=20.4,
            end_date="2023-05-23",
        ),
        Surgery(
            start_date="2023-05-31",
            experimenters=["Scientist Smith"],
            ethics_review_id="2109",
            anaesthesia=Anaesthetic(anaesthetic_type="Isoflurane", duration=30, level=3),
            workstation_id="SWS 3",
            protocol_id="doi",
            procedures=[
                Perfusion(protocol_id="dx.doi.org/10.17504/protocols.io.bg5vjy66", output_specimen_ids={"672640"})
            ],
        ),
    ],
    specimen_procedures=[
        SpecimenProcedure(
            procedure_type="Immunolabeling",
            specimen_id="625100_001",
            start_date="2023-06-09",
            end_date="2023-06-12",
            experimenters=["Scientist Smith"],
            protocol_id=["TO ENTER"],
            procedure_details=[
                ProbeReagent(
                    name="Chicken polyclonal to GFP",
                    source=Organization.ABCAM,
                    rrid=PIDName(
                        name="Chicken polyclonal to GFP", registry=Registry.RRID, registry_identifier="ab13970"
                    ),
                    lot_number="GR3361051-16",
                    target=ProteinProbe(
                        protein=PIDName(name="GFP", registry=Registry.UNIPROT, registry_identifier="P42212"),
                        species=Species.CHICKEN,
                        mass=10,
                    ),
                )
            ],
            notes="Primary dilution factor 1:1000 ---final concentration is 10ug/ml",
        ),
        SpecimenProcedure(
            procedure_type="Immunolabeling",
            specimen_id="625100_001",
            start_date="2023-06-12",
            end_date="2023-06-13",
            experimenters=["Scientist Smith"],
            protocol_id=["TO ENTER"],
            procedure_details=[
                FluorescentStain(
                    name="Alexa Fluor 488 goat anti-chicken IgY (H+L)",
                    source=Organization.THERMO_FISHER_SCIENTIFIC,
                    rrid=PIDName(
                        name="Alexa Fluor 488 goat anti-chicken IgY (H+L)",
                        registry=Registry.RRID,
                        registry_identifier="A11039",
                    ),
                    lot_number="2420700",
                    probe=ProteinProbe(
                        protein=PIDName(
                            name="Anti-chicken IgY (H+L)",
                        ),
                        species=Species.GOAT,
                        mass=4,
                    ),
                    stain_type=StainType.PROTEIN,
                    fluorophore=Fluorophore(
                        fluorophore_type=FluorophoreType.ALEXA,
                        excitation_wavelength=488,
                        excitation_wavelength_unit="nanometer",
                    ),
                ),
            ],
            notes="Secondary dilution factor 1:500 - final concentration 4ug/ml",
        ),
    ],
)

if __name__ == "__main__":
    serialized = p.model_dump_json()
    deserialized = Procedures.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="ophys")
