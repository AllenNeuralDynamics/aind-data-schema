import fnmatch
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import Field, SkipValidation

from aind_data_schema.base import DataCoreModel, DataModel


class FileSet(DataModel):
    """A set of files matching a glob pattern, inspired by Croissant cr:FileSet"""

    name: str = Field(..., title="Name")
    description: Optional[str] = Field(default=None, title="Description")
    encoding_format: str = Field(..., title="Encoding format (MIME type)")
    includes: Union[str, List[str]] = Field(..., title="Glob pattern(s) for included files")
    excludes: Optional[Union[str, List[str]]] = Field(default=None, title="Glob pattern(s) for excluded files")

    def _croissant_id(self) -> str:
        return re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")

    def to_croissant(self) -> Dict[str, Any]:
        entry: Dict[str, Any] = {
            "@type": "cr:FileSet",
            "@id": self._croissant_id(),
            "name": self.name,
            "includes": self.includes,
        }
        if self.description:
            entry["description"] = self.description
        if self.encoding_format:
            entry["encodingFormat"] = self.encoding_format
        if self.excludes:
            entry["excludes"] = self.excludes
        return entry


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

    def to_croissant(self) -> Dict[str, Any]:
        """Convert this Files instance to a Croissant JSON-LD dict."""
        return {
            "@context": {
                "@language": "en",
                "@vocab": "https://schema.org/",
                "sc": "https://schema.org/",
                "cr": "http://mlcommons.org/croissant/",
                "rai": "http://mlcommons.org/croissant/RAI/",
                "dct": "http://purl.org/dc/terms/",
                "citeAs": "cr:citeAs",
                "column": "cr:column",
                "conformsTo": "dct:conformsTo",
                "data": {"@id": "cr:data", "@type": "@json"},
                "dataType": {"@id": "cr:dataType", "@type": "@vocab"},
                "examples": {"@id": "cr:examples", "@type": "@json"},
                "extract": "cr:extract",
                "field": "cr:field",
                "fileProperty": "cr:fileProperty",
                "fileObject": "cr:fileObject",
                "fileSet": "cr:fileSet",
                "format": "cr:format",
                "includes": "cr:includes",
                "excludes": "cr:excludes",
                "isLiveDataset": "cr:isLiveDataset",
                "jsonPath": "cr:jsonPath",
                "key": "cr:key",
                "md5": "cr:md5",
                "parentField": "cr:parentField",
                "path": "cr:path",
                "recordSet": "cr:recordSet",
                "references": "cr:references",
                "regex": "cr:regex",
                "repeated": "cr:repeated",
                "replace": "cr:replace",
                "samplingRate": "cr:samplingRate",
                "separator": "cr:separator",
                "source": "cr:source",
                "subField": "cr:subField",
                "transform": "cr:transform",
            },
            "@type": "sc:Dataset",
            "conformsTo": "http://mlcommons.org/croissant/1.0",
            "name": self.default_filename().replace(".json", ""),
            "version": self.schema_version,
            "distribution": [fs.to_croissant() for fs in self.file_sets],
        }

    def to_croissant_json(self) -> str:
        """Serialize the Croissant JSON-LD to a string."""
        return json.dumps(self.to_croissant(), indent=3)

    def write_croissant_file(self, output_directory: Path) -> Path:
        """Write a Croissant JSON-LD file alongside the data."""
        output_directory = Path(output_directory)
        output_directory.mkdir(parents=True, exist_ok=True)
        out = output_directory / "files_croissant.json"
        out.write_text(self.to_croissant_json())
        return out


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
                    encoding_format="video/mp4",
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
