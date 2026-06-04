"""Helper functions for metadata inheritance in derived assets"""

from typing import List, Optional, Tuple

from aind_data_schema_models.data_name_patterns import DataLevel

from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.quality_control import QualityControl


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
