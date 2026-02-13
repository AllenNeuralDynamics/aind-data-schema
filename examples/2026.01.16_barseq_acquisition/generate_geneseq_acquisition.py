"""Generate BARseq Gene Sequencing acquisition metadata."""

import argparse
from datetime import datetime, timezone
from pathlib import Path

from barseq_geneseq_builder import create_geneseq_acquisition


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate BARseq gene sequencing acquisition metadata JSON."
    )
    parser.add_argument(
        "--subject-id",
        default="780346",
        help="Subject ID (default: 780346)",
    )
    return parser.parse_args()


def main():
    """Generate gene sequencing acquisition metadata."""
    args = parse_args()
    subject_id = args.subject_id
    specimen_id = f"{subject_id}_PLACEHOLDER_SPECIMEN_ID"

    # Tissue information
    num_sections = 51  # Number of 20μm coronal sections
    ccf_start_plate = 99  # Starting CCFv3 plate number
    ccf_end_plate = 112  # Ending CCFv3 plate number

    # Personnel
    experimenters = ["Imaging core"]

    # Acquisition timing - PLACEHOLDERS
    # TODO: Extract actual times from max projection files once file paths are known
    gene_seq_start = datetime(2025, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    gene_seq_end = datetime(2025, 6, 11, 14, 0, 0, tzinfo=timezone.utc)

    # Create gene sequencing acquisition
    acquisition = create_geneseq_acquisition(
        subject_id=subject_id,
        specimen_id=specimen_id,
        num_sections=num_sections,
        ccf_start_plate=ccf_start_plate,
        ccf_end_plate=ccf_end_plate,
        experimenters=experimenters,
        acquisition_start_time=gene_seq_start,
        acquisition_end_time=gene_seq_end,
    )

    # Validate and write to file
    output_file = Path(__file__).parent / f"barseq_{subject_id}_geneseq_acquisition.json"

    # Write JSON with validation
    json_str = acquisition.model_dump_json(indent=3)
    with open(output_file, "w") as f:
        f.write(json_str)

    # Print summary
    print("Acquisition object validated successfully")
    print(f"Acquisition JSON written to: {output_file.name}")
    print()
    print("=" * 70)
    print(f"GENE SEQUENCING ACQUISITION - Subject {subject_id}")
    print("=" * 70)
    print(f"Subject ID: {subject_id}")
    print(f"Specimen ID: {specimen_id}")
    print(f"Sections: {num_sections} x 20um coronal sections")
    print(f"CCF Range: plates {ccf_start_plate}-{ccf_end_plate}")
    print(f"Experiment Date: {gene_seq_start.date()}")
    print(f"Instrument: Dogwood (Nikon Ti2-E + Crest X-Light V3)")
    print()
    print("Data Stream:")
    print("  Gene barcode sequencing (7 cycles)")
    print(f"  Channels: {len(acquisition.data_streams[0].configurations[0].channels)}")
    print(f"  Active Devices: {len(acquisition.data_streams[0].active_devices)}")
    print(f"  ImageSPIM objects: {len(acquisition.data_streams[0].configurations[0].images)}")
    print(f"    - Tiles (not saved): {json_str.count('not saved')}")
    print(f"    - Max projections: {json_str.count('PLACEHOLDER_max_projection_path')}")
    print()

    # Count placeholders
    placeholder_count = json_str.count("PLACEHOLDER")
    print(f"PLACEHOLDER values to fill in: {placeholder_count}")
    print("  - Max projection file paths: 5")
    print("  - Specimen ID: 1")
    print()
    print("Next steps:")
    print("  1. Obtain file paths to max projection files to extract actual acquisition times")
    print("  2. Fill in specimen ID")
    print()


if __name__ == "__main__":
    main()
