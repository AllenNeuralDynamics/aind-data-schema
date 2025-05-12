"""Shared utilities for documentation generation"""

import inspect
import json
import os
from typing import Dict


def generate_enum_table(enum_class) -> str:
    """Generate a markdown table for Enum classes"""
    model_name = enum_class.__name__
    header = f"### {model_name}\n\n"
    docstring = inspect.getdoc(enum_class)
    if docstring:
        header += f"{docstring}\n\n"
    header += "| Name | Value |\n|------|-------|\n"

    rows = []
    for name, member in enum_class.__members__.items():
        rows.append(f"| `{name}` | `{member.value}` |")

    return header + "\n".join(rows) + "\n"


def save_model_info(
    model_name: str, output: str, rel_dir_path: str, doc_folder: str, model_link_map: Dict[str, str]
) -> None:
    """Save model information to a file and update the link map."""
    # Create the target directory structure
    target_dir = os.path.join(doc_folder, rel_dir_path)
    os.makedirs(target_dir, exist_ok=True)

    # Save the file in the appropriate subdirectory
    output_file = os.path.join(target_dir, f"{model_name}.md")
    with open(output_file, "w") as f:
        f.write(output)

    # Construct the relative documentation path for the link map
    # Convert directory separators to forward slashes for URLs
    doc_rel_path = rel_dir_path.replace(os.sep, "/")

    # Create the link format: "[ClassName](path/to/directory#ClassName)"
    link = f"[{model_name}]({doc_rel_path}.md#{model_name.lower()})"

    # Strip out "aind_data_schema/" and "aind_data_schema/core/" from the links
    link = link.replace("aind_data_schema/core/", "").replace("aind_data_schema/", "")

    # Add to our mapping dictionary using the format "{ClassName}" as the key
    model_link_map[f"{{{model_name}}}"] = link


def update_model_links(doc_folder: str, model_link_map: Dict[str, str]) -> None:
    """Update the model_links.json file with new entries."""
    link_map_path = os.path.join(doc_folder, "model_links.json")

    # If file exists, load and update it
    if os.path.exists(link_map_path):
        with open(link_map_path, "r") as f:
            existing_map = json.load(f)
        existing_map.update(model_link_map)
        model_link_map = existing_map

    # Save the updated model link map
    with open(link_map_path, "w") as f:
        json.dump(model_link_map, f, indent=2)
