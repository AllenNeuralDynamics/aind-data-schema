"""Helper functions for metadata inheritance in derived assets"""

import re
from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple

from aind_data_schema_models.data_name_patterns import DataLevel, DataRegex, datetime_to_name_string
from pydantic_core import PydanticUndefined

from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.quality_control import QualityControl


def _get_or_default(data_description: DataDescription, field_name: str, kwargs: dict) -> Any:
    """
    If the field is set in kwargs, use that value. Otherwise, check if
    the field is set in the DataDescription object. If not, pull from
    the field default value if the field has a default value. Otherwise,
    return None and allow pydantic to raise a Validation Error if field
    is not Optional.
    """
    if kwargs.get(field_name) is not None:
        return kwargs.get(field_name)
    elif hasattr(data_description, field_name) and getattr(data_description, field_name) is not None:
        return getattr(data_description, field_name)
    else:
        default_value = getattr(DataDescription.model_fields.get(field_name), "default")
        if default_value is PydanticUndefined:
            raise ValueError(
                f"Required field {field_name} must have a value "
                "in the original DataDescription or be passed as an argument"
            )
        else:
            return default_value


def derive_data_description_from_raw(
    data_description: DataDescription,
    process_name: str,
    source_data: Optional[List[str]] = None,
    **kwargs,
) -> DataDescription:
    """
    Create a DataLevel.DERIVED DataDescription from a DataLevel.RAW DataDescription object.

    Parameters
    ----------
    data_description : DataDescription
        The DataDescription object to use as the base for the Derived
    process_name : str
        Name of the process that created the data
    kwargs
        DataDescription fields can be explicitly set and will override
        values pulled from DataDescription

    """
    if not data_description.data_level == DataLevel.RAW:
        raise ValueError(f"Input data_description must have data_level=RAW, got {data_description.data_level}")

    creation_time = datetime.now(tz=timezone.utc) if kwargs.get("creation_time") is None else kwargs["creation_time"]

    if not isinstance(creation_time, datetime):
        raise ValueError(f"creation_time({creation_time}) must be a datetime object")

    original_name = data_description.name
    derived_name = f"{original_name}_{process_name}_{datetime_to_name_string(creation_time)}"
    if not re.match(DataRegex.DERIVED.value, derived_name):  # pragma: no cover
        raise ValueError(f"Derived name({derived_name}) does not match allowed Regex pattern")

    return DataDescription(
        subject_id=_get_or_default(data_description, "subject_id", kwargs),
        creation_time=creation_time,
        tags=_get_or_default(data_description, "tags", kwargs),
        name=derived_name,
        institution=_get_or_default(data_description, "institution", kwargs),
        funding_source=_get_or_default(data_description, "funding_source", kwargs),
        data_level=DataLevel.DERIVED,
        group=_get_or_default(data_description, "group", kwargs),
        investigators=_get_or_default(data_description, "investigators", kwargs),
        project_name=_get_or_default(data_description, "project_name", kwargs),
        restrictions=_get_or_default(data_description, "restrictions", kwargs),
        modalities=_get_or_default(data_description, "modalities", kwargs),
        data_summary=_get_or_default(data_description, "data_summary", kwargs),
        source_data=source_data if source_data else [original_name],
    )


def derive_data_description_from_derived(
    data_description: DataDescription,
    process_name: str,
    source_data: Optional[List[str]] = None,
    **kwargs,
) -> DataDescription:
    """
    Create a DataLevel.DERIVED DataDescription from another DataLevel.DERIVED DataDescription object.

    This function extracts the original input name from the existing derived data description
    and uses it as the base for creating a new derived data description, rather than
    chaining derived names.

    Parameters
    ----------
    data_description : DataDescription
        The DERIVED DataDescription object to use as the base for the new Derived
    process_name : str
        Name of the process that created the data
    source_data : Optional[List[str]]
        Optional list of source data names. If None, will use the current data_description.name
    kwargs
        DataDescription fields can be explicitly set and will override
        values pulled from DataDescription

    Returns
    -------
    DataDescription
        New DERIVED DataDescription with name based on the original input, not the full derived name

    """
    if data_description.data_level != DataLevel.DERIVED:
        raise ValueError(f"Input data_description must have data_level=DERIVED, got {data_description.data_level}")

    creation_time = datetime.now(tz=timezone.utc) if kwargs.get("creation_time") is None else kwargs["creation_time"]

    if not isinstance(creation_time, datetime):
        raise ValueError(f"creation_time({creation_time}) must be a datetime object")

    parsed_name = DataDescription.parse_name(data_description.name, DataLevel.DERIVED)
    original_input = parsed_name["input"]

    derived_name = f"{original_input}_{process_name}_{datetime_to_name_string(creation_time)}"
    if not re.match(DataRegex.DERIVED.value, derived_name):  # pragma: no cover
        raise ValueError(f"Derived name({derived_name}) does not match allowed Regex pattern")

    return DataDescription(
        subject_id=_get_or_default(data_description, "subject_id", kwargs),
        creation_time=creation_time,
        tags=_get_or_default(data_description, "tags", kwargs),
        name=derived_name,
        institution=_get_or_default(data_description, "institution", kwargs),
        funding_source=_get_or_default(data_description, "funding_source", kwargs),
        data_level=DataLevel.DERIVED,
        group=_get_or_default(data_description, "group", kwargs),
        investigators=_get_or_default(data_description, "investigators", kwargs),
        project_name=_get_or_default(data_description, "project_name", kwargs),
        restrictions=_get_or_default(data_description, "restrictions", kwargs),
        modalities=_get_or_default(data_description, "modalities", kwargs),
        data_summary=_get_or_default(data_description, "data_summary", kwargs),
        source_data=source_data if source_data else [data_description.name],
    )


def derive_data_description(
    data_description: DataDescription,
    process_name: str,
    source_data: Optional[List[str]] = None,
    **kwargs,
) -> DataDescription:
    """
    Create a DataLevel.DERIVED DataDescription from any DataDescription object.

    Automatically chooses the appropriate function (derive_data_description_from_raw or
    derive_data_description_from_derived) based on the data_level of the input DataDescription.

    Parameters
    ----------
    data_description : DataDescription
        The DataDescription object to use as the base for the new Derived
    process_name : str
        Name of the process that created the data
    source_data : Optional[List[str]]
        Optional list of source data names
    kwargs
        DataDescription fields can be explicitly set and will override
        values pulled from DataDescription

    Returns
    -------
    DataDescription
        New DERIVED DataDescription

    """
    if data_description.data_level == DataLevel.RAW:
        return derive_data_description_from_raw(data_description, process_name, source_data, **kwargs)
    elif data_description.data_level == DataLevel.DERIVED:
        return derive_data_description_from_derived(data_description, process_name, source_data, **kwargs)
    else:
        raise ValueError(f"Unsupported data_level: {data_description.data_level.value}")


def derive_data_description_analyzed(
    data_description: DataDescription,
    analysis_name: str,
    source_data: Optional[List[str]] = None,
    **kwargs,
) -> DataDescription:
    """
    Create a DataLevel.DERIVED DataDescription using the ANALYZED name pattern.

    ANALYZED names follow ``{project_abbreviation}_{analysis_name}_{creation_time}`` and are
    used for derived assets that merge data from multiple acquisitions, where the name is
    based on the project rather than a single source asset.

    Parameters
    ----------
    data_description : DataDescription
        The DataDescription object to use as the base for the new Derived
    analysis_name : str
        Name of the analysis that created the data
    source_data : Optional[List[str]]
        Optional list of source data names
    kwargs
        DataDescription fields can be explicitly set and will override
        values pulled from DataDescription

    Returns
    -------
    DataDescription
        New DERIVED DataDescription with an ANALYZED-style name

    """
    creation_time = datetime.now(tz=timezone.utc) if kwargs.get("creation_time") is None else kwargs["creation_time"]

    if not isinstance(creation_time, datetime):
        raise ValueError(f"creation_time({creation_time}) must be a datetime object")

    project_abbreviation = _get_or_default(data_description, "project_name", kwargs)

    analyzed_name = f"{project_abbreviation}_{analysis_name}_{datetime_to_name_string(creation_time)}"
    if not re.match(DataRegex.ANALYZED.value, analyzed_name):
        raise ValueError(f"Analyzed name({analyzed_name}) does not match allowed Regex pattern")

    return DataDescription(
        subject_id=_get_or_default(data_description, "subject_id", kwargs),
        creation_time=creation_time,
        tags=_get_or_default(data_description, "tags", kwargs),
        name=analyzed_name,
        institution=_get_or_default(data_description, "institution", kwargs),
        funding_source=_get_or_default(data_description, "funding_source", kwargs),
        data_level=DataLevel.DERIVED,
        group=_get_or_default(data_description, "group", kwargs),
        investigators=_get_or_default(data_description, "investigators", kwargs),
        project_name=project_abbreviation,
        restrictions=_get_or_default(data_description, "restrictions", kwargs),
        modalities=_get_or_default(data_description, "modalities", kwargs),
        data_summary=_get_or_default(data_description, "data_summary", kwargs),
        source_data=source_data,
    )


def _get_root_asset_name(data_description: DataDescription) -> Optional[str]:
    """Return the original raw asset name that this data description traces back to"""
    if data_description.data_level == DataLevel.RAW:
        return data_description.name
    if data_description.data_level == DataLevel.DERIVED and data_description.name:
        parsed = DataDescription.parse_name(data_description.name, DataLevel.DERIVED)
        return parsed.get("input")
    return None


def _get_unique_subject_ids(metadata_list) -> List[str]:
    """Extract unique subject IDs from a list of Metadata objects"""
    subject_ids = set()
    for m in metadata_list:
        if m.subject:
            subject_ids.add(m.subject.subject_id)
        elif m.data_description and m.data_description.subject_id:
            subject_ids.add(m.data_description.subject_id)
    return list(subject_ids)


def _get_unique_acquisition_names(metadata_list) -> List[str]:
    """Extract unique root raw asset names from a list of Metadata objects"""
    names = set()
    for m in metadata_list:
        if m.data_description:
            root = _get_root_asset_name(m.data_description)
            if root:
                names.add(root)
    return list(names)


def _is_single_subject(metadata_list) -> bool:
    """Check whether all metadata objects refer to the same subject"""
    return len(_get_unique_subject_ids(metadata_list)) == 1


def _is_single_acquisition(metadata_list) -> bool:
    """Check whether all metadata objects refer to the same acquisition"""
    return len(_get_unique_acquisition_names(metadata_list)) == 1


def _inherit_subject_and_procedures(metadata_list) -> Tuple:
    """Return (subject, procedures) from the first metadata that has them, or (None, None)"""
    if not _is_single_subject(metadata_list):
        return None, None
    for m in metadata_list:
        subject = m.subject
        procedures = m.procedures
        if subject or procedures:
            return subject, procedures
    return None, None


def _inherit_instrument_and_acquisition(metadata_list) -> Tuple:
    """Return (instrument, acquisition) from the first metadata that has them, or (None, None)"""
    if not _is_single_acquisition(metadata_list):
        return None, None
    for m in metadata_list:
        instrument = m.instrument
        acquisition = m.acquisition
        if instrument or acquisition:
            return instrument, acquisition
    return None, None


def _accumulate_processing(
    metadata_list,
    new_processing: Optional[Processing] = None,
) -> Optional[Processing]:
    """Accumulate processing from source metadata and new processing.

    If single acquisition, combine all existing processing with the new one.
    If multiple acquisitions, only return the new processing.
    """
    if not _is_single_acquisition(metadata_list):
        return new_processing

    accumulated = None
    for m in metadata_list:
        if m.processing:
            if accumulated is None:
                accumulated = m.processing
            else:
                accumulated = accumulated + m.processing

    if new_processing:
        if accumulated is None:
            accumulated = new_processing
        else:
            accumulated = accumulated + new_processing

    return accumulated


def _accumulate_quality_control(
    metadata_list,
    new_quality_control: Optional[QualityControl] = None,
) -> Optional[QualityControl]:
    """Accumulate quality control from source metadata and new QC.

    If single acquisition, combine all existing QC with the new one.
    If multiple acquisitions, only return the new QC.
    """
    if not _is_single_acquisition(metadata_list):
        return new_quality_control

    accumulated = None
    for m in metadata_list:
        if m.quality_control:
            if accumulated is None:
                accumulated = m.quality_control
            else:
                accumulated = accumulated + m.quality_control

    if new_quality_control:
        if accumulated is None:
            accumulated = new_quality_control
        else:
            accumulated = accumulated + new_quality_control

    return accumulated
