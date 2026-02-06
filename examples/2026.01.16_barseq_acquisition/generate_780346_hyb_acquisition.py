"""Generate BARseq Hybridization acquisition metadata for subject 780346."""

import json
from datetime import datetime, timezone
from pathlib import Path

from barseq_hyb_builder import create_hyb_acquisition


def main():
    """Generate hybridization acquisition metadata for subject 780346."""
    # Subject and specimen information
    subject_id = "780346"
    specimen_id = f"{subject_id}_PLACEHOLDER_SPECIMEN_ID"

    # Tissue information
    num_sections = 51
    ccf_start_plate = 99
    ccf_end_plate = 112

    # Personnel
    experimenters = [
        "PLACEHOLDER_EXPERIMENTER_1",
        "PLACEHOLDER_EXPERIMENTER_2",
    ]

    # Acquisition timing - PLACEHOLDERS
    # TODO: Extract actual times from max projection files once file paths are known
    hyb_start = datetime(2025, 6, 11, 18, 0, 0, tzinfo=timezone.utc)
    hyb_end = datetime(2025, 6, 11, 19, 0, 0, tzinfo=timezone.utc)

    # Additional notes
    notes = (
        "BARseq experiment performed using automation template mounted on microscope. "
        "Automated microfluidics setup for reagent delivery."
    )

    # Create hybridization acquisition
    acquisition = create_hyb_acquisition(
        subject_id=subject_id,
        specimen_id=specimen_id,
        num_sections=num_sections,
        ccf_start_plate=ccf_start_plate,
        ccf_end_plate=ccf_end_plate,
        experimenters=experimenters,
        acquisition_start_time=hyb_start,
        acquisition_end_time=hyb_end,
        notes=notes,
    )

    # Validate and write to file
    output_file = Path(__file__).parent / "barseq_780346_hyb_acquisition.json"

    # Write JSON with validation
    json_str = acquisition.model_dump_json(indent=3)
    with open(output_file, "w") as f:
        f.write(json_str)

    # Print summary
    print("Acquisition object validated successfully")
    print(f"Acquisition JSON written to: {output_file.name}")
    print()
    print("=" * 70)
    print(f"HYBRIDIZATION ACQUISITION - Subject {subject_id}")
    print("=" * 70)
    print(f"Subject ID: {subject_id}")
    print(f"Specimen ID: {specimen_id}")
    print(f"Sections: {num_sections} × 20μm coronal sections")
    print(f"CCF Range: plates {ccf_start_plate}-{ccf_end_plate}")
    print(f"Experiment Date: {hyb_start.date()}")
    print(f"Instrument: Dogwood (Nikon Ti2-E + Crest X-Light V3)")
    print()
    print("Data Stream:")
    print("  Fluorescent in situ hybridization with 4 probes")
    print(f"  Channels: {len(acquisition.data_streams[0].configurations[0].channels)}")
    print(
        f"  Active Devices: {len(acquisition.data_streams[0].active_devices)}"
    )
    print()

    # Count placeholders
    placeholder_count = json_str.count("PLACEHOLDER")
    print(f"PLACEHOLDER values to fill in: {placeholder_count}")
    print()
    print("Next steps:")
    print("  1. Obtain file paths to max projection files to extract actual acquisition times")
    print("  2. Fill in hardware configuration (lasers, filters, wavelengths, powers)")
    print("  3. Fill in experimenter names and specimen ID")
    print()


if __name__ == "__main__":
    main()
