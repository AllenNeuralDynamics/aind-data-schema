"""Examples of BarSEQ/MapSEQ sectioning procedures"""

from datetime import date
from typing import List, Optional

from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.units import SizeUnit
from aind_data_schema_models.coordinates import AnatomicalRelative

from aind_data_schema.components.coordinates import AtlasLibrary, Translation
from aind_data_schema.components.specimen_procedures import (
    PlanarSectioning,
    Section,
    Sectioning,
    SectionOrientation,
    SpecimenProcedure,
)
from aind_data_schema.core.procedures import Procedures


def create_section(
    specimen_id: str,
    section_id: str,
    coordinate_system_name: str,
    start_um: float,
    thickness: float,
    thickness_unit: SizeUnit,
    partial_slice: Optional[List[AnatomicalRelative]] = None,
) -> Section:
    return Section(
        output_specimen_id=f"{specimen_id}_{section_id}",
        coordinate_system_name=coordinate_system_name,
        start_coordinate=Translation(translation=[round(start_um), 0, 0]),
        thickness=thickness,
        thickness_unit=thickness_unit,
        partial_slice=partial_slice,
    )


def create_uniform_sections(
    specimen_id: str,
    start_section_num: int,
    num_sections: int,
    start_um: float,
    thickness: float,
    thickness_unit: SizeUnit,
    coordinate_system_name: str = "CCF",
    section_prefix: str = "sec",
    partial_slice: Optional[List[AnatomicalRelative]] = None,
) -> List[Section]:
    return [
        create_section(
            specimen_id=specimen_id,
            section_id=f"{section_prefix}{start_section_num + i:03d}",
            coordinate_system_name=coordinate_system_name,
            start_um=start_um + i * thickness,
            thickness=thickness,
            thickness_unit=thickness_unit,
            partial_slice=partial_slice,
        )
        for i in range(num_sections)
    ]


def create_nonuniform_sections(
    specimen_id: str,
    num_sections: int,
    start_positions_um: List[float],
    thickness: float,
    thickness_unit: SizeUnit,
    coordinate_system_name: str = "CCF",
    section_prefix: str = "sec",
    partial_slice: Optional[List[AnatomicalRelative]] = None,
    start_section_num: int = 1,
) -> List[Section]:
    if num_sections != len(start_positions_um):
        raise ValueError("num_sections and start_positions_um must have same length")

    return [
        create_section(
            specimen_id=specimen_id,
            section_id=f"{section_prefix}{start_section_num + i:03d}",
            coordinate_system_name=coordinate_system_name,
            start_um=start_um,
            thickness=thickness,
            thickness_unit=thickness_unit,
            partial_slice=partial_slice,
        )
        for i, start_um in enumerate(start_positions_um)
    ]


def create_planar_sectioning(
    sections: List[Section],
    section_orientation: SectionOrientation = SectionOrientation.CORONAL,
) -> PlanarSectioning:
    return PlanarSectioning(
        sections=sections,
        section_orientation=section_orientation,
    )


def generate_mapseq_slides_780345_first_batch(start_section_num: int = 1) -> PlanarSectioning:
    start_positions = [i * (9800 / 27) for i in range(27)]

    sections = create_nonuniform_sections(
        specimen_id="780345",
        num_sections=27,
        start_positions_um=start_positions,
        thickness=300,
        thickness_unit=SizeUnit.UM,
        section_prefix="map",
        partial_slice=[AnatomicalRelative.LEFT],
        start_section_num=start_section_num,
    )

    return create_planar_sectioning(sections)


def generate_barseq_lc_780345(start_section_num: int = 1) -> PlanarSectioning:
    sections = create_uniform_sections(
        specimen_id="780345",
        start_section_num=start_section_num,
        num_sections=44,
        start_um=9900,
        thickness=20,
        thickness_unit=SizeUnit.UM,
        section_prefix="bar",
    )
    
    return create_planar_sectioning(sections)


def generate_mapseq_slides_780345_second_batch(start_section_num: int = 28) -> PlanarSectioning:
    start_positions = [11200 + i * (2000 / 12) for i in range(12)]

    sections = create_nonuniform_sections(
        specimen_id="780345",
        num_sections=12,
        start_positions_um=start_positions,
        thickness=300,
        thickness_unit=SizeUnit.UM,
        section_prefix="map",
        partial_slice=[AnatomicalRelative.LEFT],
        start_section_num=start_section_num,
    )
    
    return create_planar_sectioning(sections)


def generate_mapseq_spinal_780345() -> Sectioning:
    return Sectioning(
        sections=[
            Section(
                output_specimen_id="780345_spinal",
                targeted_structure=CCFv3.CST,
            )
        ]
    )


def generate_mapseq_slides_780346_first_batch(start_section_num: int = 1) -> PlanarSectioning:
    start_positions = [i * (9800 / 30) for i in range(30)]

    sections = create_nonuniform_sections(
        specimen_id="780346",
        num_sections=30,
        start_positions_um=start_positions,
        thickness=300,
        thickness_unit=SizeUnit.UM,
        section_prefix="map",
        partial_slice=[AnatomicalRelative.LEFT],
        start_section_num=start_section_num,
    )
    
    return create_planar_sectioning(sections)


def generate_barseq_lc_780346(start_section_num: int = 1) -> PlanarSectioning:
    sections = create_uniform_sections(
        specimen_id="780346",
        start_section_num=start_section_num,
        num_sections=51,
        start_um=9900,
        thickness=20,
        thickness_unit=SizeUnit.UM,
        section_prefix="bar",
    )
    
    return create_planar_sectioning(sections)


def generate_mapseq_slides_780346_second_batch(start_section_num: int = 31) -> PlanarSectioning:
    start_positions = [11200 + i * (2000 / 9) for i in range(9)]

    sections = create_nonuniform_sections(
        specimen_id="780346",
        num_sections=9,
        start_positions_um=start_positions,
        thickness=300,
        thickness_unit=SizeUnit.UM,
        section_prefix="map",
        partial_slice=[AnatomicalRelative.LEFT],
        start_section_num=start_section_num,
    )
    
    return create_planar_sectioning(sections)


def generate_mapseq_spinal_780346() -> Sectioning:
    return Sectioning(
        sections=[
            Section(
                output_specimen_id="780346_spinal",
                targeted_structure=CCFv3.CST,
            )
        ]
    )


def generate_procedures_780345() -> Procedures:
    return Procedures(
        subject_id="780345",
        coordinate_system=AtlasLibrary.CCFv3_10um,
        specimen_procedures=[
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780345",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_mapseq_slides_780345_first_batch()],
                notes="MAPseq sections 1-27 covering plates 0-98 (300um thick, partial slices)",
            ),
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780345",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_barseq_lc_780345()],
                notes="BARseq LC sections 1-44 covering plates 99-112 (20um thick)",
            ),
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780345",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_mapseq_slides_780345_second_batch()],
                notes="MAPseq sections 28-39 covering plates 112-132 (300um thick, partial slices)",
            ),
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780345",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_mapseq_spinal_780345()],
                notes="MAPseq spinal cord CST section, 1mm length",
            ),
        ],
    )


def generate_procedures_780346() -> Procedures:
    return Procedures(
        subject_id="780346",
        coordinate_system=AtlasLibrary.CCFv3_10um,
        specimen_procedures=[
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780346",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_mapseq_slides_780346_first_batch()],
                notes="MAPseq sections 1-30 covering plates 0-98 (300um thick, partial slices)",
            ),
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780346",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_barseq_lc_780346()],
                notes="BARseq LC sections 1-51 covering plates 99-112 (20um thick)",
            ),
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780346",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_mapseq_slides_780346_second_batch()],
                notes="MAPseq sections 31-39 covering plates 112-132 (300um thick, partial slices)",
            ),
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id="780346",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[generate_mapseq_spinal_780346()],
                notes="MAPseq spinal cord CST section, 1mm length",
            ),
        ],
    )


if __name__ == "__main__":
    procedures_780345 = generate_procedures_780345()
    procedures_780346 = generate_procedures_780346()
    
    serialized_780345 = procedures_780345.model_dump_json(indent=2)
    print("Specimen 780345:")
    print(serialized_780345)
    print("\n")
    
    serialized_780346 = procedures_780346.model_dump_json(indent=2)
    print("Specimen 780346:")
    print(serialized_780346)
    
    procedures_780345.write_standard_file(filename_suffix="780345")
    procedures_780346.write_standard_file(filename_suffix="780346")
