"""BARseq acquisition metadata for subjects 780345 and 780346.

BARseq (Barcoded Anatomy Resolved by Sequencing) is a multi-day imaging
protocol in which brain sections are sequentially imaged across gene sequencing
cycles, barcode sequencing cycles, and a hybridization cycle. Each cycle images
all sections on the Nikon Ti2-E "Dogwood" spinning disk confocal at the Allen
Institute.

This script produces one acquisition.json per subject. Because the full
acquisition spans multiple slides imaged over multiple days, and the detailed
per-slide parameters are not fully documented, the acquisition is described at
a high level: inputs (brain sections), timeframe, and experimenters. The
processed output is a single cell x gene x barcode table registered to CCFv3,
stored on S3.

Timestamps are derived from folder names and experiment_detail.txt files in
the raw data at /allen/aind/stage/barseq/. Per Polina Kosillo, the folder
date is the day the sequencing run started.

Specimen IDs follow the convention {subject_id}_bar{n:03d}, matching the
section IDs defined in the companion procedures metadata.
"""

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.acquisition import Acquisition, ExternalDataStream

# Source: MAPseq-BARseq methods_forSciComp.pdf, header section
BARSEQ_PROTOCOL_ID = ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"]

# Acquisition note template applied to all subjects.
ACQUISITION_NOTE = (
    "BARseq acquisition performed across multiple slides imaged over multiple days. "
    "Full acquisition includes gene sequencing (7 cycles), barcode sequencing (15 cycles), "
    "and one hybridization cycle. Each slide folder contains all three acquisition types. "
    "Final processed output is a cell x gene x barcode table registered to Allen CCFv3."
)

SUBJECTS = {
    "780345": {
        # Experimenters will simply be "Barseq team"
        "experimenters": ["Barseq team"],
        # Start: first folder date 20250224_780345_slide4_maxprojection (no experiment_detail.txt).
        # End: last folder date 20250321_780345_slide1a_maxprojection (no experiment_detail.txt).
        # Per Polina Kosillo (2026-02-16 Teams): "Dates on the folder are the day the sequencing run was started."
        # Start time is beginning of day (no experiment_detail.txt for first slide).
        # End time is end of day (conservative estimate, no experiment_detail.txt for last slide).
        "acquisition_start": datetime(2025, 2, 24, 0, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles")),
        "acquisition_end": datetime(2025, 3, 21, 23, 59, 59, tzinfo=ZoneInfo("America/Los_Angeles")),
        # BARseq LC section IDs from PR #1763 (procedures_sectioning.py, generate_barseq_lc_780345).
        # Format: {subject_id}_bar{n:03d}, 44 sections covering CCF plates 99-112 (20um thick).
        "specimen_id": [f"780345_bar{i:03d}" for i in range(1, 45)],
    },
    "780346": {
        "experimenters": ["Barseq team"],
        # Start: confirmed from experiment_detail.txt in first slide folder.
        # Source: /allen/aind/stage/barseq/20250613_780346_slide11_maxprojection/experiment_detail.txt
        # End: last folder date 20250711_780346_slide3_maxprojection (no experiment_detail.txt).
        # End time is end of day (conservative estimate).
        "acquisition_start": datetime(2025, 6, 13, 16, 39, 31, tzinfo=ZoneInfo("America/Los_Angeles")),
        "acquisition_end": datetime(2025, 7, 11, 23, 59, 59, tzinfo=ZoneInfo("America/Los_Angeles")),
        # BARseq LC section IDs from PR #1763 (procedures_sectioning.py, generate_barseq_lc_780346).
        # Format: {subject_id}_bar{n:03d}, 51 sections covering CCF plates 99-112 (20um thick).
        "specimen_id": [f"780346_bar{i:03d}" for i in range(1, 52)],
    },
}


def build_acquisition(subject_id: str) -> Acquisition:
    """Build a black-box BARseq acquisition for a given subject."""
    params = SUBJECTS[subject_id]

    notes = ACQUISITION_NOTE

    return Acquisition(
        subject_id=subject_id,
        specimen_id=params["specimen_id"],
        acquisition_start_time=params["acquisition_start"],
        acquisition_end_time=params["acquisition_end"],
        experimenters=params["experimenters"],
        protocol_id=BARSEQ_PROTOCOL_ID,
        acquisition_type="BarcodeSequencing",
        notes=notes,
        data_streams=[
            ExternalDataStream(
                stream_start_time=params["acquisition_start"],
                stream_end_time=params["acquisition_end"],
                modalities=[Modality.BARSEQ],
                notes="Acquired externally by BARseq imaging team.",
            )
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for JSON files")
    args = parser.parse_args()

    for i, subject_id in enumerate(SUBJECTS):
        acq = build_acquisition(subject_id)
        serialized = acq.model_dump_json()
        deserialized = Acquisition.model_validate_json(serialized)
        deserialized.write_standard_file(prefix=f"barseq_{subject_id}", output_directory=args.output_dir)
        print(f"Written: barseq_{subject_id}_acquisition.json")
        if i == 0:
            deserialized.write_standard_file(prefix="barseq", output_directory=args.output_dir)
