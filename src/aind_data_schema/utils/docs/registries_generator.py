"""Code to generate markdown tables for registry models"""
import os
import inspect
from enum import Enum
from typing import Dict, List, Any, Type, Optional

from aind_data_schema_models.atlas import AtlasName
from aind_data_schema_models.brain_atlas import CCFStructure, BrainStructureModel

from aind_data_schema.utils.docs.utils import (
    generate_enum_table,
    save_model_info,
    update_model_links
)

registries = [AtlasName, CCFStructure]


def generate_ccf_structure_table(ccf_structure_class) -> str:
    """Generate a markdown table for the CCFStructure class"""
    model_name = ccf_structure_class.__name__
    header = f"### {model_name}\n\n"
    docstring = inspect.getdoc(ccf_structure_class)
    if docstring:
        header += f"{docstring}\n\n"
    
    # Find the first BrainStructureModel instance to use as reference
    reference_model = None
    for attr_name, attr_value in inspect.getmembers(ccf_structure_class):
        if not attr_name.startswith("_") and isinstance(attr_value, BrainStructureModel):
            reference_model = attr_value
            break
    
    if not reference_model:
        print(f"Warning: No BrainStructureModel instances found in {model_name}")
        return header
        
    field_names = list(reference_model.__class__.__annotations__.keys())
    
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
    for attr_name, attr_value in inspect.getmembers(ccf_structure_class):
        # Skip private attributes and non-BrainStructureModel instances
        if attr_name.startswith("_") or not isinstance(attr_value, BrainStructureModel):
            continue
        
        row = f"| `{attr_name}` |"
        for field in field_names:
            value = getattr(attr_value, field)
            row += f" `{value}` |"
        rows.append(row)
    
    return header + "\n".join(rows) + "\n"


def generate_registry_docs():
    """Generate markdown docs for registry models"""
    doc_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../docs/base/models"))
    model_link_map = {}
    
    for registry in registries:
        # Determine the output directory (use the module path)
        module_name = registry.__module__
        rel_dir_path = module_name.replace(".", os.sep)
        
        # Generate the appropriate table based on registry type
        if issubclass(registry, Enum):
            # Generate enum table
            output = generate_enum_table(registry)
        elif registry is CCFStructure:
            # Generate CCF Structure table
            output = generate_ccf_structure_table(registry)
        else:
            print(f"Unknown registry type: {registry.__name__}")
            continue
        
        # Save the model and update the link map
        save_model_info(registry.__name__, output, rel_dir_path, doc_folder, model_link_map)
    
    # Update the model links file
    update_model_links(doc_folder, model_link_map)
    print(f"Registry documentation generated successfully.")


if __name__ == "__main__":
    generate_registry_docs()
