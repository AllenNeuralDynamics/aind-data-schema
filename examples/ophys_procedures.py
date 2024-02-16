""" 0phys procedure mouse 625100 """
import datetime

from aind_data_schema.core.procedures import (
    Anaesthetic,
    Antibody,
    FiberImplant,
    FiberProbe,
    Headframe,
    Immunolabeling,
    NanojectInjection,
    OphysProbe,
    Perfusion,
    Procedures,
    SpecimenProcedure,
    Surgery,
    ViralMaterial,
    WaterRestriction,
)
from aind_data_schema.models.organizations import Organization
from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.registry import Registry

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
            anaesthesia=Anaesthetic(type="Isoflurane", duration=180, level=1.5),
            workstation_id="SWS 3",
            procedures=[
                Headframe(
                    protocol_id="2109",
                    headframe_type="AI straight",
                    headframe_part_number="TO ENTER",
                    headframe_material="Titanium",
                ),
                NanojectInjection(
                    protocol_id="5678",
                    injection_materials=[
                        ViralMaterial(
                            material_type="Virus",
                            name="AAV2/1-Syn-Flex-ChrimsonR-tdT",
                            addgene_id=PIDName(
                                registry=Registry.ADDGENE,
                                name="62723-AAV5",
                                registry_identifier="v122159",
                            ),
                            titer=20000000000000,
                        )
                    ],
                    recovery_time=0,
                    instrument_id=None,
                    injection_hemisphere="Left",
                    injection_coordinate_ml=-0.6,
                    injection_coordinate_ap=-3.05,
                    injection_coordinate_depth=[-4.2],
                    injection_coordinate_reference="Bregma",
                    injection_angle=0,
                    injection_volume=[400],
                    targeted_structure="VTA",
                ),
                FiberImplant(
                    protocol_id="TO ENTER",
                    probes=[
                        OphysProbe(
                            ophys_probe=FiberProbe(
                                name="Probe A",
                                core_diameter=200,
                                numerical_aperture=0.37,
                                ferrule_material="Ceramic",
                                total_length=0.5,
                            ),
                            targeted_structure="VTA",
                            angle=0,
                            stereotactic_coordinate_ap=-3.05,
                            stereotactic_coordinate_ml=-0.6,
                            stereotactic_coordinate_dv=-4,
                            stereotactic_coordinate_reference="Bregma",
                        )
                    ],
                ),
            ],
        ),
        WaterRestriction(start_date="2023-05-15", baseline_weight=20.4, end_date="2023-05-23"),
        Surgery(
            start_date="2023-05-31",
            experimenter_full_name="John Apple",
            iacuc_protocol="2109",
            anaesthesia=Anaesthetic(type="Isoflurane", duration=30, level=3),
            workstation_id="SWS 3",
            procedures=[
                Perfusion(protocol_id="dx.doi.org/10.17504/protocols.io.bg5vjy66", output_specimen_ids={"672640"})
            ],
        ),
    ],
    specimen_procedures=[
        SpecimenProcedure(
            procedure_type="Immunolabeling",
            specimen_id="672640",
            start_date="2023-06-09",
            end_date="2023-06-12",
            experimenter_full_name="John Apple",
            protocol_id="TO ENTER",
            reagents=[],
            immunolabeling=Immunolabeling(
                antibody=Antibody(
                    name="Chicken polyclonal",
                    source=Organization.ABCAM,
                    rrid=PIDName(
                        name="Chicken polyclonal to GFP", registry=Registry.RRID, registry_identifier="ab13970"
                    ),
                    lot_number="GR3361051-16",
                    immunolabel_class="Primary",
                    fluorophore=None,
                ),
                concentration=10,
            ),
            notes="Primary dilution factor 1:1000 ---final concentration is 10ug/ml",
        ),
        SpecimenProcedure(
            procedure_type="Immunolabeling",
            specimen_id="672640",
            start_date="2023-06-12",
            end_date="2023-06-13",
            experimenter_full_name="John Apple",
            protocol_id="TO ENTER",
            reagents=[],
            immunolabeling=Immunolabeling(
                antibody=Antibody(
                    name="Alexa Fluor 488 goat anti-chicken IgY (H+L)",
                    source=Organization.THERMOFISHER,
                    rrid=PIDName(
                        name="Alexa Fluor 488 goat anti-chicken IgY (H+L)",
                        registry=Registry.RRID,
                        registry_identifier="A11039",
                    ),
                    lot_number="2420700",
                    immunolabel_class="Secondary",
                    fluorophore="Alexa Fluor 488",
                ),
                concentration=4,
            ),
            notes="Secondary dilution factor 1:500 - final concentration 4ug/ml",
        ),
    ],
)

p.write_standard_file(prefix="ophys")
