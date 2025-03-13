""" Validator utility functions """

from typing import List
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


def recursive_axis_order_check(data, axis_order: List[AxisName]):
    """Recursively check fields, see if they match a List[FloatAxis]"""

    if not data or not hasattr(data, "__dict__"):
        return  # If data is not a class, return

    # Check if data matches an ordered axis type
    print(data)
    if isinstance(data, list) and all(isinstance(item, FloatAxis) for item in data):
        print((data, axis_order))
        if not check_order([axis.axis for axis in data], axis_order):
            raise ValueError(
                f"Axis order mismatch: {data} does not match the Instrument's coordinate system axes order"
            )

    for attr_name, attr_value in data.__dict__.items():
        if attr_name == "object_type":
            continue

        # Skip methods and other callables
        if callable(attr_value):
            continue

        # Recurse through lists and other objects
        if isinstance(attr_value, list):
            for item in attr_value:
                recursive_axis_order_check(item, axis_order)
        else:
            recursive_axis_order_check(attr_value, axis_order)
