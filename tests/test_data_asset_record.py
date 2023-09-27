"""Tests DataAssetRecord model"""

import unittest
from datetime import datetime

from aind_data_schema.data_asset_record import DataAssetRecord, MetadataStatus
from aind_data_schema.subject import Subject


class TestDataAssetRecord(unittest.TestCase):
    """Class to test DataAssetRecord model"""

    def test_constructors(self):
        """test building from component parts"""

        d1 = DataAssetRecord(
            _id="00000",
            name="Test Name",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
        )
        assert d1 is not None
        d2 = DataAssetRecord(
            _id="00000",
            name="Test Name",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
            subject=Subject.construct(),
        )
        assert d2 is not None


if __name__ == "__main__":
    unittest.main()
