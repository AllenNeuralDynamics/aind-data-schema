""" Validator utility functions """

import logging
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Union

from aind_data_schema.components.wrappers import AssetPath

# Fields that should have the same length as the coordinate system axes
AXIS_TYPES = ["Translation", "Rotation", "Scale"]


class TimeValidation(Enum):
    """Enum for time validation types."""

    BETWEEN = "between"
    """Time should be between start and end."""
    AFTER = "after"
    """Time should be after the start time."""
    BEFORE = "before"
    """Time should be before the end time."""


def subject_specimen_id_compatibility(subject_id: str, specimen_id: str) -> bool:
    """Check whether a subject_id and specimen_id are compatible"""
    return subject_id in specimen_id


def recursive_time_validation_check(data, acquisition_start_time=None, acquisition_end_time=None):
    """Recursively check fields for TimeValidation annotations and validate against acquisition times.

    Parameters
    ----------
    data : Any
        The data structure to check recursively
    acquisition_start_time : Optional[datetime]
        The acquisition start time to validate against
    acquisition_end_time : Optional[datetime]
        The acquisition end time to validate against
    """
    if not data:
        return

    # Check if this object has fields with TimeValidation annotations
    if hasattr(data, "__annotations__") and hasattr(data, "__dict__"):
        for field_name, field_value in data.__dict__.items():
            if field_name in getattr(data, "__annotations__", {}):
                # Check if the field has TimeValidation annotation
                annotation = data.__annotations__[field_name]
                if hasattr(annotation, "__metadata__"):
                    for metadata in annotation.__metadata__:
                        if isinstance(metadata, TimeValidation):
                            # Validate the field value against the time constraint
                            if field_value and acquisition_start_time and acquisition_end_time:
                                _validate_time_constraint(
                                    field_value, metadata, acquisition_start_time, acquisition_end_time, field_name
                                )

    # Recursively check nested structures
    _time_validation_recurse_helper(data, acquisition_start_time, acquisition_end_time)


def _convert_to_comparable(value, reference_datetime):
    """Convert date to datetime using the timezone from reference, or return as-is if already datetime"""
    if isinstance(value, date) and not isinstance(value, datetime):
        # Convert date to datetime at midnight with same timezone as reference
        return datetime.combine(value, datetime.min.time()).replace(tzinfo=reference_datetime.tzinfo)
    return value


def _validate_time_constraint(field_value, time_validation, start_time, end_time, field_name):
    """Validate a single time field against the specified constraint."""

    # Convert field_value to be comparable with start_time and end_time
    comparable_field_value = _convert_to_comparable(field_value, start_time)

    if time_validation == TimeValidation.BETWEEN:
        if not (start_time <= comparable_field_value <= end_time):
            raise ValueError(
                f"Field '{field_name}' with value {field_value} must be between {start_time} and {end_time}"
            )
    elif time_validation == TimeValidation.AFTER:
        if comparable_field_value <= start_time:
            raise ValueError(f"Field '{field_name}' with value {field_value} must be after {start_time}")
    elif time_validation == TimeValidation.BEFORE:
        if comparable_field_value >= end_time:
            raise ValueError(f"Field '{field_name}' with value {field_value} must be before {end_time}")


def _time_validation_recurse_helper(data, acquisition_start_time, acquisition_end_time):
    """Helper function for recursive_time_validation_check: recurse calls for lists and objects only"""
    if isinstance(data, list):
        for item in data:
            recursive_time_validation_check(item, acquisition_start_time, acquisition_end_time)
        return
    elif hasattr(data, "__dict__"):
        for attr_name, attr_value in data.__dict__.items():
            if attr_name == "object_type":
                continue  # skip object_type
            if callable(attr_value):
                continue  # skip methods

            recursive_time_validation_check(attr_value, acquisition_start_time, acquisition_end_time)


def _recurse_helper(data, **kwargs):
    """Helper function for recursive coordinate system validation.

    Recursively processes lists and objects, calling recursive_coord_system_check
    on each element or attribute.

    Parameters
    ----------
    data : Any
        The data structure to process recursively
    **kwargs
        Keyword arguments passed to recursive_coord_system_check
    """
    if isinstance(data, list):
        for item in data:
            recursive_coord_system_check(item, **kwargs)
        return
    elif hasattr(data, "__dict__"):
        for attr_name, attr_value in data.__dict__.items():
            if attr_name == "object_type":
                continue  # skip object_type
            if callable(attr_value):
                continue  # skip methods

            recursive_coord_system_check(attr_value, **kwargs)


def _system_check_helper(data, coordinate_system_name: Optional[str], axis_count: Optional[int]):
    """Helper function to validate coordinate system requirements for objects with transforms.

    Only validates coordinate system requirements if the object contains transform components
    (Translation, Rotation, or Scale). Objects without transforms don't require coordinate systems.

    Parameters
    ----------
    data : object
        The object to validate
    coordinate_system_name : Optional[str]
        Expected coordinate system name (can be None if no transforms present)
    axis_count : Optional[int]
        Expected number of axes in the coordinate system (can be None if no transforms present)

    Raises
    ------
    ValueError
        If coordinate system is required but missing, system name doesn't match,
        or transform field length doesn't match axis count
    """
    # First check if this object has any transform components
    has_transforms = False
    transform_components = []
    object_type = getattr(data, "object_type", type(data).__name__)

    if hasattr(data, "__dict__"):
        for attr_name, attr_value in data.__dict__.items():
            # Check if the attribute's class name is one of the AXIS_TYPES
            if hasattr(attr_value, "__class__") and attr_value.__class__.__name__ in AXIS_TYPES:
                has_transforms = True
                transform_components.append(attr_value)

    # Only require coordinate system if there are transforms present
    if has_transforms:
        if not coordinate_system_name or not axis_count:
            raise ValueError(
                f"CoordinateSystem is required when a Transform or Coordinate is present (object_type: {object_type})"
            )

        if data.coordinate_system_name not in coordinate_system_name:
            raise ValueError(
                f"System name mismatch for {object_type}, expected {coordinate_system_name}, "
                f"found {data.coordinate_system_name}"
            )

        # Check lengths of transform fields match axis count
        for transform_component in transform_components:
            field_name = transform_component.__class__.__name__.lower()
            sub_data = getattr(data, field_name, None)
            # Check if the object has the corresponding field and if it's a list with correct length
            if sub_data and hasattr(sub_data, field_name):
                field_value = getattr(sub_data, field_name)
                if len(field_value) != axis_count:
                    raise ValueError(
                        f"Axis count mismatch for {object_type}, expected {axis_count} axes, "
                        f"but found {len(field_value)}"
                    )


def recursive_coord_system_check(data, coordinate_system_name: Optional[str], axis_count: Optional[int]):
    """Recursively validate coordinate system requirements for objects with transforms.

    Traverses the data structure and validates that objects with transform components
    (Translation, Rotation, Scale) have the correct coordinate system name and that
    transform field lengths match the expected axis count.

    Parameters
    ----------
    data : Any
        The data structure to validate recursively
    coordinate_system_name : Optional[str]
        Expected coordinate system name (can be None if no transforms present)
    axis_count : Optional[int]
        Expected number of axes in the coordinate system (can be None if no transforms present)

    Raises
    ------
    ValueError
        If coordinate system is required but missing, system name doesn't match,
        or transform field length doesn't match axis count

    Notes
    -----
    Objects without transform components are not required to have coordinate systems.
    When a new coordinate_system is encountered in the data, it overrides the provided
    coordinate_system_name and axis_count for subsequent validation.
    """

    if not data:
        return

    if hasattr(data, "coordinate_system") and data.coordinate_system:
        # If we find a new coordinate_system, allow it to over-write our settings
        coordinate_system_name = data.coordinate_system.name
        axis_count = len(data.coordinate_system.axes)

    # Check if the object we are looking at has a coordinate_system_name field
    if hasattr(data, "coordinate_system_name"):
        _system_check_helper(data, coordinate_system_name, axis_count)

    _recurse_helper(data=data, coordinate_system_name=coordinate_system_name, axis_count=axis_count)


def recursive_get_all_names(obj: Any) -> List[str]:
    """Recursively extract all 'name' fields from an object and its nested fields."""
    names = []

    if obj is None or isinstance(obj, Enum):  # Skip None and Enums
        return names

    elif isinstance(obj, list):  # Handle lists
        for item in obj:
            names.extend(recursive_get_all_names(item))

    elif hasattr(obj, "__dict__"):  # Handle objects (including Pydantic models)
        if hasattr(obj, "name") and isinstance(obj.name, str):  # Ensure name is a string
            names.append(obj.name)
        for field_value in vars(obj).values():  # Use vars() for robustness
            names.extend(recursive_get_all_names(field_value))

    return names


def recursive_check_paths(obj: Any, directory: Optional[Path] = None):
    """Recursively check for AssetPath objects and validate their paths.
    This function checks if the paths are absolute and logs a warning if they are.
    It also checks if the paths exist and logs a warning if they do not.
    If the object is a list, tuple, set, or dict, it recursively checks each item.

    Parameters
    ----------
    obj : Any
    directory : Optional[Path], optional
        root directory, by default uses the current working directory
    """
    if isinstance(obj, Enum):
        return

    if isinstance(obj, AssetPath):
        if obj.is_absolute():
            logging.warning(f"AssetPath {obj} is absolute, ensure file paths are relative to the metadata directory")

        full_path = directory / obj if directory else obj
        full_path = Path(full_path)
        if not full_path.exists():
            logging.warning(
                f"AssetPath {full_path} does not exist, ensure file paths are relative to the metadata directory"
            )
    elif isinstance(obj, (list, tuple, set, dict)):
        items = obj.values() if isinstance(obj, dict) else obj
        for item in items:
            recursive_check_paths(item, directory)
    elif hasattr(obj, "__dict__"):
        for value in vars(obj).values():
            recursive_check_paths(value, directory)


def validate_creation_time_after_midnight(
    creation_time: Optional[Union[datetime, date]], reference_time: Optional[datetime]
) -> None:
    """Validate that creation_time is on or after midnight of the reference_time's day.

    Parameters
    ----------
    creation_time : Optional[datetime]
        The creation time to validate (datetime or date objects are supported)
    reference_time : Optional[datetime]
        The reference time to compare against (typically acquisition_end_time)

    Raises
    ------
    ValueError
        If creation_time is before midnight of the reference_time's day
    """
    if not creation_time or not reference_time:
        return

    # Convert date to datetime if needed
    if isinstance(creation_time, date) and not isinstance(creation_time, datetime):
        creation_time = datetime.combine(creation_time, datetime.min.time())

    # If creation_time is timezone-naive (local time),
    # add the same timezone as reference_time
    if isinstance(creation_time, datetime) and creation_time.tzinfo is None and reference_time.tzinfo is not None:
        creation_time = creation_time.replace(tzinfo=reference_time.tzinfo)

    # Get midnight of the reference time day
    reference_date = reference_time.date()
    midnight_of_reference_day = datetime.combine(reference_date, datetime.min.time()).replace(
        tzinfo=reference_time.tzinfo
    )

    # Validate that creation_time is on or after midnight of the reference day
    if isinstance(creation_time, datetime) and creation_time < midnight_of_reference_day:
        raise ValueError(
            f"Creation time ({creation_time}) "
            f"must be on or after midnight of the reference day ({midnight_of_reference_day})"
        )
