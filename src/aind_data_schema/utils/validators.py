""" Validator utility functions """

from typing import Dict, List
from aind_data_schema.components.coordinates import AxisName, FloatAxis


def subject_specimen_id_compatibility(subject_id: str, specimen_id: str) -> bool:
    """Check whether a subject_id and specimen_id are compatible"""
    return subject_id in specimen_id


def check_order(axes_to_check: List[AxisName], order: List[AxisName]):
    """Check that the order of axes matches a defined order"""
    for axis0, axis1 in zip(axes_to_check, order):
        if axis0 != axis1:
            return False
    return True


def _recurse_helper(data, system_name: str, system_axes: List[AxisName]):
    """ Helper function for recursive_axis_order_check: recurse calls for lists and objects only """
    if isinstance(data, list):
        for item in data:
            recursive_axis_order_check(item, system_name, system_axes)
        return
    elif hasattr(data, "__dict__"):
        for attr_name, attr_value in data.__dict__.items():
            if attr_name == "object_type":
                continue  # skip object_type
            if callable(attr_value):
                continue  # skip methods

            recursive_axis_order_check(attr_value, system_name, system_axes)


def recursive_axis_order_check(data, system_name: str, system_axes: List[AxisName]):
    """Recursively check fields, see if they are Coordinates and check if they match a List[FloatAxis]

    Note that we just need to check if the axes all show up, not necessarily in matching order
    """

    if not data:
        return

    # Check if the object we are looking at has a system_name field
    if hasattr(data, "system_name"):
        if data.system_name != system_name:
            raise ValueError(
                f"System name mismatch: {data.system_name} does not match the top-level coordinate system {system_name}"
            )

    # Check if data matches an ordered axis type
    if isinstance(data, list) and all(hasattr(item, "object_type") and item.object_type == "Float axis" for item in data):
        data_axes = [axis.axis for axis in data]
        if not all(axis in system_axes for axis in data_axes):
            raise ValueError(
                f"Axis mismatch: at least one of {data_axes} does not appear in {system_axes}"
            )

    _recurse_helper(data, system_name, system_axes)
    # implicit return if data is not a list or object
