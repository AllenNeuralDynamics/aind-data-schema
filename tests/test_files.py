"""Tests for the Files core model and helpers."""

import json
import sys
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch

from aind_data_schema.core.files import (
    CROISSANT_CONTEXT,
    FileSet,
    Files,
    _as_pattern_list,
    _glob_match,
    _match_parts,
    _validate_croissant,
)


class GlobMatchTests(unittest.TestCase):
    """Tests for the path-aware glob matcher."""

    def test_star_does_not_cross_separator(self):
        self.assertTrue(_glob_match("a/metadata.csv", "*/metadata.csv"))
        self.assertFalse(_glob_match("a/b/metadata.csv", "*/metadata.csv"))
        self.assertFalse(_glob_match("metadata.csv", "*/metadata.csv"))

    def test_double_star_matches_any_depth(self):
        self.assertTrue(_glob_match("metadata.csv", "**/metadata.csv"))
        self.assertTrue(_glob_match("a/metadata.csv", "**/metadata.csv"))
        self.assertTrue(_glob_match("a/b/c/metadata.csv", "**/metadata.csv"))

    def test_double_star_terminal(self):
        self.assertTrue(_glob_match("a/b/c", "a/**"))
        self.assertTrue(_glob_match("a", "a/**"))

    def test_double_star_no_match(self):
        self.assertFalse(_glob_match("x/metadata.csv", "**/foo/metadata.csv"))

    def test_question_mark(self):
        self.assertTrue(_glob_match("a/b.txt", "?/b.txt"))
        self.assertFalse(_glob_match("ab/b.txt", "?/b.txt"))

    def test_empty_pattern(self):
        self.assertFalse(_glob_match("foo", ""))

    def test_path_longer_than_pattern(self):
        self.assertFalse(_glob_match("a/b", "a"))

    def test_match_parts_direct(self):
        # Exercise the recursive helper directly for the all-empty case.
        self.assertTrue(_match_parts([], []))


class AsPatternListTests(unittest.TestCase):
    """Tests for the pattern-normalizer helper."""

    def test_none(self):
        self.assertEqual(_as_pattern_list(None), [])

    def test_string(self):
        self.assertEqual(_as_pattern_list("*.csv"), ["*.csv"])

    def test_list(self):
        self.assertEqual(_as_pattern_list(["*.csv", "*.tsv"]), ["*.csv", "*.tsv"])


class FileSetTests(unittest.TestCase):
    """Tests for the FileSet pydantic model."""

    def test_croissant_id_normalizes_name(self):
        fs = FileSet(name="Hello World!", encoding_format="text/plain", includes="*.txt")
        self.assertEqual(fs._croissant_id(), "hello-world")

    def test_to_croissant_minimal(self):
        fs = FileSet(name="x", encoding_format="text/plain", includes="*.txt")
        entry = fs.to_croissant()
        self.assertEqual(entry["@type"], "cr:FileSet")
        self.assertEqual(entry["@id"], "x")
        self.assertEqual(entry["includes"], "*.txt")
        self.assertEqual(entry["encodingFormat"], "text/plain")
        self.assertNotIn("description", entry)
        self.assertNotIn("excludes", entry)

    def test_to_croissant_with_description_and_excludes(self):
        fs = FileSet(
            name="Logs",
            description="some logs",
            encoding_format="text/plain",
            includes=["*.log"],
            excludes=["*.tmp.log"],
        )
        entry = fs.to_croissant()
        self.assertEqual(entry["description"], "some logs")
        self.assertEqual(entry["excludes"], ["*.tmp.log"])


class ValidateFolderTests(unittest.TestCase):
    """Tests for Files.validate_folder."""

    @staticmethod
    def _touch(root: Path, *paths: str) -> None:
        for rel in paths:
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()

    def test_valid_folder_no_error(self):
        spec = Files(file_sets=[FileSet(name="csv", encoding_format="text/csv", includes="*.csv")])
        with tempfile.TemporaryDirectory() as d:
            self._touch(Path(d), "a.csv", "b.csv")
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                spec.validate_folder(Path(d))

    def test_unmatched_include_raises(self):
        spec = Files(file_sets=[FileSet(name="csv", encoding_format="text/csv", includes="*.csv")])
        with tempfile.TemporaryDirectory() as d:
            self._touch(Path(d), "a.txt")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with self.assertRaises(ValueError) as cm:
                    spec.validate_folder(Path(d))
            self.assertIn("FileSet 'csv'", str(cm.exception))
            self.assertIn("*.csv", str(cm.exception))

    def test_multiple_errors_collected(self):
        spec = Files(
            file_sets=[
                FileSet(name="csv", encoding_format="text/csv", includes=["*.csv", "*.tsv"]),
                FileSet(name="json", encoding_format="application/json", includes="*.json"),
            ]
        )
        with tempfile.TemporaryDirectory() as d:
            self._touch(Path(d), "a.csv")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with self.assertRaises(ValueError) as cm:
                    spec.validate_folder(Path(d))
            msg = str(cm.exception)
            self.assertIn("*.tsv", msg)
            self.assertIn("*.json", msg)
            self.assertNotIn("*.csv'", msg)

    def test_excludes_filters_match_list(self):
        spec = Files(
            file_sets=[
                FileSet(
                    name="csv",
                    encoding_format="text/csv",
                    includes="*.csv",
                    excludes="*.csv",
                )
            ]
        )
        with tempfile.TemporaryDirectory() as d:
            self._touch(Path(d), "a.csv")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with self.assertRaises(ValueError):
                    spec.validate_folder(Path(d))

    def test_excludes_list_form(self):
        spec = Files(
            file_sets=[
                FileSet(
                    name="csv",
                    encoding_format="text/csv",
                    includes="*.csv",
                    excludes=["skip.csv"],
                )
            ]
        )
        with tempfile.TemporaryDirectory() as d:
            self._touch(Path(d), "a.csv", "skip.csv")
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                spec.validate_folder(Path(d))
            msgs = " ".join(str(w.message) for w in caught)
            self.assertNotIn("skip.csv", msgs)

    def test_orphan_files_warn(self):
        spec = Files(file_sets=[FileSet(name="csv", encoding_format="text/csv", includes="*.csv")])
        with tempfile.TemporaryDirectory() as d:
            self._touch(Path(d), "a.csv", "extra.bin")
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                spec.validate_folder(Path(d))
            self.assertTrue(
                any("extra.bin" in str(w.message) for w in caught),
                f"Expected orphan warning for extra.bin; got: {caught}",
            )

    def test_sidecar_files_ignored(self):
        spec = Files(file_sets=[FileSet(name="csv", encoding_format="text/csv", includes="*.csv")])
        with tempfile.TemporaryDirectory() as d:
            self._touch(
                Path(d),
                "a.csv",
                "files.json",
                "metadata.nd.json",
                "files_croissant.json",
            )
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                spec.validate_folder(Path(d))
            msgs = " ".join(str(w.message) for w in caught)
            self.assertNotIn("files.json", msgs)
            self.assertNotIn("metadata.nd.json", msgs)
            self.assertNotIn("files_croissant.json", msgs)


class CroissantTests(unittest.TestCase):
    """Tests for the Croissant JSON-LD export."""

    def test_to_croissant_top_level(self):
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        doc = spec.to_croissant()
        self.assertEqual(doc["@context"], CROISSANT_CONTEXT)
        self.assertEqual(doc["@type"], "sc:Dataset")
        self.assertEqual(doc["name"], "files")
        self.assertEqual(doc["version"], "0.1.0")
        self.assertEqual(len(doc["distribution"]), 1)

    def test_to_croissant_json_round_trip(self):
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        parsed = json.loads(spec.to_croissant_json())
        self.assertEqual(parsed["@type"], "sc:Dataset")

    def test_write_croissant_file_creates_nested_directory(self):
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        with tempfile.TemporaryDirectory() as d:
            out = spec.write_croissant_file(Path(d) / "nested" / "out")
            self.assertTrue(out.exists())
            self.assertEqual(out.name, "files_croissant.json")
            data = json.loads(out.read_text())
            self.assertEqual(data["@type"], "sc:Dataset")


class SerializationTests(unittest.TestCase):
    """Tests for serialization / deserialization round-trips."""

    def test_round_trip(self):
        spec = Files(
            file_sets=[
                FileSet(
                    name="logs",
                    description="d",
                    encoding_format="text/plain",
                    includes="*.log",
                    excludes="ignore.log",
                )
            ]
        )
        round_tripped = Files.model_validate_json(spec.model_dump_json())
        self.assertEqual(round_tripped.file_sets[0].name, "logs")
        self.assertEqual(round_tripped.file_sets[0].excludes, "ignore.log")


class ValidateCroissantTests(unittest.TestCase):
    """Tests for the mlcroissant validation hook."""

    def test_valid_document_passes(self):
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        # to_croissant() runs validation; should not raise
        spec.to_croissant()

    def test_invalid_document_raises(self):
        import mlcroissant as mlc

        with self.assertRaises(mlc.ValidationError):
            _validate_croissant({"@type": "sc:Dataset"})

    def test_to_croissant_validate_false_skips(self):
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        with patch("aind_data_schema.core.files._validate_croissant") as m:
            spec.to_croissant(validate=False)
            m.assert_not_called()

    def test_to_croissant_json_passes_validate_flag(self):
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        with patch("aind_data_schema.core.files._validate_croissant") as m:
            spec.to_croissant_json(validate=False)
            m.assert_not_called()

    def test_write_croissant_file_passes_validate_flag(self):
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        with tempfile.TemporaryDirectory() as d:
            with patch("aind_data_schema.core.files._validate_croissant") as m:
                spec.write_croissant_file(Path(d), validate=False)
                m.assert_not_called()

    def test_missing_mlcroissant_skips(self):
        """When mlcroissant is not importable, validation is a no-op."""
        with patch.dict(sys.modules, {"mlcroissant": None}):
            # patch.dict with None forces ImportError on import
            _validate_croissant({"@type": "sc:Dataset"})  # would raise if validated


if __name__ == "__main__":
    unittest.main()
