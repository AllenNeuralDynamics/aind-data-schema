""" Tests for merge utilities """

import unittest

from aind_data_schema.utils.merge import merge_notes, merge_optional_list


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


if __name__ == "__main__":
    unittest.main()
