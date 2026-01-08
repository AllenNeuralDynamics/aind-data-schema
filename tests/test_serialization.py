"""Tests for serialization utilities"""

import json
import unittest
from aind_data_schema.utils.serialization import compress_list_of_dicts_delta, expand_list_of_dicts_delta


class SerializationTests(unittest.TestCase):
    """Test serialization utility functions"""

    def test_compress_list_of_dicts_delta_basic(self):
        """Test basic delta compression"""
        data = [
            {"a": 1, "b": 2},
            {"a": 1, "b": 3},
            {"a": 2, "b": 3},
        ]

        result = compress_list_of_dicts_delta(data)

        self.assertTrue(result["_dc"])
        self.assertIn("_v", result)
        compressed = result["_v"]

        self.assertEqual(len(compressed), 3)
        self.assertEqual(compressed[0], {"a": 1, "b": 2})
        self.assertEqual(compressed[1], {"b": 3})
        self.assertEqual(compressed[2], {"a": 2})

    def test_compress_list_of_dicts_delta_no_changes(self):
        """Test compression when values don't change"""
        data = [
            {"a": 1, "b": 2},
            {"a": 1, "b": 2},
            {"a": 1, "b": 2},
        ]

        result = compress_list_of_dicts_delta(data)
        compressed = result["_v"]

        self.assertEqual(compressed[0], {"a": 1, "b": 2})
        self.assertEqual(compressed[1], {})
        self.assertEqual(compressed[2], {})

    def test_compress_list_of_dicts_delta_single_element(self):
        """Test compression with single element"""
        data = [{"a": 1, "b": 2}]

        result = compress_list_of_dicts_delta(data)

        self.assertFalse(result["_dc"])
        self.assertEqual(result["_v"], data)

    def test_compress_list_of_dicts_delta_empty(self):
        """Test compression with empty list"""
        data = []

        result = compress_list_of_dicts_delta(data)

        self.assertFalse(result["_dc"])
        self.assertEqual(result["_v"], [])

    def test_compress_list_of_dicts_delta_mixed_change_frequencies(self):
        """Test compression where different keys change at different frequencies"""
        # Key 'a' changes every index, key 'b' changes every other index, key 'c' never changes
        data = [
            {"a": 0, "b": 0, "c": 100},
            {"a": 1, "b": 0, "c": 100},
            {"a": 2, "b": 1, "c": 100},
            {"a": 3, "b": 1, "c": 100},
            {"a": 4, "b": 2, "c": 100},
            {"a": 5, "b": 2, "c": 100},
        ]

        result = compress_list_of_dicts_delta(data)
        compressed = result["_v"]

        # First dict should be complete
        self.assertEqual(compressed[0], {"a": 0, "b": 0, "c": 100})

        # Index 1: only 'a' changes
        self.assertEqual(compressed[1], {"a": 1})

        # Index 2: both 'a' and 'b' change
        self.assertEqual(compressed[2], {"a": 2, "b": 1})

        # Index 3: only 'a' changes
        self.assertEqual(compressed[3], {"a": 3})

        # Index 4: both 'a' and 'b' change
        self.assertEqual(compressed[4], {"a": 4, "b": 2})

        # Index 5: only 'a' changes
        self.assertEqual(compressed[5], {"a": 5})

        # Verify roundtrip
        expanded = expand_list_of_dicts_delta(result)
        self.assertEqual(expanded, data)

    def test_compress_list_of_dicts_delta_sparse_changes(self):
        """Test compression with sparse changes across many elements"""
        # Simulate 100 units where only unit_0 changes across 5 events
        first = {f"unit_{i}": {"quality": "good"} for i in range(100)}

        data = [first]
        for event in range(1, 5):
            new_dict = first.copy()
            new_dict["unit_0"] = {"quality": f"event_{event}"}
            data.append(new_dict)

        result = compress_list_of_dicts_delta(data)
        compressed = result["_v"]

        self.assertEqual(len(compressed[0]), 100)
        for i in range(1, 5):
            self.assertEqual(len(compressed[i]), 1)
            self.assertIn("unit_0", compressed[i])
            self.assertNotIn("unit_1", compressed[i])

    def test_expand_list_of_dicts_delta_basic(self):
        """Test basic delta expansion"""
        compressed = {"_dc": True, "_v": [{"a": 1, "b": 2}, {"b": 3}, {"a": 2}]}

        result = expand_list_of_dicts_delta(compressed)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {"a": 1, "b": 2})
        self.assertEqual(result[1], {"a": 1, "b": 3})
        self.assertEqual(result[2], {"a": 2, "b": 3})

    def test_expand_list_of_dicts_delta_no_marker(self):
        """Test expansion with no delta marker returns original"""
        data = [{"a": 1}, {"b": 2}]

        result = expand_list_of_dicts_delta(data)

        self.assertEqual(result, data)

    def test_expand_list_of_dicts_delta_false_marker(self):
        """Test expansion with _dc=False returns original"""
        data = {"_dc": False, "_v": [{"a": 1}, {"b": 2}]}

        result = expand_list_of_dicts_delta(data)

        self.assertEqual(result, data)

    def test_expand_list_of_dicts_delta_carry_forward(self):
        """Test that values are carried forward correctly"""
        compressed = {
            "_dc": True,
            "_v": [
                {"a": 1, "b": 2, "c": 3},
                {"b": 4},
                {},
                {"a": 5, "c": 6},
            ],
        }

        result = expand_list_of_dicts_delta(compressed)

        self.assertEqual(result[0], {"a": 1, "b": 2, "c": 3})
        self.assertEqual(result[1], {"a": 1, "b": 4, "c": 3})
        self.assertEqual(result[2], {"a": 1, "b": 4, "c": 3})
        self.assertEqual(result[3], {"a": 5, "b": 4, "c": 6})

    def test_roundtrip_compression_expansion(self):
        """Test that compress -> expand roundtrip preserves data"""
        original = [
            {"x": 1, "y": 2, "z": 3},
            {"x": 1, "y": 5, "z": 3},
            {"x": 10, "y": 5, "z": 3},
            {"x": 10, "y": 5, "z": 30},
        ]

        compressed = compress_list_of_dicts_delta(original)
        expanded = expand_list_of_dicts_delta(compressed)

        self.assertEqual(expanded, original)

    def test_roundtrip_with_sparse_data(self):
        """Test roundtrip with realistic sparse curation data"""
        # Simulate 1000 units with 10 curation events, sparse changes
        first = {f"unit_{i}": {"quality": "good", "notes": ""} for i in range(1000)}

        data = [first]
        for event in range(1, 10):
            new_dict = first.copy()
            # Only change 3 random units each event
            for unit_idx in [event, event + 100, event + 500]:
                if f"unit_{unit_idx}" in new_dict:
                    new_dict[f"unit_{unit_idx}"] = {"quality": f"q{event}", "notes": f"note{event}"}
            data.append(new_dict)

        compressed = compress_list_of_dicts_delta(data)
        expanded = expand_list_of_dicts_delta(compressed)

        self.assertEqual(expanded, data)

        # Verify compression actually reduced size
        for i in range(1, 10):
            self.assertLess(len(compressed["_v"][i]), 1000)

    def test_compressed_json_size_reduction(self):
        """Test that compressed JSON string is actually smaller than uncompressed"""
        # Create realistic curation data: 1000 units, 10 events, sparse changes
        first = {f"unit_{i}": {"quality": "good", "notes": "initial", "score": 0.95} for i in range(1000)}

        data = [first]
        for event in range(1, 10):
            new_dict = first.copy()
            # Only change 5 units each event
            for unit_idx in [event, event + 100, event + 200, event + 500, event + 700]:
                if f"unit_{unit_idx}" in new_dict:
                    new_dict[f"unit_{unit_idx}"] = {
                        "quality": f"q{event}",
                        "notes": f"updated_{event}",
                        "score": 0.8 + event * 0.01,
                    }
            data.append(new_dict)

        # Get compressed version
        compressed = compress_list_of_dicts_delta(data)

        # Serialize both to JSON strings
        original_json = json.dumps(data)
        compressed_json = json.dumps(compressed)

        # Verify compressed is actually smaller
        original_size = len(original_json)
        compressed_size = len(compressed_json)

        self.assertLess(compressed_size, original_size)

        # Calculate compression ratio
        compression_ratio = compressed_size / original_size

        # For this sparse change pattern, we expect significant compression
        # (should be less than 20% of original size)
        self.assertLess(compression_ratio, 0.2)

    def test_compress_with_non_dict_elements(self):
        """Test compression handles non-dict elements gracefully"""
        data = [
            {"a": 1},
            None,
            {"a": 2},
        ]

        result = compress_list_of_dicts_delta(data)
        compressed = result["_v"]

        self.assertEqual(compressed[0], {"a": 1})
        self.assertIsNone(compressed[1])
        self.assertEqual(compressed[2], {"a": 2})

    def test_expand_with_non_dict_elements(self):
        """Test expansion handles non-dict elements gracefully"""
        compressed = {"_dc": True, "_v": [{"a": 1}, None, {"a": 2}]}

        result = expand_list_of_dicts_delta(compressed)

        self.assertEqual(result[0], {"a": 1})
        self.assertIsNone(result[1])
        self.assertEqual(result[2], {"a": 2})

    def test_expand_with_empty_compressed_list(self):
        """Test expansion with empty _v list returns empty list"""
        compressed = {"_dc": True, "_v": []}

        result = expand_list_of_dicts_delta(compressed)

        self.assertEqual(result, [])

    def test_expand_with_non_dict_first_element(self):
        """Test expansion when first element is not a dict"""
        compressed = {"_dc": True, "_v": ["not_a_dict", {"a": 1}]}

        result = expand_list_of_dicts_delta(compressed)

        self.assertEqual(result, ["not_a_dict", {"a": 1}])


if __name__ == "__main__":
    unittest.main()
