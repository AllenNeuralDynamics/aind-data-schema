""" Tests for merge utilities """

import unittest

from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.utils.merge import (
    merge_notes,
    merge_optional_list,
    merge_coordinate_systems,
    merge_str_tuple_lists,
)


class TestMergeStrTupleLists(unittest.TestCase):

    def test_empty_lists(self):
        result = merge_str_tuple_lists([], [])
        self.assertEqual(result, [])

    def test_first_list_empty(self):
        b = ["a", "b", "c"]
        result = merge_str_tuple_lists([], b)
        self.assertEqual(result, ["a", "b", "c"])

    def test_second_list_empty(self):
        a = ["a", "b", "c"]
        result = merge_str_tuple_lists(a, [])
        self.assertEqual(result, ["a", "b", "c"])

    def test_equal_length_strings(self):
        a = ["a", "b", "c"]
        b = ["d", "e", "f"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "d"), ("b", "e"), ("c", "f")])

    def test_first_list_longer(self):
        a = ["a", "b", "c", "d"]
        b = ["e", "f"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "e"), ("b", "f"), "c", "d"])

    def test_second_list_longer(self):
        a = ["a", "b"]
        b = ["c", "d", "e", "f"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "c"), ("b", "d"), "e", "f"])

    def test_tuples_in_first_list(self):
        a = [("a", "b"), "c"]
        b = ["d", "e"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "d"), ("c", "e")])

    def test_tuples_in_second_list(self):
        a = ["a", "b"]
        b = [("c", "d"), "e"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "c", "d"), ("b", "e")])

    def test_tuples_in_both_lists(self):
        a = [("a", "b"), ("c", "d")]
        b = [("e", "f"), ("g", "h")]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "e", "f"), ("c", "d", "g", "h")])

    def test_mixed_strings_and_tuples_equal_length(self):
        a = ["a", ("b", "c"), "d"]
        b = [("e", "f"), "g", ("h", "i")]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "e", "f"), ("b", "c", "g"), ("d", "h", "i")])

    def test_mixed_strings_and_tuples_different_lengths(self):
        a = ["a", ("b", "c")]
        b = [("d", "e"), "f", "g"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "d", "e"), ("b", "c", "f"), "g"])

    def test_single_element_lists(self):
        a = ["a"]
        b = ["b"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b")])

    def test_single_element_tuple_lists(self):
        a = [("a",)]
        b = [("b",)]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b")])

    def test_single_tuple_with_multiple_elements(self):
        a = [("a", "b", "c")]
        b = ["d"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "c", "d")])

    def test_large_tuple_merge(self):
        a = [("a", "b", "c", "d")]
        b = [("e", "f", "g", "h")]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "c", "d", "e", "f", "g", "h")])

    def test_asymmetric_lists_with_tuples(self):
        a = [("a", "b"), "c", "d", ("e", "f", "g")]
        b = ["h"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "h"), "c", "d", ("e", "f", "g")])

    def test_only_first_has_elements_at_end(self):
        a = ["a", "b", "c"]
        b = ["d"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "d"), "b", "c"])

    def test_only_second_has_elements_at_end(self):
        a = ["a"]
        b = ["b", "c", "d"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b"), "c", "d"])

    def test_deduplication_in_merge(self):
        a = ["a", "b"]
        b = ["a", "c"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, ["a", ("b", "c")])

    def test_deduplication_with_tuples(self):
        a = [("a", "b"), "c"]
        b = [("b", "d"), "c"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "d"), "c"])

    def test_deduplication_all_same(self):
        a = ["x", "y"]
        b = ["x", "y"]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, ["x", "y"])

    def test_deduplication_preserves_order(self):
        a = [("a", "b", "c")]
        b = [("b", "d", "a")]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("a", "b", "c", "d")])

    def test_deduplication_complex_case(self):
        a = [("x", "y"), ("a", "b", "c")]
        b = [("y", "z"), ("c", "d")]
        result = merge_str_tuple_lists(a, b)
        self.assertEqual(result, [("x", "y", "z"), ("a", "b", "c", "d")])


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


if __name__ == "__main__":
    unittest.main()
