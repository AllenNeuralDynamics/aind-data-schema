"""Class for holding generic helper functions that are usable within many packages"""
from __future__ import annotations

import inspect
import sys
import json
import warnings
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional, Type
from packaging.version import parse

from aind_data_schema.base import AindCoreModel
from aind_data_schema.data_description import (
    DataDescription,
    DerivedDataDescription,
    Institution,
    Funding,
    Modality,
    ExperimentType,
)


_skip_existing_data_description_keys = [
    "schema_version",
    "version",
    "data_level",
    "described_by",
    "ror_id",
    "creation_time",
    "creation_date",
]


def get_classes(module: Optional[str] = None) -> list:
    """
    Searches for all imported classes and returns those modules in a list
    Parameters
    ----------
    module : Optional[str]
      Name of module to check. If None, weill return calling namespace's imports. Defaults to None.

    Returns
    -------
    list
      List of tuples of class name and class.

    """
    if not module:
        frm = inspect.currentframe().f_back  # Get frame for most recent level of scope (function caller level of scope)
        return inspect.getmembers(sys.modules[frm.f_globals["__name__"]], inspect.isclass)  # getmem for caller scope
    else:
        return inspect.getmembers(sys.modules[module], inspect.isclass)  # getmem for passed __name__ scope


def aind_core_models() -> Iterator[Type[AindCoreModel]]:
    """
    Returns Iterator of AindCoreModel classes
    """
    for model in AindCoreModel.__subclasses__():
        yield model


def create_derived_data_description(
    process_name: str,
    existing_data_description: str | Path | DataDescription | None = None,
    input_data_name: str | None = None,
    subject_id: str = None,
    institution: Institution = Institution.AIND,
    funding_source: list[Funding] = [Funding(funder="AIND")],
    investigators: list = [],
    modality: Modality | None = None,
    experiment_type: list[ExperimentType] | None = None,
):
    """
    Create a new data description from an existing data description, or from scratch if no existing
    data description is provided.

    Parameters
    ----------
    process_name : str
        Name of the process that created the data
    existing_data_description : str | Path | DataDescription | None, optional
        Path to existing data description, or existing data description object, or None if creating
        from scratch, by default None
    input_data_name : str, optional
        Name of the input data, by default None
    subject_id : str, optional
        Subject ID, by default None
    institution : Institution, optional
        Institution, by default Institution.AIND
    funding_source : Funding, optional
        Funding source, by default Funding(funder="AIND")
    investigators : list, optional
        List of investigators, by default []
    modality : Modality | None, optional
        Modality, by default None
    experiment_type : list[ExperimentType] | None, optional
        Experiment type, by default None

    Returns
    -------
    DerivedDataDescription
        The derived data description
    """
    now = datetime.now()
    # make base dictionary form scratch
    base_data_description_dict = {}
    base_data_description_dict["creation_time"] = now.time()
    base_data_description_dict["creation_date"] = now.date()
    base_data_description_dict["institution"] = institution
    base_data_description_dict["investigators"] = investigators
    base_data_description_dict["funding_source"] = funding_source

    if existing_data_description is None:
        assert modality is not None, "Must provide modality if creating new data description"
        assert experiment_type is not None, "Must provide experiment type if creating new data description"
        assert input_data_name is not None, "Must provide input_data_name if creating new data description"
        assert subject_id is not None, "Must provide subject ID if creating new data description"
        base_data_description_dict["modality"] = modality
        base_data_description_dict["experiment_type"] = experiment_type
        base_data_description_dict["input_data_name"] = input_data_name
        base_data_description_dict["subject_id"] = subject_id
    else:
        if isinstance(existing_data_description, (str, Path)):
            assert Path(existing_data_description).is_file(), "Must provide path to existing data description file"
            with open(existing_data_description, "r") as data_description_file:
                data_description_json = json.load(data_description_file)
            data_description = DataDescription.construct(**data_description_json)
        else:
            assert isinstance(
                existing_data_description, DataDescription
            ), "Must provide existing DataDescription object"
            data_description = existing_data_description
        # construct data_description.json
        existing_data_description_dict = data_description.dict()
        existing_version = existing_data_description_dict.get("schema_version")
        if existing_version is not None and parse(existing_version) < parse("0.4.0"):
            existing_data_description_dict["institution"] = Institution(existing_data_description_dict["institution"])
            existing_data_description_dict["modality"] = [Modality(existing_data_description_dict["modality"])]
            assert experiment_type is not None, "Must provide experiment type if existing data description is < 0.4.0"
            existing_data_description_dict["experiment_type"] = experiment_type
        else:
            existing_data_description_dict["institution"] = Institution(
                existing_data_description_dict["institution"]["abbreviation"]
            )
        # check that funder is validated
        funding_source = existing_data_description_dict.get("funding_source")
        if funding_source is not None:
            for funding in funding_source:
                funder = funding["funder"]
                institution_abbrvs = [inst.value.abbreviation for inst in Institution]
                institution_names = [inst.value.name for inst in Institution]
                if funder not in institution_abbrvs:
                    if funder not in institution_names:
                        warnings.warn(f"{funder} is not a valid funder. Using AIND as default")
                        funding["funder"] = institution
                    else:
                        funding["funder"] = institution_abbrvs[institution_names.index(funder)]

        for key in _skip_existing_data_description_keys:
            if key in existing_data_description_dict:
                del existing_data_description_dict[key]
        base_data_description_dict.update(existing_data_description_dict)
        base_data_description_dict["input_data_name"] = existing_data_description_dict["name"]

    derived_data_description = DerivedDataDescription(process_name=process_name, **base_data_description_dict)
    return derived_data_description
