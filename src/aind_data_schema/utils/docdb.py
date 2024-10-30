""" Utility methods for metadata jsons stored in AWS DocumentDB. """


def is_dict_corrupt(input_dict: dict) -> bool:
    """
    Checks that all the keys, included nested keys, do not contain
    forbidden characters ("$" and ".").

    Parameters
    ----------
    input_dict : dict

    Returns
    -------
    bool
        True if input_dict is not a dict, or if nested keys contain
        forbidden characters. False otherwise.

    """

    def has_corrupt_keys(input) -> bool:
        """Recursively checks nested dictionaries and lists"""
        if isinstance(input, dict):
            for key, value in input.items():
                if "$" in key or "." in key:
                    return True
                elif has_corrupt_keys(value):
                    return True
        elif isinstance(input, list):
            for item in input:
                if has_corrupt_keys(item):
                    return True
        return False

    # Top-level input must be a dictionary
    if not isinstance(input_dict, dict):
        return True
    return has_corrupt_keys(input_dict)
