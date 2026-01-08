"""Utilities for custom serialization and deserialization of data models"""

from typing import List, Dict, Any


def compress_list_of_dicts_delta(value: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Apply delta compression to a list of dictionaries

    The first dict is stored completely. Subsequent dicts only include
    keys whose values changed compared to the previous dict.

    Delta compression is only applied when all dictionaries have identical keys.
    If keys vary across dictionaries, the list is returned uncompressed.

    Parameters
    ----------
    value : List[Dict[str, Any]]
        List of dictionaries to compress

    Returns
    -------
    Dict[str, Any]
        Dictionary with structure {"_dc": True, "_v": compressed_list}
        where compressed_list has full first dict and deltas for subsequent dicts.
        If compression is not possible, returns {"_dc": False, "_v": value}

    Examples
    --------
    >>> data = [
    ...     {"a": 1, "b": 2},
    ...     {"a": 1, "b": 3},
    ...     {"a": 2, "b": 3},
    ... ]
    >>> result = compress_list_of_dicts_delta(data)
    >>> result["_v"]
    [{'a': 1, 'b': 2}, {'b': 3}, {'a': 2}]
    """
    if not isinstance(value, list) or len(value) <= 1:
        return {"_dc": False, "_v": value}

    first_keys = set(value[0].keys()) if isinstance(value[0], dict) else set()

    for item in value:
        if not isinstance(item, dict) or set(item.keys()) != first_keys:
            return {"_dc": False, "_v": value}

    compressed = [value[0]]

    for i in range(1, len(value)):
        current = value[i]
        previous = value[i - 1]

        delta = {key: val for key, val in current.items() if key not in previous or previous[key] != val}
        compressed.append(delta)

    return {"_dc": True, "_v": compressed}


def expand_list_of_dicts_delta(compressed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Expand delta-compressed list of dictionaries back to full format

    Detects delta-compressed format by looking for the "_dc" marker.
    If _dc is True, expands by carrying forward unchanged values from previous dicts.
    If _dc is False or missing, returns the data as-is.

    Parameters
    ----------
    compressed_data : Dict[str, Any]
        Dictionary with structure {"_dc": bool, "_v": compressed_list}

    Returns
    -------
    List[Dict[str, Any]]
        Fully expanded list of dictionaries. If compression was applied,
        all keys are restored to each dict. If no compression, returns as-is.

    Examples
    --------
    >>> compressed = {"_dc": True, "_v": [{"a": 1, "b": 2}, {"b": 3}, {"a": 2}]}
    >>> expand_list_of_dicts_delta(compressed)
    [{'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 2, 'b': 3}]

    >>> uncompressed = {"_dc": False, "_v": [{"a": 1}, {"b": 2}]}
    >>> expand_list_of_dicts_delta(uncompressed)
    [{'a': 1}, {'b': 2}]
    """
    if not isinstance(compressed_data, dict):
        return compressed_data

    if "_dc" not in compressed_data or "_v" not in compressed_data:
        return compressed_data

    if compressed_data["_dc"] is not True:
        return compressed_data["_v"]

    compressed = compressed_data["_v"]
    if not isinstance(compressed, list) or len(compressed) == 0:
        return compressed

    if not isinstance(compressed[0], dict):
        return compressed

    expanded = [compressed[0].copy() if isinstance(compressed[0], dict) else compressed[0]]

    for i in range(1, len(compressed)):
        if not isinstance(compressed[i], dict):
            expanded.append(compressed[i])
            continue

        if isinstance(expanded[i - 1], dict):
            new_dict = expanded[i - 1].copy()
            new_dict.update(compressed[i])
            expanded.append(new_dict)
        else:
            expanded.append(compressed[i])

    return expanded
