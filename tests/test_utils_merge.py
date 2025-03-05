""" Tests for merge utilities """

import unittest
from aind_data_schema.utils.merge import merge_notes


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


if __name__ == "__main__":
    unittest.main()
