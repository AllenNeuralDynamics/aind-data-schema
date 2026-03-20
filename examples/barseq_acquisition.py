"""BARseq acquisition metadata (black-box approach)

Creates one acquisition.json per subject for BARseq subjects 780345 and 780346.

This uses a "black-box" approach: each acquisition is described by its inputs
(brain sections) and approximate timeframe without attempting to capture the
detailed multi-day, multi-slide imaging process. This decision was made because
fully describing the acquisition would require more coordination with the BARseq
team than is currently feasible.

For the detailed (abandoned) approach, see PR #1690:
https://github.com/AllenNeuralDynamics/aind-data-schema/pull/1690

Remaining placeholders:
- specimen_id: Pending from BARseq procedures (see PR #1763:
  https://github.com/AllenNeuralDynamics/aind-data-schema/pull/1763)
"""

import argparse
from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.acquisition import Acquisition, DataStream

# Raw data location on allen network share.
# Source: Polina Kosillo, 2026-02-16 Teams chat (MapSeq/BARseq metadata channel)
BARSEQ_RAW_DATA_PATH = "smb://allen/aind/stage/barseq/"

# Source: MAPseq-BARseq methods_forSciComp.pdf, header section
BARSEQ_PROTOCOL_ID = ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"]

# Instrument ID for the Nikon Ti2-E "Dogwood" spinning disk confocal.
# Source: aind-data-schema barseq instrument PR #1685
INSTRUMENT_ID = "Dogwood"

# Acquisition note template applied to all subjects.
ACQUISITION_NOTE = (
    "BARseq acquisition performed across multiple slides imaged over multiple days "
    f"on the Dogwood spinning disk confocal. Raw data stored at {BARSEQ_RAW_DATA_PATH}. "
    "Full acquisition includes gene sequencing (7 cycles), barcode sequencing (15 cycles), "
    "and one hybridization cycle. Each slide folder contains all three acquisition types. "
    "Final processed output is a cell x gene x barcode table registered to Allen CCFv3."
)

SUBJECTS = {
    "780345": {
        # Experimenters from experiment_detail.txt files in raw data slide folders.
        # Source: smb://allen/aind/stage/barseq/20250303_780345_slide7_maxprojection/experiment_detail.txt
        #         smb://allen/aind/stage/barseq/20250305_780345_slide8_maxprojection/experiment_detail.txt
        #         smb://allen/aind/stage/barseq/20250317_780345_slide9_maxprojection/experiment_detail.txt
        "experimenters": ["Mara Rue", "Shannon Khem", "Tracy"],
        # Start: first folder date 20250224_780345_slide4_maxprojection (no experiment_detail.txt).
        # End: last folder date 20250321_780345_slide1a_maxprojection (no experiment_detail.txt).
        # Per Polina Kosillo (2026-02-16 Teams): "Dates on the folder are the day the sequencing run was started."
        # Start time is beginning of day (no experiment_detail.txt for first slide).
        # End time is end of day (conservative estimate, no experiment_detail.txt for last slide).
        # NOTE: The S3 asset date (2025-02-20) is 4 days before the first imaging folder date (2025-02-24).
        # This discrepancy is unresolved — it may reflect when the asset was registered or when library prep began.
        "acquisition_start": datetime(2025, 2, 24, 0, 0, 0, tzinfo=timezone.utc),
        "acquisition_end": datetime(2025, 3, 21, 23, 59, 59, tzinfo=timezone.utc),
        # Processed output file location on S3.
        # Source: Polina Kosillo, 2026-02-16 Teams chat (MapSeq/BARseq metadata channel)
        "output_path": "s3://aind-private-data-prod-o5171v/780345_2025-02-20_00-00-00/BARseq/combined_neurons_clust_CCFv2.mat",
        # TODO: Replace with actual specimen IDs from BARseq procedures (PR #1763).
        # Slides imaged (from folder names at BARSEQ_RAW_DATA_PATH):
        # slide1, slide1a, slide1a_cont2, slide1b, slide2, slide4, slide5, slide6, slide7, slide8, slide9
        "specimen_id": "780345_PLACEHOLDER_SPECIMEN_ID",
    },
    "780346": {
        # Experimenters from experiment_detail.txt files in raw data slide folders.
        # Source: smb://allen/aind/stage/barseq/20250613_780346_slide11_maxprojection/experiment_detail.txt
        #         smb://allen/aind/stage/barseq/20250623_780346_slide9_maxprojection/experiment_detail.txt
        #         smb://allen/aind/stage/barseq/20250703_780346_slide15_maxprojection/experiment_detail.txt
        #         smb://allen/aind/stage/barseq/20250707_780346_slide13_maxprojection/experiment_detail.txt
        #         smb://allen/aind/stage/barseq/20250709_780346_slide14_maxprojection/experiment_detail.txt
        "experimenters": ["Mara Rue", "Shannon Khem"],
        # Start: confirmed from experiment_detail.txt in first slide folder.
        # Source: smb://allen/aind/stage/barseq/20250613_780346_slide11_maxprojection/experiment_detail.txt
        # End: last folder date 20250711_780346_slide3_maxprojection (no experiment_detail.txt).
        # End time is end of day (conservative estimate).
        "acquisition_start": datetime(2025, 6, 13, 16, 39, 31, tzinfo=timezone.utc),
        "acquisition_end": datetime(2025, 7, 11, 23, 59, 59, tzinfo=timezone.utc),
        # Processed output file location on S3.
        # Source: Polina Kosillo, 2026-02-16 Teams chat (MapSeq/BARseq metadata channel)
        "output_path": "s3://aind-private-data-prod-o5171v/780346_2025-06-11_00-00-00/BARseq/combined_neurons_clust_CCFv2.mat",
        # TODO: Replace with actual specimen IDs from BARseq procedures (PR #1763).
        # Slides imaged (from folder names at BARSEQ_RAW_DATA_PATH):
        # slide3, slide5, slide5_cont, slide9, slide10, slide11, slide12, slide13, slide14, slide15
        "specimen_id": "780346_PLACEHOLDER_SPECIMEN_ID",
    },
}


def build_acquisition(subject_id: str) -> Acquisition:
    """Build a black-box BARseq acquisition for a given subject."""
    params = SUBJECTS[subject_id]

    notes = ACQUISITION_NOTE + f" Processed output: {params['output_path']}."

    return Acquisition(
        subject_id=subject_id,
        specimen_id=params["specimen_id"],
        instrument_id=INSTRUMENT_ID,
        acquisition_start_time=params["acquisition_start"],
        acquisition_end_time=params["acquisition_end"],
        experimenters=params["experimenters"],
        protocol_id=BARSEQ_PROTOCOL_ID,
        acquisition_type="BarcodeSequencing",
        notes=notes,
        data_streams=[
            DataStream(
                stream_start_time=params["acquisition_start"],
                stream_end_time=params["acquisition_end"],
                modalities=[Modality.BARSEQ],
                active_devices=[],
                configurations=[],
                notes="Acquired externally by BARseq imaging team.",
            )
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for JSON files")
    args = parser.parse_args()

    for subject_id in SUBJECTS:
        acq = build_acquisition(subject_id)
        serialized = acq.model_dump_json()
        deserialized = Acquisition.model_validate_json(serialized)
        deserialized.write_standard_file(prefix=f"barseq_{subject_id}", output_directory=args.output_dir)
        print(f"Written: barseq_{subject_id}_acquisition.json")
