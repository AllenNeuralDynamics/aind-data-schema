"""Tests metadata module"""

import unittest

from aind_data_schema.core.metadata import Metadata, MetadataStatus
from aind_data_schema.core.subject import Sex, Subject
from aind_data_schema.models.species import MUS_MUSCULUS


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    def test_valid_subject_info(self):
        """Tests that the record is marked as VALID if a valid subject model
        is present."""
        s1 = Subject(
            species=MUS_MUSCULUS,
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


if __name__ == "__main__":
    unittest.main()
