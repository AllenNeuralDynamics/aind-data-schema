""" Helper functions for composability """

import logging
from typing import Any, List, Optional


def merge_process_graph(
    graph1: Optional[dict],
    graph2: Optional[dict],
    processes1: List[Any],
    processes2: List[Any],
) -> Optional[dict]:
    """Merge two process dependency graphs"""

    # Merge process graphs - start with self's graph and update with other's graph
    if graph1 and graph2:
        merged_graph = graph1.copy()
        merged_graph.update(graph2)
    elif graph1 and not graph2:
        merged_graph = graph1.copy()
        # Add entries for other's processes
        for process in processes2:
            merged_graph[process.name] = []
    elif graph2 and not graph1:
        merged_graph = graph2.copy()
        # Add entries for self's processes
        for process in processes1:
            merged_graph[process.name] = []
    else:
        merged_graph = None

    return merged_graph


def merge_str_tuple_lists(
    a: list[str | tuple[str, ...]], b: list[str | tuple[str, ...]]
) -> list[str | tuple[str, ...]]:
    """Merge two lists of strings or tuples of strings such that elements at the
    same index position in both lists are merged into one tuple in the final list"""

    max_len = max(len(a), len(b))
    merged: list[str | tuple[str, ...]] = []

    for i in range(max_len):
        a_elem = a[i] if i < len(a) else None
        b_elem = b[i] if i < len(b) else None

        if a_elem is not None and b_elem is not None:
            if isinstance(a_elem, tuple):
                a_values = a_elem
            else:
                a_values = (a_elem,)

            if isinstance(b_elem, tuple):
                b_values = b_elem
            else:
                b_values = (b_elem,)

            combined = a_values + b_values
            deduped = tuple(dict.fromkeys(combined))
            merged.append(deduped[0] if len(deduped) == 1 else deduped)
        elif a_elem is not None:
            merged.append(a_elem)
        elif b_elem is not None:
            merged.append(b_elem)

    return merged


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
