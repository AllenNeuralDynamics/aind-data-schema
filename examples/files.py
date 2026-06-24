"""Example Files description for an AIND behavior-videos data asset folder.

Expected folder structure::

    <data-asset>/
      behavior-videos/
        <CameraName>/
          metadata.csv
          video.<ext>
"""

import argparse

from aind_data_schema.core.files import FileSet, Files

f = Files(
    file_sets=[
        FileSet(
            name="Metadata CSV Files",
            description="Per-camera metadata CSV files",
            encoding_format="text/csv",
            includes="behavior-videos/*/metadata.csv",
        ),
        FileSet(
            name="Video Files",
            description="Per-camera video files",
            encoding_format="video/mp4",
            includes="behavior-videos/*/video.*",
        ),
    ],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = f.model_dump_json()
    deserialized = Files.model_validate_json(serialized)
    deserialized.write_standard_file(output_directory=args.output_dir)
