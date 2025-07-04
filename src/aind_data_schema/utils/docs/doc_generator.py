#!/usr/bin/env python
"""
Script to generate documentation for AIND data schema.
"""

import json
import os

from aind_data_schema.core.metadata import CORE_FILES


def process_core_file(core_file):
    """
    Copy a core file from the base_files directory to the docs/source/ folder
    and append the contents of all generated model documentation files in the corresponding directory.

    Args:
        core_file: Name of the core file to process (e.g., "data_description")
    """
    # Define paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    base_file_path = os.path.join(base_dir, "docs", "base", "core", f"{core_file}.md")
    output_file_path = os.path.join(base_dir, "docs", "source", f"{core_file}.md")
    model_docs_dir = os.path.join(base_dir, "docs", "base", "models", "aind_data_schema", "core", core_file)

    # Check if files exist
    if not os.path.exists(base_file_path):
        print(f"Warning: Base file not found: {base_file_path}")
        return
    if not os.path.exists(model_docs_dir):
        print(f"Warning: Model documentation directory not found: {model_docs_dir}")
        return

    # Copy the base file to the output location
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Read content from base file
    with open(base_file_path, "r") as base_file:
        base_content = base_file.read()

    # Load model link map
    link_map_path = os.path.join(base_dir, "docs", "base", "models", "model_links.json")
    with open(link_map_path, "r") as f:
        model_link_map = json.load(f)

    # Find all .md files in the model_docs_dir
    md_files = sorted([f for f in os.listdir(model_docs_dir) if f.endswith(".md")])

    # Bring the core file to the front of the md_files list
    # core file format is "data_description"
    # file name format is "DataDescription.md"
    # Convert snake_case to PascalCase (e.g., "data_description" to "DataDescription.md")
    file_name = "".join(word.capitalize() for word in core_file.split("_")) + ".md"

    # Move the core model file to the front if it exists
    print((file_name, md_files))
    if file_name in md_files:
        md_files.remove(file_name)
        md_files.insert(0, file_name)

    if not md_files:
        print(f"Warning: No markdown files found in: {model_docs_dir}")

    # Read and process all model content
    all_model_content = []
    for md_file in md_files:
        model_doc_path = os.path.join(model_docs_dir, md_file)
        with open(model_doc_path, "r") as model_doc:
            model_content = model_doc.read()

        all_model_content.append(model_content)

    # Combine the content
    # Start with the core file content
    combined_content = base_content + "\n## Core file\n\n" + all_model_content[0]

    if not core_file == "metadata" and len(all_model_content) > 1:
        combined_content += "\n\n## Model definitions"
        for content in all_model_content[1:]:
            combined_content += f"\n\n{content}"

    # Apply the link map replacements
    for link in model_link_map:
        # Replace the link in the model content
        replacement = model_link_map[link]
        # Remove the core file name from the replacement link, to avoid circular references
        replacement = replacement.replace(f"/{core_file}.md", "")
        combined_content = combined_content.replace(link, replacement)

    # Write to the output file
    with open(output_file_path, "w") as output_file:
        output_file.write(combined_content)

    print(f"Documentation generated for {core_file} with {len(md_files)} files: {output_file_path}")


def process_components(component_folder, output_rel_path):
    """
    Process a component folder and generate a markdown file with all models in that folder.

    Args:
        component_folder: Name of the component folder to process (e.g., "configs")
    """
    # Define paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    component_docs_dir = os.path.join(
        base_dir, "docs", "base", "models", "aind_data_schema", "components", component_folder
    )
    output_dir = os.path.join(base_dir, output_rel_path)
    output_file_path = os.path.join(output_dir, f"{component_folder}.md")

    # Check if directory exists
    if not os.path.exists(component_docs_dir):
        print(f"Warning: Component documentation directory not found: {component_docs_dir}")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load model link map
    link_map_path = os.path.join(base_dir, "docs", "base", "models", "model_links.json")
    with open(link_map_path, "r") as f:
        model_link_map = json.load(f)

    # Find all .md files in the component_docs_dir
    md_files = sorted([f for f in os.listdir(component_docs_dir) if f.endswith(".md")])

    if not md_files:
        print(f"Warning: No markdown files found in: {component_docs_dir}")
        return

    # Create the content with headers
    capitalized_name = component_folder.capitalize()
    combined_content = f"# {capitalized_name}\n\n## Model definitions\n\n"

    # Read and process all model content
    for md_file in md_files:
        model_doc_path = os.path.join(component_docs_dir, md_file)
        with open(model_doc_path, "r") as model_doc:
            model_content = model_doc.read()

        combined_content += f"{model_content}\n\n"

    # Apply the link map replacements
    for link in model_link_map:
        replacement = model_link_map[link]

        # Remove the component folder, we're already in it
        replacement = replacement.replace("components/", "")

        # If we aren't linking out of the component folder, remove the component folder from the link
        if "aind_data_schema_models/" not in replacement:
            replacement = replacement.replace(f"{component_folder}.md", "")

        combined_content = combined_content.replace(link, replacement)

    # Deal with special cases which are incorrectly linked too deep
    combined_content = combined_content.replace("(aind_data_schema_models/", "(../aind_data_schema_models/")

    # Write to the output file
    with open(output_file_path, "w") as output_file:
        output_file.write(combined_content)

    print(f"Documentation generated for component {component_folder} with {len(md_files)} files: {output_file_path}")


def generate_all_component_documentation():
    """
    Generate documentation for all component folders.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    components_dir = os.path.join(base_dir, "docs", "base", "models", "aind_data_schema", "components")

    if not os.path.exists(components_dir):
        print(f"Warning: Components directory not found: {components_dir}")
        return

    component_folders = [d for d in os.listdir(components_dir) if os.path.isdir(os.path.join(components_dir, d))]

    for component_folder in component_folders:
        process_components(component_folder, os.path.join("docs", "source", "components"))


def process_registry(registry_folder, output_rel_path):
    """Process a registry folder and generate a markdown file with all models in that folder.

    Args:
        registry_folder: Name of the registry folder to process
        output_rel_path: Relative path to the output directory
    """
    # Define paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    registry_docs_dir = os.path.join(base_dir, "docs", "base", "models", "aind_data_schema_models", registry_folder)
    output_dir = os.path.join(base_dir, output_rel_path)
    output_file_path = os.path.join(output_dir, f"{registry_folder}.md")

    # Check if directory exists
    if not os.path.exists(registry_docs_dir):
        print(f"Warning: Registry documentation directory not found: {registry_docs_dir}")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load model link map
    link_map_path = os.path.join(base_dir, "docs", "base", "models", "model_links.json")
    with open(link_map_path, "r") as f:
        model_link_map = json.load(f)

    # Find all .md files in the registry_docs_dir
    md_files = sorted([f for f in os.listdir(registry_docs_dir) if f.endswith(".md")])

    if not md_files:
        print(f"Warning: No markdown files found in: {registry_docs_dir}")
        return

    # Create the content with headers
    capitalized_name = registry_folder.capitalize()
    combined_content = f"# {capitalized_name}\n\n## Model definitions\n\n"

    # Read and process all model content
    for md_file in md_files:
        model_doc_path = os.path.join(registry_docs_dir, md_file)
        with open(model_doc_path, "r") as model_doc:
            model_content = model_doc.read()

        # Apply the link map replacements
        for link in model_link_map:
            model_content = model_content.replace(link, model_link_map[link])

        combined_content += f"{model_content}\n\n"

    # Write to the output file
    with open(output_file_path, "w") as output_file:
        output_file.write(combined_content)

    print(f"Documentation generated for registry {registry_folder} with {len(md_files)} files: {output_file_path}")


def generate_all_registry_documentation():
    """Generate documentation for registries folders"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    registries_dir = os.path.join(base_dir, "docs", "base", "models", "aind_data_schema_models")

    if not os.path.exists(registries_dir):
        print(f"Warning: Registry directory not found: {registries_dir}")
        return

    registry_folders = [d for d in os.listdir(registries_dir) if os.path.isdir(os.path.join(registries_dir, d))]

    for registry_folder in registry_folders:
        process_registry(registry_folder, os.path.join("docs", "source", "aind_data_schema_models"))


def generate_all_core_documentation():
    """
    Generate documentation for all core files defined in CORE_FILES.
    """
    for core_file in CORE_FILES:
        process_core_file(core_file)

    process_core_file("metadata")


if __name__ == "__main__":
    generate_all_core_documentation()
    generate_all_component_documentation()
    generate_all_registry_documentation()
