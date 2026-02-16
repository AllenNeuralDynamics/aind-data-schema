"""Hardware constants for BARseq acquisition metadata generation.

This module contains hardware configuration and channel settings that are
universal across all BARseq acquisitions (instrument settings, tile parameters,
laser wavelengths, filters, exposure times).

For experiment-specific parameters (subject-specific sections, timing, personnel),
see experiment_params.py.

Sources:
- MMConfig_Ti2E-xc2.1.txt: Laser wavelengths, filter names, exposure times
- dogwood.json: Tile dimensions, overlap
- Email from Aixin (2026-02-09): Pixel size, channel order
- Methods document: Z-step
"""

# =============================================================================
# SHARED TILING CONFIGURATION
# =============================================================================
# These parameters are identical for gene sequencing, barcode sequencing, and hybridization

# Tile dimensions (pixels)
TILE_WIDTH_PX = 3200
TILE_HEIGHT_PX = 3200
Z_PLANES_PER_TILE = 10  # Max projection depth

# Pixel size and z-step (micrometers)
PIXEL_SIZE_UM = 0.33
Z_STEP_UM = 1.5

# Tiling configuration (from Aixin's email + Dan's estimate)
TILE_OVERLAP_PERCENT = 0.23  # 23% overlap between tiles
TILE_STEP_PX = int(TILE_WIDTH_PX * (1 - TILE_OVERLAP_PERCENT))  # 2464 pixels
TILES_X = 14  # Estimated grid size (Dan's estimate)
TILES_Y = 8
FIRST_TILE_OFFSET_PX = 0  # Confirmed by Xiaoyin (2026-02-13): First tile starts at (0,0)

# =============================================================================
# GENE SEQUENCING CHANNEL CONFIGURATION
# =============================================================================
# Channels: G, T, A, C, DAPI
# Source: MMConfig_Ti2E-xc2.1.txt (laser wavelengths, filters, exposure times)

GENESEQ_CHANNEL_CONFIG = {
    "G": {
        "laser_wavelength_nm": 514,
        "filter_name": "565/24",
        "exposure_ms": 60.0,
    },
    "T": {
        "laser_wavelength_nm": 561,
        "filter_name": "441/511/593/684/817",
        "exposure_ms": 30.0,
    },
    "A": {
        "laser_wavelength_nm": 640,
        "filter_name": "676/29",
        "exposure_ms": 20.0,
    },
    "C": {
        "laser_wavelength_nm": 640,
        "filter_name": "775/140",
        "exposure_ms": 40.0,
    },
    "DAPI": {
        "laser_wavelength_nm": 365,
        "filter_name": "DAPI/GFP/TxRed-69401",
        "exposure_ms": 20.0,  # Hyb-DAPI per Aixin's email
    },
}

# =============================================================================
# BARCODE SEQUENCING CHANNEL CONFIGURATION
# =============================================================================
# Channels: G, T, A, C (no DAPI in barcode sequencing cycles 2+)
# Configuration is identical to gene sequencing for G, T, A, C

BARCODESEQ_CHANNEL_CONFIG = {
    "G": {
        "laser_wavelength_nm": 514,
        "filter_name": "565/24",
        "exposure_ms": 60.0,
    },
    "T": {
        "laser_wavelength_nm": 561,
        "filter_name": "441/511/593/684/817",
        "exposure_ms": 30.0,
    },
    "A": {
        "laser_wavelength_nm": 640,
        "filter_name": "676/29",
        "exposure_ms": 20.0,
    },
    "C": {
        "laser_wavelength_nm": 640,
        "filter_name": "775/140",
        "exposure_ms": 40.0,
    },
}

# =============================================================================
# HYBRIDIZATION CHANNEL CONFIGURATION
# =============================================================================
# Channels: 4 probes (XC2758, XC2759, XC2760, YS221) + DAPI
# Probe-to-fluorophore mapping is unknown, using placeholders

# DAPI configuration for hybridization
# Note: Gene sequencing also uses "Hyb-DAPI" with the same 20ms exposure
HYB_DAPI_CONFIG = {
    "laser_wavelength_nm": 365,
    "filter_name": "DAPI/GFP/TxRed-69401",
    "exposure_ms": 20.0,
}

# Hybridization probe measurements
HYB_PROBE_MEASUREMENTS = {
    "Hyb_XC2758": "Probe XC2758",
    "Hyb_XC2759": "Probe XC2759",
    "Hyb_XC2760": "Probe XC2760",
    "Hyb_YS221": "Probe YS221",
}

# Hybridization fluorophore configurations (from MMConfig file)
# These are the 4 known fluorophore configurations used in hybridization
HYB_FLUOROPHORE_CONFIG = {
    "GFP": {"wavelength_nm": 488, "exposure_ms": 100.0},
    "YFP": {"wavelength_nm": 514, "exposure_ms": 30.0},
    "TxRed": {"wavelength_nm": 561, "exposure_ms": 30.0},
    "Cy5": {"wavelength_nm": 640, "exposure_ms": 20.0},
}

# Probe-to-fluorophore mapping
# Source: Email from Xiaoyin Chen (2026-02-13)
# XC2758, XC2759 confirmed correct. XC2760 is Cy5, YS221 is TxRed.
# Wavelengths and exposure times are defined in HYB_FLUOROPHORE_CONFIG.
HYB_PROBE_TO_FLUOROPHORE = {
    "Hyb_XC2758": "GFP",     # Confirmed by Xiaoyin (2026-02-13)
    "Hyb_XC2759": "YFP",     # Confirmed by Xiaoyin (2026-02-13)
    "Hyb_XC2760": "Cy5",     # Confirmed by Xiaoyin (2026-02-13) - corrected from TxRed
    "Hyb_YS221": "TxRed",    # Confirmed by Xiaoyin (2026-02-13) - corrected from Cy5
}
