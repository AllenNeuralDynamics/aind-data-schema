""" Helper functions for composability """

from typing import Any, List, Optional


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
