#!/usr/bin/env python
"""
Script to generate documentation for AIND data schema.
"""

import os
import json


from aind_data_schema.core.metadata import CORE_FILES


def process_core_file(core_file):
    """
    Copy a core file from the base_files directory to the docs/source/ folder
    and append the contents of all generated model documentation files in the corresponding directory.
    
    Args:
        core_file: Name of the core file to process (e.g., "data_description")
    """
    # Define paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    base_file_path = os.path.join(base_dir, 'docs_base', 'base_files', f'{core_file}.md')
    output_file_path = os.path.join(base_dir, 'docs', 'source', f'{core_file}.md')
    model_docs_dir = os.path.join(
        base_dir,
        'docs_base',
        'models',
        'aind_data_schema',
        'core',
        core_file
    )
    
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
    with open(base_file_path, 'r') as base_file:
        base_content = base_file.read()
    
    # Load model link map
    link_map_path = os.path.join(base_dir, "docs_base", "models", "model_links.json")
    with open(link_map_path, "r") as f:
        model_link_map = json.load(f)
    
    # Find all .md files in the model_docs_dir
    md_files = sorted([f for f in os.listdir(model_docs_dir) if f.endswith('.md')])
    
    if not md_files:
        print(f"Warning: No markdown files found in: {model_docs_dir}")
    
    # Read and process all model content
    all_model_content = []
    for md_file in md_files:
        model_doc_path = os.path.join(model_docs_dir, md_file)
        with open(model_doc_path, 'r') as model_doc:
            model_content = model_doc.read()

        # Apply the link map replacements
        for link in model_link_map:
            # Replace the link in the model content
            model_content = model_content.replace(link, model_link_map[link])
        
        all_model_content.append(model_content)
    
    # Combine the content
    combined_content = base_content
    for content in all_model_content:
        combined_content += f"\n\n{content}"
    
    # Write to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(combined_content)
    
    print(f"Documentation generated for {core_file} with {len(md_files)} files: {output_file_path}")


def generate_all_core_documentation():
    """
    Generate documentation for all core files defined in CORE_FILES.
    """
    for core_file in CORE_FILES:
        process_core_file(core_file)


if __name__ == "__main__":
    generate_all_core_documentation()
