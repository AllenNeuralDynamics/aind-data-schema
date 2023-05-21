""" example for specimen procedures """

import datetime

from aind_data_schema import procedures

experimenter = "John Smith"
# subject and specimen id can be the same?
specimen_id = "651286"

# Reagents
shield_buffer = procedures.Reagent(name="SHIELD Buffer", lot_number="1234", source="Vendor")

shield_epoxy = procedures.Reagent(name="SHIELD Epoxy", lot_number="1234", source="Vendor")

shield_on = procedures.Reagent(name="SHIELD On", lot_number="1234", source="Vendor")

delipidation_buffer = procedures.Reagent(name="Delipidation Buffer", lot_number="1234", source="Vendor")

conductivity_buffer = procedures.Reagent(name="Conductivity Buffer", lot_number="1234", source="Vendor")

easy_index = procedures.Reagent(name="Easy Index", lot_number="1234", source="Vendor")

water = procedures.Reagent(name="Deionized water", lot_number="DDI/Filtered in house", source="This is not a reagent")

agarose = procedures.Reagent(name="Agarose", lot_number="1234", source="Other vendor")

# Procedures

perfusion = procedures.Perfusion(
    output_specimen_ids=[
        specimen_id,
    ],
    experimenter_full_name="LAS",
    start_date=datetime.date(2022, 11, 17),
    end_date=datetime.date(2022, 11, 17),
    protocol_id="unknown",
)

# perfused brain goes into SHIELD OFF solution
shield_off_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Fixation",
    start_date=datetime.date(2023, 1, 13),
    end_date=datetime.date(2023, 1, 17),
    experimenter_full_name=experimenter,
    protocol_id="unknown",
    reagents=[shield_buffer, shield_epoxy],
)

# specimen gets transfered to SHIELD ON and baked
shield_on_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Fixation",
    start_date=datetime.date(2023, 1, 17),
    end_date=datetime.date(2023, 1, 18),
    experimenter_full_name=experimenter,
    protocol_id="unknown",
    reagents=[
        shield_on,
    ],
    notes="40 deg. C",
)

# specimen gets transferred to delipidation buffer
delipidation_prep_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Soak",
    start_date=datetime.date(2023, 1, 18),
    end_date=datetime.date(2023, 1, 19),
    experimenter_full_name=experimenter,
    protocol_id="unknown",
    reagents=[
        delipidation_buffer,
    ],
)

# specimen goes into active delipidation box
active_delipidation_procedure = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Active delipidation",
    start_date=datetime.date(2023, 1, 19),
    end_date=datetime.date(2023, 1, 20),
    experimenter_full_name=experimenter,
    protocol_id="unknown",
    reagents=[delipidation_buffer, conductivity_buffer],
)

# First index matching is to 50% EasyIndex
index1 = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Soak",
    start_date=datetime.date(2023, 1, 30),
    end_date=datetime.date(2023, 1, 31),
    experimenter_full_name=experimenter,
    protocol_id="unknown",
    reagents=[
        easy_index,
        water,
    ],
)

# Now to 100% EasyIndex
index2 = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Soak",
    start_date=datetime.date(2023, 1, 31),
    end_date=datetime.date(2023, 2, 2),
    experimenter_full_name=experimenter,
    protocol_id="unknown",
    reagents=[
        easy_index,
    ],
)

# Specimen embedded into 2% agarose, prepared with EasyIndex
embedding = procedures.SpecimenProcedure(
    specimen_id=specimen_id,
    procedure_type="Embedding",
    start_date=datetime.date(2023, 1, 31),
    end_date=datetime.date(2023, 2, 2),
    experimenter_full_name=experimenter,
    protocol_id="unknown",
    reagents=[
        easy_index,
        agarose,
    ],
)

all_procedures = procedures.Procedures(
    subject_id=specimen_id,
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

all_procedures.write_standard_file(prefix="aibs_smartspim")
