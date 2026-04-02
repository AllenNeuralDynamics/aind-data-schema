"""Example of a BARseq acquisition using ExternalDataStream.

BARseq is acquired by the AIBS Molecular Anatomy team using an instrument
and workflows not yet fully documented in the AIND schema. ExternalDataStream
is used here to record acquisition metadata without requiring full instrument
configuration details, treating the data as if it were acquired externally.
"""

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.acquisition import Acquisition, ExternalDataStream

acquisition = Acquisition(
    subject_id="123456",
    acquisition_start_time=datetime(2025, 1, 1, 9, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles")),
    acquisition_end_time=datetime(2025, 1, 31, 17, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles")),
    acquisition_type="BarcodeSequencing",
    data_streams=[
        ExternalDataStream(
            stream_start_time=datetime(2025, 1, 1, 9, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles")),
            stream_end_time=datetime(2025, 1, 31, 17, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles")),
            modalities=[Modality.BARSEQ],
            notes="Acquired externally.",
        )
    ],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = acquisition.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="barseq", output_directory=args.output_dir)
