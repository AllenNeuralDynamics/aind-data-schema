"""Module to build diagrams of core models"""

import importlib
import sys
from pathlib import Path
from typing import Optional, Type

import erdantic as erd
from pydantic import BaseModel

from aind_data_schema import core
from aind_data_schema.base import AindCoreModel

# Import all modules in core package
for mod in core.__loader__.get_resource_reader().contents():
    if "__" not in mod:
        importlib.import_module(f"aind_data_schema.core.{mod.replace('.py','')}")


def save_diagram(
    model: Type[BaseModel], output_directory: Optional[Path] = None, filename: Optional[str] = None
) -> None:
    """
    Save a BaseModel diagram to a directory.
    Parameters
    ----------
    model : Type[BaseModel]
        Model to create a diagram. For example,
        from aind_data_schema.core.subject import Subject
        model = Subject
    output_directory : Optional[Path]
        If None, will use current working directory.
    filename : Optional[str]
        If None, will use model class name plus '.svg'

    Returns
    -------
    None

    """
    if filename is None:
        output_filename = f"{model.__name__}.svg"
    else:
        output_filename = filename
    if output_directory is None:
        output_path = Path(".") / output_filename
    else:
        output_path = output_directory / output_filename

    diagram = erd.create(model)
    diagram.draw(output_path)


def save_all_core_model_diagrams(output_directory: Optional[Path] = None) -> None:
    """
    Save all the core model diagrams to a directory.
    Parameters
    ----------
    output_directory : Optional[Path]
        Location where to save the diagrams to. Default is current directory

    Returns
    -------
    None

    """
    if output_directory is None:
        output_path = Path(".")
    else:
        output_path = output_directory

    for model in AindCoreModel.__subclasses__():
        filename = model.default_filename().replace(".json", ".svg")
        diagram = erd.create(model)
        diagram.draw(output_path / filename)


if __name__ == "__main__":
    """User defined argument for output directory"""
    args = sys.argv[1:]
    output_directory = None if not args else Path(args[0])
    save_all_core_model_diagrams(output_directory=output_directory)
