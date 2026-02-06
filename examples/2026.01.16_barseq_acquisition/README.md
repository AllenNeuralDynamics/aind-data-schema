# BARseq Acquisition Metadata Generation

This directory contains scripts to generate acquisition metadata JSON files for BARseq experiments conducted at the Allen Institute for Neural Dynamics.

## Overview

BARseq (Barcoded Anatomy Resolved by Sequencing) is a technique for mapping neural projections using barcoded viral libraries and in situ sequencing. Each BARseq experiment generates **3 separate raw data assets**, each requiring its own acquisition.json file:

1. **Gene Sequencing (7 cycles):** Reads 7-base barcodes from a 109-gene codebook
2. **Barcode Sequencing (15 cycles):** Reads 30-base Sindbis virus barcodes from HZ120 library
3. **Hybridization (1 cycle):** Direct fluorescent probe visualization for anatomical reference

These 3 raw assets are later processed together to create a single derived asset.

## Files

**Builder modules:**
- `barseq_geneseq_builder.py` - Gene sequencing acquisition builder
- `barseq_barcodeseq_builder.py` - Barcode sequencing acquisition builder
- `barseq_hyb_builder.py` - Hybridization acquisition builder

**Generator scripts for subject 780346:**
- `generate_780346_geneseq_acquisition.py` - Generates gene seq acquisition
- `generate_780346_barcodeseq_acquisition.py` - Generates barcode seq acquisition
- `generate_780346_hyb_acquisition.py` - Generates hybridization acquisition

**Generated acquisition JSON files:**
- `barseq_780346_geneseq_acquisition.json` - Gene sequencing (18 placeholders)
- `barseq_780346_barcodeseq_acquisition.json` - Barcode sequencing (15 placeholders)
- `barseq_780346_hyb_acquisition.json` - Hybridization (24 placeholders)

**Documentation:**
- `PLACEHOLDERS_TO_FILL.md` - Detailed list of remaining placeholders
- `README.md` - This file

## Usage

### Generating Acquisition Files

```bash
# Using uv (recommended)
uv run python generate_780346_geneseq_acquisition.py
uv run python generate_780346_barcodeseq_acquisition.py
uv run python generate_780346_hyb_acquisition.py
```

### Validating Generated Files

The scripts automatically validate the generated JSON against the aind-data-schema. You'll see:
- Success message if validation passes
- Summary of channels and active devices
- Count of remaining placeholder values

## What's Filled In

**From instrument config files (MMConfig_Ti2E-xc2.1.txt and dogwood.json):**
- Tile dimensions: 3200 × 3200 pixels, 10 z-planes
- Pixel size: 0.33 μm
- Z-step: 1.5 μm
- Laser wavelengths for gene/barcode bases (514, 561, 640 nm) and DAPI (365 nm)
- Emission filter names for all gene/barcode channels
- Exposure time estimates from presets

## Placeholders Remaining

**Total: 57 placeholders across all 3 files**
- Gene sequencing: 18
- Barcode sequencing: 15
- Hybridization: 24

### Priority Items:

1. **File paths** (CRITICAL): Need paths to max projection files to extract acquisition timestamps
2. **Hybridization probe mapping** (CRITICAL): Which probe (XC2758/XC2759/XC2760/YS221) uses which fluorophore (GFP/YFP/TxRed/Cy5)?
3. **Laser powers**: Actual mW values used during acquisition (not available in instrument config)
4. **Peak emission wavelengths**: For each channel (filter ranges are known, but not peaks)
5. **Personnel**: Experimenter names and specimen IDs

See `PLACEHOLDERS_TO_FILL.md` for complete details.

## File Structure

Each acquisition JSON represents a single raw data asset:

**Gene Sequencing:**
- 1 DataStream with 5 channels (GeneSeq_G/T/A/C, DAPI)
- 5 ImageSPIM placeholders (one per channel)
- Tile dimensions: 3200×3200×10 pixels

**Barcode Sequencing:**
- 1 DataStream with 4 channels (BarcodeSeq_G/T/A/C)
- 4 ImageSPIM placeholders
- Same tile dimensions

**Hybridization:**
- 1 DataStream with 5 channels (Hyb_XC2758/XC2759/XC2760/YS221, DAPI)
- 5 ImageSPIM placeholders
- Same tile dimensions

## Next Steps

1. **Obtain file paths** to max projection files for each acquisition phase to extract actual timestamps
2. **Determine probe-to-fluorophore mapping** for hybridization channels (XC2758/XC2759/XC2760/YS221)
3. **Gather remaining parameters** using `PLACEHOLDERS_TO_FILL.md` as a guide
4. **Update generator scripts** with actual values and regenerate JSON files

## Dependencies

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv sync

# Run generators
uv run python generate_780346_geneseq_acquisition.py
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
