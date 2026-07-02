"""Generate a markdown bullet-tree of all core schema fields"""

import enum
import importlib
import types as builtin_types
import typing
from typing import Annotated, Union, get_args, get_origin

from aind_data_schema import core
from aind_data_schema.base import DataCoreModel, _GenericModel

for _mod in core.__loader__.get_resource_reader().contents():
    if "__" not in _mod and _mod.endswith(".py"):
        importlib.import_module(f"aind_data_schema.core.{_mod.replace('.py', '')}")

_SKIP_FIELDS = {"object_type", "describedBy", "schema_version"}


def _discriminated_str(types: list) -> str:
    """Return a string representation for a list of types that are part of a discriminated union."""
    bases = {t.__bases__[0] for t in types if isinstance(t, type) and t.__bases__}
    registry_bases = {b for b in bases if "aind_data_schema_models" in getattr(b, "__module__", "")}
    if len(registry_bases) == 1:
        return next(iter(registry_bases)).__name__.removesuffix("Model")
    names = [_annotation_to_str(t) for t in types]
    return "ONE OF: " + ", ".join(names)


def _annotation_to_str(annotation) -> str:
    """Return a string representation of a type annotation."""
    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is Annotated:
        return _annotation_to_str(args[0])

    if origin is Union or isinstance(annotation, builtin_types.UnionType):
        args = get_args(annotation)
        non_none = [a for a in args if a is not type(None)]
        has_none = len(non_none) < len(args)
        inner = _annotation_to_str(non_none[0]) if len(non_none) == 1 else _discriminated_str(non_none)
        return f"Optional[{inner}]" if has_none else inner

    if origin is list:
        return f"LIST OF: {_annotation_to_str(args[0])}"

    if origin is dict:
        k = _annotation_to_str(args[0]) if args else "any"
        v = _annotation_to_str(args[1]) if len(args) > 1 else "any"
        return f"dict[{k}, {v}]"

    if isinstance(annotation, type):
        if annotation is _GenericModel:
            return "dict"
        return annotation.__name__

    return str(annotation)


def _extract_expandable_types(annotation) -> list:
    """Return all locally-defined DataModel types embedded in an annotation."""
    from pydantic import BaseModel

    origin = get_origin(annotation)

    if origin is Annotated:
        return _extract_expandable_types(get_args(annotation)[0])

    if origin is Union or isinstance(annotation, builtin_types.UnionType):
        result = []
        for a in get_args(annotation):
            if a is not type(None):
                result.extend(_extract_expandable_types(a))
        return result

    if origin is list:
        return _extract_expandable_types(get_args(annotation)[0])

    if (
        isinstance(annotation, type)
        and annotation is not _GenericModel
        and issubclass(annotation, BaseModel)
        and annotation.__module__.startswith("aind_data_schema.")
    ):
        return [annotation]

    return []


def _extract_named_types(annotation) -> list:
    """Return every named class (model or enum) embedded in an annotation, from either
    aind_data_schema or aind_data_schema_models, for documentation-link purposes.

    Broader than :func:`_extract_expandable_types`: it also picks up enums and
    registry classes from aind_data_schema_models, which have their own docs page but
    aren't locally-defined models we can recurse into within the diagram.
    """
    from pydantic import BaseModel

    origin = get_origin(annotation)

    if origin is Annotated:
        return _extract_named_types(get_args(annotation)[0])

    if origin is Union or isinstance(annotation, builtin_types.UnionType):
        result = []
        for a in get_args(annotation):
            if a is not type(None):
                result.extend(_extract_named_types(a))
        return result

    if origin in (list, dict):
        result = []
        for a in get_args(annotation):
            result.extend(_extract_named_types(a))
        return result

    if (
        isinstance(annotation, type)
        and annotation is not _GenericModel
        and (issubclass(annotation, BaseModel) or issubclass(annotation, enum.Enum))
    ):
        module = annotation.__module__
        if module.startswith("aind_data_schema.") or module.startswith("aind_data_schema_models."):
            return [annotation]

    return []


def _append_fields(lines: list, model_cls, indent: str, seen: frozenset, depth: int, max_depth: int):
    """Append the fields of a model class to the lines list, including nested models up to the specified maximum depth.

    Args:
        lines (list): The list of strings representing the schema tree.
        model_cls: The model class whose fields are to be appended.
        indent (str): The current indentation level for the fields.
        seen (frozenset): A set of model classes that have already been processed to avoid recursion loops.
        depth (int): The current depth in the schema tree.
        max_depth (int): The maximum depth to expand nested models.
    """
    seen = seen | {model_cls}
    try:
        hints = typing.get_type_hints(model_cls, include_extras=True)
    except Exception:
        return

    for field_name, field_info in model_cls.model_fields.items():
        if field_name in _SKIP_FIELDS:
            continue
        annotation = hints.get(field_name, field_info.annotation)
        type_str = _annotation_to_str(annotation)
        title = field_info.title or field_name
        desc = field_info.description or ""
        req_marker = ", required" if field_info.is_required() else ""
        detail = title + (f": {desc}" if desc else "")
        lines.append(f"{indent}- `{field_name}` ({type_str}{req_marker}) — {detail}")

        if depth < max_depth:
            for t in _extract_expandable_types(annotation):
                if t not in seen:
                    t_desc = (t.__doc__ or "").strip().split("\n")[0]
                    lines.append(f"{indent}  - **{t.__name__}** — {t_desc}")
                    _append_fields(lines, t, indent + "    ", seen, depth + 1, max_depth)


def generate_schema_tree(max_depth: int = 2) -> str:
    """Generate a textual tree representation of the schema for all DataCoreModel subclasses.

    Each model is represented with its fields, types, and descriptions, expanding nested models
    up to the specified maximum depth.
    """
    lines = []
    for model in sorted(DataCoreModel.__subclasses__(), key=lambda m: m.__name__):
        description = (model.__doc__ or "").strip().split("\n")[0]
        lines.append(f"- **{model.__name__}** — {description}")
        model_depth = 0 if model.__name__ == "Metadata" else max_depth
        _append_fields(lines, model, "  ", frozenset(), depth=0, max_depth=model_depth)
    return "\n".join(lines)


def _model_key(model_cls) -> str:
    """A stable, unique identifier for a model class."""
    return f"{model_cls.__module__}.{model_cls.__qualname__}"


def _doc_url(model_cls) -> str:
    """The docs page + anchor for a model class, matching the layout produced by
    ``aind_data_schema.utils.docs.model_generator`` (core files get a top-level page,
    everything else gets a page per module under its top-level package folder).
    """
    module = model_cls.__module__
    for prefix in ("aind_data_schema.", "aind_data_schema_models."):
        prefix_len = len(prefix)
        if module.startswith(prefix):
            parts = module[prefix_len:].split(".")
            if prefix == "aind_data_schema." and parts[0] == "core":
                doc_path = parts[1]
            elif prefix == "aind_data_schema_models.":
                doc_path = "aind_data_schema_models/" + parts[0]
            else:
                doc_path = "/".join(parts)
            return f"{doc_path}.html#{model_cls.__name__.lower()}"
    return ""


def _build_model_entry(model_cls) -> tuple:
    """Build the JSON-able entry describing a single model's fields.

    Returns the entry dict plus the list of distinct model classes referenced
    by its fields, so the caller can continue a breadth-first traversal.
    """
    try:
        hints = typing.get_type_hints(model_cls, include_extras=True)
    except Exception:
        hints = {}

    fields = []
    referenced = []
    for field_name, field_info in model_cls.model_fields.items():
        if field_name in _SKIP_FIELDS:
            continue
        annotation = hints.get(field_name, field_info.annotation)
        type_str = _annotation_to_str(annotation)

        expandable = []
        for t in _extract_expandable_types(annotation):
            if t not in expandable:
                expandable.append(t)
        referenced.extend(expandable)

        named = []
        for t in _extract_named_types(annotation):
            if t not in named:
                named.append(t)

        # A field's `links` cover every named type it touches: local models get a `key`
        # so the popup can drill into them in-app, while enums and aind_data_schema_models
        # registry classes only get a `url` out to their own docs page.
        links = [
            {
                "key": _model_key(t) if t in expandable else None,
                "label": t.__name__,
                "url": _doc_url(t),
            }
            for t in named
        ]

        fields.append(
            {
                "name": field_name,
                "title": field_info.title or field_name,
                "typeStr": type_str,
                "required": field_info.is_required(),
                "description": field_info.description or "",
                "links": links,
            }
        )

    description = (model_cls.__doc__ or "").strip().split("\n")[0]
    entry = {
        "name": model_cls.__name__,
        "description": description,
        "docUrl": _doc_url(model_cls),
        "fields": fields,
    }
    return entry, referenced


# Preferred display order for the core files around the Metadata hub node.
_CORE_FILE_ORDER = [
    "DataDescription",
    "Subject",
    "Procedures",
    "Instrument",
    "Acquisition",
    "Processing",
    "QualityControl",
    "Model",
]


def generate_schema_diagram_data() -> dict:
    """Build the data backing the interactive schema React Flow diagram.

    Traverses every model reachable from ``Metadata`` and returns a JSON-able
    dict of ``{root, coreFiles, models}`` where ``models`` maps a stable model
    key to its field list (with links to other models for expandable fields).
    """
    root_cls = next(m for m in DataCoreModel.__subclasses__() if m.__name__ == "Metadata")

    models = {}
    visited = set()
    queue = [root_cls]
    while queue:
        model_cls = queue.pop(0)
        key = _model_key(model_cls)
        if key in visited:
            continue
        visited.add(key)
        entry, referenced = _build_model_entry(model_cls)
        models[key] = entry
        for t in referenced:
            if _model_key(t) not in visited:
                queue.append(t)

    core_classes = {m.__name__: m for m in DataCoreModel.__subclasses__() if m.__name__ != "Metadata"}
    ordered_names = _CORE_FILE_ORDER + sorted(set(core_classes) - set(_CORE_FILE_ORDER))
    core_files = [_model_key(core_classes[name]) for name in ordered_names if name in core_classes]

    return {"root": _model_key(root_cls), "coreFiles": core_files, "models": models}


def write_schema_diagram_json(output_path) -> None:
    """Write the schema diagram data to ``output_path`` as JSON."""
    import json
    from pathlib import Path

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(generate_schema_diagram_data(), indent=2))


if __name__ == "__main__":
    # Print to an output file
    with open("schema_tree.md", "w") as f:
        f.write(generate_schema_tree())
