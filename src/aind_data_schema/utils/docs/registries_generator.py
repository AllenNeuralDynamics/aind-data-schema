"""Code to generate markdown tables for registry models"""

import inspect
import os
from enum import Enum

# Atlas models
from aind_data_schema_models.atlas import AtlasName
from aind_data_schema_models.brain_atlas import BrainStructureModel, CCFv3

# Coordinates models
from aind_data_schema_models.coordinates import AnatomicalRelative, AxisName, Direction, Origin

# Name patterns
from aind_data_schema_models.data_name_patterns import DataLevel, Group

# Devices models
from aind_data_schema_models.devices import (
    BinMode,
    CameraChroma,
    CameraTarget,
    Cooling,
    Coupling,
    DaqChannelType,
    DataInterface,
    DetectorType,
    DeviceDriver,
    FerruleMaterial,
    FilterType,
    ImagingDeviceType,
    ImmersionMedium,
    LickSensorType,
    MyomatrixArrayType,
    ObjectiveType,
    ProbeModel,
    StageAxisDirection,
)
from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.licenses import License

# Other registry models
from aind_data_schema_models.modalities import Modality

# Organization models
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName

# Processing
from aind_data_schema_models.process_names import ProcessName

# Reagent models
from aind_data_schema_models.reagent import StainType, FluorophoreType

# Registries
from aind_data_schema_models.registries import Registry

# Species models
from aind_data_schema_models.species import Species, Strain
from aind_data_schema_models.specimen_procedure_types import SpecimenProcedureType
from aind_data_schema_models.stimulus_modality import StimulusModality
from aind_data_schema_models.system_architecture import CPUArchitecture, ModelArchitecture, OperatingSystem

# Units models
from aind_data_schema_models.units import (
    AngleUnit,
    ConcentrationUnit,
    CurrentUnit,
    FrequencyUnit,
    MagneticFieldUnit,
    MassUnit,
    MemoryUnit,
    PowerUnit,
    PressureUnit,
    SizeUnit,
    SoundIntensityUnit,
    TemperatureUnit,
    TimeUnit,
    UnitlessUnit,
    SpeedUnit,
    VoltageUnit,
    VolumeUnit,
)

from aind_data_schema.utils.docs.utils import generate_enum_table, save_model_info, update_model_links

# Special case classes that should be processed as model schemas even if they don't contain model instances
MODEL_SCHEMA_CLASSES = [
    "PIDName",
]

registries = [
    # Atlas and brain structure models
    AtlasName,
    BrainStructureModel,
    CCFv3,
    # Name patterns
    DataLevel,
    Group,
    License,
    # Coordinates models
    Origin,
    AxisName,
    Direction,
    AnatomicalRelative,
    # Organization models
    Organization,
    # Process names
    ProcessName,
    # Reagent
    StainType,
    FluorophoreType,
    # Registries
    Registry,
    # Species models
    Species,
    Strain,
    # Units models
    AngleUnit,
    ConcentrationUnit,
    CurrentUnit,
    FrequencyUnit,
    MassUnit,
    MemoryUnit,
    PowerUnit,
    SizeUnit,
    TimeUnit,
    UnitlessUnit,
    VolumeUnit,
    PressureUnit,
    TemperatureUnit,
    SoundIntensityUnit,
    SpeedUnit,
    VoltageUnit,
    MemoryUnit,
    MagneticFieldUnit,
    UnitlessUnit,
    # Devices models
    ImagingDeviceType,
    StageAxisDirection,
    DeviceDriver,
    Coupling,
    DataInterface,
    FilterType,
    CameraChroma,
    DaqChannelType,
    ImmersionMedium,
    ObjectiveType,
    CameraTarget,
    ProbeModel,
    DetectorType,
    Cooling,
    BinMode,
    FerruleMaterial,
    LickSensorType,
    MyomatrixArrayType,
    # Other registry models
    Modality,
    PIDName,
    SpecimenProcedureType,
    StimulusModality,
    ModelArchitecture,
    OperatingSystem,
    CPUArchitecture,
    HarpDeviceType,
]

special_cases = {
    "ADDGENE": "[Addgene](aind_data_schema_models/registries.md#registry)",
    "EMAPA": "[Emapa](aind_data_schema_models/registries.md#registry)",
    "MGI": "[MGI](aind_data_schema_models/registries.md#registry)",
    "NCBI": "[NBCI](aind_data_schema_models/registries.md#registry)",
    "ORCID": "[ORCID](aind_data_schema_models/registries.md#registry)",
    "ROR": "[ROR](aind_data_schema_models/registries.md#registry)",
    "RID": "[RID](aind_data_schema_models/registries.md#registry)",
    "aind_data_schema.components.wrappers.AssetPath": "AssetPath",
}


def generate_model_instance_table(model_class) -> str:
    """Generate a markdown table for any class that contains model instances."""
    model_name = model_class.__name__
    header = generate_table_header(model_class, model_name)
    model_instances, field_names = collect_model_instances_and_fields(model_class)

    if not model_instances:
        print(f"Warning: No model instances found in {model_name}")
        return header

    header += create_table_structure(field_names, model_instances)
    return header


def generate_table_header(model_class, model_name) -> str:
    """Generate the header for the markdown table."""
    header = f"### {model_name}\n\n"
    docstring = inspect.getdoc(model_class)
    if docstring:
        header += f"{docstring}\n\n"
    return header


def collect_model_instances_and_fields(model_class):
    """Collect model instances and determine field names."""
    model_instances = []
    model_instance_types = {}

    for attr_name, attr_value in inspect.getmembers(model_class):
        if is_valid_model_instance(attr_name, attr_value):
            model_instances.append((attr_name, attr_value))
            model_type = attr_value.__class__
            model_instance_types.setdefault(model_type, []).append((attr_name, attr_value))

    field_names = determine_field_names(model_instance_types, model_instances, model_class)
    return model_instances, field_names


def is_valid_model_instance(attr_name, attr_value) -> bool:
    """Check if an attribute is a valid model instance."""
    return (
        not attr_name.startswith("_")
        and not inspect.ismethod(attr_value)
        and not inspect.isfunction(attr_value)
        and hasattr(attr_value, "__class__")
        and hasattr(attr_value.__class__, "__annotations__")
        and "ALL" not in attr_name
        and "ONE_OF" not in attr_name
    )


def determine_field_names(model_instance_types, model_instances, model_class):
    """Determine the field names for the table."""
    if model_instance_types:
        model_type = max(model_instance_types.keys(), key=lambda k: len(model_instance_types[k]))
        field_names = list(model_type.__annotations__.keys()) if hasattr(model_type, "__annotations__") else []
    else:
        field_names = []

    if not field_names and model_instances:
        sample_instance = model_instances[0][1]
        field_names = extract_instance_fields(sample_instance)

    if model_class.__name__ == "Organization":
        field_names = ensure_organization_fields(field_names, model_instances)

    return field_names


def extract_instance_fields(sample_instance):
    """Extract fields from a sample instance."""
    return [
        attr
        for attr in dir(sample_instance)
        if not attr.startswith("_")
        and not callable(getattr(sample_instance, attr))
        and attr
        not in (
            "ALL",
            "ONE_OF",
            "model_config",
            "model_fields",
            "model_computed_fields",
            "model_extra",
            "model_fields_set",
        )
    ]


def ensure_organization_fields(field_names, model_instances):
    """Ensure specific fields are included for the Organization model."""
    sample_instance = model_instances[0][1]
    for key in ["abbreviation", "registry", "registry_identifier"]:
        if hasattr(sample_instance, key) and key not in field_names:
            field_names.append(key)
    return field_names


def create_table_structure(field_names, model_instances) -> str:
    """Create the markdown table structure."""
    header_row = "| Name |" + "".join(f" {field} |" for field in field_names) + "\n"
    separator_row = "|------|" + "------|" * len(field_names) + "\n"

    rows = []
    for attr_name, attr_value in model_instances:
        row_data = []
        for field in field_names:
            field_value = getattr(attr_value, field, "N/A")
            # Check if this is a registry value that needs to be remapped
            if field == "registry" and any(str(field_value) in key for key in special_cases.keys()):
                # Map the registry value to its corresponding special case
                key = next(key for key in special_cases.keys() if str(field_value) in key)

                row_data.append(f" {special_cases[key]} |")
            else:
                row_data.append(f" `{field_value}` |")

        rows.append(f"| `{attr_name}` |" + "".join(row_data))

    return header_row + separator_row + "\n".join(rows) + "\n"


def generate_model_schema_table(model_class) -> str:
    """Generate a markdown table for a Pydantic model schema showing its fields."""
    model_name = model_class.__name__
    header = generate_table_header(model_class, model_name)

    # Get model fields from Pydantic model
    if hasattr(model_class, "model_fields"):
        fields = model_class.model_fields

        if not fields:
            print(f"Warning: No fields found in model schema {model_name}")
            return header

        # Create table structure for model fields
        header_row = "| Field | Type | Description |\n"
        separator_row = "|-------|------|-------------|\n"

        rows = []
        for field_name, field_info in fields.items():
            field_type = str(field_info.annotation) if hasattr(field_info, "annotation") else "Unknown"
            # Clean up the type representation
            field_type = field_type.replace("typing.", "").replace("<class '", "").replace("'>", "")

            description = ""
            if hasattr(field_info, "description") and field_info.description:
                description = field_info.description
            elif hasattr(field_info, "title") and field_info.title:
                description = field_info.title

            rows.append(f"| `{field_name}` | `{field_type}` | {description} |")

        header += header_row + separator_row + "\n".join(rows) + "\n"
    else:
        print(f"Warning: {model_name} does not appear to be a valid Pydantic model")

    return header


def detect_registry_type(registry):
    """Detect the registry type based on its attributes and structure"""
    # Check if it's an Enum subclass
    if issubclass(registry, Enum):
        return "enum"

    # Check if this is a special case model schema class
    if registry.__name__ in MODEL_SCHEMA_CLASSES:
        return "model_schema"

    # Check if it has at least one model instance
    for attr_name, attr_value in inspect.getmembers(registry):
        if attr_name.startswith("_") or inspect.ismethod(attr_value) or inspect.isfunction(attr_value):
            continue

        # If an attribute has __annotations__, it's likely a model instance
        if hasattr(attr_value, "__class__") and hasattr(attr_value.__class__, "__annotations__"):
            return "model_instance"

    # If we can't determine the type, return unknown
    return "unknown"


def generate_registry_docs():
    """Generate markdown docs for registry models"""
    doc_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../docs/base/models"))
    model_link_map = {}

    for registry in registries:
        try:
            # Determine the output directory (use the module path)
            module_name = registry.__module__
            rel_dir_path = module_name.replace(".", os.sep)

            # Detect registry type
            registry_type = detect_registry_type(registry)

            # Generate the appropriate table based on registry type
            if registry_type == "enum":
                output = generate_enum_table(registry)
            elif registry_type == "model_instance":
                output = generate_model_instance_table(registry)
            elif registry_type == "model_schema":
                output = generate_model_schema_table(registry)
            else:
                print(f"Unknown registry type for {registry.__name__}")
                continue

            # Save the model and update the link map
            save_model_info(registry.__name__, output, rel_dir_path, doc_folder, model_link_map)
        except Exception as e:
            print(f"Error processing registry {registry.__name__}: {str(e)}")

    # Update the model links file
    update_model_links(doc_folder, model_link_map)
    print("Registry documentation generated successfully.")


if __name__ == "__main__":
    generate_registry_docs()
