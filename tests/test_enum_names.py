"""Unit test for EnumNames"""

import unittest

from aind_data_schema import DataDescription, Subject
from aind_data_schema.data_description import Institution, Modality
from aind_data_schema.subject import Species


class TestEnumNames(unittest.TestCase):
    """tests enum names"""

    def test_data_description(self):
        """tests that Institution and Modality enumnames are generated as expected"""
        data_description_json = DataDescription.schema_json()
        institution_enum_names = [e.value.name for e in Institution]
        expected_inst_enum_names = str(institution_enum_names).replace("'", '"')
        self.assertIn(expected_inst_enum_names, data_description_json)

        modality_enum_names = [e.value.name for e in Modality]
        expected_modality_enum_names = str(modality_enum_names).replace("'", '"')
        self.assertIn(expected_modality_enum_names, data_description_json)

    def test_subject(self):
        """tests that Species enumnames is generated as expected"""
        subject_json = Subject.schema_json()
        species_enum_names = [e.value.name for e in Species]
        expected_species_enum_names = str(species_enum_names).replace("'", '"')
        self.assertIn(expected_species_enum_names, subject_json)


if __name__ == "__main__":
    unittest.main()
