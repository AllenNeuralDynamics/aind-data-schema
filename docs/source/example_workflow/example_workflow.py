import pandas as pd
import os

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.platforms import Platform

from aind_data_schema.core.data_description import Funding, RawDataDescription
from aind_data_schema.core.subject import Subject, Species, BreedingInfo, Housing
from aind_data_schema.core.procedures import (
    NanojectInjection,
    Procedures,
    Surgery,
    ViralMaterial,
    Perfusion,
)

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

# loop through all of the sessions
for session_idx, session in sessions_df.iterrows():

    # our data always contains planar optical physiology and behavior videos
    d = RawDataDescription(
        modality=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
        platform=Platform.BEHAVIOR,
        subject_id=str(session["subject_id"]),
        creation_time=session["end_time"].to_pydatetime(),
        institution=Organization.OTHER,
        investigators=[PIDName(name="Some Investigator")],
        funding_source=[Funding(funder=Organization.NIMH)],
    )

    # we will store our json files in a directory named after the session
    os.makedirs(d.name, exist_ok=True)

    d.write_standard_file(output_directory=d.name)

    # lookup the mouse used in this session
    subject = mice_df[mice_df["id"] == session["subject_id"]].iloc[0]
    dam = mice_df[mice_df["id"] == subject["dam_id"]].iloc[0]
    sire = mice_df[mice_df["id"] == subject["sire_id"]].iloc[0]

    # construct the subject
    s = Subject(
        subject_id=str(subject["id"]),
        species=Species.MUS_MUSCULUS,  # assumes all subjects are mice
        sex=subject_sex_lookup.get(subject["sex"]),
        date_of_birth=subject["dob"],
        genotype=subject["genotype"],
        breeding_info=BreedingInfo(
            maternal_id=str(dam["id"]),
            maternal_genotype=dam["genotype"],
            paternal_id=str(sire["id"]),
            paternal_genotype=sire["genotype"],
            breeding_group="unknown",  # not in spreadsheet
        ),
        housing=Housing(
            home_cage_enrichment=["Running wheel"],  # assumes all subjects have a running wheel
            cage_id="unknown",  # not in spreadsheet
        ),
        background_strain="C57BL/6J",  # assumes all subjects are C57BL/6J
        source=Organization.JAX,  # the animal came from JAX, not in spreadsheet
    )
    s.write_standard_file(output_directory=d.name)

    proc_row = procedures_df[procedures_df["mouse_id"] == subject["id"]].iloc[0]

    # we stored the injection coordinates as a comma-delimited string: AP,ML,DV,angle
    coords = proc_row.injection_coord.split(",")

    # in this example, a single iacuc protocol that covers all surgical procedures
    protocol = str(proc_row["protocol"])

    p = Procedures(
        subject_id=str(subject["id"]),
        subject_procedures=[
            Surgery(
                start_date=proc_row["injection_date"].to_pydatetime().date(),
                protocol_id=protocol,
                iacuc_protocol=protocol,
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
                iacuc_protocol=protocol,
                protocol_id=protocol,
                procedures=[Perfusion(protocol_id=protocol, output_specimen_ids=["1"])],
            ),
        ],
    )
    p.write_standard_file(output_directory=d.name)
