""" Tests for compatibility check utilities """

import unittest
from aind_data_schema.utils.validators import subject_specimen_id_compatibility


class TestCompatibilityCheck(unittest.TestCase):
    """Tests compatibility checks"""

    def test_subj_spec_valid(self):
        """Test subject_id specimen_id valid"""
        subject_id = "123456"
        specimen_id = "123456-valid"
        self.assertTrue(subject_specimen_id_compatibility(subject_id, specimen_id))

    def test_subj_spec_invalid(self):
        """Test invalid subject_id specimen_id"""
        subject_id = "123456"
        specimen_id = "invalid"
        self.assertFalse(subject_specimen_id_compatibility(subject_id, specimen_id))


if __name__ == "__main__":
    unittest.main()
