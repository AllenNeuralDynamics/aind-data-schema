"""Code to generate markdown tables for each model"""

from typing import Type, List, Dict
from pydantic import BaseModel
import inspect
import os
from aind_data_schema.base import DataModel
import importlib.util
import re


special_cases = {
    "pydantic.types.AwareDatetime": "datetime (timezone-aware)",
    "aind_data_schema_models.organizations": (
        "[Organization](https://github.com/AllenNeuralDynamics/aind-data-schema-"
        "models/blob/main/src/aind_data_schema_models/organizations.py)"
    ),
    "aind_data_schema_models.modalities": (
        "[Modality](https://github.com/AllenNeuralDynamics/aind-data-schema-models"
        "/blob/main/src/aind_data_schema_models/modalities.py)"
    ),
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
    """Check if the value is in special cases and return the replacement."""
    for special_case, replacement in special_cases.items():
        if special_case in value:
            return replacement
    return value


def check_for_union(value: str) -> str:
    """Extract class names from Annotated types in complex strings and wrap them with {}.
    
    Example:
    Input: "List[typing.Annotated[aind_data_schema.components.measurements.Calibration | aind_data_schema.components.measurements.LiquidCalibration, FieldInfo(...)]]"
    Output: "List[{Calibration} | {LiquidCalibration}]"
    """
    # Check if this is an Annotated type
    if "Annotated" in value:
        # Extract content between Annotated[ and the first , or ] if no comma
        annotated_content_match = re.search(r'Annotated\[(.*?)(?:,|\])', value)
        if annotated_content_match:
            annotated_content = annotated_content_match.group(1)
            
            # Process union types within the annotated content
            if "|" in annotated_content:
                # Split by | and process each type
                types = annotated_content.split("|")
                clean_types = []
                
                for t in types:
                    # Extract just the class name from the full path
                    class_match = re.search(r'\.([A-Za-z0-9_]+)$', t.strip())
                    if class_match:
                        clean_types.append(f"{{{class_match.group(1)}}}")
                    else:
                        # If pattern doesn't match, use the original trimmed string
                        clean_types.append(f"{{{t.strip()}}}")
                
                # If this is inside a List or other container, preserve that structure
                list_match = re.match(r'(List|Dict|Optional)\[(.*)', value)
                if list_match:
                    container = list_match.group(1)
                    return f"{container}[{' | '.join(clean_types)}]"
                
                return " | ".join(clean_types)
    
    return value


def _get_type_string_helper(tp: Type, origin, args) -> str:
    """Helper function to format the type into a readable string."""
    if origin is list or origin is List:
        return f"List[{get_type_string(args[0])}]"
    if origin is dict or origin is Dict:
        return f"Dict[{get_type_string(args[0])}, {get_type_string(args[1])}]"
    union_type = getattr(__import__("typing"), "Union", None)
    if origin is union_type and len(args) == 2 and type(None) in args:
        non_none_type = next(arg for arg in args if arg is not type(None))
        return f"Optional[{get_type_string(non_none_type)}]"
    if origin is union_type:
        return " | ".join(get_type_string(arg) for arg in args)

    # Check for annotated types and unions in the string representation
    str_rep = str(tp)
    result = check_for_union(str_rep)
    
    # Only proceed with normal replacement if check_for_union didn't change anything
    if result == str_rep:
        result = check_for_replacement(str_rep)
        
    return result


def get_type_string(tp: Type) -> str:
    """Format the type into a readable string."""
    origin = getattr(tp, "__origin__", None)
    args = getattr(tp, "__args__", None)

    if origin is None:
        try:
            if hasattr(tp, "__name__") and issubclass(tp, DataModel):
                return f"{{{tp.__name__}}}"  # Wrap class names in {} for DataModel subclasses
        except Exception as e:
            print(f"Error checking if {tp} is a DataModel subclass: {e}")

        str_repr = str(tp)
        if str_repr.startswith("<") and "'" in str_repr:
            # Extract the type name between single quotes
            match = re.search(r"'([^']+)'", str_repr)
            if match:
                return match.group(1)

    return _get_type_string_helper(tp, origin, args)


def generate_markdown_table(model: Type[BaseModel], stop_at: Type[BaseModel]) -> str:
    """Generate the full markdown table for a model"""
    model_name = model.__name__
    header = f"### `{model_name}`\n\n"
    docstring = inspect.getdoc(model)
    if docstring:
        header += f"{docstring}\n\n"
    header += "| Field | Type | Description |\n|-------|------|-------------|\n"

    fields = get_model_fields(model, stop_at)
    rows = []
    for name, (annotation, field_info) in fields.items():
        type_str = get_type_string(annotation)
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


# Example usage
if __name__ == "__main__":

    src_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    doc_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../docs/base/models"))

    # Get absolute path of this script to skip it
    current_script_path = os.path.abspath(__file__)

    # Dictionary to store model name to link mappings
    model_link_map = {}

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file)

                # Skip the current script to avoid circular import issues
                if os.path.abspath(module_path) == current_script_path:
                    continue

                # Get the relative module path from src folder
                rel_module_path = os.path.relpath(module_path, src_folder)
                # Convert to directory structure (remove .py extension)
                rel_dir_path = os.path.splitext(rel_module_path)[0]

                module_name = rel_dir_path.replace(os.sep, ".")
                print(f"Processing module: {module_name}")

                try:
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)

                        # Check if the attribute is a DataModel subclass AND is defined in this module
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, DataModel)
                            and attr is not DataModel
                            and attr.__module__ == module_name
                        ):  # Check if defined in current module

                            markdown_output = generate_markdown_table(attr, BaseModel)

                            # Create the target directory structure
                            target_dir = os.path.join(doc_folder, rel_dir_path)
                            os.makedirs(target_dir, exist_ok=True)

                            # Save the file in the appropriate subdirectory
                            output_file = os.path.join(target_dir, f"{attr.__name__}.md")
                            with open(output_file, "w") as f:
                                f.write(markdown_output)

                            # Construct the relative documentation path for the link map
                            # Convert directory separators to forward slashes for URLs
                            doc_rel_path = rel_dir_path.replace(os.sep, "/")

                            # Create the link format: "[ClassName](path/to/directory#ClassName)"
                            link = f"[{attr.__name__}]({doc_rel_path}#{attr.__name__})"

                            # Strip out "aind_data_schema/" and "aind_data_schema/core/" from the links
                            link = link.replace("aind_data_schema/core/", "").replace("aind_data_schema/", "")

                            # Add to our mapping dictionary using the format "{ClassName}" as the key
                            model_link_map[f"{attr.__name__}"] = link
                        else:
                            pass
                except Exception as e:
                    print(f"Error processing {module_path}: {e}")

    # Save the model link map as a JSON file
    import json

    link_map_path = os.path.join(doc_folder, "model_links.json")
    with open(link_map_path, "w") as f:
        json.dump(model_link_map, f, indent=2)

    print(f"Model link map saved to {link_map_path}")
