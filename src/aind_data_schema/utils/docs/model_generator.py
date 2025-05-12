"""Code to generate markdown tables for each model"""

import importlib.util
import inspect
import json
import os
import re
from enum import Enum
from typing import Dict, List, Type

from pydantic import BaseModel

from aind_data_schema.base import DataModel
from aind_data_schema.utils.docs.utils import generate_enum_table

special_cases = {
    "pydantic.types.AwareDatetime": "datetime (timezone-aware)",
    "aind_data_schema_models.organizations": ("[Organization](aind_data_schema_models/organizations.md#organization)"),
    "aind_data_schema_models.modalities": ("[Modality](aind_data_schema_models/modalities.md#modality)"),
    "aind_data_schema_models.brain_atlas": ("[BrainAtlas](aind_data_schema_models/brain_atlas.md#ccfstructure)"),
    "aind_data_schema_models.harp_types": ("[HarpDeviceType](aind_data_schema_models/harp_types.md#harpdevicetype)"),
    "aind_data_schema.core.quality_control.QCMetric": "{QCMetric} or {CurationMetric}",
}

skip_fields = ["object_type", "describedBy", "schema_version"]


def get_model_fields(model: Type[BaseModel], stop_at: Type[BaseModel]) -> Dict[str, tuple]:
    """Collect fields up to (but not including) `stop_at`."""
    field_data = {}

    for cls in inspect.getmro(model):
        if not issubclass(cls, BaseModel) or cls == stop_at:
            break

        annotations = getattr(cls, "__annotations__", {})
        model_fields = getattr(cls, "model_fields", {})

        for name, annotation in annotations.items():
            if any(name.startswith(skip) for skip in skip_fields):
                continue

            if name not in field_data:
                field_info = model_fields.get(name)
                if field_info is not None:
                    field_data[name] = (annotation, field_info)

    return field_data


def check_for_replacement(value: str, in_subdirectory: bool = False) -> str:
    """Check if the value is in special cases and return the replacement.

    Args:
        value: The string to check for replacement
        in_subdirectory: If True, adjust links to go up one directory level
    """
    for special_case, replacement in special_cases.items():
        if special_case in value:
            if in_subdirectory and "aind_data_schema_models/" in replacement:
                # Add ../ prefix to make the link work from subdirectories
                return replacement.replace("aind_data_schema_models/", "../aind_data_schema_models/")
            return replacement
    return value


def check_for_union(value: str) -> str:
    """Extract class names from Annotated types in complex strings and wrap them with {}.

    Example:
    Input: "List[typing.Annotated[aind_data_schema.components.measurements.Calibration |
        aind_data_schema.components.measurements.LiquidCalibration, FieldInfo(...)]]"
    Output: "List[{Calibration} or {LiquidCalibration}]"
    """
    # Check if this is an Annotated type
    if "Annotated" in value:
        # Extract content between Annotated[ and the first , or ] if no comma
        annotated_content_match = re.search(r"Annotated\[(.*?)(?:,|\])", value)
        if annotated_content_match:
            annotated_content = annotated_content_match.group(1)

            # Process union types within the annotated content
            if "|" in annotated_content:
                # Split by | and process each type
                types = annotated_content.split("|")
                clean_types = []

                for t in types:
                    # Extract just the class name from the full path
                    class_match = re.search(r"\.([A-Za-z0-9_]+)$", t.strip())
                    if class_match:
                        clean_types.append(f"{{{class_match.group(1)}}}")
                    else:
                        # If pattern doesn't match, use the original trimmed string
                        clean_types.append(f"{{{t.strip()}}}")

                # If this is inside a List or other container, preserve that structure
                list_match = re.match(r"(List|Dict|Optional)\[(.*)", value)
                if list_match:
                    container = list_match.group(1)
                    return f"{container}[{' or '.join(clean_types)}]"

                return " or ".join(clean_types)

    return value


def _get_type_string_helper(tp: Type, origin, args, **kwargs) -> str:
    """Helper function to format the type into a readable string."""
    # Get in_subdirectory parameter or default to False
    in_subdirectory = kwargs.get("in_subdirectory", False)

    if origin is list or origin is List:
        return f"List[{get_type_string(args[0], in_subdirectory=in_subdirectory)}]"
    if origin is dict or origin is Dict:
        return (
            f"Dict[{get_type_string(args[0], in_subdirectory=in_subdirectory)},"
            f" {get_type_string(args[1], in_subdirectory=in_subdirectory)}]"
        )
    union_type = getattr(__import__("typing"), "Union", None)
    if origin is union_type and len(args) == 2 and type(None) in args:
        non_none_type = next(arg for arg in args if arg is not type(None))
        return f"Optional[{get_type_string(non_none_type, in_subdirectory=in_subdirectory)}]"
    if origin is union_type:
        return " or ".join(get_type_string(arg, in_subdirectory=in_subdirectory) for arg in args)

    # Check for annotated types and unions in the string representation
    str_rep = str(tp)
    result = check_for_union(str_rep)

    # Only proceed with normal replacement if check_for_union didn't change anything
    if result == str_rep:
        # Pass in_subdirectory parameter from the calling function
        result = check_for_replacement(str_rep, in_subdirectory=kwargs.get("in_subdirectory", False))

    return result


def get_type_string(tp: Type, in_subdirectory: bool = False) -> str:
    """Format the type into a readable string.

    Args:
        tp: The type to format
        in_subdirectory: If True, adjust links to go up one directory level
    """
    origin = getattr(tp, "__origin__", None)
    args = getattr(tp, "__args__", None)

    if origin is None:
        try:
            # Wrap class names in {} for DataModel subclasses
            if hasattr(tp, "__name__") and issubclass(tp, DataModel):
                return f"{{{tp.__name__}}}"
            # Also wrap Enum types in {} for proper linking
            if hasattr(tp, "__name__") and hasattr(tp, "__members__") and issubclass(tp, Enum):
                return f"{{{tp.__name__}}}"
        except Exception as e:
            print(f"Error checking if {tp} is a DataModel or Enum subclass: {e}")

        str_repr = str(tp)
        if str_repr.startswith("<") and "'" in str_repr:
            # Extract the type name between single quotes
            match = re.search(r"'([^']+)'", str_repr)
            if match:
                return match.group(1)

    return _get_type_string_helper(tp, origin, args, in_subdirectory=in_subdirectory)


def generate_markdown_table(model: Type[BaseModel], stop_at: Type[BaseModel], in_subdirectory: bool = False) -> str:
    """Generate the full markdown table for a model

    Args:
        model: The model to generate documentation for
        stop_at: The parent class to stop at when getting fields
        in_subdirectory: If True, adjust links to go up one directory level
    """
    model_name = model.__name__
    header = f"### {model_name}\n\n"
    docstring = inspect.getdoc(model)
    if docstring:
        header += f"{docstring}\n\n"
    header += "| Field | Type | Description |\n|-------|------|-------------|\n"

    fields = get_model_fields(model, stop_at)
    rows = []
    for name, (annotation, field_info) in fields.items():
        type_str = get_type_string(annotation, in_subdirectory=in_subdirectory)
        desc = field_info.description or ""

        # Check of the type_str includes a markdown link [text](link)
        link_regex = r"\[.*?\]\(.*?\)"
        # Also check if the type_str has {<anything>}
        class_regex = r"\{.*?\}"
        if re.search(link_regex, type_str) or re.search(class_regex, type_str):
            # type str has a link, don't break the link
            rows.append(f"| `{name}` | {type_str} | {desc} |")
        else:
            rows.append(f"| `{name}` | `{type_str}` | {desc} |")

    return header + "\n".join(rows) + "\n"


def process_module(module_name, module_path, src_folder, doc_folder, current_script_path, model_link_map):
    """Process a single module to generate markdown documentation."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        rel_dir_path = os.path.splitext(os.path.relpath(module_path, src_folder))[0]

        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            # Check if the attribute is a DataModel subclass AND is defined in this module
            if (
                isinstance(attr, type)
                and issubclass(attr, DataModel)
                and attr is not DataModel
                and attr.__module__ == module_name
            ):
                process_data_model(attr, rel_dir_path, doc_folder, model_link_map)
            elif isinstance(attr, type) and issubclass(attr, Enum) and attr.__module__ == module_name:
                process_enum(attr, rel_dir_path, doc_folder, model_link_map)
    except Exception as e:
        print(f"Error processing {module_path}: {e}")


def process_data_model(attr, rel_dir_path, doc_folder, model_link_map):
    """Generate markdown documentation for a DataModel."""
    is_component = "components" in rel_dir_path
    markdown_output = generate_markdown_table(attr, BaseModel, in_subdirectory=is_component)

    target_dir = os.path.join(doc_folder, rel_dir_path)
    os.makedirs(target_dir, exist_ok=True)

    output_file = os.path.join(target_dir, f"{attr.__name__}.md")
    with open(output_file, "w") as f:
        f.write(markdown_output)

    doc_rel_path = rel_dir_path.replace(os.sep, "/")
    link = f"[{attr.__name__}]({doc_rel_path}.md#{attr.__name__.lower()})"
    link = link.replace("aind_data_schema/core/", "").replace("aind_data_schema/", "")
    model_link_map[f"{{{attr.__name__}}}"] = link


def process_enum(attr, rel_dir_path, doc_folder, model_link_map):
    """Generate markdown documentation for an Enum."""
    markdown_output = generate_enum_table(attr)

    target_dir = os.path.join(doc_folder, rel_dir_path)
    os.makedirs(target_dir, exist_ok=True)

    output_file = os.path.join(target_dir, f"{attr.__name__}.md")
    with open(output_file, "w") as f:
        f.write(markdown_output)

    doc_rel_path = rel_dir_path.replace(os.sep, "/")
    link = f"[{attr.__name__}]({doc_rel_path}.md#{attr.__name__.lower()})"
    link = link.replace("aind_data_schema/core/", "").replace("aind_data_schema/", "")
    model_link_map[f"{{{attr.__name__}}}"] = link


def save_model_link_map(doc_folder, model_link_map):
    """Save the model link map as a JSON file."""
    link_map_path = os.path.join(doc_folder, "model_links.json")
    with open(link_map_path, "w") as f:
        json.dump(model_link_map, f, indent=2)
    print(f"Model link map saved to {link_map_path}")


if __name__ == "__main__":
    src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    doc_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../docs/base/models"))
    current_script_path = os.path.abspath(__file__)
    model_link_map = {}

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file)

                if os.path.abspath(module_path) == current_script_path:
                    continue

                module_name = os.path.splitext(os.path.relpath(module_path, src_folder))[0].replace(os.sep, ".")
                print(f"Processing module: {module_name}")
                process_module(module_name, module_path, src_folder, doc_folder, current_script_path, model_link_map)

    save_model_link_map(doc_folder, model_link_map)
