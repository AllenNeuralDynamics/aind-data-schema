"""Tests DataRecord model"""

import unittest
from datetime import datetime

from aind_data_schema.data_record import DataRecord, MetadataStatus
from aind_data_schema.subject import Subject


class TestDataRecord(unittest.TestCase):
    """Class to test DataRecord model"""

    def test_constructors(self):
        """test building from component parts"""

        d1 = DataRecord(
            _id="00000",
            name="Test Name",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
        )
        self.assertIsNotNone(d1)
        self.assertEqual(d1.schema_version, '0.0.1')
        self.assertEqual(d1.location, "Test Location")
        d2 = DataRecord(
            _id="00000",
            name="Test Name",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
            subject=Subject.construct(),
        )
        self.assertIsNotNone(d2)
        self.assertTrue(hasattr(d2, "subject"))


if __name__ == "__main__":
    unittest.main()
