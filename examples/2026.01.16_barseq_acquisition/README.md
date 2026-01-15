# BARseq Acquisition Metadata Generation

This directory contains scripts to generate acquisition metadata JSON files for BARseq experiments conducted at the Allen Institute for Neural Dynamics.

## Overview

BARseq (Barcoded Anatomy Resolved by Sequencing) is a technique for mapping neural projections using barcoded viral libraries and in situ sequencing. The acquisition process consists of three main phases:

1. **Gene Sequencing (7 cycles):** Reads 7-base barcodes from a 109-gene codebook
2. **Barcode Sequencing (15 cycles):** Reads 30-base Sindbis virus barcodes from HZ120 library
3. **Hybridization (1 cycle):** Direct fluorescent probe visualization for anatomical reference

## Files

- `barseq_acquisition_builder.py` - Main builder function with shared logic
- `generate_780345_acquisition.py` - Generates acquisition for subject 780345 (2025-02-19)
- `generate_780346_acquisition.py` - Generates acquisition for subject 780346 (2025-06-11)
- `barseq_780345_acquisition.json` - Generated acquisition metadata for 780345
- `barseq_780346_acquisition.json` - Generated acquisition metadata for 780346
- `PLACEHOLDERS_TO_FILL.md` - Detailed list of missing information

## Generated Files

Each acquisition JSON contains:
- 3 DataStreams (gene sequencing, barcode sequencing, hybridization)
- 14 total channels across all streams
- Complete protocol references
- Placeholder values clearly marked with `PLACEHOLDER_` prefix

## Usage

### Generating Acquisition Files

```bash
# Generate acquisition for subject 780345
python generate_780345_acquisition.py

# Generate acquisition for subject 780346
python generate_780346_acquisition.py
```

### Validating Generated Files

The scripts automatically validate the generated JSON against the aind-data-schema. You'll see:
- ✓ Success message if validation passes
- Summary of data streams and channels
- Count of placeholder values that need to be filled in

## Placeholders

Each generated JSON contains **60 placeholder values** that need to be replaced with actual experimental data. These are clearly marked with the `PLACEHOLDER_` prefix and fall into these categories:

1. **Personnel:**
   - Experimenter names
   - IACUC protocol numbers

2. **Specimen:**
   - Specimen IDs for brain sections

3. **Hardware Configuration:**
   - Laser device names (which specific Lumencor lasers for each base)
   - Laser wavelengths
   - Laser power settings
   - Emission filter device names
   - Emission wavelengths

4. **Acquisition Settings:**
   - Camera exposure times
   - Exact start/end times for each sequencing phase

See `PLACEHOLDERS_TO_FILL.md` for a complete list of questions to answer.

## File Structure

```json
{
  "schema_version": "2.2.3",
  "subject_id": "780345",
  "specimen_id": "PLACEHOLDER_SPECIMEN_ID_780345",
  "experimenters": ["PLACEHOLDER_EXPERIMENTER_1", ...],
  "acquisition_type": "BarcodeSequencing",
  "instrument_id": "Dogwood",
  "data_streams": [
    {
      "stream_start_time": "2025-02-19T12:00:00+00:00",
      "stream_end_time": "2025-02-19T14:00:00+00:00",
      "modalities": ["BARSEQ"],
      "configurations": [
        {
          "device_name": "Ti2-E__0",
          "channels": [
            {
              "channel_name": "Gene_G",
              "intended_measurement": "Gene sequencing - base G",
              "light_sources": [...],
              "emission_filters": [...],
              "detector": {...}
            },
            ...
          ]
        }
      ]
    },
    ...
  ]
}
```

## Next Steps

1. **For Schema Review:** The JSON files can be reviewed for format/structure correctness independently of scientific details
2. **For Scientific Review:** Use `PLACEHOLDERS_TO_FILL.md` to gather missing experimental parameters
3. **After Filling Placeholders:** Re-run the generator scripts with actual values to create final metadata files

## Dependencies

```bash
pip install aind-data-schema
```

## References

- BARseq Protocol: dx.doi.org/10.17504/protocols.io.81wgbp4j3vpk/v2
- AIND Data Schema: https://aind-data-schema.readthedocs.io/
- Instrument: Nikon Ti2-E "Dogwood" with Crest X-Light V3 spinning disk confocal

## Technical Details

### Imaging Parameters (from protocol):
- **Objective:** Nikon CFI S Plan Fluor LWD 20X 0.7NA (non-immersion)
- **Z-stack:** 10 images per FOV
- **Step size:** 1.5 μm
- **Tile overlap:** 24%
- **Pixel size:** 0.33 μm
- **Camera:** Photometrics Kinetix
- **Light source:** Lumencor Celesta

### Tissue:
- **Section thickness:** 20 μm
- **Orientation:** Coronal
- **Target region:** Locus Coeruleus
- **Mounting:** 4 sections per slide
