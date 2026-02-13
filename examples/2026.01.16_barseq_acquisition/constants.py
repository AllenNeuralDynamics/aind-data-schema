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
TILES_X = 14  # Estimated grid size
TILES_Y = 8
FIRST_TILE_OFFSET_PX = -736  # Starting position in pixels

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
        "exposure_ms": 30.0,
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

# DAPI configuration for hybridization (updated exposure time per Aixin: 20ms vs 30ms in gene seq)
HYB_DAPI_CONFIG = {
    "laser_wavelength_nm": 365,
    "filter_name": "DAPI/GFP/TxRed-69401",
    "exposure_ms": 20.0,  # Different from gene sequencing (30ms)
}

# Hybridization probe measurements
HYB_PROBE_MEASUREMENTS = {
    "Hyb_XC2758": "Probe XC2758",
    "Hyb_XC2759": "Probe XC2759",
    "Hyb_XC2760": "Probe XC2760",
    "Hyb_YS221": "Probe YS221",
}

# Known fluorophore exposure times (can't be applied until probe-to-fluorophore mapping is known)
# GFP=100ms, YFP=30ms, TxRed=30ms, Cy5=20ms
HYB_FLUOROPHORE_EXPOSURE_MS = {
    "GFP": 100.0,
    "YFP": 30.0,
    "TxRed": 30.0,
    "Cy5": 20.0,
}

# Hybridization probe configuration
# Each probe uses one of the 4 fluorophores, but the mapping is currently unknown.
# ASSUMPTION: All probes set to placeholder (9999) until actual mapping is determined.
# Once mapping is known, replace 9999 values with actual fluorophore values:
#   GFP:   wavelength_nm=488,  exposure_ms=100.0
#   YFP:   wavelength_nm=514,  exposure_ms=30.0
#   TxRed: wavelength_nm=561,  exposure_ms=30.0
#   Cy5:   wavelength_nm=640,  exposure_ms=20.0
HYB_PROBE_CONFIG = {
    "Hyb_XC2758": {"wavelength_nm": 9999, "exposure_ms": 9999.0},  # PLACEHOLDER
    "Hyb_XC2759": {"wavelength_nm": 9999, "exposure_ms": 9999.0},  # PLACEHOLDER
    "Hyb_XC2760": {"wavelength_nm": 9999, "exposure_ms": 9999.0},  # PLACEHOLDER
    "Hyb_YS221": {"wavelength_nm": 9999, "exposure_ms": 9999.0},   # PLACEHOLDER
}
