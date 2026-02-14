# BARseq Acquisition Metadata Summary

Please answer the following questions to complete the acquisition metadata for subjects 780345 and 780346.

## Questions for BARseq Team

### Q1: Max Projection File Paths
Where are the stitched max projection files stored for Subjects 780345 and 780346? Please provide file paths or directory structure for:
- Gene sequencing (5 channels: GeneSeq_G/T/A/C, DAPI)
- Barcode sequencing (4 channels: BarcodeSeq_G/T/A/C)
- Hybridization (5 channels: Hyb_XC2758/XC2759/XC2760/YS221, DAPI)

File format: _______ (e.g., .tif, .ims, .nd2)

These paths will be used to extract acquisition timestamps and complete the file_name fields for both subjects.

### Q2: Hybridization Probe Mapping
**Current assumptions** (need verification):
- Probe XC2758: **GFP** (488nm, 100ms exposure)
- Probe XC2759: **YFP** (514nm, 30ms exposure)
- Probe XC2760: **TxRed** (561nm, 30ms exposure)
- Probe YS221: **Cy5** (640nm, 20ms exposure)

These assumptions were made to structure the code properly and avoid duplication. The wavelengths and exposures are known from MMConfig, but the specific probe-to-fluorophore assignments need confirmation. Emission filter configurations remain as "PLACEHOLDER_FILTER_HYB" until verified.

### Q3: Specimen IDs
What are the specimen identifiers for Subjects 780345 and 780346's brain sections?
- Current placeholders: "780345_PLACEHOLDER_SPECIMEN_ID" and "780346_PLACEHOLDER_SPECIMEN_ID"
- Suggested format: "780345_thin_slices_59-62" or similar (should these be unique per section or per subject?)

### Q4: DIC Channel
Should the DIC (Differential Interference Contrast) channel be included in the hybridization acquisition metadata?
- Mentioned in emails but not currently modeled
- **Impact if included:** Adds a 6th channel to hybridization (currently 5), requires additional laser wavelength, filter configuration, and exposure time
- **Impact on placeholders:** Would add 1 more file path placeholder per subject

### Q5: Coordinate System Verification
**Is SPIM_RPI the correct coordinate system for coronal section tiling?**

SPIM_RPI defines:
- X: Left_to_right
- Y: Anterior_to_posterior
- Z: Superior_to_inferior

For coronal sections:
- X (left-right on slide): matches
- Y (up-down on slide): should be Superior-Inferior, but SPIM_RPI has this as Z
- Z (z-stack depth): should be Anterior-Posterior, but SPIM_RPI has this as Y

**Question:** Does this coordinate system correctly represent your imaging setup, or should we use a different system?

### Q6: Other Validation Questions
Please confirm or correct:

1. Is the 14×8 tile grid estimate correct?
2. Is the first tile offset position (-736, -736) pixels correct? Currently assuming this is 23% overlap applied to first tile positioning (3200 × 0.23 = 736), based on Dan's description.
3. Number of sections and CCF plates: Currently using 51 sections covering CCF plates 99-112 (placeholder values that need confirmation)
4. Acquisition timestamps: All timestamps in the JSON files are placeholders (see experiment_params.py). These need to be extracted from the actual max projection file metadata.
5. Are the acquisition notes accurate regarding the experimental setup?

---

# ════════════════════════════════════════════════════════════════════════════════
# IMPLEMENTATION DETAILS — Documentation of implementation decisions, sources and rationale
# ════════════════════════════════════════════════════════════════════════════════

## Decisions and Assumptions Made

### 1. Three Separate Acquisition Files

**Decision:** Create 3 separate acquisition.json files (gene sequencing, barcode sequencing, hybridization)

**Source:** Email from Saskia
> "No, I don't agree. Each cycle has a folder of images. That is one asset with one acquisition. These different assets then get processed together to create a single derived asset."

**Rationale:** Each phase produces a distinct raw data asset, even though they are later processed together. Each subject has 3 acquisition.json files (gene sequencing, barcode sequencing, hybridization).

---

### 2. Experimenters

**Decision:** Set experimenters to "Imaging core"

**Source:** Email from Aixin
> "I think now image core will help us collect data."

**Note:** This generic attribution means no individuals receive credit for the work. Specific experimenter names should be provided if available.

---

### 3. Tile Grid Structure

**Decision:** 14x8 tile grid (112 tiles per channel) with 23% overlap

**Sources:**
- Dan's estimate (Teams DM): "I would guess that it's roughly 14 x 8 based on the size of typical brains and the amount of overlap they are using"
- dogwood.json: Contains "stitch_overlap: 0.23", tile dimensions (3200×3200 pixels)

**Implementation:**
- Tile step: 2464 pixels = 3200 × (1 - 0.23)
- First tile offset: **ASSUMPTION: (-736, -736) pixels** - Derived by applying 23% overlap to first tile (3200 × 0.23 = 736). Based on Dan's DM describing the tiling setup.
- Positions calculated for all 112 tiles in micron space

**Note:** The first tile offset affects the coordinate system origin but not the stitched image dimensions (which depend only on tile count, step, and size).

---

### 4. Tile Representation

**Decision:** Document only saved max projections as ImageSPIM objects; document tiling parameters in DataStream.notes

**Sources:**
- Aixin's email: "We don't save the raw images only save the max projection images. The software will automatically delete the raw image stacks if the number of max projection matched with the required tile number."
- Schema exploration: No dedicated tile/grid fields exist in the schema

**Rationale:**
The microscope acquires data as a 14x8 tile grid (112 tiles per channel), but these individual tiles are transient intermediate files that get deleted after stitching and max projection. Two approaches were considered:

1. **Create 112 ImageSPIM objects per channel** - One for each tile, even though the files don't exist
   - Pro: Explicitly documents the tiling structure in structured metadata
   - Con: Results in much larger JSON files (~20,600 lines vs ~457 lines) documenting files that were deleted
   - Con: Schema has no dedicated tile/grid fields; using ImageSPIM objects this way is an interpretation, not a requirement

2. **Create 1 ImageSPIM object per channel** - One for the saved max projection (chosen approach)
   - Pro: Metadata documents actual data assets (files that exist)
   - Pro: More concise JSON files (~457 lines for gene/hyb, ~386 lines for barcode)
   - Pro: All tiling information can be documented in DataStream.notes field
   - Con: Tiling structure is in notes rather than structured fields

I chose approach #2 because the schema should document data assets that exist, not transient intermediate files. All tiling information needed to recreate the experiment is preserved in DataStream.notes.

**Implementation:**
- 1 ImageSPIM object per channel for stitched max projection with file_name="PLACEHOLDER_max_projection_path"
- Comprehensive tiling description in DataStream.notes including:
  - Grid size: 14x8 (112 tiles per channel)
  - Overlap: 23%
  - Tile dimensions: 3200x3200 pixels, 10 z-planes
  - Tile step: 2464 pixels
  - First tile offset: (-736, -736) pixels
  - Pixel size: 0.33 μm (XY), z-step: 1.5 μm
  - Stitched dimensions: 35,232x20,448 pixels, 10 z-planes

**Results:**
- Gene sequencing: 5 ImageSPIM objects, ~457 lines
- Barcode sequencing: 4 ImageSPIM objects, ~386 lines
- Hybridization: 5 ImageSPIM objects, ~457 lines

---

### 5. Image Dimensions and Section Thickness

**Decision:**
- Individual tiles: 3200 x 3200 pixels, 10 z-planes
- Stitched max projection: 35,232 x 20,448 pixels, 10 z-planes (calculated)
- Section thickness: 20 μm (coronal sections)
- Sections per slide: 4 sections for BARseq

**Sources:**
- Aixin's email:
  > "Dimensions of each tile before max projection is 3200x3200x100 in geneseq01 and bcseq01, 3200x3200x120 in any hyb cycle, 3200x3200x80 in any geneseq02+ and bcseq02+."

- Methods document (MAPseq-BARseq methods_forSciComp.txt):
  > "10-plane maximum intensity projection"

- Lab notes (780345 and 780346):
  > "BARseq → 4 x 20μm Sections/Slide"
  > "BARseq → 20μm throughout LC"

**Interpretation:** Raw z-stacks have 100/120/80 planes, but only the top 10 planes are kept in max projections. Brain sections are cut at 20 μm thickness and mounted 4 per slide.

**Stitched dimensions calculation:**
- Width = (14-1) × 2464 + 3200 = 35,232 pixels
- Height = (8-1) × 2464 + 3200 = 20,448 pixels

**Calculation explanation:** The total span is determined by the tile grid geometry: (NUM_TILES - 1) × TILE_STEP + TILE_SIZE. The first tile offset (assumed to be -736, -736) indicates where the grid starts in the coordinate system but doesn't affect the total span of the stitched image.

---

### 6. Pixel Size and Z-Step

**Decision:**
- XY pixel size: 0.33 μm
- Z-step: 1.5 μm

**Sources:**
- Aixin's email: "Pixel size is 0.33"
- Methods document (MAPseq-BARseq methods_forSciComp.txt): "1.5 μm z-spacing"

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

**Source:** Reviewer feedback (Saskia)
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
- Aixin's email:
  > "Acquisition channel order:
  > Geneseq01 and bcseq01: G T A C Hyb-DAPI
  > Geneseq02+ and bc seq02+: G T A C
  > Hyb: Hyb-GFP Hyb-YFP Hyb-TxRed Hyb-Cy5 Hyb-DAPI DIC"

- Xiaoyin's email:
  > "For the images, in cycles geneseq01 and bcseq01, the channels are G/T/A/C/DAPI. In other geneseq or bcseq cycles, the channels are GTAC. In hyb cycles, the channels are GFP/G/TxRed/Cy5/DAPI/DIC."

**Implementation:** Three separate acquisition files (gene sequencing, barcode sequencing, hybridization) per Saskia's guidance. Gene and barcode metadata includes DAPI channel (present in cycle 1), while subsequent cycles without DAPI share the same acquisition record. DIC channel mentioned in hyb emails but not currently included; confirmation needed if it should be modeled.

---

### 9. Laser Wavelengths

**Source:** MMConfig_Ti2E-xc2.1.txt

Gene/Barcode sequencing: G=514nm, T=561nm, A=640nm, C=640nm, DAPI=365nm

Hybridization: Assumed probe mapping (GFP=488nm, YFP=514nm, TxRed=561nm, Cy5=640nm, DAPI=365nm). See Q2 for verification.

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
- Aixin's email:
  > "exposure time is: G 60, T 30, A 20, C 40, DIC 20, Hyb-GFP 100, Hyb-YFP 30, Hyb-TxRed 30, Hyb-Cy5 20, Hyb-DAPI 20."

- MMConfig_Ti2E-xc2.1.txt: Confirmed exposure times in channel preset configurations

**CONFLICT - Hyb-DAPI Exposure Time:**
- **MMConfig_Ti2E-xc2.1.txt**: Hyb-DAPI = 30.0ms
- **Aixin's email**: Hyb-DAPI = 20ms
- **Decision**: Using 20ms from Aixin's email as the authoritative source (more recent communication, direct from experimenter)
- **Note**: Both gene sequencing and hybridization use the "Hyb-DAPI" channel configuration at 20ms exposure

**ASSUMPTION - Probe-to-Fluorophore Mapping:**
I didn't know the actual probe-to-fluorophore mapping. I made an arbitrary assignment in `HYB_PROBE_TO_FLUOROPHORE`:
- Hyb_XC2758 → GFP (488nm, 100ms)
- Hyb_XC2759 → YFP (514nm, 30ms)
- Hyb_XC2760 → TxRed (561nm, 30ms)
- Hyb_YS221 → Cy5 (640nm, 20ms)

**Rationale:** This allows the metadata to be complete and reviewable. The fluorophore configurations (wavelengths and exposure times) are correct and come from MMConfig file. Only the mapping of which probe uses which fluorophore needs verification.

**To update when actual mapping is known:** Simply change the fluorophore assignments in `HYB_PROBE_TO_FLUOROPHORE` in `constants.py`. The wavelengths and exposures are defined separately in `HYB_FLUOROPHORE_CONFIG` and will automatically be applied correctly. Then regenerate: `python generate_barseq_acquisitions.py --subject-id 780346`

The probe identifiers (XC2758, XC2759, XC2760, YS221) appear to be internal lab codes not documented in public protocols or MMConfig files.

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

**Source:** Copied from exaspim_acquisition.py example in aind-data-schema repository

**SPIM_RPI Definition:**
- X axis: Left_to_right
- Y axis: Anterior_to_posterior
- Z axis: Superior_to_inferior

**CONCERN - Potential Mismatch with Coronal Imaging:**

For coronal sections being tiled and imaged:
- **X (left-right on slide):** Medial-lateral → matches SPIM_RPI X (Left_to_right)
- **Y (up-down on slide):** Dorsal-ventral (superior-inferior) → but SPIM_RPI Y is Anterior_to_posterior
- **Z (z-stack through 20μm section):** Anterior-posterior direction → but SPIM_RPI Z is Superior_to_inferior

**The mismatch:** For single coronal sections with z-stacks through the section thickness, SPIM_RPI appears to have Y and Z swapped relative to the actual imaging coordinates.

**Possible interpretations:**
1. SPIM_RPI is intended for 3D volume reconstruction where Y tracks which coronal section you're at (anterior to posterior through the brain)
2. A different coordinate system should be used for coronal section tiling
3. The coordinate system is correct and our understanding of the mapping is wrong

**NEEDS VERIFICATION:** Confirm with imaging team whether SPIM_RPI is the appropriate coordinate system for coronal section tiling, or if a different system should be used.

**Note:** The coordinate system applies to both the Acquisition object and the ImagingConfig within each DataStream.

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

### 16. Acquisition Type

**Decision:** acquisition_type = "BarcodeSequencing" for all three phases (gene sequencing, barcode sequencing, and hybridization)

**Source:** Schema field description suggests this should be consistent across similar acquisitions for the same experiment.

**Rationale:**
- All three phases are part of the same BARseq (Barcoded Anatomy Resolved by Sequencing) workflow
- The acquisition_type field is meant to group related acquisitions from the same experiment
- While hybridization technically uses fluorescent in situ hybridization, it serves as anatomical reference for the barcode sequencing data and is an integral part of the BARseq protocol
- Using the same acquisition_type makes it clear these three acquisitions belong together and will be processed as a unit

**Implementation:** All three builders set `acquisition_type="BarcodeSequencing"`

---

### 17. Specimen ID Strategy

**Decision:** Use single specimen_id per acquisition representing the collection of sections imaged together (schema limitation: field is `Optional[str]`, not a list).

**Current placeholder:** `"780346_PLACEHOLDER_SPECIMEN_ID"` - see Q3 for details needed from team.

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
   - Tile dimensions: 3200x3200
   - Stitch overlap: 23%

4. **Email correspondence**:
   - Aixin: XY pixel size, channel order, exposure times
   - Xiaoyin: Channel lists, filter information
   - Saskia: Separate acquisition files per phase
   - Dan: Tile grid estimate, device naming

5. **Lab notes** (780345 and 780346):
   - Section thickness: 20 μm coronal sections
   - Sections per slide: 4 sections for BARseq
   - Anatomical coverage: Throughout Locus Coeruleus (LC)

5. **Schema examples**: exaspim_acquisition.py
   - ImageSPIM structure
   - Coordinate system usage
