"""Integration test: load files.json as a data instance and validate
that the described files exist in the behavior-videos folder.

Fake empty files mirror the real S3 layout:
  aind-open-data/behavior_811026_2025-12-01_22-31-16/behavior-videos/
"""

import unittest
from pathlib import Path

from aind_data_schema.core.files import BehaviorVideoFiles

BEHAVIOR_VIDEOS = Path(__file__).parent / "behavior-videos"
FILES_JSON = BEHAVIOR_VIDEOS / "files.json"


class TestBehaviorVideosFolderValidation(unittest.TestCase):
    def test_round_trip(self):
        serialized = FILES_JSON.read_text()
        spec = BehaviorVideoFiles.model_validate_json(serialized)
        reserialized = spec.model_dump_json()
        BehaviorVideoFiles.model_validate_json(reserialized)

    def test_valid_folder_has_no_errors(self):
        spec = BehaviorVideoFiles.model_validate_json(FILES_JSON.read_text())
        errors = spec.validate_folder(BEHAVIOR_VIDEOS)
        self.assertEqual(errors, [], f"Unexpected errors: {errors}")

    def test_missing_video_detected(self):
        spec = BehaviorVideoFiles.from_standard()
        missing_dir = BEHAVIOR_VIDEOS.parent / "missing-video"
        missing_dir.mkdir(exist_ok=True)
        cam = missing_dir / "FaceCamera"
        cam.mkdir(exist_ok=True)
        (cam / "metadata.csv").touch()
        try:
            errors = spec.validate_folder(missing_dir)
            self.assertTrue(
                any("video" in e.lower() for e in errors),
                f"Expected missing-video error, got: {errors}",
            )
        finally:
            (cam / "metadata.csv").unlink()
            cam.rmdir()
            missing_dir.rmdir()

    def test_missing_metadata_detected(self):
        spec = BehaviorVideoFiles.from_standard()
        missing_dir = BEHAVIOR_VIDEOS.parent / "missing-metadata"
        missing_dir.mkdir(exist_ok=True)
        cam = missing_dir / "FrontCamera"
        cam.mkdir(exist_ok=True)
        (cam / "video.mp4").touch()
        try:
            errors = spec.validate_folder(missing_dir)
            self.assertTrue(
                any("metadata" in e.lower() for e in errors),
                f"Expected missing-metadata error, got: {errors}",
            )
        finally:
            (cam / "video.mp4").unlink()
            cam.rmdir()
            missing_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
