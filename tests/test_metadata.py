"""Tests metadata module"""

import json
import unittest
from datetime import time

from pydantic import ValidationError

from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.metadata import Metadata, MetadataStatus
from aind_data_schema.core.procedures import Procedures
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.subject import Sex, Species, Subject
from aind_data_schema.models.modalities import Ecephys


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
            "  Field required [type=missing, input_value={}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing\n"
            "location\n"
            "  Field required [type=missing, input_value={}, input_type=dict]\n"
            "    For further information visit https://errors.pydantic.dev/2.5/v/missing"
        )
        self.assertEqual(expected_exception_message, str(e.exception))

    def test_invalid_core_models(self):
        """Test that invalid models don't raise an error, but marks the
        metadata_status as INVALID"""

        # Invalid subject model
        d1 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=Subject.model_construct())
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
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            subject=s2,
            procedures=Procedures.model_construct(injection_materials=["some materials"]),
        )
        self.assertEqual(MetadataStatus.INVALID, d2.metadata_status)

        # Tests constructed via dictionary
        d3 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            subject=json.loads(Subject.model_construct().model_dump_json()),
        )
        self.assertEqual(MetadataStatus.INVALID, d3.metadata_status)

    def test_default_file_extension(self):
        """Tests that the default file extension used is as expected."""
        self.assertEqual(".nd.json", Metadata._FILE_EXTENSION.default)

    def test_validate_ecephys_metadata(self):
        """Tests that ecephys validator works as expected"""
        with self.assertRaises(ValueError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label", platform=Ecephys, creation_time=time(12, 12, 12)
                ),
                procedures=Procedures.model_construct(injection_materials=["some materials"]),
                rig=Rig.model_construct(),
            )
        self.assertIn("Missing some metadata", str(context.exception))

        with self.assertRaises(ValueError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(),
                rig=Rig.model_construct(),
            )
        self.assertIn("Procedures is missing injection materials.", str(context.exception))


if __name__ == "__main__":
    unittest.main()
