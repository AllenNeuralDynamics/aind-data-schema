""" example for specimen procedures """

from datetime import date

from aind_data_schema_models.organizations import Organization

from aind_data_schema.core import procedures
from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.reagent import Reagent
from aind_data_schema.components.subject_procedures import Perfusion

experimenters = ["John Smith"]
# subject and specimen id can be the same?
specimen_id = "651286"

# Reagents
shield_buffer = Reagent(name="SHIELD Buffer", lot_number="1234", source=Organization.LIFECANVAS)

shield_epoxy = Reagent(name="SHIELD Epoxy", lot_number="1234", source=Organization.LIFECANVAS)

shield_on = Reagent(name="SHIELD On", lot_number="1234", source=Organization.LIFECANVAS)

delipidation_buffer = Reagent(name="Delipidation Buffer", lot_number="1234", source=Organization.OTHER)

conductivity_buffer = Reagent(name="Conductivity Buffer", lot_number="1234", source=Organization.OTHER)

easy_index = Reagent(name="Easy Index", lot_number="1234", source=Organization.LIFECANVAS)

water = Reagent(
    name="Deionized water",
    lot_number="DDI/Filtered in house",
    source=Organization.OTHER,
)

agarose = Reagent(name="Agarose", lot_number="1234", source=Organization.OTHER)

# Procedures

perfusion = procedures.Surgery(
    start_date=date(2022, 11, 17),
    experimenters=["LAS"],
    ethics_review_id="xxxx",
    protocol_id="doi_of_protocol_surgery",
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    procedures=[
        Perfusion(
            protocol_id="doi_of_protocol_perfusion",
            output_specimen_ids=[
                specimen_id,
            ],
        )
    ],
)

# perfused brain goes into SHIELD OFF solution
shield_off_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_name="SHIELD OFF",
    procedure_type="Fixation",
    start_date=date(2023, 1, 13),
    end_date=date(2023, 1, 17),
    experimenters=experimenters,
    protocol_id=["unknown"],
    procedure_details=[shield_buffer, shield_epoxy],
)

# specimen gets transferred to SHIELD ON and baked
shield_on_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_name="SHIELD ON",
    procedure_type="Fixation",
    start_date=date(2023, 1, 17),
    end_date=date(2023, 1, 18),
    experimenters=experimenters,
    protocol_id=["unknown"],
    procedure_details=[
        shield_on,
    ],
    notes="40 deg. C",
)

# specimen gets transferred to delipidation buffer
delipidation_prep_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Soak",
    start_date=date(2023, 1, 18),
    end_date=date(2023, 1, 19),
    experimenters=experimenters,
    protocol_id=["unknown"],
    procedure_details=[
        delipidation_buffer,
    ],
)

# specimen goes into active delipidation box
active_delipidation_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Delipidation",
    procedure_name="Active Delipidation",
    start_date=date(2023, 1, 19),
    end_date=date(2023, 1, 20),
    experimenters=experimenters,
    protocol_id=["unknown"],
    procedure_details=[delipidation_buffer, conductivity_buffer],
)

# First index matching is to 50% EasyIndex
index1 = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Soak",
    procedure_name="EasyIndex 50%",
    start_date=date(2023, 1, 30),
    end_date=date(2023, 1, 31),
    experimenters=experimenters,
    protocol_id=["unknown"],
    procedure_details=[
        easy_index,
        water,
    ],
)

# Now to 100% EasyIndex
index2 = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Soak",
    procedure_name="EasyIndex 100%",
    start_date=date(2023, 1, 31),
    end_date=date(2023, 2, 2),
    experimenters=experimenters,
    protocol_id=["unknown"],
    procedure_details=[
        easy_index,
    ],
)

# Specimen embedded into 2% agarose, prepared with EasyIndex
embedding = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Embedding",
    start_date=date(2023, 1, 31),
    end_date=date(2023, 2, 2),
    experimenters=experimenters,
    protocol_id=["unknown"],
    procedure_details=[
        easy_index,
        agarose,
    ],
)

all_procedures = procedures.Procedures(
    subject_id=specimen_id,
    subject_procedures=[
        perfusion,
    ],
    specimen_procedures=[
        shield_off_procedure,
        shield_on_procedure,
        delipidation_prep_procedure,
        active_delipidation_procedure,
        index1,
        index2,
        embedding,
    ],
)

if __name__ == "__main__":
    serialized = all_procedures.model_dump_json()
    deserialized = procedures.Procedures.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="aibs_smartspim")
