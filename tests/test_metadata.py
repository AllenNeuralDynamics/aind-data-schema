"""Tests metadata module"""

import json
import unittest

from pydantic import ValidationError

from aind_data_schema.metadata import Metadata, MetadataStatus
from aind_data_schema.procedures import Procedures
from aind_data_schema.subject import Sex, Species, Subject


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    def test_valid_subject_info(self):
        """Tests that the record is marked as VALID if a valid subject model
        is present."""
        s1 = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="123345",
            sex=Sex.MALE,
            date_of_birth="2020-10-10",
            genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
        )
        d1 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=s1)
        self.assertEqual("ecephys_655019_2023-04-03_18-17-09", d1.name)
        self.assertEqual("bucket", d1.location)
        self.assertEqual(MetadataStatus.VALID, d1.metadata_status)
        self.assertEqual(s1, d1.subject)

        # Test construction via dictionary
        d2 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=s1.dict())
        self.assertEqual(MetadataStatus.VALID, d2.metadata_status)
        self.assertEqual(s1, d2.subject)

        # Test round-trip serialization
        # We may want override the default file writer to always use by_alias
        # when writing the Metadata records. This sets the field in the json
        # file to _id instead of id, which makes it easier to write to
        # MongoDB.
        d3 = Metadata.parse_obj(json.loads(d2.json(by_alias=True)))
        self.assertEqual(d2, d3)

    def test_missing_subject_info(self):
        """Marks the metadata status as MISSING if a Subject model is not
        present"""

        d1 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
        )
        self.assertEqual(MetadataStatus.MISSING, d1.metadata_status)
        self.assertEqual("ecephys_655019_2023-04-03_18-17-09", d1.name)
        self.assertEqual("bucket", d1.location)

        # Assert at least a name and location are required
        with self.assertRaises(ValidationError) as e:
            Metadata()
        expected_exception_message = (
            "2 validation errors for Metadata\n"
            "name\n"
            "  field required (type=value_error.missing)\n"
            "location\n"
            "  field required (type=value_error.missing)"
        )
        self.assertEqual(expected_exception_message, str(e.exception))

    def test_invalid_core_models(self):
        """Test that invalid models don't raise an error, but marks the
        metadata_status as INVALID"""

        # Invalid subject model
        d1 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=Subject.construct())
        self.assertEqual(MetadataStatus.INVALID, d1.metadata_status)

        # Valid subject model, but invalid procedures model
        s2 = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="123345",
            sex=Sex.MALE,
            date_of_birth="2020-10-10",
            genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
        )
        d2 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=s2, procedures=Procedures.construct()
        )
        self.assertEqual(MetadataStatus.INVALID, d2.metadata_status)


if __name__ == "__main__":
    unittest.main()
