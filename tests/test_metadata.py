"""Tests Metadata model"""

import unittest
from datetime import datetime

from aind_data_schema.metadata import Metadata, MetadataStatus
from aind_data_schema.procedures import Procedures
from aind_data_schema.subject import Subject


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    def test_constructors(self):
        """test building from component parts"""

        d1 = Metadata(
            _id="00000",
            name="Test Name",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
            subject=Subject.construct(),
        )
        self.assertIsNotNone(d1)
        self.assertEqual(d1.schema_version, "0.0.1")
        self.assertEqual(d1.location, "Test Location")
        self.assertTrue(hasattr(d1, "subject"))
        d2 = Metadata(
            _id="00000",
            name="Test Name",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
            subject=Subject.construct(),
            procedures=Procedures.construct(),
        )
        self.assertIsNotNone(d2)
        self.assertTrue(hasattr(d2, "procedures"))


if __name__ == "__main__":
    unittest.main()
