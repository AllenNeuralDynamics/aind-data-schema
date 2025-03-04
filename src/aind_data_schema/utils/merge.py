""" Helper functions for composability """
from typing import Optional


def merge_notes(notes1: Optional[str], notes2: Optional[str]) -> Optional[str]:
    """ Merge two notes strings """

    if notes1 and notes2:
        notes = notes1 + "\n" + notes2
    else:
        notes = notes1 if notes1 else notes2
    return notes
