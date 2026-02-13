# BARseq Acquisition Metadata Generation

This directory contains scripts to generate acquisition metadata JSON files for BARseq experiments conducted at the Allen Institute for Neural Dynamics.

**Subjects:** This metadata structure applies to both subjects 780345 and 780346. Both follow the same BARseq protocol with 20μm coronal sections through the Locus Coeruleus (LC). The example files currently demonstrate the structure using subject 780346.

## Overview

BARseq (Barcoded Anatomy Resolved by Sequencing) is a technique for mapping neural projections using barcoded viral libraries and in situ sequencing. Each BARseq experiment generates **3 separate raw data assets**, each requiring its own acquisition.json file:

1. **Gene Sequencing (7 cycles):** Reads 7-base barcodes from a 109-gene codebook
2. **Barcode Sequencing (15 cycles):** Reads 30-base Sindbis virus barcodes from HZ120 library
3. **Hybridization (1 cycle):** Direct fluorescent probe visualization for anatomical reference

These 3 raw assets are later processed together to create a single derived asset.

**Specimen Details:**
- 20 μm coronal sections through Locus Coeruleus (LC)
- 4 sections per slide (from lab notes 780345/780346)
- Imaged on Nikon Ti2-E "Dogwood" with Crest X-Light V3 spinning disk confocal

## Files

**Builder modules:**
- `barseq_geneseq_builder.py` - Gene sequencing acquisition builder
- `barseq_barcodeseq_builder.py` - Barcode sequencing acquisition builder
- `barseq_hyb_builder.py` - Hybridization acquisition builder

**Generator scripts:**
- `generate_geneseq_acquisition.py` - Gene seq acquisition (`--subject-id` defaults to 780346)
- `generate_barcodeseq_acquisition.py` - Barcode seq acquisition (`--subject-id` defaults to 780346)
- `generate_hyb_acquisition.py` - Hybridization acquisition (`--subject-id` defaults to 780346)

**Generated acquisition JSON files** (named `barseq_{subject_id}_*.json`):
- `barseq_780346_geneseq_acquisition.json` - Gene sequencing (6 placeholders)
- `barseq_780346_barcodeseq_acquisition.json` - Barcode sequencing (5 placeholders)
- `barseq_780346_hyb_acquisition.json` - Hybridization (14 placeholders)
- Same naming for 780345 when run with `--subject-id 780345`
- Total: 25 placeholders per subject

**Documentation:**
- `SUMMARY.md` - Decisions made, sources, and remaining placeholders
- `README.md` - This file

## Usage

### Generating Acquisition Files

```bash
# Using uv (recommended) - defaults to subject 780346
uv run python generate_geneseq_acquisition.py
uv run python generate_barcodeseq_acquisition.py
uv run python generate_hyb_acquisition.py

# For subject 780345:
uv run python generate_geneseq_acquisition.py --subject-id 780345
uv run python generate_barcodeseq_acquisition.py --subject-id 780345
uv run python generate_hyb_acquisition.py --subject-id 780345
```

### Validating Generated Files

The scripts automatically validate the generated JSON against the aind-data-schema. You'll see:
- Success message if validation passes
- Summary of channels and active devices
- Count of remaining placeholder values

## What's Filled In

**From Aixin's email + instrument config files (MMConfig_Ti2E-xc2.1.txt and dogwood.json):**
- Experimenters: "Imaging core"
- Tile dimensions: 3200 × 3200 × 10 pixels (max projection)
- Tile grid: 14 × 8 = 112 tiles per channel with 23% overlap
- First tile position: (-736, -736) pixels
- Pixel size: 0.33 μm (XY)
- Z-step: 1.5 μm (from methods doc)
- Laser wavelengths for gene/barcode bases (514, 561, 640 nm) and DAPI (365 nm)
- Emission filter names for all gene/barcode channels
- Exposure times: G=60ms, T=30ms, A=20ms, C=40ms, Hyb-DAPI=20ms

## Placeholders Remaining

**Total: 25 placeholders per subject (50 total for 780345 and 780346)**
- Gene sequencing: 6 (5 max projection file paths + 1 specimen ID)
- Barcode sequencing: 5 (4 max projection file paths + 1 specimen ID)
- Hybridization: 14 (5 max projection file paths + 8 hyb laser/filter + 1 specimen ID)

### What We Removed:
- Laser power values (not available from config files)
- Peak emission wavelengths (only filter ranges available)

### Priority Items:

1. **File paths** (CRITICAL): Need paths to max projection files to extract acquisition timestamps and fill file_name fields for both subjects
   - Gene: 5 channels (GeneSeq_G/T/A/C, DAPI)
   - Barcode: 4 channels (BarcodeSeq_G/T/A/C)
   - Hyb: 5 channels (Hyb_XC2758/XC2759/XC2760/YS221, DAPI)
   - **Total: 14 file paths per subject (28 for both 780345 and 780346)**

2. **Hybridization probe mapping** (CRITICAL): Which probe (XC2758/XC2759/XC2760/YS221) uses which fluorophore (GFP/YFP/TxRed/Cy5)? (8 placeholders: 4 lasers + 4 filters)

3. **Specimen IDs**: Actual specimen identifiers for both subjects (6 placeholders: 3 per subject)

### Note on Tiling:
Images are acquired as a 14×8 tile grid (112 tiles per channel) with 23% overlap. Individual tiles are transient and deleted after stitching, but they are documented in the acquisition metadata with file_name="not saved" to capture the acquisition process. Only the final stitched max projection image is saved per channel.

See `SUMMARY.md` for complete details on decisions made, data sources, and remaining placeholders.

## File Structure

Each acquisition JSON represents a single raw data asset:

**Gene Sequencing:**
- 1 DataStream with 5 channels (GeneSeq_G/T/A/C, DAPI)
- 565 ImageSPIM objects per acquisition:
  - 560 tiles (5 channels × 112 tiles, file_name="not saved")
  - 5 max projections (1 per channel, file_name="PLACEHOLDER_max_projection_path")

**Barcode Sequencing:**
- 1 DataStream with 4 channels (BarcodeSeq_G/T/A/C)
- 452 ImageSPIM objects per acquisition:
  - 448 tiles (4 channels × 112 tiles, file_name="not saved")
  - 4 max projections (1 per channel, file_name="PLACEHOLDER_max_projection_path")

**Hybridization:**
- 1 DataStream with 5 channels (Hyb_XC2758/XC2759/XC2760/YS221, DAPI)
- 565 ImageSPIM objects per acquisition:
  - 560 tiles (5 channels × 112 tiles, file_name="not saved")
  - 5 max projections (1 per channel, file_name="PLACEHOLDER_max_projection_path")

**Note:** Tiles document the acquisition process (14×8 grid with 23% overlap) even though they are transient and deleted after stitching. Max projections are the saved files.

**Calculated dimensions:**
- Individual tile: 3200 × 3200 × 10 pixels
- Stitched max projection: 35,968 × 21,184 × 10 pixels (calculated from tile grid)

## Next Steps

1. **Obtain file paths** to max projection files for both subjects (780345 and 780346) to extract actual timestamps
2. **Determine probe-to-fluorophore mapping** for hybridization channels (XC2758/XC2759/XC2760/YS221)
3. **Gather specimen IDs** for both subjects
4. **Generate metadata for subject 780345** using the same builder scripts
5. **Review `SUMMARY.md`** with the BARseq team for validation

## Dependencies

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv sync

# Run generators
uv run python generate_geneseq_acquisition.py
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
