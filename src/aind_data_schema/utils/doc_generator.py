from typing import Type, List, Dict
from pydantic import BaseModel
import inspect
import os


def get_model_fields(model: Type[BaseModel], stop_at: Type[BaseModel]) -> Dict[str, tuple]:
    """Collect fields up to (but not including) `stop_at`."""
    field_data = {}

    for cls in inspect.getmro(model):
        if not issubclass(cls, BaseModel) or cls == stop_at:
            break

        annotations = getattr(cls, '__annotations__', {})
        model_fields = getattr(cls, 'model_fields', {})

        for name, annotation in annotations.items():
            if name not in field_data:
                field_info = model_fields.get(name)
                if field_info is not None:
                    field_data[name] = (annotation, field_info)

    return field_data


def get_type_string(tp: Type) -> str:
    """Format the type into a readable string."""
    origin = getattr(tp, '__origin__', None)
    args = getattr(tp, '__args__', None)

    if origin is None:
        try:
            if hasattr(tp, '__name__') and issubclass(tp, DataModel):
                return f"{{{tp.__name__}}}"  # Wrap class names in {} for DataModel subclasses
        except:
            pass
        return str(tp)
    if origin is list or origin is List:
        return f"List[{get_type_string(args[0])}]"
    if origin is dict or origin is Dict:
        return f"Dict[{get_type_string(args[0])}, {get_type_string(args[1])}]"
    union_type = getattr(__import__('typing'), 'Union', None)
    if origin is union_type and len(args) == 2 and type(None) in args:
        non_none_type = next(arg for arg in args if arg is not type(None))
        return f"Optional[{get_type_string(non_none_type)}]"
    if origin is union_type:
        return " | ".join(get_type_string(arg) for arg in args)
    return str(tp)


def generate_markdown_table(model: Type[BaseModel], stop_at: Type[BaseModel]) -> str:
    model_name = model.__name__
    header = f"## `{model_name}`\n\n"
    docstring = inspect.getdoc(model)
    if docstring:
        header += f"{docstring}\n\n"
    header += "| Field | Type | Description |\n|-------|------|-------------|\n"

    fields = get_model_fields(model, stop_at)
    rows = []
    for name, (annotation, field_info) in fields.items():
        type_str = get_type_string(annotation)
        desc = field_info.description or ""
        rows.append(f"| `{name}` | `{type_str}` | {desc} |")

    return header + "\n".join(rows) + "\n"


def generate_all_docs(base_class: Type[BaseModel], stop_at: Type[BaseModel]) -> str:
    docs = []
    for cls in base_class.__subclasses__():
        if inspect.isabstract(cls):
            continue
        docs.append(generate_markdown_table(cls, stop_at))
    return "\n".join(filter(None, docs))  # Filter out any empty strings


# Example usage
if __name__ == "__main__":
    from aind_data_schema.base import DataModel  # update this with your path
    import importlib.util

    src_folder = "/Users/daniel.birman/proj/aind-data-schema/src"
    doc_folder = "/Users/daniel.birman/proj/aind-data-schema/docs/source/models"

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, src_folder))[0].replace(os.sep, ".")
                
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, DataModel) and attr is not DataModel:
                        markdown_output = generate_markdown_table(attr, BaseModel)
                        output_file = os.path.join(doc_folder, f"{attr.__name__}_docs.md")
                        with open(output_file, "w") as f:
                            f.write(markdown_output)
