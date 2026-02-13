# BARseq Acquisition Metadata Summary

This document summarizes the decisions made in creating the acquisition metadata files, their sources, and remaining information needed.

**Note:** This metadata structure applies to both subjects 780345 and 780346. Both follow the same BARseq protocol with 20μm coronal sections through the Locus Coeruleus (LC), acquired using the same imaging parameters and tile grid configuration.

## Information Still Needed

**Total placeholders: 25 per subject (50 total for 780345 and 780346)**
- Gene sequencing: 6 (5 max projection file paths + 1 specimen ID)
- Barcode sequencing: 5 (4 max projection file paths + 1 specimen ID)
- Hybridization: 14 (5 max projection file paths + 8 hyb probe mapping + 1 specimen ID)

### Priority Items:

1. **Max projection file paths** (14 total)
   - Gene: GeneSeq_G, GeneSeq_T, GeneSeq_A, GeneSeq_C, DAPI
   - Barcode: BarcodeSeq_G, BarcodeSeq_T, BarcodeSeq_A, BarcodeSeq_C
   - Hyb: Hyb_XC2758, Hyb_XC2759, Hyb_XC2760, Hyb_YS221, DAPI
   - **Why needed:** To extract acquisition timestamps and fill file_name fields

2. **Hybridization probe-to-fluorophore mapping** (8 placeholders: 4 lasers + 4 filters)
   - Which probe (XC2758/XC2759/XC2760/YS221) uses which fluorophore (GFP/YFP/TxRed/Cy5)?
   - **Why needed:** To specify correct laser wavelengths and emission filters for each hyb channel

3. **Specimen IDs** (3 placeholders: 1 per file)
   - Current placeholder: "780346_PLACEHOLDER_SPECIMEN_ID"
   - **Why needed:** Required field for in vitro imaging modalities

---

## Questions for BARseq Team

### Q1: Max Projection File Paths
Where are the stitched max projection files stored for Subjects 780345 and 780346? Please provide file paths or directory structure for:
- Gene sequencing (5 channels: GeneSeq_G/T/A/C, DAPI)
- Barcode sequencing (4 channels: BarcodeSeq_G/T/A/C)
- Hybridization (5 channels: Hyb_XC2758/XC2759/XC2760/YS221, DAPI)

File format: _______ (e.g., .tif, .ims, .nd2)

These paths will be used to extract acquisition timestamps and complete the file_name fields for both subjects.

### Q2: Hybridization Probe Mapping
Which probe uses which fluorophore?
- Probe XC2758: _______ (GFP / YFP / TxRed / Cy5?)
- Probe XC2759: _______ (GFP / YFP / TxRed / Cy5?)
- Probe XC2760: _______ (GFP / YFP / TxRed / Cy5?)
- Probe YS221: _______ (GFP / YFP / TxRed / Cy5?)

Once known, this will complete the laser device names and emission filter configurations for hybridization channels.

### Q3: Specimen IDs
What are the specimen identifiers for Subjects 780345 and 780346's brain sections?
- Current placeholders: "780345_PLACEHOLDER_SPECIMEN_ID" and "780346_PLACEHOLDER_SPECIMEN_ID"
- Suggested format: "780345_LC_section" or similar (should these be unique per section or per subject?)

### Q4: DIC Channel
Should the DIC (Differential Interference Contrast) channel be included in the hybridization acquisition metadata?
- Mentioned in emails but not currently modeled
- If yes, need: laser wavelength, filter configuration, exposure time

### Q5: Validation Questions
Please confirm or correct:
1. Is the 14×8 tile grid estimate correct?
2. Is the SPIM_RPI coordinate system appropriate (Right-Posterior-Inferior)?
3. Are the acquisition notes accurate regarding the experimental setup?

---

## Decisions and Assumptions Made

### 1. Three Separate Acquisition Files

**Decision:** Create 3 separate acquisition.json files (gene sequencing, barcode sequencing, hybridization)

**Source:** Email from Saskia (2026-01-20)
> "No, I don't agree. Each cycle has a folder of images. That is one asset with one acquisition. These different assets then get processed together to create a single derived asset."

**Rationale:** Each phase produces a distinct raw data asset, even though they are later processed together.

**Application:** This structure applies to both subjects 780345 and 780346. Each subject will have 3 acquisition.json files (gene sequencing, barcode sequencing, hybridization).

---

### 2. Experimenters

**Decision:** Set experimenters to "Imaging core"

**Source:** Email from Aixin (2026-02-09)
> "I think now image core will help us collect data."

**Note:** Dan flagged that this means nobody will be attributed for credit. Once specific names are available, this should be updated for both subjects.

---

### 3. Tile Grid Structure

**Decision:** 14×8 tile grid (112 tiles per channel) with 23% overlap, starting at (-736, -736) pixels

**Sources:**
- Dan's estimate (Slack, 2026-02-10): "I would guess that it's roughly 14 x 8 based on the size of typical brains and the amount of overlap they are using"
- dogwood.json: Contains "stitch_overlap: 0.23"

**Implementation:**
- Tile step: 2464 pixels = 3200 × (1 - 0.23)
- First tile offset: -736 pixels
- Positions calculated for all 112 tiles in micron space

---

### 4. Transient Tiles vs. Saved Max Projections

**Decision:** Document both tiles (file_name="not saved") and max projections (file_name="PLACEHOLDER_max_projection_path")

**Sources:**
- Email clarification (2026-02-15): Tiles are transient and deleted after max projection
- Aixin's email (2026-02-09):
  > "We don't save the raw images only save the max projection images. The software will automatically delete the raw image stacks if the number of max projection matched with the required tile number."

**Rationale:** Schema should document the acquisition process (what was acquired), not just what was saved to disk. Dan's request for tiling information supports documenting the tile grid even though tiles are deleted.

**Implementation:**
- 112 ImageSPIM objects per channel with tile positions and file_name="not saved"
- 1 ImageSPIM object per channel for stitched max projection with file_name="PLACEHOLDER_max_projection_path"

---

### 5. Image Dimensions and Section Thickness

**Decision:**
- Individual tiles: 3200 × 3200 × 10 pixels
- Stitched max projection: 35,968 × 21,184 × 10 pixels (calculated)
- Section thickness: 20 μm (coronal sections)
- Sections per slide: 4 sections for BARseq

**Sources:**
- Aixin's email (2026-02-09):
  > "Dimensions of each tile before max projection is 3200x3200x100 in geneseq01 and bcseq01, 3200x3200x120 in any hyb cycle, 3200x3200x80 in any geneseq02+ and bcseq02+."

- Methods document (MAPseq-BARseq methods_forSciComp.txt):
  > "10-plane maximum intensity projection"

- Lab notes (780345 and 780346):
  > "BARseq → 4 × 20μm Sections/Slide"
  > "BARseq → 20μm throughout LC"

**Interpretation:** Raw z-stacks have 100/120/80 planes, but only the top 10 planes are kept in max projections. Brain sections are cut at 20 μm thickness and mounted 4 per slide.

**Stitched dimensions calculation:**
- Width = 736 + (14-1) × 2464 + 3200 = 35,968 pixels
- Height = 736 + (8-1) × 2464 + 3200 = 21,184 pixels

---

### 6. Pixel Size and Z-Step

**Decision:**
- XY pixel size: 0.33 μm
- Z-step: 1.5 μm

**Sources:**
- Aixin's email (2026-02-09): "Pixel size is 0.33"
- Methods document (MAPseq-BARseq methods_forSciComp.txt): "1.5 μm z-spacing"

**Note:** Dan's comment (2026-02-10) "Isotropic 0.33 um voxels (this is definitely wrong)" indicates the voxels are not isotropic. Z-step of 1.5 μm from methods doc differs from XY pixel size of 0.33 μm.

---

### 7. Channel Configuration

**Decision:** Channel names and intended measurements:

**Gene/Barcode Sequencing:**
- GeneSeq_G / BarcodeSeq_G → "Guanine"
- GeneSeq_T / BarcodeSeq_T → "Thymine"
- GeneSeq_A / BarcodeSeq_A → "Adenine"
- GeneSeq_C / BarcodeSeq_C → "Cytosine"
- DAPI → "Nuclear counterstain"

**Hybridization:**
- Hyb_XC2758 → "Probe XC2758"
- Hyb_XC2759 → "Probe XC2759"
- Hyb_XC2760 → "Probe XC2760"
- Hyb_YS221 → "Probe YS221"
- DAPI → "Nuclear counterstain"

**Source:** Reviewer feedback (Saskia, 2026-01-15)
> "This is not an appropriate intended measurement. DNA Base G is not a gene."
> "I'd remove 'GeneSeq' since DAPI is not part of the sequencing."
> "I think 'Guanine' is sufficient, personally."

**Rationale:** Channel names describe the acquisition phase + target, intended_measurement describes what's being measured in simple terms.

---

### 8. Channel Acquisition Order

**Decision:**
- Gene sequencing cycle 1: G, T, A, C, Hyb-DAPI (5 channels)
- Barcode sequencing cycles 2+: G, T, A, C (4 channels, no DAPI)
- Hybridization: Hyb-GFP, Hyb-YFP, Hyb-TxRed, Hyb-Cy5, Hyb-DAPI (5 channels, DIC not included)

**Sources:**
- Aixin's email (2026-02-09):
  > "Acquisition channel order:
  > Geneseq01 and bcseq01: G T A C Hyb-DAPI
  > Geneseq02+ and bc seq02+: G T A C
  > Hyb: Hyb-GFP Hyb-YFP Hyb-TxRed Hyb-Cy5 Hyb-DAPI DIC"

- Xiaoyin's email (2025-12-12):
  > "For the images, in cycles geneseq01 and bcseq01, the channels are G/T/A/C/DAPI. In other geneseq or bcseq cycles, the channels are GTAC. In hyb cycles, the channels are GFP/G/TxRed/Cy5/DAPI/DIC."

**Implementation:** Modeling gene cycle 1 and barcode cycle 1 separately (as distinct acquisitions per Saskia's guidance). DIC channel mentioned in emails but not currently included in metadata.

**Note:** DIC (Differential Interference Contrast) channel is mentioned in hyb acquisition but not currently modeled. Should confirm if DIC should be included.

---

### 9. Laser Wavelengths

**Decision:**
- Base G: 514 nm
- Base T: 561 nm
- Base A: 640 nm
- Base C: 640 nm
- DAPI: 365 nm
- Hyb probes: PLACEHOLDER (wavelength 9999 until probe mapping known)

**Source:** MMConfig_Ti2E-xc2.1.txt
- Extracted from Property Browser sections for each laser configuration
- Confirmed against Lumencor Celesta available wavelengths

---

### 10. Emission Filters

**Decision:**
- Base G: "565/24"
- Base T: "441/511/593/684/817"
- Base A: "676/29"
- Base C: "775/140"
- DAPI: "DAPI/GFP/TxRed-69401"
- Hyb probes: "PLACEHOLDER_FILTER_HYB" (until probe mapping known)

**Source:** MMConfig_Ti2E-xc2.1.txt
- Extracted from ConfigGroup sections matching channel presets

---

### 11. Exposure Times

**Decision:**
- Gene/Barcode G: 60 ms
- Gene/Barcode T: 30 ms
- Gene/Barcode A: 20 ms
- Gene/Barcode C: 40 ms
- Hyb-DAPI: 20 ms
- Detector average: Gene=40ms, Barcode=37.5ms, Hyb=30ms

**Sources:**
- Aixin's email (2026-02-09):
  > "exposure time is: G 60, T 30, A 20, C 40, DIC 20, Hyb-GFP 100, Hyb-YFP 30, Hyb-TxRed 30, Hyb-Cy5 20, Hyb-DAPI 20."

- MMConfig_Ti2E-xc2.1.txt: Confirmed exposure times in channel preset configurations

**Note:** Hyb fluorophore exposure times (GFP=100, YFP=30, TxRed=30, Cy5=20) are known but cannot be applied until probe-to-fluorophore mapping is determined.

---

### 12. Active Devices

**Decision:** Minimal list of core devices only:
- Ti2-E__0 (microscope)
- 20x Objective
- Camera-1
- XLIGHT Spinning Disk

**Rationale:** Removed placeholder laser and filter device names to keep metadata lightweight. Actual device names can be inferred from laser wavelengths and filter names in Channel configurations.

---

### 13. Coordinate System

**Decision:** CoordinateSystemLibrary.SPIM_RPI for ImagingConfig

**Source:** exaspim_acquisition.py example in aind-data-schema repository

**Note:** This assumes Right-Posterior-Inferior orientation. Should be confirmed with BARseq team.

---

### 14. Optional Fields Removed

**Decision:** Do not include the following optional fields:
- Laser power and power_unit (no data available)
- Emission wavelength and emission_wavelength_unit (only filter ranges known, not peaks)
- variable_power (always false)
- excitation_filters (always null)
- additional_device_names (always null)
- compression (always null)

**Rationale:** Goal is to keep metadata lightweight and only include fields with reliable data.

---

### 15. Protocol Reference

**Decision:** protocol_id = ["https://www.protocols.io/view/barseq-2-5-kqdg3ke9qv25/v1"]

**Source:** Methods document (MAPseq-BARseq methods_forSciComp.txt) header

---

### 16. Ethics Review

**Decision:** ethics_review_id = null (not included)

**Source:** Reviewer comment
> "there is no iacuc for in vitro experiments"

**Rationale:** BARseq is performed on post-mortem brain tissue sections, which are in vitro preparations not requiring IACUC approval.

---

### 17. Acquisition Type

**Decision:** acquisition_type = "BarcodeSequencing" for all three phases

**Source:** Schema field description suggests this should be consistent across similar acquisitions for the same experiment.

**Rationale:** All three phases are part of the same BARseq barcoding workflow.

---

### 18. Instrument Identification

**Decision:**
- instrument_id: "Dogwood"
- ImagingConfig.device_name: "Dogwood"
- DataStream.active_devices: "Ti2-E__0" (component-level)

**Source:** Reviewer comment (Dan, 2026-01-14)
> "The 'device_name' should actually be the instrument_id, per a comment from Dan. In this case, that's 'Dogwood'."

**Clarification:** instrument_id and ImagingConfig.device_name use system-level identifier, while active_devices uses component-level identifiers from instrument.json.

---

## Data Sources Reference

### Primary Documents:
1. **Methods document**: MAPseq-BARseq methods_forSciComp.txt
   - Z-step: 1.5 μm
   - Protocol reference
   - 10-plane max projection

2. **Instrument config**: MMConfig_Ti2E-xc2.1.txt
   - Laser wavelengths (514, 561, 640, 365 nm)
   - Emission filter names
   - Exposure times (G=60, T=30, A=20, C=40, DAPI=30/20 ms)

3. **Instrument metadata**: dogwood.json
   - Tile dimensions: 3200×3200
   - Stitch overlap: 23%

4. **Email correspondence**: 
   - Aixin (2026-02-09): XY pixel size, channel order, exposure times
   - Xiaoyin (2025-12-12): Channel lists, filter information
   - Saskia (2026-01-20): Separate acquisition files per phase
   - Dan (2026-02-10): Tile grid estimate, device naming

5. **Lab notes** (780345 and 780346):
   - Section thickness: 20 μm coronal sections
   - Sections per slide: 4 sections for BARseq
   - Anatomical coverage: Throughout Locus Coeruleus (LC)

5. **Schema examples**: exaspim_acquisition.py
   - ImageSPIM structure
   - Coordinate system usage

### Team Members Consulted:
- **Saskia de Vries**: Asset separation, channel naming, intended measurements
- **Daniel Birman**: Device naming, tiling requirements, metadata structure
- **Polina Kosillo**: Initial requirements gathering, workflow clarification
- **Xiaoyin Chen**: Filter configurations, channel lists
- **Aixin Zhang**: Instrument parameters, exposure times, pixel size
- **Yoh Isogai**: CC'd on email thread
- **Carolyn Eng**: CC'd on email thread
