"""Description of the expected file organization for a data asset folder"""

import fnmatch
import json
import re
import warnings
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set, Union

from pydantic import Field, SkipValidation

from aind_data_schema.base import DataCoreModel, DataModel

# Sidecar filenames that should be ignored when validating folder contents
_DEFAULT_SIDECARS: Set[str] = {"metadata.nd.json", "files_croissant.json"}

# Croissant JSON-LD @context block, held at module level so it is not
# re-allocated on every call to to_croissant.
CROISSANT_CONTEXT: Dict[str, Any] = {
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
    "equivalentProperty": "cr:equivalentProperty",
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
}


def _as_pattern_list(value: Optional[Union[str, List[str]]]) -> List[str]:
    """Normalize a string-or-list-of-strings field into a list of patterns."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def _validate_croissant(doc: Dict[str, Any]) -> None:
    """Validate a Croissant JSON-LD document via ``mlcroissant``.

    If ``mlcroissant`` is not installed, validation is skipped.
    Raises ``mlcroissant.ValidationError`` if the document is invalid.
    """
    try:
        import mlcroissant as mlc
        from absl import logging as absl_logging
    except ImportError:
        return
    previous = absl_logging.get_verbosity()
    absl_logging.set_verbosity(absl_logging.ERROR)
    try:
        mlc.Dataset(jsonld=doc)
    finally:
        absl_logging.set_verbosity(previous)


def _glob_match(path: str, pattern: str) -> bool:
    """Shell-style glob match where ``*`` does not cross ``/``.

    Supports ``**`` to match zero or more path components.
    """
    return _match_parts(path.split("/"), pattern.split("/"))


def _match_parts(path_parts: List[str], pat_parts: List[str]) -> bool:
    """Recursive component-wise matcher used by _glob_match."""
    if not pat_parts:
        return not path_parts
    head, rest = pat_parts[0], pat_parts[1:]
    if head == "**":
        if not rest:
            return True
        for i in range(len(path_parts) + 1):
            if _match_parts(path_parts[i:], rest):
                return True
        return False
    if not path_parts:
        return False
    if fnmatch.fnmatchcase(path_parts[0], head):
        return _match_parts(path_parts[1:], rest)
    return False


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
            "encodingFormat": self.encoding_format,
        }
        if self.description:
            entry["description"] = self.description
        if self.excludes:
            entry["excludes"] = self.excludes
        return entry


class Files(DataCoreModel):
    """Description of the expected file organization for a data asset folder"""

    _DESCRIBED_BY_URL = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/files.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["0.1.0"]] = Field(default="0.1.0")

    file_sets: List[FileSet] = Field(..., title="File sets", min_length=1)

    def _ignored_filenames(self) -> Set[str]:
        """Sidecar filenames that do not participate in folder validation."""
        return _DEFAULT_SIDECARS | {self.default_filename()}

    def validate_folder(self, folder: Path) -> None:
        """Validate that the file sets describe the contents of ``folder``.

        - Each include pattern must match at least one file (unmatched
          patterns are collected and reported together as a single error).
        - ``excludes`` patterns are honored: matching files are removed from
          the include match list and are treated as known (not orphan) files.
        - Files in the folder that are not described by any FileSet (and are
          not known sidecars) trigger a warning.
        """
        ignored = self._ignored_filenames()
        relative_paths = [
            str(p.relative_to(folder)).replace("\\", "/")
            for p in folder.rglob("*")
            if p.is_file() and p.name not in ignored
        ]

        errors: List[str] = []
        matched: Set[str] = set()
        known_excluded: Set[str] = set()

        for file_set in self.file_sets:
            include_patterns = _as_pattern_list(file_set.includes)
            exclude_patterns = _as_pattern_list(file_set.excludes)
            fs_excluded = {p for p in relative_paths if any(_glob_match(p, ep) for ep in exclude_patterns)}
            known_excluded.update(fs_excluded)
            for pattern in include_patterns:
                fs_matches = [p for p in relative_paths if _glob_match(p, pattern) and p not in fs_excluded]
                if not fs_matches:
                    errors.append(f"FileSet '{file_set.name}': no files matching pattern '{pattern}'")
                matched.update(fs_matches)

        orphans = sorted(set(relative_paths) - matched - known_excluded)
        if orphans:
            warnings.warn("Files in folder not described by any FileSet: " + ", ".join(orphans))

        if errors:
            raise ValueError("Files validation failed:\n  - " + "\n  - ".join(errors))

    def to_croissant(self, validate: bool = True) -> Dict[str, Any]:
        """Convert this Files instance to a Croissant JSON-LD dict.

        When ``validate`` is True (the default) and ``mlcroissant`` is
        available, the resulting document is validated against the
        Croissant 1.0 specification and any ``mlcroissant.ValidationError``
        is raised. If ``mlcroissant`` is not installed, validation is
        skipped silently.
        """
        doc: Dict[str, Any] = {
            "@context": CROISSANT_CONTEXT,
            "@type": "sc:Dataset",
            "conformsTo": "http://mlcommons.org/croissant/1.0",
            "name": self.default_filename().replace(".json", ""),
            "version": self.schema_version,
            "distribution": [fs.to_croissant() for fs in self.file_sets],
        }
        if validate:
            _validate_croissant(doc)
        return doc

    def to_croissant_json(self, validate: bool = True) -> str:
        """Serialize the Croissant JSON-LD to a string."""
        return json.dumps(self.to_croissant(validate=validate), indent=3)

    def write_croissant_file(self, output_directory: Path, validate: bool = True) -> Path:
        """Write a Croissant JSON-LD file alongside the data."""
        output_directory = Path(output_directory)
        output_directory.mkdir(parents=True, exist_ok=True)
        out = output_directory / "files_croissant.json"
        out.write_text(self.to_croissant_json(validate=validate))
        return out
