"""example for specimen procedures"""

import argparse
from datetime import date

from aind_data_schema_models.organizations import Organization

from aind_data_schema.core import procedures
from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.reagent import Reagent
from aind_data_schema.components.subject_procedures import Perfusion

experimenters = ["John Smith"]
specimen_id = "651286"

# Reagents
shield_buffer = Reagent(name="SHIELD Buffer", lot_number="1234", source=Organization.LIFECANVAS)

shield_epoxy = Reagent(name="SHIELD Epoxy", lot_number="1234", source=Organization.LIFECANVAS)

shield_on = Reagent(name="SHIELD On", lot_number="1234", source=Organization.LIFECANVAS)

delipidation_buffer = Reagent(name="Delipidation Buffer", lot_number="1234", source=Organization.OTHER)

easy_index = Reagent(name="Easy Index", lot_number="1234", source=Organization.LIFECANVAS)

# Procedures

perfusion = procedures.Surgery(
    start_date=date(2022, 11, 17),
    experimenters=["LAS"],
    ethics_review_id="2234",
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    procedures=[
        Perfusion(
            protocol_id="dx.doi.org/10.17504/protocols.io.8epv51bejl1b/v6",
            output_specimen_ids=[
                specimen_id,
            ],
        )
    ],
)

# perfused brain goes into SHIELD OFF solution
delipidation_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_name="Delipidation",
    procedure_type="Delipidation",
    start_date=date(2023, 1, 13),
    end_date=date(2023, 1, 17),
    experimenters=experimenters,
    protocol_id=["dx.doi.org/10.17504/protocols.io.rm7vzbz5rvx1/v1"],
    procedure_details=[shield_buffer, shield_epoxy, shield_on, delipidation_buffer],
)

# Now to 100% EasyIndex
index2 = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Refractive index matching",
    procedure_name="EasyIndex Index Matching",
    start_date=date(2023, 1, 31),
    end_date=date(2023, 2, 2),
    experimenters=experimenters,
    protocol_id=["dx.doi.org/10.17504/protocols.io.kxygx965kg8j/v1"],
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
    protocol_id=["dx.doi.org/10.17504/protocols.io.3byl4jpn8lo5/v1"],
    procedure_details=[
        easy_index,
    ],
)

all_procedures = procedures.Procedures(
    subject_id=specimen_id,
    subject_procedures=[
        perfusion,
    ],
    specimen_procedures=[
        delipidation_procedure,
        index2,
        embedding,
    ],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = all_procedures.model_dump_json()
    deserialized = procedures.Procedures.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="aibs_smartspim", output_directory=args.output_dir)
