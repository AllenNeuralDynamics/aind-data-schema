""" Validator utility functions """

import logging
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional

from aind_data_schema.components.wrappers import AssetPath

# Fields that should have the same length as the coordinate system axes
AXIS_TYPES = ["Translation", "Rotation", "Scale"]


class CoordinateSystemException(Exception):
    """Raised when a coordinate system is missing."""

    def __init__(self):
        """Initialize the exception."""
        super().__init__("CoordinateSystem is required when a Transform or Coordinate is present")


class SystemNameException(Exception):
    """Raised when there is a system name mismatch."""

    def __init__(self, expected, found):
        """Initialize the exception with the expected and found axis counts."""
        self.expected = expected
        self.found = found
        super().__init__(f"System name mismatch, expected {expected}, found {found}")


class AxisCountException(Exception):
    """Raised when the axis count does not match."""

    def __init__(self, expected, found):
        """Initialize the exception with the expected and found axis counts."""
        self.expected = expected
        self.found = found
        super().__init__(f"Axis count mismatch, expected {expected} axes, but found {found}")


def subject_specimen_id_compatibility(subject_id: str, specimen_id: str) -> bool:
    """Check whether a subject_id and specimen_id are compatible"""
    return subject_id in specimen_id


def _recurse_helper(data, **kwargs):
    """Helper function for recursive_axis_order_check: recurse calls for lists and objects only"""
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


def _system_check_helper(data, coordinate_system_name: str, axis_count: int):
    """Helper function to raise errors if the coordinate_system_name or axis_count don't match"""
    if not coordinate_system_name or not axis_count:
        raise CoordinateSystemException()

    if data.coordinate_system_name not in coordinate_system_name:
        raise SystemNameException(coordinate_system_name, data.coordinate_system_name)

    # Check lengths of subfields based on class types
    if hasattr(data, "__dict__"):
        for attr_name, attr_value in data.__dict__.items():
            # Check if the attribute's class name is one of the AXIS_TYPES
            if hasattr(attr_value, "__class__") and attr_value.__class__.__name__ in AXIS_TYPES:
                # Construct the field name by converting the class name to lowercase
                field_name = attr_value.__class__.__name__.lower()
                sub_data = getattr(data, field_name, None)
                # Check if the object has the corresponding field and if it's a list with correct length
                if sub_data and hasattr(sub_data, field_name):
                    field_value = getattr(sub_data, field_name)
                    if len(field_value) != axis_count:
                        raise AxisCountException(axis_count, len(field_value))


def recursive_coord_system_check(data, coordinate_system_name: str, axis_count: int):
    """Recursively check fields, see if they are Coordinates and check if they match a List[values]

    Note that we just need to check if the axes all show up, not necessarily in matching order
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


def recursive_device_name_check(obj: Any, implanted_devices: List[str]):
    """Recursively check for `implanted_device_name` or `implanted_device_names` fields against `implanted_devices`."""

    if isinstance(obj, Enum):
        return

    if hasattr(obj, "implanted_device_name") and obj.implanted_device_name not in implanted_devices:
        raise ValueError(
            f"implanted_device_name {obj.implanted_device_name} not found in implanted_devices {implanted_devices}"
        )

    if hasattr(obj, "implanted_device_names"):
        missing = [name for name in obj.implanted_device_names if name not in implanted_devices]
        if missing:
            raise ValueError(f"implanted_device_names {missing} not found in implanted_devices {implanted_devices}")

    items = (
        vars(obj).values()
        if hasattr(obj, "__dict__")
        else obj.values() if isinstance(obj, dict) else obj if isinstance(obj, (list, tuple, set)) else []
    )

    for item in items:
        recursive_device_name_check(item, implanted_devices)
