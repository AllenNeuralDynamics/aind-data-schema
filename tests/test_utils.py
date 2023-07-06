"""Test aind_utils"""

import json
import unittest
from pathlib import Path

from aind_data_schema.utils.aind_utils import aind_core_models, create_derived_data_description, get_classes


class UtilsTests(unittest.TestCase):
    """Tests for aind_utils methods"""

    def test_get_schemas(self):
        """Tests get schemas method"""
        schema_gen = aind_core_models()

        for schema in schema_gen:
            filename = schema.default_filename()
            schema_filename = filename.replace(".json", "_schema.json")
            schema_contents = schema.schema_json(indent=3)
            self.assertIsNotNone(schema_filename)
            self.assertIsNotNone(schema_contents)

    def test_get_classes(self):
        """Tests get classes method"""
        self.assertEqual(list(get_classes()), list(get_classes(__name__)))

    def test_create_derived_data_description(self):
        """Tests create_derived_data_description method"""
        from aind_data_schema.data_description import DataDescription, DerivedDataDescription, ExperimentType, Modality

        data_description_files_path = Path(__file__).parent / "resources" / "ephys_data_description"
        data_description_args = [p for p in data_description_files_path.iterdir()]

        for data_description_arg in data_description_args:
            if "0.3.0" in data_description_arg.name:
                experiment_type = ExperimentType.ECEPHYS
            else:
                experiment_type = None
            print(data_description_arg.name, experiment_type)
            derived_data_description_from_file = create_derived_data_description(
                process_name="test_process",
                existing_data_description=data_description_arg,
                experiment_type=experiment_type,
            )
            with open(data_description_arg, "r") as f:
                data_description_dict = json.load(f)
            if "experiment_type" not in data_description_dict:
                data_description_dict["experiment_type"] = ExperimentType.ECEPHYS
            data_description = DataDescription.construct(**data_description_dict)
            derived_data_description_from_obj = create_derived_data_description(
                process_name="test_process", existing_data_description=data_description, experiment_type=experiment_type
            )
            self.assertTrue(isinstance(derived_data_description_from_file, DerivedDataDescription))
            self.assertTrue(isinstance(derived_data_description_from_obj, DerivedDataDescription))

        # Test from scratch
        derived_data_description_from_scratch = create_derived_data_description(
            process_name="test_process",
            existing_data_description=None,
            modality=[Modality.ECEPHYS],
            experiment_type=ExperimentType.ECEPHYS,
            subject_id="00000",
            input_data_name="test_input_data_name",
        )
        self.assertTrue(isinstance(derived_data_description_from_scratch, DerivedDataDescription))


if __name__ == "__main__":
    unittest.main()
