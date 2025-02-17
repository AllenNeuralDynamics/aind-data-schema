import os

import pandas as pd
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.platforms import Platform

from aind_data_schema.core.data_description import Funding, RawDataDescription
from aind_data_schema.core.procedures import NanojectInjection, Perfusion, Procedures, Surgery, ViralMaterial
from aind_data_schema.core.subject import BreedingInfo, Housing, Species, Subject

sessions_df = pd.read_excel("example_workflow.xlsx", sheet_name="sessions")
mice_df = pd.read_excel("example_workflow.xlsx", sheet_name="mice")
procedures_df = pd.read_excel("example_workflow.xlsx", sheet_name="procedures")

# everything was done by one person, so it's not in the spreadsheet
experimenter = "Sam Student"

# in our spreadsheet, we stored sex as M/F instead of Male/Female
subject_sex_lookup = {
    "F": "Female",
    "M": "Male",
}

# everything is covered by the same IACUC protocol
iacuc_protocol = "2109"

# loop through all of the sessions
for session_idx, session in sessions_df.iterrows():
    # our data always contains planar optical physiology and behavior videos
    d = RawDataDescription(
        modality=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
        platform=Platform.BEHAVIOR,
        subject_id=str(session["mouse_id"]),
        creation_time=session["end_time"].to_pydatetime(),
        institution=Organization.OTHER,
        investigators=[PIDName(name="Some Investigator")],
        funding_source=[Funding(funder=Organization.NIMH)],
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
        background_strain="C57BL/6J",
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
                iacuc_protocol=iacuc_protocol,
                experimenter_full_name=experimenter,
                procedures=[
                    NanojectInjection(
                        protocol_id=protocol,
                        injection_materials=[
                            ViralMaterial(
                                material_type="Virus",
                                name=proc_row["virus_name"],
                                titer=proc_row["virus_titer"],
                            )
                        ],
                        targeted_structure=proc_row["brain_area"],
                        injection_coordinate_ml=float(coords[1]),
                        injection_coordinate_ap=float(coords[0]),
                        injection_angle=float(coords[3]),
                        # multiple injection volumes at different depths are allowed, but that's not happening here
                        injection_coordinate_depth=[float(coords[2])],
                        injection_volume=[float(proc_row["injection_volume"])],
                    )
                ],
            ),
            Surgery(
                start_date=proc_row["perfusion_date"].to_pydatetime().date(),
                experimenter_full_name=experimenter,
                iacuc_protocol=iacuc_protocol,
                protocol_id=protocol,
                procedures=[Perfusion(protocol_id=protocol, output_specimen_ids=["1"])],
            ),
        ],
    )
    p.write_standard_file(output_directory=d.name)
