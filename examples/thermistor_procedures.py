"""Thermistor implant procedure example"""

import argparse
from datetime import date

from aind_data_schema.components.coordinates import Axis, CoordinateSystem, Translation
from aind_data_schema.components.devices import Device, ThermistorAssembly
from aind_data_schema.components.surgery_procedures import Anaesthetic, ThermistorImplant
from aind_data_schema.core.procedures import Procedures, Surgery
from aind_data_schema_models.coordinates import AnatomicalRelative, AxisName, Direction, Origin
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import SizeUnit

thermistor_wire = Device(
    name="Thermistor wire",
    manufacturer=Organization.TE_CONNECTIVITY,
    model="GAG22K7MCD419",
    notes="Digi-Key part number: GAG22K7MCD419. "
    "https://www.digikey.com/en/products/detail/te-connectivity-measurement-specialties/GAG22K7MCD419/5277253",
)

connector = Device(
    name="Connector",
    manufacturer=Organization.OTHER,
    model="0533984002",
    notes="Molex connector. Digi-Key part number: 900-0533984002CT-ND. "
    "https://www.digikey.com/en/products/detail/molex/0533984002/15622916",
)

thermistor_assembly = ThermistorAssembly(
    name="Thermistor",
    thermistor=thermistor_wire,
    connector=connector,
)

thermistor_coordinate_system = CoordinateSystem(
    name="THERMISTOR",
    origin=Origin.ORIGIN,
    axis_unit=SizeUnit.MM,
    axes=[],
)

procedures_coordinate_system = CoordinateSystem(
    name="FRONTNASAL-SUTURE_AR",
    origin=Origin.BREGMA,
    axis_unit=SizeUnit.MM,
    axes=[
        Axis(name=AxisName.AP, direction=Direction.PA),
        Axis(name=AxisName.ML, direction=Direction.LR),
    ],
)


# Position: from frontonasal suture, 3.1 mm anterior, 0.5 mm lateral to the right
thermistor_implant = ThermistorImplant(
    implanted_device=thermistor_assembly,
    relative_position=[AnatomicalRelative.ANTERIOR, AnatomicalRelative.RIGHT],
    local_coordinate_system=thermistor_coordinate_system,
    transform=[
        Translation(
            translation=[3.1, 0.5],  # 3.1 mm anterior, 0.5 mm lateral to the right
        )
    ],
)

surgery = Surgery(
    start_date=date(2026, 6, 30),
    experimenters=["Dr. Dan"],
    ethics_review_id="1234",
    anaesthesia=Anaesthetic(anaesthetic_type="Isoflurane", duration=60, level=1.5),
    procedures=[thermistor_implant],
)

p = Procedures(
    subject_id="000000",
    global_coordinate_system=procedures_coordinate_system,
    subject_procedures=[surgery],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = p.model_dump_json()
    deserialized = Procedures.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="thermistor", output_directory=args.output_dir)
