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
        """Single star should not match across path separators."""
        self.assertTrue(_glob_match("a/metadata.csv", "*/metadata.csv"))
        self.assertFalse(_glob_match("a/b/metadata.csv", "*/metadata.csv"))
        self.assertFalse(_glob_match("metadata.csv", "*/metadata.csv"))

    def test_double_star_matches_any_depth(self):
        """Double star should match at any depth."""
        self.assertTrue(_glob_match("metadata.csv", "**/metadata.csv"))
        self.assertTrue(_glob_match("a/metadata.csv", "**/metadata.csv"))
        self.assertTrue(_glob_match("a/b/c/metadata.csv", "**/metadata.csv"))

    def test_double_star_terminal(self):
        """Double star at end should match any trailing path."""
        self.assertTrue(_glob_match("a/b/c", "a/**"))
        self.assertTrue(_glob_match("a", "a/**"))

    def test_double_star_no_match(self):
        """Double star should not match when intermediate components don't align."""
        self.assertFalse(_glob_match("x/metadata.csv", "**/foo/metadata.csv"))

    def test_question_mark(self):
        """Question mark should match a single character."""
        self.assertTrue(_glob_match("a/b.txt", "?/b.txt"))
        self.assertFalse(_glob_match("ab/b.txt", "?/b.txt"))

    def test_empty_pattern(self):
        """Empty pattern should not match any path."""
        self.assertFalse(_glob_match("foo", ""))

    def test_path_longer_than_pattern(self):
        """Pattern shorter than path should not match."""
        self.assertFalse(_glob_match("a/b", "a"))

    def test_match_parts_direct(self):
        """Exercise the recursive helper directly for the all-empty case."""
        self.assertTrue(_match_parts([], []))


class AsPatternListTests(unittest.TestCase):
    """Tests for the pattern-normalizer helper."""

    def test_none(self):
        """None should return empty list."""
        self.assertEqual(_as_pattern_list(None), [])

    def test_string(self):
        """String input should be wrapped in a list."""
        self.assertEqual(_as_pattern_list("*.csv"), ["*.csv"])

    def test_list(self):
        """List input should be returned as-is."""
        self.assertEqual(_as_pattern_list(["*.csv", "*.tsv"]), ["*.csv", "*.tsv"])


class FileSetTests(unittest.TestCase):
    """Tests for the FileSet pydantic model."""

    def test_croissant_id_normalizes_name(self):
        """Croissant ID should normalize special characters to lowercase hyphenated form."""
        fs = FileSet(name="Hello World!", encoding_format="text/plain", includes="*.txt")
        self.assertEqual(fs._croissant_id(), "hello-world")

    def test_to_croissant_minimal(self):
        """Minimal FileSet should serialize to Croissant with required fields only."""
        fs = FileSet(name="x", encoding_format="text/plain", includes="*.txt")
        entry = fs.to_croissant()
        self.assertEqual(entry["@type"], "cr:FileSet")
        self.assertEqual(entry["@id"], "x")
        self.assertEqual(entry["includes"], "*.txt")
        self.assertEqual(entry["encodingFormat"], "text/plain")
        self.assertNotIn("description", entry)
        self.assertNotIn("excludes", entry)

    def test_to_croissant_with_description_and_excludes(self):
        """FileSet with description and excludes should include those in serialization."""
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
        """Create empty files at relative paths under root."""
        for rel in paths:
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()

    def test_valid_folder_no_error(self):
        """Folder with all required files should validate without errors."""
        spec = Files(file_sets=[FileSet(name="csv", encoding_format="text/csv", includes="*.csv")])
        with tempfile.TemporaryDirectory() as d:
            self._touch(Path(d), "a.csv", "b.csv")
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                spec.validate_folder(Path(d))

    def test_unmatched_include_raises(self):
        """Unmatched include pattern should raise ValueError."""
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
        """Multiple unmatched patterns should all be reported in one error."""
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
        """Excludes should filter out matching files from the match list."""
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
        """Excluded files should not be treated as orphans."""
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
        """Files not described by any FileSet should emit a warning."""
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
        """Sidecar files like files.json and metadata.nd.json should be ignored."""
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
        """Croissant document should have correct top-level structure."""
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        doc = spec.to_croissant()
        self.assertEqual(doc["@context"], CROISSANT_CONTEXT)
        self.assertEqual(doc["@type"], "sc:Dataset")
        self.assertEqual(doc["name"], "files")
        self.assertEqual(doc["version"], "0.1.0")
        self.assertEqual(len(doc["distribution"]), 1)

    def test_to_croissant_json_round_trip(self):
        """Croissant JSON serialization should produce valid JSON."""
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        parsed = json.loads(spec.to_croissant_json())
        self.assertEqual(parsed["@type"], "sc:Dataset")

    def test_write_croissant_file_creates_nested_directory(self):
        """Writing Croissant file should create nested directories as needed."""
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
        """Files object should round-trip through JSON serialization/deserialization."""
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
        """Valid Croissant document should pass validation without errors."""
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        spec.to_croissant()

    def test_invalid_document_raises(self):
        """Invalid Croissant document should raise mlcroissant.ValidationError."""
        import mlcroissant as mlc

        with self.assertRaises(mlc.ValidationError):
            _validate_croissant({"@type": "sc:Dataset"})

    def test_to_croissant_validate_false_skips(self):
        """When validate=False, validation hook should not be called."""
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        with patch("aind_data_schema.core.files._validate_croissant") as m:
            spec.to_croissant(validate=False)
            m.assert_not_called()

    def test_to_croissant_json_passes_validate_flag(self):
        """to_croissant_json should pass validate flag to to_croissant."""
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        with patch("aind_data_schema.core.files._validate_croissant") as m:
            spec.to_croissant_json(validate=False)
            m.assert_not_called()

    def test_write_croissant_file_passes_validate_flag(self):
        """write_croissant_file should pass validate flag through the chain."""
        spec = Files(file_sets=[FileSet(name="logs", encoding_format="text/plain", includes="*.log")])
        with tempfile.TemporaryDirectory() as d:
            with patch("aind_data_schema.core.files._validate_croissant") as m:
                spec.write_croissant_file(Path(d), validate=False)
                m.assert_not_called()

    def test_missing_mlcroissant_skips(self):
        """When mlcroissant is not importable, validation is a no-op and does not raise."""
        with patch.dict(sys.modules, {"mlcroissant": None}):
            _validate_croissant({"@type": "sc:Dataset"})  # would raise if validated


if __name__ == "__main__":
    unittest.main()
