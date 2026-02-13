"""Utility functions for BARseq acquisition metadata generation.

This module contains shared functions used by gene sequencing, barcode sequencing,
and hybridization acquisition builders.
"""

from aind_data_schema.components.configs import ImageSPIM
from aind_data_schema.components.coordinates import Scale, Translation
from aind_data_schema_models.units import SizeUnit

from constants import (
    FIRST_TILE_OFFSET_PX,
    PIXEL_SIZE_UM,
    TILE_HEIGHT_PX,
    TILE_OVERLAP_PERCENT,
    TILE_STEP_PX,
    TILE_WIDTH_PX,
    TILES_X,
    TILES_Y,
    Z_PLANES_PER_TILE,
    Z_STEP_UM,
)


def create_tiling_description() -> str:
    """
    Generate a description of the tiling process for documentation.

    This description is included in DataStream.notes to document the acquisition
    process while keeping the metadata compact (only saved max projections are
    included as ImageSPIM objects).

    Returns
    -------
    str
        Comprehensive description of tiling parameters and process
    """
    total_width_px = abs(FIRST_TILE_OFFSET_PX) + (TILES_X - 1) * TILE_STEP_PX + TILE_WIDTH_PX
    total_height_px = abs(FIRST_TILE_OFFSET_PX) + (TILES_Y - 1) * TILE_STEP_PX + TILE_HEIGHT_PX

    return (
        f"Images acquired as {TILES_X}x{TILES_Y} tile grid ({TILES_X * TILES_Y} tiles per channel) "
        f"with {int(TILE_OVERLAP_PERCENT * 100)}% overlap. "
        f"Individual tiles: {TILE_WIDTH_PX}x{TILE_HEIGHT_PX} pixels, {Z_PLANES_PER_TILE} z-planes. "
        f"Tile step: {TILE_STEP_PX} pixels. First tile offset: ({FIRST_TILE_OFFSET_PX}, {FIRST_TILE_OFFSET_PX}) pixels. "
        f"Pixel size: {PIXEL_SIZE_UM} μm (XY), z-step: {Z_STEP_UM} μm. "
        f"Individual tile z-stacks were acquired, max-projected ({Z_PLANES_PER_TILE} planes), and stitched. "
        f"Only stitched max projections were saved. "
        f"Stitched dimensions: {total_width_px}x{total_height_px} pixels, {Z_PLANES_PER_TILE} z-planes."
    )


def create_max_projection_image(channel_name: str) -> ImageSPIM:
    """
    Create ImageSPIM object for a saved max projection.

    Only the final stitched max projections are saved to disk. Individual tiles
    are transient and deleted after stitching. This function creates the ImageSPIM
    object for the saved stitched max projection.

    Tiling parameters are documented in the DataStream.notes field (see
    create_tiling_description()).

    Parameters
    ----------
    channel_name : str
        Name of the channel this image corresponds to (e.g., "GeneSeq_G", "BarcodeSeq_T", "Hyb_XC2758")

    Returns
    -------
    ImageSPIM
        Image object for the stitched max projection with placeholder file path
    """
    # Calculate stitched dimensions from tile grid parameters
    total_width_px = abs(FIRST_TILE_OFFSET_PX) + (TILES_X - 1) * TILE_STEP_PX + TILE_WIDTH_PX
    total_height_px = abs(FIRST_TILE_OFFSET_PX) + (TILES_Y - 1) * TILE_STEP_PX + TILE_HEIGHT_PX

    return ImageSPIM(
        channel_name=channel_name,
        file_name="PLACEHOLDER_max_projection_path",
        dimensions_unit=SizeUnit.PX,
        dimensions=Scale(scale=[total_width_px, total_height_px, Z_PLANES_PER_TILE]),
        image_to_acquisition_transform=[
            Translation(translation=[0, 0, 0]),
            Scale(scale=[PIXEL_SIZE_UM, PIXEL_SIZE_UM, Z_STEP_UM]),
        ],
    )
