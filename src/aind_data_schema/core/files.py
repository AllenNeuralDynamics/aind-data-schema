import fnmatch
from pathlib import Path
from typing import List, Literal, Optional, Union

from pydantic import Field, SkipValidation

from aind_data_schema.base import DataCoreModel, DataModel


class FileSet(DataModel):
    """A set of files matching a glob pattern, inspired by Croissant cr:FileSet"""

    name: str = Field(..., title="Name")
    description: Optional[str] = Field(default=None, title="Description")
    encoding_format: Optional[str] = Field(default=None, title="Encoding format (MIME type)")
    includes: Union[str, List[str]] = Field(..., title="Glob pattern(s) for included files")
    excludes: Optional[Union[str, List[str]]] = Field(default=None, title="Glob pattern(s) for excluded files")


class Files(DataCoreModel):
    """Description of the expected file organization for a data asset folder"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/files.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["0.1.0"]] = Field(default="0.1.0")

    file_sets: List[FileSet] = Field(..., title="File sets", min_length=1)

    def validate_folder(self, folder: Path) -> List[str]:
        """Check that the file sets match actual files in the given folder.

        Returns a list of error strings. Empty list means valid.
        """
        relative_paths = [
            str(p.relative_to(folder)).replace("\\", "/")
            for p in folder.rglob("*")
            if p.is_file() and p.name != "files.json"
        ]
        errors = []
        for file_set in self.file_sets:
            patterns = [file_set.includes] if isinstance(file_set.includes, str) else file_set.includes
            for pattern in patterns:
                matches = [p for p in relative_paths if fnmatch.fnmatch(p, pattern)]
                if not matches:
                    errors.append(
                        f"FileSet '{file_set.name}': no files matching pattern '{pattern}'"
                    )
        return errors


class BehaviorVideoFiles(Files):
    """File organization for AIND behavior videos.

    Expected folder structure:
        behavior-videos/
          <CameraName>/
            metadata.csv
            video.<ext>
    """

    @classmethod
    def from_standard(cls) -> "BehaviorVideoFiles":
        return cls(
            file_sets=[
                FileSet(
                    name="Metadata CSV Files",
                    description="Per-camera metadata CSV files",
                    encoding_format="text/csv",
                    includes="*/metadata.csv",
                ),
                FileSet(
                    name="Video Files",
                    description="Per-camera video files",
                    includes="*/video.*",
                ),
            ],
        )

    def validate_folder(self, folder: Path) -> List[str]:
        errors = super().validate_folder(folder)
        relative_paths = [
            str(p.relative_to(folder)).replace("\\", "/")
            for p in folder.rglob("*")
            if p.is_file() and p.name != "files.json"
        ]

        camera_dirs: dict[str, list[str]] = {}
        for p in relative_paths:
            parts = p.split("/", 1)
            if len(parts) == 2:
                camera_dirs.setdefault(parts[0], []).append(parts[1])

        for camera_name, files in camera_dirs.items():
            has_metadata = "metadata.csv" in files
            has_video = any(f.startswith("video.") for f in files)
            if has_metadata and not has_video:
                errors.append(f"Camera '{camera_name}': has metadata.csv but no video file")
            if has_video and not has_metadata:
                errors.append(f"Camera '{camera_name}': has video file but no metadata.csv")

        return errors
