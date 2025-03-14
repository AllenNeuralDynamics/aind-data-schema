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


def _recurse_helper(data, axis_order: List[AxisName]):
    """ Helper function for recursive_axis_order_check: recurse calls for lists and objects only """
    if isinstance(data, list):
        for item in data:
            recursive_axis_order_check(item, axis_order)
        return
    elif hasattr(data, "__dict__"):
        for attr_name, attr_value in data.__dict__.items():
            if attr_name == "object_type":
                continue  # skip object_type
            if callable(attr_value):
                continue  # skip methods

            recursive_axis_order_check(attr_value, axis_order)


def recursive_axis_order_check(data, systems: Dict[str, List[AxisName]]):
    """Recursively check fields, see if they match a List[FloatAxis]"""

    if not data:
        return

    # Check if data matches an ordered axis type
    if isinstance(data, list) and all(hasattr(item, "object_type") and item.object_type == "Float axis" for item in data):
        data_order = [axis.axis for axis in data]
        if not check_order(data_order, axis_order):
            raise ValueError(
                f"Axis order mismatch: {data_order} does not match the Instrument's coordinate system {axis_order}"
            )

    _recurse_helper(data, axis_order)
    # implicit return if data is not a list or object
