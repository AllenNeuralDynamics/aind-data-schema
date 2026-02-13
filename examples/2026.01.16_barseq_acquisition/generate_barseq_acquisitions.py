"""Generate all BARseq acquisition metadata files."""

import argparse
from pathlib import Path

from barseq_barcodeseq_builder import create_barcodeseq_acquisition
from barseq_geneseq_builder import create_geneseq_acquisition
from barseq_hyb_builder import create_hyb_acquisition
from experiment_params import get_experiment_params


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate all BARseq acquisition metadata JSON files."
    )
    parser.add_argument(
        "--subject-id",
        default="780346",
        help="Subject ID (default: 780346)",
    )
    return parser.parse_args()


def main():
    """Generate all three BARseq acquisition metadata files."""
    args = parse_args()
    subject_id = args.subject_id

    # Get experiment parameters for this subject
    params = get_experiment_params(subject_id)

    # Define the three acquisition phases
    acquisitions = [
        {
            "name": "geneseq",
            "builder": create_geneseq_acquisition,
            "start_key": "geneseq_start",
            "end_key": "geneseq_end",
            "display_name": "Gene sequencing",
        },
        {
            "name": "barcodeseq",
            "builder": create_barcodeseq_acquisition,
            "start_key": "barcodeseq_start",
            "end_key": "barcodeseq_end",
            "display_name": "Barcode sequencing",
        },
        {
            "name": "hyb",
            "builder": create_hyb_acquisition,
            "start_key": "hyb_start",
            "end_key": "hyb_end",
            "display_name": "Hybridization",
        },
    ]

    # Generate each acquisition file
    output_dir = Path(__file__).parent
    print(f"Generating BARseq acquisition files for subject {subject_id}:")
    print()

    for acq in acquisitions:
        # Create acquisition object
        acquisition = acq["builder"](
            subject_id=subject_id,
            specimen_id=params["specimen_id"],
            num_sections=params["num_sections"],
            ccf_start_plate=params["ccf_start_plate"],
            ccf_end_plate=params["ccf_end_plate"],
            experimenters=params["experimenters"],
            acquisition_start_time=params[acq["start_key"]],
            acquisition_end_time=params[acq["end_key"]],
        )

        # Write to file
        output_file = output_dir / f"barseq_{subject_id}_{acq['name']}_acquisition.json"
        json_str = acquisition.model_dump_json(indent=3)

        with open(output_file, "w") as f:
            f.write(json_str)

        # Print summary
        num_channels = len(acquisition.data_streams[0].configurations[0].channels)
        num_images = len(acquisition.data_streams[0].configurations[0].images)
        num_placeholders = json_str.count("PLACEHOLDER")

        print(f"{acq['display_name']} → {output_file.name}")
        print(f"  Channels: {num_channels}, Images: {num_images}, Placeholders: {num_placeholders}")
        print()


if __name__ == "__main__":
    main()
