import os

import pandas as pd
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization

from aind_data_schema.core.data_description import Funding, DataDescription
from aind_data_schema.core.procedures import (
    BrainInjection,
    Perfusion,
    Procedures,
    Surgery,
    ViralMaterial,
    InjectionDynamics,
    InjectionProfile,
)
from aind_data_schema.core.subject import BreedingInfo, Housing, Species, Subject
from aind_data_schema_models.species import Strain
from aind_data_schema_models.units import VolumeUnit
from aind_data_schema.components.coordinates import (
    AtlasCoordinate,
    Rotation,
)

from aind_data_schema.components.identifiers import Person

sessions_df = pd.read_excel("example_workflow.xlsx", sheet_name="sessions")
mice_df = pd.read_excel("example_workflow.xlsx", sheet_name="mice")
procedures_df = pd.read_excel("example_workflow.xlsx", sheet_name="procedures")

# everything was done by one person, so it's not in the spreadsheet
experimenter = Person(name="Some experimenter")

# in our spreadsheet, we stored sex as M/F instead of Male/Female
subject_sex_lookup = {
    "F": "Female",
    "M": "Male",
}

# everything is covered by the same IACUC protocol
ethics_review_id = "2109"

# loop through all of the sessions
for session_idx, session in sessions_df.iterrows():
    # our data always contains planar optical physiology and behavior videos
    d = DataDescription(
        modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
        subject_id=str(session["mouse_id"]),
        creation_time=session["end_time"].to_pydatetime(),
        institution=Organization.OTHER,
        funding_source=[Funding(funder=Organization.NIMH)],
        investigators=[experimenter],
        data_level="raw",
        project_name="Example workflow",
    )

    # we will store our json files in a directory named after the session
    os.makedirs(d.name, exist_ok=True)

    d.write_standard_file(output_directory=d.name)

    # look up the mouse used in this session
    mouse = mice_df[mice_df["id"] == session["mouse_id"]].iloc[0]
    dam = mice_df[mice_df["id"] == mouse["dam_id"]].iloc[0]
    sire = mice_df[mice_df["id"] == mouse["sire_id"]].iloc[0]

    # construct the subject
    s = Subject(
        subject_id=str(mouse["id"]),
        species=Species.MUS_MUSCULUS,  # all subjects are mice
        sex=subject_sex_lookup.get(mouse["sex"]),
        date_of_birth=mouse["dob"],
        genotype=mouse["genotype"],
        breeding_info=BreedingInfo(
            maternal_id=str(dam["id"]),
            maternal_genotype=dam["genotype"],
            paternal_id=str(sire["id"]),
            paternal_genotype=sire["genotype"],
            breeding_group="unknown",  # not in spreadsheet
        ),
        housing=Housing(
            home_cage_enrichment=["Running wheel"],  # all subjects had a running wheel in their cage
            cage_id="unknown",  # not in spreadsheet
        ),
        background_strain=Strain.C57BL_6J,
        source=Organization.OTHER,
    )
    s.write_standard_file(output_directory=d.name)

    # look up the procedures performed in this session
    proc_row = procedures_df[procedures_df["mouse_id"] == mouse["id"]].iloc[0]

    # we stored the injection coordinates as a comma-delimited string: AP,ML,DV,angle
    coords = proc_row.injection_coord.split(",")

    # in this example, a single protocol that covers all surgical procedures
    protocol = str(proc_row["protocol"])

    p = Procedures(
        subject_id=str(mouse["id"]),
        subject_procedures=[
            Surgery(
                start_date=proc_row["injection_date"].to_pydatetime().date(),
                protocol_id=protocol,
                ethics_review_id=ethics_review_id,
                experimenters=[experimenter],
                procedures=[
                    BrainInjection(
                        protocol_id=protocol,
                        injection_materials=[
                            ViralMaterial(
                                material_type="Virus",
                                name=proc_row["virus_name"],
                                titer=proc_row["virus_titer"],
                            )
                        ],
                        targeted_structure=proc_row["brain_area"],
                        coordinates=[
                            AtlasCoordinate(
                                system_name="BREGMA_ARI",
                                position=[coords[1], coords[0], 0, coords[2]],
                                angles=Rotation(
                                    angles=[0, coords[3], 0],
                                ),
                            ),
                        ],
                        dynamics=[
                            InjectionDynamics(
                                volume=proc_row["injection_volume"],
                                volume_unit=VolumeUnit.NL,
                                profile=InjectionProfile.BOLUS,
                            )
                        ],
                    )
                ],
            ),
            Surgery(
                start_date=proc_row["perfusion_date"].to_pydatetime().date(),
                experimenters=[experimenter],
                ethics_review_id=ethics_review_id,
                protocol_id=protocol,
                procedures=[Perfusion(protocol_id=protocol, output_specimen_ids=["1"])],
            ),
        ],
    )
    p.write_standard_file(output_directory=d.name)
