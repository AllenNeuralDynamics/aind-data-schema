"""Generate acquisition.json for BARseq experiment - Subject 780346.

Specimen Information (from Paulina's table):
- Lab Tracks ID: 780346
- Sections: 51 coronal sections (20μm thickness)
- Target: Locus Coeruleus (BARseq LC)
- CCF range: plates 99-112
- Coordinate system: CCF Allen (CCFv3)
- Date: 2025-06-11
- Automation: Used automation template

Usage:
    python generate_780346_acquisition.py
"""

from datetime import datetime, timezone
from pathlib import Path

from barseq_acquisition_builder import create_barseq_acquisition


def main():
    """Generate acquisition JSON for subject 780346."""
    
    # Basic experiment information from Paulina's table
    subject_id = "780346"
    specimen_id = f"{subject_id}_PLACEHOLDER_SPECIMEN_ID"  # Must contain subject ID
    num_sections = 51  # From Paulina's table: sec 1 - sec 51
    ccf_start_plate = 99
    ccf_end_plate = 112
    
    # Experimenters - NEEDS TO BE FILLED IN
    experimenters = [
        "PLACEHOLDER_EXPERIMENTER_1",
        "PLACEHOLDER_EXPERIMENTER_2",
    ]
    
    # Experiment date from notebook (6/11/25)
    # Using noon as placeholder time since exact time unknown
    experiment_date = datetime(2025, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    
    # Timing for each phase - using experiment_date as base with placeholder offsets
    # These will need to be updated with actual acquisition times
    gene_seq_start = datetime(2025, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    gene_seq_end = datetime(2025, 6, 11, 14, 0, 0, tzinfo=timezone.utc)
    
    barcode_seq_start = datetime(2025, 6, 11, 14, 0, 0, tzinfo=timezone.utc)
    barcode_seq_end = datetime(2025, 6, 11, 18, 0, 0, tzinfo=timezone.utc)
    
    hyb_start = datetime(2025, 6, 11, 18, 0, 0, tzinfo=timezone.utc)
    hyb_end = datetime(2025, 6, 11, 19, 0, 0, tzinfo=timezone.utc)
    
    # Ethics approval - NEEDS TO BE FILLED IN
    ethics_review_id = ["PLACEHOLDER_IACUC_PROTOCOL"]
    
    # Additional notes from notebook
    notes = (
        "BARseq experiment performed using automation template mounted on microscope. "
        "Automated microfluidics setup for reagent delivery."
    )
    
    # Create the acquisition object
    acquisition = create_barseq_acquisition(
        subject_id=subject_id,
        specimen_id=specimen_id,
        num_sections=num_sections,
        ccf_start_plate=ccf_start_plate,
        ccf_end_plate=ccf_end_plate,
        experimenters=experimenters,
        acquisition_date=experiment_date,
        instrument_id="Dogwood",
        gene_seq_start_time=gene_seq_start,
        gene_seq_end_time=gene_seq_end,
        barcode_seq_start_time=barcode_seq_start,
        barcode_seq_end_time=barcode_seq_end,
        hyb_start_time=hyb_start,
        hyb_end_time=hyb_end,
        ethics_review_id=ethics_review_id,
        notes=notes,
    )
    
    # Validate and write the JSON file
    output_path = Path("barseq_780346_acquisition.json")
    
    try:
        # Validate the acquisition object
        acquisition.model_validate(acquisition.model_dump())
        print("✓ Acquisition object validated successfully")
        
        # Write to file
        acquisition.write_standard_file(prefix="barseq_780346")
        print(f"✓ Acquisition JSON written to: {output_path}")
        
        # Print summary
        print("\n" + "="*70)
        print("ACQUISITION SUMMARY - Subject 780346")
        print("="*70)
        print(f"Subject ID: {subject_id}")
        print(f"Specimen ID: {specimen_id}")
        print(f"Sections: {num_sections} × 20μm coronal sections")
        print(f"CCF Range: plates {ccf_start_plate}-{ccf_end_plate}")
        print(f"Coordinate System: CCFv3 (Allen Common Coordinate Framework)")
        print(f"Experiment Date: {experiment_date.date()}")
        print(f"Instrument: Dogwood (Nikon Ti2-E + Crest X-Light V3)")
        print(f"Number of Data Streams: {len(acquisition.data_streams)}")
        print("\nData Streams:")
        for i, stream in enumerate(acquisition.data_streams, 1):
            cycle_info = stream.notes.split(':')[0]
            print(f"  {i}. {cycle_info}")
            print(f"     Channels: {len(stream.configurations[0].channels)}")
            print(f"     Active Devices: {len(stream.active_devices)}")
        
        # Count placeholders
        json_str = acquisition.model_dump_json(indent=2)
        placeholder_count = json_str.count("PLACEHOLDER")
        print(f"\n⚠  PLACEHOLDER values to fill in: {placeholder_count}")
        
        print("\nPlaceholder Categories:")
        print("  • Personnel: Experimenter names, IACUC protocol")
        print("  • Specimen: Specimen ID naming convention")
        print("  • Hardware: Laser/filter assignments for each base (G/T/A/C)")
        print("  • Settings: Laser powers, exposure time")
        print("  • Timing: Exact acquisition start/end times for each phase")
        
    except Exception as e:
        print(f"✗ Error generating acquisition: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
