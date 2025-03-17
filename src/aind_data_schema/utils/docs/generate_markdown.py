import ast
from pydantic import BaseModel, Field
from typing import Any

skip_fields = ["_DESCRIBED_BY_URL", "schema_version", "describedBy"]


# Function to extract fields from Pydantic models
def extract_pydantic_fields(cls_node: ast.ClassDef) -> list:
    fields = []
    for node in cls_node.body:
        # Check if the node is an annotated assignment (field definition)
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                field_name = node.target.id
            elif isinstance(node.target, ast.Attribute):
                field_name = node.target.attr
            else:
                continue

            if field_name in skip_fields:
                continue

            field_value = node.value

            # Check if this field is an instance of Field
            if (isinstance(field_value, ast.Call) and isinstance(field_value.func, ast.Name) and 
                field_value.func.id == "Field"):
                title = None
                description = None
                # Check for 'title' and 'description' arguments
                for keyword in field_value.keywords:
                    if keyword.arg == 'title':
                        title = ast.literal_eval(keyword.value)
                    elif keyword.arg == 'description':
                        description = ast.literal_eval(keyword.value)
                # Assume the type is in the annotation (if present)
                field_type = get_type_annotation(node.annotation)  # Get the type annotation as a string
                fields.append((field_name, field_type, title, description))
    return fields

# Helper function to get type annotation as a string
def get_type_annotation(annotation: ast.AST) -> str:
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Subscript):
        value = get_type_annotation(annotation.value)
        slice = get_type_annotation(annotation.slice)
        return f"{value}[{slice}]"
    elif isinstance(annotation, ast.Attribute):
        return f"{annotation.value.id}.{annotation.attr}"
    elif isinstance(annotation, ast.Tuple):
        return f"({', '.join(get_type_annotation(elt) for elt in annotation.elts)})"
    else:
        return ast.dump(annotation)


# Function to generate markdown table from fields
def generate_markdown_table(class_name: str, fields: list) -> str:
    table = f"### {class_name}\n\n"
    table += "| Field Name | Type | Title | Description |\n"
    table += "|------------|------|-------|-------------|\n"

    for field in fields:
        name, field_type, title, description = field
        table += f"| `{name}` | {field_type or ''} | {title or ''} | {description or ''} |\n"

    return table


# Function to parse Python files and generate markdown for Pydantic models
def parse_pydantic_models(file_paths: list) -> str:
    markdown_content = ""

    for file_path in file_paths:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        for node in tree.body:
            # Check if the node is a class definition
            if isinstance(node, ast.ClassDef):
                # Check if class is a subclass of Pydantic's BaseModel
                if any(base.id == "AindModel" or base.id == "AindCoreModel" for base in node.bases):
                    fields = extract_pydantic_fields(node)
                    markdown_content += generate_markdown_table(node.name, fields)

    return markdown_content


# Example usage
file_paths = ['src/aind_data_schema/core/acquisition.py']  # List of Python files
markdown = parse_pydantic_models(file_paths)

# Print or save the generated markdown
print(markdown)
