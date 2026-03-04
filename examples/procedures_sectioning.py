"""Examples of BarSEQ/MapSEQ sectioning procedures"""

from datetime import date
from typing import Dict, List

from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.units import SizeUnit

from aind_data_schema.components.coordinates import AtlasLibrary, Translation
from aind_data_schema.components.specimen_procedures import (
    PlanarSectioning,
    PlanarSection,
    Section,
    Sectioning,
    SectionOrientation,
    SpecimenProcedure,
)
from aind_data_schema.core.procedures import Procedures

_SLIDE_REGIONS = [
    {
        "slide_num": 1,
        "section_start": 1,
        "section_end": 3,
        "chunk_name": "MOB",
        "ccf_acronym": "MOB",
        "includes_surrounding_tissue": False,
        "notes": "Main olfactory bulb",
    },
    {
        "slide_num": 2,
        "section_start": 4,
        "section_end": 6,
        "chunk_name": "MOB",
        "ccf_acronym": "MOB",
        "includes_surrounding_tissue": False,
        "notes": "Main olfactory bulb",
    },
    {
        "slide_num": 3,
        "section_start": 7,
        "section_end": 9,
        "chunk_name": "ORB",
        "ccf_acronym": "ORB",
        "includes_surrounding_tissue": False,
        "notes": "Orbital area (orbitofrontal cortex)",
    },
    {
        "slide_num": 3,
        "section_start": 7,
        "section_end": 9,
        "chunk_name": "MO",
        "ccf_acronym": "MO",
        "includes_surrounding_tissue": False,
        "notes": "Somatomotor areas (motor cortex)",
    },
    {
        "slide_num": 3,
        "section_start": 7,
        "section_end": 9,
        "chunk_name": "AON",
        "ccf_acronym": "AON",
        "includes_surrounding_tissue": False,
        "notes": "Anterior olfactory nucleus",
    },
    {
        "slide_num": 4,
        "section_start": 10,
        "section_end": 12,
        "chunk_name": "ORB",
        "ccf_acronym": "ORB",
        "includes_surrounding_tissue": False,
        "notes": "Orbital area (orbitofrontal cortex)",
    },
    {
        "slide_num": 4,
        "section_start": 10,
        "section_end": 12,
        "chunk_name": "MO",
        "ccf_acronym": "MO",
        "includes_surrounding_tissue": False,
        "notes": "Somatomotor areas (motor cortex)",
    },
    {
        "slide_num": 4,
        "section_start": 10,
        "section_end": 12,
        "chunk_name": "AON",
        "ccf_acronym": "AON",
        "includes_surrounding_tissue": False,
        "notes": "Anterior olfactory nucleus",
    },
    {
        "slide_num": 5,
        "section_start": 13,
        "section_end": 15,
        "chunk_name": "CP",
        "ccf_acronym": "CP",
        "includes_surrounding_tissue": False,
        "notes": "Caudoputamen",
    },
    {
        "slide_num": 5,
        "section_start": 13,
        "section_end": 15,
        "chunk_name": "ACB",
        "ccf_acronym": "ACB",
        "includes_surrounding_tissue": False,
        "notes": "Nucleus accumbens",
    },
    {
        "slide_num": 5,
        "section_start": 13,
        "section_end": 15,
        "chunk_name": "LSX",
        "ccf_acronym": "LSX",
        "includes_surrounding_tissue": False,
        "notes": "Lateral septal complex",
    },
    {
        "slide_num": 5,
        "section_start": 13,
        "section_end": 15,
        "chunk_name": "ctx_1",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Superior/dorsal cortex ribbon (ctx 1 in figure)",
    },
    {
        "slide_num": 5,
        "section_start": 13,
        "section_end": 15,
        "chunk_name": "ctx_2",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Lateral cortex ribbon (ctx 2 in figure)",
    },
    {
        "slide_num": 5,
        "section_start": 13,
        "section_end": 15,
        "chunk_name": "ctx_3",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Inferior/ventrolateral cortex ribbon (ctx 3 in figure)",
    },
    {
        "slide_num": 6,
        "section_start": 16,
        "section_end": 18,
        "chunk_name": "CP",
        "ccf_acronym": "CP",
        "includes_surrounding_tissue": False,
        "notes": "Caudoputamen",
    },
    {
        "slide_num": 6,
        "section_start": 16,
        "section_end": 18,
        "chunk_name": "ACB",
        "ccf_acronym": "ACB",
        "includes_surrounding_tissue": False,
        "notes": "Nucleus accumbens",
    },
    {
        "slide_num": 6,
        "section_start": 16,
        "section_end": 18,
        "chunk_name": "LSX",
        "ccf_acronym": "LSX",
        "includes_surrounding_tissue": False,
        "notes": "Lateral septal complex",
    },
    {
        "slide_num": 6,
        "section_start": 16,
        "section_end": 18,
        "chunk_name": "ctx_1",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Superior/dorsal cortex ribbon (ctx 1 in figure)",
    },
    {
        "slide_num": 6,
        "section_start": 16,
        "section_end": 18,
        "chunk_name": "ctx_2",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Lateral cortex ribbon (ctx 2 in figure)",
    },
    {
        "slide_num": 6,
        "section_start": 16,
        "section_end": 18,
        "chunk_name": "ctx_3",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Inferior/ventrolateral cortex ribbon (ctx 3 in figure)",
    },
    {
        "slide_num": 7,
        "section_start": 19,
        "section_end": 21,
        "chunk_name": "CP",
        "ccf_acronym": "CP",
        "includes_surrounding_tissue": False,
        "notes": "Caudoputamen",
    },
    {
        "slide_num": 7,
        "section_start": 19,
        "section_end": 21,
        "chunk_name": "LSX",
        "ccf_acronym": "LSX",
        "includes_surrounding_tissue": False,
        "notes": "Lateral septal complex",
    },
    {
        "slide_num": 7,
        "section_start": 19,
        "section_end": 21,
        "chunk_name": "BST",
        "ccf_acronym": "BST",
        "includes_surrounding_tissue": False,
        "notes": "Bed nuclei of the stria terminalis (BNST)",
    },
    {
        "slide_num": 7,
        "section_start": 19,
        "section_end": 21,
        "chunk_name": "ctx_1",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Superior/dorsal cortex ribbon (ctx 1 in figure)",
    },
    {
        "slide_num": 7,
        "section_start": 19,
        "section_end": 21,
        "chunk_name": "ctx_2",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Lateral cortex ribbon (ctx 2 in figure)",
    },
    {
        "slide_num": 7,
        "section_start": 19,
        "section_end": 21,
        "chunk_name": "ctx_3",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Inferior/ventrolateral cortex ribbon (ctx 3 in figure)",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "HPF",
        "ccf_acronym": "HPF",
        "includes_surrounding_tissue": False,
        "notes": "Hippocampal formation",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "TH",
        "ccf_acronym": "TH",
        "includes_surrounding_tissue": False,
        "notes": "Thalamus",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "HY",
        "ccf_acronym": "HY",
        "includes_surrounding_tissue": False,
        "notes": "Hypothalamus",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "amygdala",
        "ccf_acronym": "BLA",
        "includes_surrounding_tissue": True,
        "notes": "Amygdala (targeting whole structure via BLA + surrounding tissue)",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "GPE",
        "ccf_acronym": "GPe",
        "includes_surrounding_tissue": False,
        "notes": "Globus pallidus external segment (GPe)",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "ctx_1",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Superior/dorsal cortex ribbon (ctx 1 in figure)",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "ctx_2",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Lateral cortex ribbon (ctx 2 in figure)",
    },
    {
        "slide_num": 8,
        "section_start": 22,
        "section_end": 24,
        "chunk_name": "ctx_3",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Inferior/ventrolateral cortex ribbon (ctx 3 in figure)",
    },
    {
        "slide_num": 9,
        "section_start": 25,
        "section_end": 27,
        "chunk_name": "MB",
        "ccf_acronym": "MB",
        "includes_surrounding_tissue": False,
        "notes": "Midbrain",
    },
    {
        "slide_num": 9,
        "section_start": 25,
        "section_end": 27,
        "chunk_name": "ctx_1",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Superior/dorsal cortex ribbon (ctx 1 in figure)",
    },
    {
        "slide_num": 9,
        "section_start": 25,
        "section_end": 27,
        "chunk_name": "ctx_2",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Lateral cortex ribbon (ctx 2 in figure)",
    },
    {
        "slide_num": 9,
        "section_start": 25,
        "section_end": 27,
        "chunk_name": "ctx_3",
        "ccf_acronym": "CTX",
        "includes_surrounding_tissue": True,
        "notes": "Inferior/ventrolateral cortex ribbon (ctx 3 in figure)",
    },
    {
        "slide_num": 10,
        "section_start": 28,
        "section_end": 30,
        "chunk_name": "MB",
        "ccf_acronym": "MB",
        "includes_surrounding_tissue": False,
        "notes": "Midbrain (more caudal)",
    },
    {
        "slide_num": 10,
        "section_start": 28,
        "section_end": 30,
        "chunk_name": "HB",
        "ccf_acronym": "HB",
        "includes_surrounding_tissue": False,
        "notes": "Hindbrain",
    },
    {
        "slide_num": 11,
        "section_start": 31,
        "section_end": 33,
        "chunk_name": "MB",
        "ccf_acronym": "MB",
        "includes_surrounding_tissue": False,
        "notes": "Midbrain (most caudal)",
    },
    {
        "slide_num": 11,
        "section_start": 31,
        "section_end": 33,
        "chunk_name": "HB",
        "ccf_acronym": "HB",
        "includes_surrounding_tissue": False,
        "notes": "Hindbrain",
    },
    {
        "slide_num": 12,
        "section_start": 34,
        "section_end": 36,
        "chunk_name": "CB",
        "ccf_acronym": "CB",
        "includes_surrounding_tissue": False,
        "notes": "Cerebellum",
    },
    {
        "slide_num": 12,
        "section_start": 34,
        "section_end": 36,
        "chunk_name": "MY",
        "ccf_acronym": "MY",
        "includes_surrounding_tissue": False,
        "notes": "Medulla",
    },
    {
        "slide_num": 13,
        "section_start": 37,
        "section_end": 39,
        "chunk_name": "MY",
        "ccf_acronym": "MY",
        "includes_surrounding_tissue": False,
        "notes": "Medulla",
    },
]


def _load_slide_regions() -> Dict[int, dict]:
    slides: Dict[int, dict] = {}
    for row in _SLIDE_REGIONS:
        slide = row["slide_num"]
        if slide not in slides:
            slides[slide] = {
                "section_start": row["section_start"],
                "section_end": row["section_end"],
                "chunks": [],
            }
        slides[slide]["chunks"].append(
            {
                "chunk_name": row["chunk_name"],
                "ccf_acronym": row["ccf_acronym"],
                "includes_surrounding_tissue": row["includes_surrounding_tissue"],
                "notes": row["notes"],
            }
        )
    return slides


def generate_mapseq_slide_chunks(specimen_id: str) -> List[SpecimenProcedure]:
    slides = _load_slide_regions()
    procedures = []
    for slide_num, slide_data in slides.items():
        section_start = slide_data["section_start"]
        section_end = slide_data["section_end"]
        chunks = slide_data["chunks"]

        input_ids = [f"{specimen_id}_map{i:03d}" for i in range(section_start, section_end + 1)]

        output_sections = []
        for chunk_idx, chunk in enumerate(chunks, start=1):
            structure = CCFv3.by_acronym(chunk["ccf_acronym"])
            surrounding = True if chunk["includes_surrounding_tissue"] else None
            for sec_id in input_ids:
                output_sections.append(
                    Section(
                        output_specimen_id=f"{sec_id}_{chunk_idx:03d}",
                        targeted_structure=structure,
                        includes_surrounding_tissue=surrounding,
                    )
                )

        chunk_names = ", ".join(c["chunk_name"] for c in chunks)
        ctx_notes = "; ".join(c["notes"] for c in chunks if c["ccf_acronym"] == "CTX")
        note = f"Slide {slide_num}: sections {section_start}-{section_end} chunked into [{chunk_names}]"
        if ctx_notes:
            note += f". CTX chunks: {ctx_notes}"

        procedures.append(
            SpecimenProcedure(
                procedure_type="Sectioning",
                specimen_id=input_ids,
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 1),
                experimenters=["Polina Kosillo"],
                procedure_details=[Sectioning(sections=output_sections)],
                notes=note,
            )
        )
    return procedures


def create_planar_section(
    specimen_id: str,
    section_id: str,
    coordinate_system_name: str,
    start_um: float,
    thickness: float,
    thickness_unit: SizeUnit,
) -> PlanarSection:
    return PlanarSection(
        output_specimen_id=f"{specimen_id}_{section_id}",
        coordinate_system_name=coordinate_system_name,
        start_coordinate=Translation(translation=[round(start_um), 0, 0]),
        thickness=thickness,
        thickness_unit=thickness_unit,
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
) -> List[PlanarSection]:
    return [
        create_planar_section(
            specimen_id=specimen_id,
            section_id=f"{section_prefix}{start_section_num + i:03d}",
            coordinate_system_name=coordinate_system_name,
            start_um=start_um + i * thickness,
            thickness=thickness,
            thickness_unit=thickness_unit,
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
    start_section_num: int = 1,
) -> List[PlanarSection]:
    if num_sections != len(start_positions_um):
        raise ValueError("num_sections and start_positions_um must have same length")

    return [
        create_planar_section(
            specimen_id=specimen_id,
            section_id=f"{section_prefix}{start_section_num + i:03d}",
            coordinate_system_name=coordinate_system_name,
            start_um=start_um,
            thickness=thickness,
            thickness_unit=thickness_unit,
        )
        for i, start_um in enumerate(start_positions_um)
    ]


def create_planar_sectioning(
    sections: List[PlanarSection],
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
        start_section_num=start_section_num,
    )

    return create_planar_sectioning(sections)


def generate_mapseq_spinal_780345() -> Sectioning:
    return Sectioning(
        sections=[
            Section(
                output_specimen_id="780345_spinal",
                targeted_structure=CCFv3.CST,
                thickness=1000,
                thickness_unit=SizeUnit.UM,
            ),
            Section(
                output_specimen_id="780345_spinal",
                targeted_structure=CCFv3.CST,
                thickness=1000,
                thickness_unit=SizeUnit.UM,
            ),
            Section(
                output_specimen_id="780345_spinal",
                targeted_structure=CCFv3.CST,
                thickness=1000,
                thickness_unit=SizeUnit.UM,
            ),
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
        start_section_num=start_section_num,
    )

    return create_planar_sectioning(sections)


def generate_mapseq_spinal_780346() -> Sectioning:
    return Sectioning(
        sections=[
            Section(
                output_specimen_id="780346_spinal",
                targeted_structure=CCFv3.CST,
                thickness=1000,
                thickness_unit=SizeUnit.UM,
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
                notes="MAPseq spinal cord sections, size is approximate (1/3rd length each)",
            ),
            *generate_mapseq_slide_chunks("780345"),
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
                notes="MAPseq spinal cord sections, size is approximate (1/3rd length each)",
            ),
            *generate_mapseq_slide_chunks("780346"),
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
