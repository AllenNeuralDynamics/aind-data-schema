"""Generate a markdown bullet-tree of all core schema fields"""

import enum
import importlib
import types as builtin_types
import typing
from typing import Annotated, Union, get_args, get_origin

from aind_data_schema import core
from aind_data_schema.base import DataCoreModel

for _mod in core.__loader__.get_resource_reader().contents():
    if "__" not in _mod and _mod.endswith(".py"):
        importlib.import_module(f"aind_data_schema.core.{_mod.replace('.py', '')}")

_SKIP_FIELDS = {"object_type", "describedBy", "schema_version"}


def _discriminated_str(types: list) -> str:
    bases = {t.__bases__[0] for t in types if isinstance(t, type) and t.__bases__}
    registry_bases = {b for b in bases if "aind_data_schema_models" in getattr(b, "__module__", "")}
    if len(registry_bases) == 1:
        return next(iter(registry_bases)).__name__.removesuffix("Model")
    names = [_annotation_to_str(t) for t in types]
    return "ONE OF: " + ", ".join(names)


def _annotation_to_str(annotation) -> str:
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
        if issubclass(annotation, enum.Enum):
            return annotation.__name__
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
        and issubclass(annotation, BaseModel)
        and annotation.__module__.startswith("aind_data_schema.")
    ):
        return [annotation]

    return []


def _append_fields(lines: list, model_cls, indent: str, seen: frozenset, depth: int, max_depth: int):
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
    lines = []
    for model in sorted(DataCoreModel.__subclasses__(), key=lambda m: m.__name__):
        description = (model.__doc__ or "").strip().split("\n")[0]
        lines.append(f"- **{model.__name__}** — {description}")
        model_depth = 0 if model.__name__ == "Metadata" else max_depth
        _append_fields(lines, model, "  ", frozenset(), depth=0, max_depth=model_depth)
    return "\n".join(lines)


if __name__ == "__main__":
    # Print to an output file
    with open("schema_tree.md", "w") as f:
        f.write(generate_schema_tree())
