"""Tests Metadata model"""

import unittest
from datetime import datetime
from pydantic import ValidationError
from aind_data_schema.metadata import Metadata, MetadataStatus
from aind_data_schema.procedures import Procedures
from aind_data_schema.subject import Subject
from aind_data_schema.data_description import DataDescription
from aind_data_schema.processing import Processing
from aind_data_schema.session import Session
from aind_data_schema.rig import Rig


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    def test_constructors(self):
        """test building from component parts and validator"""

        d1 = Metadata(
            _id="00000",
            name="ecephys_655019_2023-04-03_18-17-09",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
            subject=Subject.construct(),
            data_description=DataDescription.construct(),
            procedures=Procedures.construct(),
            session=Session.construct(),
            rig=Rig.construct(),
            processing=Processing.construct(),
        )
        self.assertIsNotNone(d1)
        self.assertEqual(d1.schema_version, "0.0.1")
        self.assertEqual(d1.location, "Test Location")
        self.assertTrue(hasattr(d1, "subject"))
        d2 = Metadata(
            _id="00000",
            name="ecephys_AK655019_2023-04-03_18-17-09",
            created=datetime(2023, 9, 27, 0, 0, 0),
            last_modified=datetime(2023, 9, 28, 10, 20, 30),
            location="Test Location",
            metadata_status=MetadataStatus.VALID,
            subject=Subject.construct(),
            data_description=DataDescription.construct(),
            procedures=None,
            session=Session.construct(),
            rig=Rig.construct(),
            processing=Processing.construct(),
        )
        self.assertIsNotNone(d2)
        self.assertIsNone(d2.procedures)
        with self.assertRaises(ValidationError) as context:
            d3 = Metadata(
                _id="00000",
                name="SmartSPIM_655019_2023-04-03_18-17-09",
                created=datetime(2023, 9, 27, 0, 0, 0),
                last_modified=datetime(2023, 9, 28, 10, 20, 30),
                location="Test Location",
                metadata_status=MetadataStatus.MISSING,
                subject=Subject.construct(),
                data_description=DataDescription.construct(),
                procedures=Procedures.construct(),
                rig=Rig.construct(),
            )
        error_message = str(context.exception)
        print(error_message)
        self.assertIn("Missing metadata:", error_message)


if __name__ == "__main__":
    unittest.main()
