"""Code to generate markdown tables for registry models"""

import os
import inspect
from enum import Enum

# Atlas models
from aind_data_schema_models.atlas import AtlasName
from aind_data_schema_models.brain_atlas import CCFStructure

# Name patterns
from aind_data_schema_models.data_name_patterns import DataLevel, Group

# Coordinates models
from aind_data_schema_models.coordinates import Origin, AxisName, Direction, AnatomicalRelative

# Organization models
from aind_data_schema_models.organizations import Organization

# Species models
from aind_data_schema_models.species import Species, Strain

# Units models
from aind_data_schema_models.units import (
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
)

# Other registry models
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.specimen_procedure_types import SpecimenProcedureType
from aind_data_schema_models.stimulus_modality import StimulusModality
from aind_data_schema_models.system_architecture import ModelArchitecture, OperatingSystem, CPUArchitecture
from aind_data_schema_models.mouse_anatomy import MouseAnatomyModel
from aind_data_schema_models.harp_types import HarpDeviceType

from aind_data_schema.utils.docs.utils import generate_enum_table, save_model_info, update_model_links

registries = [
    # Atlas and brain structure models
    AtlasName,
    CCFStructure,
    # Name patterns
    DataLevel,
    Group,
    # Coordinates models
    Origin,
    AxisName,
    Direction,
    AnatomicalRelative,
    # Organization models
    Organization,
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


def generate_model_instance_table(model_class) -> str:
    """Generate a markdown table for any class that contains model instances

    This function replaces the specific CCFStructure table generator with a more generic
    approach that can handle any class that contains model instances like BrainStructureModel,
    Organization, etc.
    """
    model_name = model_class.__name__
    header = f"### {model_name}\n\n"
    docstring = inspect.getdoc(model_class)
    if docstring:
        header += f"{docstring}\n\n"

    # Collect all model instances regardless of type
    model_instances = []
    model_instance_types = {}

    # First pass: collect all instances that have annotations
    for attr_name, attr_value in inspect.getmembers(model_class):
        # Skip special attributes, methods and specific markers
        if (
            attr_name.startswith("_")
            or inspect.ismethod(attr_value)
            or inspect.isfunction(attr_value)
            or "ALL" in attr_name
            or "ONE_OF" in attr_name
        ):
            continue

        # Check if the attribute is a model instance (has __annotations__)
        if hasattr(attr_value, "__class__") and hasattr(attr_value.__class__, "__annotations__"):
            model_instances.append((attr_name, attr_value))

            # Track the model type for later grouping
            model_type = attr_value.__class__
            if model_type not in model_instance_types:
                model_instance_types[model_type] = []
            model_instance_types[model_type].append((attr_name, attr_value))

    print(f"Found {len(model_instances)} model instances in {model_name}")

    if not model_instances:
        print(f"Warning: No model instances found in {model_name}")
        return header

    # If there are multiple types, use the most common one as reference
    model_type = max(model_instance_types.keys(), key=lambda k: len(model_instance_types[k]))
    reference_instances = model_instance_types[model_type]

    # Get field names from the model's annotations and instance attributes
    # First try annotations
    field_names = list(model_type.__annotations__.keys()) if hasattr(model_type, "__annotations__") else []

    # If field_names is empty or incomplete, try to get fields from one instance
    if not field_names and model_instances:
        # Get the first instance
        sample_instance = model_instances[0][1]
        # Get fields from instance (excluding dunder methods and callable attributes)
        instance_fields = [
            attr
            for attr in dir(sample_instance)
            if not attr.startswith("_")
            and not callable(getattr(sample_instance, attr))
            and not attr in ("ALL", "ONE_OF", "model_config", "model_fields")
        ]
        # Add any fields not already in field_names
        for field in instance_fields:
            if field not in field_names:
                field_names.append(field)

    # Handle Organization model specifically - make sure to include abbreviation and registry_identifier
    if model_class.__name__ == "Organization" and model_instances:
        sample_instance = model_instances[0][1]
        for key in ["abbreviation", "registry", "registry_identifier"]:
            if hasattr(sample_instance, key) and key not in field_names:
                field_names.append(key)

    # Create table header with these fields
    header_row = "| Name |"
    for field in field_names:
        header_row += f" {field} |"
    header += header_row + "\n"

    # Add separator row
    separator_row = "|------|"
    for _ in field_names:
        separator_row += "------|"
    header += separator_row + "\n"

    # Populate table rows
    rows = []
    for attr_name, attr_value in model_instances:
        row = f"| `{attr_name}` |"
        for field in field_names:
            try:
                value = getattr(attr_value, field)
                row += f" `{value}` |"
            except AttributeError:
                row += " N/A |"
        rows.append(row)

    return header + "\n".join(rows) + "\n"


def detect_registry_type(registry):
    """Detect the registry type based on its attributes and structure"""
    # Check if it's an Enum subclass
    if issubclass(registry, Enum):
        return "enum"

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
            else:
                print(f"Unknown registry type for {registry.__name__}")
                continue

            # Save the model and update the link map
            save_model_info(registry.__name__, output, rel_dir_path, doc_folder, model_link_map)
        except Exception as e:
            print(f"Error processing registry {registry.__name__}: {str(e)}")

    # Update the model links file
    update_model_links(doc_folder, model_link_map)
    print(f"Registry documentation generated successfully.")


if __name__ == "__main__":
    generate_registry_docs()
