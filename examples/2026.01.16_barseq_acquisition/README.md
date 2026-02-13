# BARseq Acquisition Metadata

Scripts to generate acquisition metadata JSON files for BARseq (Barcoded Anatomy Resolved by Sequencing) experiments on subjects 780345 and 780346.

## Quick Start

```bash
# Generate all three acquisition files for a subject (defaults to 780346)
uv run python generate_barseq_acquisitions.py

# For subject 780345
uv run python generate_barseq_acquisitions.py --subject-id 780345
```

This generates 3 acquisition JSON files per subject:
- `barseq_{subject_id}_geneseq_acquisition.json` - Gene sequencing (7 cycles)
- `barseq_{subject_id}_barcodeseq_acquisition.json` - Barcode sequencing (15 cycles)
- `barseq_{subject_id}_hyb_acquisition.json` - Hybridization (1 cycle)

## Files

**Generator:**
- `generate_barseq_acquisitions.py` - Unified entry point that generates all three acquisition files

**Builders:**
- `barseq_geneseq_builder.py` - Creates gene sequencing acquisition metadata
- `barseq_barcodeseq_builder.py` - Creates barcode sequencing acquisition metadata
- `barseq_hyb_builder.py` - Creates hybridization acquisition metadata

**Shared modules:**
- `constants.py` - Hardware configuration (tiling, channels, lasers, filters)
- `utils.py` - Shared utility functions (tiling descriptions, ImageSPIM objects)
- `experiment_params.py` - Subject-specific parameters (timestamps, section counts, CCF plates)

**Documentation:**
- `SUMMARY.md` - Detailed decisions, sources, and remaining placeholders (READ THIS for full context)

## What's Still Needed

**25 placeholders per subject** (50 total for both subjects):
- **File paths** (14 per subject): Max projection file paths for all channels to extract timestamps
- **Probe mapping** (8): Which hybridization probe uses which fluorophore (GFP/YFP/TxRed/Cy5)
- **Specimen IDs** (3 per subject): Actual specimen identifiers

See `SUMMARY.md` for complete details.

## Technical Overview

- **Instrument:** Nikon Ti2-E "Dogwood" with spinning disk confocal
- **Imaging:** 14x8 tile grid (112 tiles/channel) with 23% overlap, max projected (10 z-planes)
- **Tissue:** 51 sections (20μm coronal) through Locus Coeruleus, covering CCF plates 99-112
- **Data:** Only stitched max projections are saved (~35,968 x 21,184 pixels per channel)

## References

- **Protocol:** https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1
- **Schema:** https://aind-data-schema.readthedocs.io/
