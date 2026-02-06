# Placeholders to Fill In - BARseq Acquisition Metadata

This document lists all the missing information needed to complete the BARseq acquisition metadata files. The questions are organized by category for easy assignment to the appropriate team members.

## Quick Summary

**NOTE:** BARseq experiments now generate **3 separate acquisition files** (one per raw data asset):
1. Gene sequencing (7 cycles) - 8 placeholders
2. Barcode sequencing (15 cycles) - 7 placeholders
3. Hybridization (1 cycle) - 16 placeholders

**Total remaining placeholders:** 31 across all 3 files (reduced from 57)

**What we have filled in:**
- Tile dimensions: 3200 × 3200 pixels
- Laser wavelengths for gene/barcode bases (G/T/A/C) and DAPI
- Emission filter names for gene/barcode channels and DAPI
- Exposure time estimates from instrument presets

**What we removed (optional/questionable data):**
- Laser power values (not available from config files)
- Peak emission wavelengths (only filter ranges available)
- Placeholder laser/filter device names from active_devices lists

**Priority remaining items:**
1. **Tile layout and image files (MAJOR GAP):** Current JSONs have ~14 placeholder ImageSPIM objects (one per channel), but reality needs hundreds to thousands (one per tile per channel) with proper positions and file paths
2. File paths to max projection files (to extract acquisition times and fill file_name fields)
3. Probe-to-fluorophore mapping for hybridization channels (affects 8 placeholders)
4. Personnel information (experimenters, specimen IDs)

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

### Question 3.1: Hybridization probes - which fluorophores? CRITICAL

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

**Current status:** Using `PLACEHOLDER_LASER_HYB` (wavelength 9999) and `PLACEHOLDER_FILTER_HYB` until mapping is known.

**This affects:** 8 placeholders in hybridization JSON (4 lasers + 4 filters)

---

## 4. Tile Layout and Image Files - CRITICAL

### IMPORTANT: Current ImageSPIM structure is oversimplified

**Current state:** Each JSON file has one ImageSPIM object per channel as a placeholder:
- Gene sequencing: 5 ImageSPIM objects (G, T, A, C, DAPI channels)
- Barcode sequencing: 4 ImageSPIM objects (G, T, A, C channels)
- Hybridization: 5 ImageSPIM objects (4 probes + DAPI)

**Reality:** BARseq uses tiled imaging with 24% overlap. Each acquisition likely has:
- 51 sections × multiple tiles per section × channels = hundreds to thousands of tiles total
- Each tile needs its own ImageSPIM object with:
  - Unique file path (`file_name`)
  - Unique spatial position (`Translation` in `image_to_acquisition_transform`)
  - Tile dimensions (3200 × 3200 × 10 pixels per tile)

**What's needed from BARseq team:**
1. **Tile layout information:**
   - How many tiles per section?
   - Tile grid dimensions (e.g., 5×5 grid per section?)
   - Tile positions in microns (X, Y offsets)
   - Section Z-positions

2. **File paths and naming:**
   - Where are the max projection files (or raw tile images) stored?
   - File naming convention (how to identify: section, tile position, channel, cycle)
   - File format (e.g., .tif, .ims, .nd2)

3. **Timing information:**
   - File timestamps to extract acquisition start/end times

**Current placeholders:**
- All tile positions: `Translation([0, 0, 0])` - needs real X,Y,Z positions
- All file paths: `"PLACEHOLDER_raw_data_path"`
- All `image_start_time` and `image_end_time`: `null`

**Impact:** This is a major gap. The current JSON files have ~14 placeholder ImageSPIM objects, but the real acquisitions need hundreds to thousands of properly positioned ImageSPIM objects with correct file paths.

---

## 5. Acquisition Timing - CRITICAL

### Question 5.1: File paths needed to extract acquisition times

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

