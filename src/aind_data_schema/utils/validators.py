""" Validator utility functions """


def subject_specimen_id_compatibility(subject_id: str, specimen_id: str) -> bool:
    """Check whether a subject_id and specimen_id are compatible"""
    return subject_id in specimen_id


def _recurse_helper(data, system_name: str):
    """Helper function for recursive_axis_order_check: recurse calls for lists and objects only"""
    if isinstance(data, list):
        for item in data:
            recursive_coord_system_check(item, system_name)
        return
    elif hasattr(data, "__dict__"):
        for attr_name, attr_value in data.__dict__.items():
            if attr_name == "object_type":
                continue  # skip object_type
            if callable(attr_value):
                continue  # skip methods

            recursive_coord_system_check(attr_value, system_name)


def recursive_coord_system_check(data, system_name: str):
    """Recursively check fields, see if they are Coordinates and check if they match a List[values]

    Note that we just need to check if the axes all show up, not necessarily in matching order
    """

    if not data:
        return

    # Check if the object we are looking at has a system_name field
    if hasattr(data, "system_name"):
        if data.system_name not in system_name:
            raise ValueError(
                f"System name mismatch: {data.system_name} does not match the top-level coordinate system {system_name}"
            )

    _recurse_helper(data, system_name)
    # implicit return if data is not a list or object
