"""Tests for merge utilities"""

import unittest
from unittest.mock import Mock

from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.utils.merge import (
    merge_notes,
    merge_optional_list,
    merge_coordinate_systems,
    merge_str_tuple_lists,
    merge_process_graph,
    merge_str_alphabetical,
)


class TestMergeStrTupleLists(unittest.TestCase):
    """Tests for merge_str_tuple_lists function"""

    def test_empty_lists(self):
        """Test merging two empty lists"""
        result = merge_str_tuple_lists([], [])
        self.assertEqual(result, [])

    def test_first_list_longer(self):
        """Test merging when the first list is longer"""
        a = ["a", "b", "c"]
        b = ["d"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "d"), "b", "c"])

    def test_second_list_longer(self):
        """Test merging when the second list is longer"""
        a = ["a"]
        b = ["b", "c", "d"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b"), "c", "d"])

    def test_tuples_in_both_lists(self):
        """Test merging when both lists contain tuples"""
        a = [("a", "b"), ("c", "d")]
        b = [("e", "f"), ("g", "h")]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "e", "f"), ("c", "d", "g", "h")])

    def test_deduplication_with_tuples(self):
        """Test deduplication when merging tuples"""
        a = [("a", "b"), "c"]
        b = [("b", "d"), "c"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "d"), "c"])


class TestMergeStrAlphabetical(unittest.TestCase):
    """Tests for merge_str_alphabetical function"""

    def test_both_strings_present(self):
        """Test merging when both strings are present"""
        result = merge_str_alphabetical("zebra", "apple")
        self.assertEqual(result, "apple_zebra")

    def test_both_strings_present_reverse_order(self):
        """Test merging with strings in reverse alphabetical order"""
        result = merge_str_alphabetical("apple", "zebra")
        self.assertEqual(result, "apple_zebra")

    def test_identical_strings(self):
        """Test merging identical strings"""
        result = merge_str_alphabetical("test", "test")
        self.assertEqual(result, "test")

    def test_first_string_none(self):
        """Test merging when first string is None"""
        result = merge_str_alphabetical(None, "test")
        self.assertEqual(result, "test")

    def test_second_string_none(self):
        """Test merging when second string is None"""
        result = merge_str_alphabetical("test", None)
        self.assertEqual(result, "test")

    def test_both_strings_none(self):
        """Test merging when both strings are None"""
        result = merge_str_alphabetical(None, None)
        self.assertIsNone(result)

    def test_multiple_words_sorted(self):
        """Test merging with multiple word strings"""
        result = merge_str_alphabetical("instrument_2", "instrument_1")
        self.assertEqual(result, "instrument_1_instrument_2")


class TestMergeNotes(unittest.TestCase):
    """Tests for merge_notes function"""

    def test_both_notes_present(self):
        """Test merging when both notes are present"""
        notes1 = "Note 1"
        notes2 = "Note 2"
        result = merge_notes(notes1, notes2)
        self.assertEqual(result, "Note 1\nNote 2")

    def test_first_note_none(self):
        """Test merging when the first note is None"""
        notes1 = None
        notes2 = "Note 2"
        result = merge_notes(notes1, notes2)
        self.assertEqual(result, "Note 2")

    def test_second_note_none(self):
        """Test merging when the second note is None"""
        notes1 = "Note 1"
        notes2 = None
        result = merge_notes(notes1, notes2)
        self.assertEqual(result, "Note 1")

    def test_both_notes_none(self):
        """Test merging when both notes are None"""
        notes1 = None
        notes2 = None
        result = merge_notes(notes1, notes2)
        self.assertIsNone(result)


class RemoveDuplicatesTests(unittest.TestCase):
    """Tests for remove_duplicates function"""

    def test_empty_list(self):
        """Test with empty list"""
        from aind_data_schema.utils.merge import remove_duplicates

        self.assertEqual(remove_duplicates([]), [])

    def test_no_duplicates(self):
        """Test with list that has no duplicates"""
        from aind_data_schema.utils.merge import remove_duplicates

        self.assertEqual(remove_duplicates([1, 2, 3, 4]), [1, 2, 3, 4])

    def test_with_duplicates(self):
        """Test with list that has duplicates"""
        from aind_data_schema.utils.merge import remove_duplicates

        with self.assertLogs(level="INFO") as log:
            self.assertEqual(remove_duplicates([1, 2, 2, 3, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(len(log.output), 1)
        self.assertIn("Removed 2 duplicates from list", log.output[0])

    def test_preserves_order(self):
        """Test that order is preserved when removing duplicates"""
        from aind_data_schema.utils.merge import remove_duplicates

        self.assertEqual(remove_duplicates([3, 1, 2, 1, 3, 4]), [3, 1, 2, 4])

    def test_string_duplicates(self):
        """Test with string duplicates"""
        from aind_data_schema.utils.merge import remove_duplicates

        self.assertEqual(remove_duplicates(["a", "b", "a", "c", "b"]), ["a", "b", "c"])

    def test_all_duplicates(self):
        """Test with all elements being duplicates"""
        from aind_data_schema.utils.merge import remove_duplicates

        self.assertEqual(remove_duplicates([1, 1, 1, 1]), [1])


class MergeOptionalListTests(unittest.TestCase):
    """Tests for merge_optional_list"""

    def test_both_none(self):
        """Test when both inputs are None"""
        self.assertIsNone(merge_optional_list(None, None))

    def test_first_none(self):
        """Test when first input is None"""
        self.assertEqual(merge_optional_list(None, [1, 2, 3]), [1, 2, 3])

    def test_second_none(self):
        """Test when second input is None"""
        self.assertEqual(merge_optional_list([1, 2, 3], None), [1, 2, 3])

    def test_both_empty(self):
        """Test when both inputs are empty lists"""
        self.assertIsNone(merge_optional_list([], []))

    def test_first_empty(self):
        """Test when first input is an empty list"""
        self.assertEqual(merge_optional_list([], [1, 2, 3]), [1, 2, 3])

    def test_second_empty(self):
        """Test when second input is an empty list"""
        self.assertEqual(merge_optional_list([1, 2, 3], []), [1, 2, 3])

    def test_both_non_empty(self):
        """Test when both inputs are non-empty lists"""
        self.assertEqual(merge_optional_list([1, 2], [3, 4]), [1, 2, 3, 4])


class MergeCSTests(unittest.TestCase):
    """Tests for merge_coordinate_systems"""

    def setUp(self):
        """Set up test cases"""
        self.CSA = CoordinateSystemLibrary.BREGMA_ARI
        self.CSB = CoordinateSystemLibrary.MPM_MANIP_RFB

    def test_both_none(self):
        """Test when both inputs are None"""

        self.assertIsNone(merge_coordinate_systems(None, None))

    def test_first_none(self):
        """Test when first input is None"""

        self.assertEqual(merge_coordinate_systems(None, self.CSA), self.CSA)

    def test_second_none(self):
        """Test when second input is None"""

        self.assertEqual(merge_coordinate_systems(self.CSA, None), self.CSA)

    def test_both_same(self):
        """Test when both inputs are the same"""

        self.assertEqual(
            merge_coordinate_systems(self.CSA, self.CSA),
            self.CSA,
        )

    def test_both_different(self):
        """Test when both inputs are different"""

        with self.assertRaises(ValueError):
            merge_coordinate_systems(self.CSA, self.CSB)


class MergeProcessGraphTests(unittest.TestCase):
    """Tests for merge_process_graph"""

    def test_both_graphs_present(self):
        """Test merging when both graphs are present"""
        graph1 = {"proc1": ["proc2"], "proc2": []}
        graph2 = {"proc3": ["proc4"], "proc4": []}
        result = merge_process_graph(graph1, graph2, [], [])
        self.assertEqual(result, {"proc1": ["proc2"], "proc2": [], "proc3": ["proc4"], "proc4": []})

    def test_only_first_graph(self):
        """Test when only first graph is present"""
        graph1 = {"proc1": ["proc2"], "proc2": []}
        proc = Mock()
        proc.name = "proc3"
        result = merge_process_graph(graph1, None, [], [proc])
        self.assertEqual(result, {"proc1": ["proc2"], "proc2": [], "proc3": []})

    def test_only_second_graph(self):
        """Test when only second graph is present"""
        graph2 = {"proc3": ["proc4"], "proc4": []}
        proc = Mock()
        proc.name = "proc1"
        result = merge_process_graph(None, graph2, [proc], [])
        self.assertEqual(result, {"proc3": ["proc4"], "proc4": [], "proc1": []})

    def test_both_graphs_none(self):
        """Test when both graphs are None"""
        result = merge_process_graph(None, None, [], [])
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
