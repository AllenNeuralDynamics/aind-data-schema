# Placeholders to Fill In - BARseq Acquisition Metadata

This document lists all the missing information needed to complete the BARseq acquisition metadata files. The questions are organized by category for easy assignment to the appropriate team members.

## Quick Summary

**NOTE:** BARseq experiments now generate **3 separate acquisition files** (one per raw data asset):
1. Gene sequencing (7 cycles) - 18 placeholders
2. Barcode sequencing (15 cycles) - 15 placeholders
3. Hybridization (1 cycle) - 24 placeholders

**Total remaining placeholders:** 57 across all 3 files

**What we now have from instrument config files:**
- Tile dimensions: 3200 × 3200 pixels
- Laser wavelengths for gene/barcode bases (G/T/A/C) and DAPI
- Emission filter names for gene/barcode channels and DAPI
- Exposure time estimates from instrument presets

**Priority remaining items:**
1. File paths to max projection files (to extract acquisition times)
2. Probe-to-fluorophore mapping for hybridization channels
3. Actual laser powers used during acquisition
4. Personnel information

---

## 1. Personnel Information

### Question 1.1: Who performed the acquisitions?
**For both experiments:**
- What are the full names of the experimenters who performed the BARseq imaging?
- Format: First and Last name (e.g., "Jane Smith", "John Doe")

**Current placeholder:**
```json
"experimenters": [
  "PLACEHOLDER_EXPERIMENTER_1",
  "PLACEHOLDER_EXPERIMENTER_2"
]
```

---

## 2. Specimen Identification

### Question 2.1: What are the specimen IDs?
For each brain section that was imaged:
- **Subject 780345:** What identifier should be used for the brain section specimen?
- **Subject 780346:** What identifier should be used for the brain section specimen?

**Suggested format:** `{subject_id}_LC_section_{number}` 
- Example: "780345_LC_section_01"
- Or use existing lab naming convention

**Current placeholders:**
- Subject 780345: `"PLACEHOLDER_SPECIMEN_ID_780345"`
- Subject 780346: `"PLACEHOLDER_SPECIMEN_ID_780346"`

---

## 3. Hardware Configuration (CRITICAL)

This section requires input from someone familiar with the Dogwood microscope setup and the BARseq imaging protocol.

### Question 3.1: Laser wavelengths for bases - FILLED

**Gene & Barcode Sequencing lasers (from MMConfig):**
- Base G (Guanine): **514 nm**
- Base T (Thymine): **561 nm**
- Base A (Adenine): **640 nm**
- Base C (Cytosine): **640 nm**
- DAPI: **365 nm**

### Question 3.2: Emission filters for bases - FILLED

**Gene & Barcode Sequencing filters (from MMConfig):**
- Base G: **565/24**
- Base T: **441/511/593/684/817**
- Base A: **676/29**
- Base C: **775/140**
- DAPI: **DAPI/GFP/TxRed-69401**

**Still need:** Peak emission wavelengths for each channel (currently `9999` nm placeholders)

### Question 3.3: What are the laser power settings?

For each laser used during acquisition:
- Base G laser: _______ mW
- Base T laser: _______ mW
- Base A laser: _______ mW
- Base C laser: _______ mW
- DAPI laser: _______ mW

**Current placeholder:** `9999.0` mW for all lasers

### Question 3.4: Hybridization probes - which fluorophores? CRITICAL

**Available fluorophore channels in MMConfig:**
- GFP: 488nm laser, "DAPI/GFP/TxRed-69401" filter
- YFP: 514nm laser, "565/24" filter
- TxRed: 561nm laser, "DAPI/GFP/TxRed-69401" filter
- Cy5: 640nm laser, "532/640" filter

**Need to determine mapping:**
- Probe XC2758: _______ (GFP, YFP, TxRed, or Cy5?)
- Probe XC2759: _______ 
- Probe XC2760: _______ 
- Probe YS221: _______

**Current status:** Using `PLACEHOLDER_LASER_HYB` and `PLACEHOLDER_FILTER_HYB` until mapping is known.

---

## 4. Camera Settings

### Question 4.1: Exposure times - ESTIMATED FROM CONFIG

**Using values from MMConfig presets (may need adjustment):**
- Gene/Barcode G: 60 ms
- Gene/Barcode T: 30 ms
- Gene/Barcode A: 20 ms
- Gene/Barcode C: 40 ms
- DAPI: 30 ms

**Note:** Detector exposure_time is set to the average (gene: 40ms, barcode: 37.5ms, hyb: 42ms). Individual channel exposure times vary as shown above.

---

## 5. Image and Tiling Information

### Question 5.1: Tile dimensions - FILLED

**From dogwood.json and methods doc:**
- Tile width: **3200 pixels**
- Tile height: **3200 pixels**
- Z-planes per tile: **10**
- Pixel size: **0.33 μm**
- Z-step: **1.5 μm**
- Tile overlap: **23%**

### Question 5.2: Tiling layout - STILL NEEDED

- Total number of tiles per section: _______
- Tiling pattern: _______ (e.g., 10×10 grid, serpentine pattern, etc.)
- Are tile positions recorded in a metadata file? If yes, what format?

### Question 5.3: File paths for raw image data - CRITICAL

**Need file paths or directory structure to:**
1. Extract actual acquisition start/end times from file metadata or timestamps
2. Fill in `file_name` fields in ImageSPIM objects

**Questions for BARseq team:**
- Where are the max projection files stored for each acquisition phase (gene/barcode/hyb)?
- What is the file naming convention?
- Are tiles saved as individual files or combined stacks?
- File format: _______ (e.g., .tif, .ims, .nd2, etc.)

**Current placeholder:** `"PLACEHOLDER_raw_data_path"` in all ImageSPIM objects

**Note:** Once tile layout information is available, the single placeholder ImageSPIM per channel should be replaced with one ImageSPIM object per actual tile, with accurate positions in the Translation transform.

---

## 6. Acquisition Timing - CRITICAL

### Question 6.1: File paths needed to extract acquisition times

**To extract actual acquisition start/end times, we need:**
- File paths or directory locations for max projection files (or raw image folders) for each phase
- These files should have timestamps in filename, file metadata, or TIFF headers

**For Subject 780346 (June 11, 2025):**
1. Gene sequencing max projection files: _______
2. Barcode sequencing max projection files: _______
3. Hybridization max projection files: _______

**Current placeholders in JSON files:**
- Gene sequencing: 2025-06-11 12:00:00 - 14:00:00 UTC (2 hour estimate)
- Barcode sequencing: 2025-06-11 14:00:00 - 18:00:00 UTC (4 hour estimate)
- Hybridization: 2025-06-11 18:00:00 - 19:00:00 UTC (1 hour estimate)

**Note:** Once file paths are provided, timestamps can be automatically extracted from file system metadata or TIFF headers.

