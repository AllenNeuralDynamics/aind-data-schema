"""Code to generate markdown tables for each model"""

import importlib.util
import inspect
import json
import os
import re
from enum import Enum
from typing import Dict, List, Optional, Type, get_origin, get_args

from pydantic import BaseModel

from aind_data_schema.base import DataModel, GenericModel
from aind_data_schema.utils.docs.utils import generate_enum_table

special_cases = {
    "pydantic.types.AwareDatetime": "datetime (timezone-aware)",
    "aind_data_schema_models.organizations": ("[Organization](aind_data_schema_models/organizations.md#organization)"),
    "aind_data_schema_models.modalities": ("[Modality](aind_data_schema_models/modalities.md#modality)"),
    "aind_data_schema_models.brain_atlas": ("[BrainAtlas](aind_data_schema_models/brain_atlas.md#ccfv3)"),
    "aind_data_schema_models.harp_types": ("[HarpDeviceType](aind_data_schema_models/harp_types.md#harpdevicetype)"),
    "aind_data_schema_models.species._C57Bl_6J": "[Strain](aind_data_schema_models/species.md#strain)",
    "aind_data_schema_models.species._Callithrix_Jacchus": "[Species](aind_data_schema_models/species.md#species)",
    "aind_data_schema.core.quality_control.QCMetric": "{QCMetric} or {CurationMetric}",
    "aind_data_schema.components.wrappers.AssetPath": "AssetPath",
    "aind_data_schema.base.GenericModel": "dict",
    "aind_data_schema_models.mouse_anatomy.MouseAnatomyModel": (
        "[MouseAnatomyModel](aind_data_schema_models/external" ".md#mouseanatomymodel)"
    ),
    "aind_data_schema_models.pid_names.PIDName": "{PIDName}",
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


def check_for_replacement(value: str) -> str:
    """Check if the value is in special cases and return the replacement.

    Args:
        value: The string to check for replacement
    """
    for special_case, replacement in special_cases.items():
        if special_case in value:
            return replacement
    return value


def check_for_union(value: str) -> str:
    """Extract class names from complex strings and replace pipe symbols with 'or'.

    Examples:
    Input: "List[typing.Annotated[aind_data_schema.components.measurements.Calibration |
        aind_data_schema.components.measurements.LiquidCalibration, FieldInfo(...)]]"
    Output: "List[{Calibration} or {LiquidCalibration}]"

    Input: "List[float | str]"
    Output: "List[float or str]"
    """
    # Check direct pipe syntax first (handles List[float | str] case)
    container_match = re.match(r"(List|Dict|Optional|Set|Tuple|Sequence)\[(.*)\]", value)
    if container_match and "|" in container_match.group(2):
        container = container_match.group(1)
        content = container_match.group(2)
        # Replace pipes with 'or' in the content but maintain the structure
        content_with_or = re.sub(r"\s*\|\s*", " or ", content)
        return f"{container}[{content_with_or}]"

    # Check if this is a direct union type without container (like 'float | str')
    elif "|" in value and not any(x in value for x in ["Annotated", "List[", "Dict[", "Optional["]):
        # Replace pipes with 'or'
        return re.sub(r"\s*\|\s*", " or ", value)

    # Check if this is an Annotated type
    elif "Annotated" in value:
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


def _get_type_string_helper(tp, origin, args, **kwargs) -> str:
    """Helper function to format the type into a readable string."""

    if origin is list or origin is List:
        return f"List[{get_type_string(args[0])}]"
    if origin is dict or origin is Dict:
        return f"Dict[{get_type_string(args[0])}," f" {get_type_string(args[1])}]"
    union_type = getattr(__import__("typing"), "Union", None)
    if origin is union_type and len(args) == 2 and type(None) in args:
        non_none_type = next(arg for arg in args if arg is not type(None))
        return f"Optional[{get_type_string(non_none_type)}]"
    if origin is union_type:
        return " or ".join(get_type_string(arg) for arg in args)

    # Handle Literal types - extract the string content directly if it's a string literal
    literal_type = getattr(__import__("typing"), "Literal", None)
    if origin is literal_type:
        # If there's only one argument and it's a string, return just the string content
        if len(args) == 1 and isinstance(args[0], str):
            return f'"{args[0]}"'
        # Otherwise return all literal values joined with 'or'
        return " or ".join(f'"{arg}"' if isinstance(arg, str) else str(arg) for arg in args)

    # Check for annotated types and unions in the string representation
    str_rep = str(tp)
    result = check_for_union(str_rep)

    # Check for special cases
    result = check_for_replacement(result)

    return result


def _handle_annotated_type(origin, args) -> Optional[str]:
    """Handle annotated types"""
    if origin is not None and hasattr(origin, "__name__") and origin.__name__ == "Annotated":
        if args and len(args) >= 2:
            # Check if the second argument is NOT a FieldInfo (Pydantic field annotation)
            # If it's not FieldInfo, it's likely simple metadata we want to unwrap
            second_arg = args[1]
            is_field_info = hasattr(second_arg, "__class__") and second_arg.__class__.__name__ == "FieldInfo"

            if not is_field_info:
                # This is a simple metadata annotation like TimeValidation.BEFORE
                # Unwrap it to just the first type
                return get_type_string(args[0])
            # If it IS FieldInfo, fall through to normal processing
    return None


def _handle_class_types(tp) -> Optional[str]:
    """Handle class types (DataModel, GenericModel, Enum subclasses)"""
    try:
        # Wrap class names in {} for DataModel subclasses
        if hasattr(tp, "__name__") and issubclass(tp, DataModel):
            return check_for_replacement(f"{{{tp.__name__}}}")
        # Also wrap GenericModel subclasses in {} for proper linking (but not GenericModel itself)
        if hasattr(tp, "__name__") and issubclass(tp, GenericModel) and tp is not GenericModel:
            return check_for_replacement(f"{{{tp.__name__}}}")
        # Also wrap Enum types in {} for proper linking
        if hasattr(tp, "__name__") and hasattr(tp, "__members__") and issubclass(tp, Enum):
            return check_for_replacement(f"{{{tp.__name__}}}")
    except Exception as e:
        print(f"Error checking if {tp} is a DataModel, GenericModel, or Enum subclass: {e}")
    return None


def get_type_string(tp) -> str:
    """Format the type into a readable string.

    Args:
        tp: The type to format
    """
    # Use get_origin and get_args for proper type inspection
    origin = get_origin(tp)
    args = get_args(tp)

    # Handle Annotated types - but only unwrap if it's a simple metadata annotation
    annotated_result = _handle_annotated_type(origin, args)
    if annotated_result is not None:
        return annotated_result

    # Fallback to old behavior for compatibility
    if origin is None:
        origin = getattr(tp, "__origin__", None)
        args = getattr(tp, "__args__", None)

    if origin is None:
        # Try to handle class types
        class_result = _handle_class_types(tp)
        if class_result is not None:
            return class_result

        str_repr = str(tp)
        if str_repr.startswith("<") and "'" in str_repr:
            # Extract the type name between single quotes
            match = re.search(r"'([^']+)'", str_repr)
            if match:
                return check_for_replacement(match.group(1))

    return _get_type_string_helper(tp, origin, args)


def generate_markdown_table(model: Type[BaseModel], stop_at: Type[BaseModel]) -> str:
    """Generate the full markdown table for a model

    Args:
        model: The model to generate documentation for
        stop_at: The parent class to stop at when getting fields
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
        type_str = get_type_string(annotation)
        desc = field_info.description or ""

        # Check if field is deprecated
        is_deprecated = hasattr(field_info, "deprecated") and field_info.deprecated

        # Format field name with strikethrough if deprecated
        field_name = f"<del>`{name}`</del>" if is_deprecated else f"`{name}`"

        # Prefix description with [DEPRECATED] if deprecated
        if is_deprecated:
            deprecated_msg = field_info.deprecated if isinstance(field_info.deprecated, str) else ""
            desc = f"**[DEPRECATED]** {deprecated_msg}. {desc}".strip()

        # Check of the type_str includes a markdown link [text](link)
        link_regex = r"\[.*?\]\(.*?\)"
        # Also check if the type_str has {<anything>}
        class_regex = r"\{.*?\}"
        if re.search(link_regex, type_str) or re.search(class_regex, type_str):
            # type str has a link, don't break the link
            rows.append(f"| {field_name} | {type_str} | {desc} |")
        else:
            rows.append(f"| {field_name} | `{type_str}` | {desc} |")

    return header + "\n".join(rows) + "\n"


def clear_directory(path):
    """Clear all files in the given directory."""
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root, file))


def process_module(module_name, module_path, src_folder, doc_folder, model_link_map):
    """Process a single module to generate markdown documentation."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        rel_dir_path = os.path.splitext(os.path.relpath(module_path, src_folder))[0]

        output_path = os.path.join(doc_folder, rel_dir_path)

        clear_directory(output_path)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            # Check if the attribute is defined in this module
            if not isinstance(attr, type) or not attr.__module__ == module_name:
                continue

            # Check if the attribute is a DataModel subclass, GenericModel subclass, or an Enum
            if issubclass(attr, DataModel) and attr is not DataModel:
                process_data_model(attr, rel_dir_path, doc_folder, model_link_map)
            elif issubclass(attr, GenericModel) and attr is not GenericModel:
                process_data_model(attr, rel_dir_path, doc_folder, model_link_map)
            elif issubclass(attr, Enum) and attr is not Enum:
                process_enum(attr, rel_dir_path, doc_folder, model_link_map)
    except Exception as e:
        print(f"Error processing {module_path}: {e}")


def process_data_model(attr, rel_dir_path, doc_folder, model_link_map):
    """Generate markdown documentation for a DataModel or GenericModel subclass."""
    markdown_output = generate_markdown_table(attr, BaseModel)

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
                process_module(module_name, module_path, src_folder, doc_folder, model_link_map)

    save_model_link_map(doc_folder, model_link_map)
