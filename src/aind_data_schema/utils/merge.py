""" Helper functions for composability """

import logging
from typing import Any, List, Optional


def remove_duplicates(lst: List[Any]) -> List[Any]:
    """Remove duplicates from a list while preserving order"""
    seen = set()

    output_list = [x for x in lst if not (x in seen or seen.add(x))]

    if len(output_list) != len(lst):
        logging.info(f"Removed {len(lst) - len(output_list)} duplicates from list")
    return output_list


def merge_optional_list(a: Optional[List[Any]], b: Optional[List[Any]]) -> Optional[List[Any]]:
    """Merge two Optional[List[Any]] values"""

    merged = (a or []) + (b or [])
    return merged or None


def merge_notes(notes1: Optional[str], notes2: Optional[str]) -> Optional[str]:
    """Merge two notes strings"""

    if notes1 and notes2:
        notes = notes1 + "\n" + notes2
    else:
        notes = notes1 if notes1 else notes2
    return notes


def merge_coordinate_systems(cs1: Optional[Any], cs2: Optional[Any]) -> Optional[Any]:
    """Merge two coordinate system strings"""

    if cs1 and cs2:
        if cs1 != cs2:
            raise ValueError(f"Cannot merge differing coordinate systems: '{cs1.name}' and '{cs2.name}'")
        return cs1
    else:
        return cs1 if cs1 else cs2
