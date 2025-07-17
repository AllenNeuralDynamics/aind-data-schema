import os
from typing import List
import pandas as pd
from datetime import datetime, date
from zoneinfo import ZoneInfo

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.species import Strain
from aind_data_schema_models.units import VolumeUnit
from aind_data_schema_models.data_name_patterns import DataLevel
from aind_data_schema_models.brain_atlas import CCFv3

from aind_data_schema.components.coordinates import Rotation, Translation
from aind_data_schema.components.identifiers import Person
from aind_data_schema.components.injection_procedures import InjectionDynamics, InjectionProfile, ViralMaterial
from aind_data_schema.components.subject_procedures import BrainInjection, Perfusion
from aind_data_schema.components.subjects import BreedingInfo, Housing, MouseSubject, Species, Sex, HomeCageEnrichment
from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.core.data_description import DataDescription, Funding
from aind_data_schema.core.procedures import Procedures, Surgery
from aind_data_schema.core.subject import Subject

sessions_df = pd.read_excel("example_workflow.xlsx", sheet_name="sessions")
mice_df = pd.read_excel("example_workflow.xlsx", sheet_name="mice")
procedures_df = pd.read_excel("example_workflow.xlsx", sheet_name="procedures")

# everything was done by one person, so it's not in the spreadsheet
experimenter = Person(name="Some experimenter")

# in our spreadsheet, we stored sex as M/F instead of Male/Female
subject_sex_lookup = {
    "F": Sex.FEMALE,
    "M": Sex.MALE,
}

# everything is covered by the same IACUC protocol
ethics_review_id = "2109"


def generate_data_description(subject_id: str, creation_time: datetime) -> DataDescription:
    """Create the DataDescription object
    our data always contains planar optical physiology and behavior videos
    """
    return DataDescription(
        modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
        subject_id=subject_id,
        creation_time=creation_time,
        institution=Organization.AIND,
        funding_source=[Funding(funder=Organization.NIMH)],
        investigators=[experimenter],
        data_level=DataLevel.RAW,
        project_name="Example workflow",
    )


def generate_subject(
    subject_id: str,
    sex: Sex,
    date_of_birth: date,
    genotype: str,
    maternal_id: str,
    maternal_genotype: str,
    paternal_id: str,
    paternal_genotype: str,
) -> Subject:
    """Create the subject object"""
    return Subject(
        subject_id=subject_id,
        subject_details=MouseSubject(
            species=Species.HOUSE_MOUSE,
            sex=sex,
            date_of_birth=date_of_birth,
            genotype=genotype,
            breeding_info=BreedingInfo(
                maternal_id=maternal_id,
                maternal_genotype=maternal_genotype,
                paternal_id=paternal_id,
                paternal_genotype=paternal_genotype,
                breeding_group="unknown",  # not in spreadsheet
            ),
            housing=Housing(
                home_cage_enrichment=[HomeCageEnrichment.RUNNING_WHEEL],  # all subjects had a running wheel
                cage_id="unknown",  # not in spreadsheet
            ),
            strain=Strain.C57BL_6J,
            source=Organization.OTHER,
        ),
    )


def generate_procedures(
        subject_id: str,
        protocol: str,
        virus_name: str,
        virus_titer: int,
        coords: List[float],
        injection_volume: float,
        brain_area: str,
        injection_date: datetime,
        perfusion_date: datetime,
        experimenter: Person,
        ethics_review_id: str,
) -> Procedures:
    """Create the procedures object"""

    # Create the first surgery (brain injection)

    # we stored the injection coordinates as a comma-delimited string: AP, ML, Depth (from surface), Rotation angle
    # Note that the depth coordinate is inverted, it should be positive downward
    # We don't know which axis was rotated around, so we'll assume this is sagittal angle (around the AP axis)
    coord = [
        Translation(
            translation=[float(coords[0]), float(coords[1]), 0, -float(coords[2])],
        ),
        Rotation(
            angles=[float(coords[3]), 0, 0],
        )
    ]

    brain_injection = BrainInjection(
        protocol_id=protocol,
        coordinate_system_name=CoordinateSystemLibrary.BREGMA_ARID.name,
        injection_materials=[
            ViralMaterial(
                name=virus_name,
                titer=virus_titer,
            )
        ],
        targeted_structure=getattr(CCFv3, brain_area.upper()),
        coordinates=[coord],  # Note: this is a list, because we could have multiple depths
        dynamics=[
            InjectionDynamics(
                volume=injection_volume,
                volume_unit=VolumeUnit.NL,
                profile=InjectionProfile.BOLUS,
            )
        ],
    )

    brain_injection_surgery = Surgery(
        start_date=injection_date,
        protocol_id=protocol,
        ethics_review_id=ethics_review_id,
        experimenters=[experimenter],
        procedures=[
            brain_injection,
        ],
    )

    # Create the second surgery (perfusion)
    perfusion_surgery = Surgery(
        start_date=perfusion_date,
        experimenters=[experimenter],
        ethics_review_id=ethics_review_id,
        protocol_id=protocol,
        procedures=[Perfusion(protocol_id=protocol, output_specimen_ids=["1"])],
    )

    # Return the full Procedures object
    return Procedures(
        subject_id=subject_id,
        coordinate_system=CoordinateSystemLibrary.BREGMA_ARID,
        subject_procedures=[
            brain_injection_surgery,
            perfusion_surgery,
        ],
    )


# loop through all of the sessions
for _, row in sessions_df.iterrows():
    # Pull information from the session row
    subject_id = row["mouse_id"]
    start_time = row["start_time"].to_pydatetime()
    end_time = row["end_time"].to_pydatetime()

    # If there's no timezone information, add the pacific timezone
    pacific_tz = ZoneInfo("America/Los_Angeles")
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=pacific_tz)
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=pacific_tz)

    # Build the data_description
    data_description = generate_data_description(str(subject_id), end_time)

    # Get the mouse data for this session
    mouse_df_row = mice_df[mice_df["id"] == subject_id].iloc[0]  # Gets all matching rows
    sex = Sex.MALE if mouse_df_row["sex"] == "M" else Sex.FEMALE
    genotype = mouse_df_row["genotype"]
    dob = mouse_df_row["dob"].to_pydatetime().date()
    dam_id = mouse_df_row["dam_id"]
    sire_id = mouse_df_row["sire_id"]

    # Get the full dam and sire information
    dam_row = mice_df[mice_df["id"] == dam_id].iloc[0]
    dam_genotype = dam_row["genotype"]
    sire_row = mice_df[mice_df["id"] == sire_id].iloc[0]
    sire_genotype = sire_row["genotype"]

    # Build the subject
    subject = generate_subject(
        subject_id=str(subject_id),
        sex=sex,
        date_of_birth=dob,
        genotype=genotype,
        maternal_id=str(dam_id),
        maternal_genotype=dam_genotype,
        paternal_id=str(sire_id),
        paternal_genotype=sire_genotype,
    )

    # Get the procedures information
    proc_row = procedures_df[procedures_df["mouse_id"] == subject_id].iloc[0]

    # First surgery
    injection_date = proc_row["injection_date"].to_pydatetime()
    protocol = str(proc_row["protocol"])
    brain_area = proc_row["brain_area"]
    virus_name = proc_row["virus_name"]
    virus_titer = proc_row["virus_titer"]
    injection_volume = proc_row["injection_volume"]
    # we stored the injection coordinates as a comma-delimited string: AP,ML,DV,Rotation angle
    coords = proc_row.injection_coord.split(",")

    # Second surgery
    perfusion_date = proc_row["perfusion_date"].to_pydatetime()

    procedures = generate_procedures(
        subject_id=str(subject_id),
        protocol=protocol,
        virus_name=virus_name,
        virus_titer=virus_titer,
        coords=[float(coord) for coord in coords],
        injection_volume=injection_volume,
        brain_area=brain_area,
        injection_date=injection_date.date(),
        perfusion_date=perfusion_date.date(),
        experimenter=experimenter,
        ethics_review_id=ethics_review_id,
    )

    # we will store our json files in a directory named after the session
    os.makedirs(data_description.name, exist_ok=True)

    # Save the metadata files
    data_description.write_standard_file(output_directory=data_description.name)
    subject.write_standard_file(output_directory=data_description.name)
    procedures.write_standard_file(output_directory=data_description.name)
