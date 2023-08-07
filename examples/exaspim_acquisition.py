""" example ExaSPIM acquisition """

import datetime

from aind_data_schema.imaging import acquisition, tile

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

acq = acquisition.Acquisition(
    experimenter_full_name=["###"],
    specimen_id="###",
    subject_id="###",
    instrument_id="###",
    session_start_time=t,
    session_end_time=t,
    local_storage_directory="D:",
    external_storage_directory="Z:",
    chamber_immersion=acquisition.Immersion(medium="PBS", refractive_index=1.33),
    axes=[
        acquisition.Axis(
            name="X",
            dimension=2,
            direction="Left_to_right",
        ),
        acquisition.Axis(
            name="Y",
            dimension=1,
            direction="Anterior_to_posterior",
        ),
        acquisition.Axis(
            name="Z",
            dimension=0,
            direction="Inferior_to_superior",
        ),
    ],
    tiles=[
        tile.AcquisitionTile(
            file_name="tile_X_0000_Y_0000_Z_0000_CH_488.ims",
            coordinate_transformations=[
                tile.Scale3dTransform(scale=[0.748, 0.748, 1]),
                tile.Translation3dTransform(translation=[0, 0, 0]),
            ],
            channel=tile.Channel(
                channel_name="488",
                laser_wavelength=488,
                laser_power=200,
                filter_wheel_index=0,
            ),
            notes="these are my notes",
        ),
        tile.AcquisitionTile(
            file_name="tile_X_0000_Y_0000_Z_0000_CH_561.ims",
            coordinate_transformations=[
                tile.Scale3dTransform(scale=[0.748, 0.748, 1]),
                tile.Translation3dTransform(translation=[0, 0, 0]),
            ],
            channel=tile.Channel(
                channel_name="561",
                laser_wavelength=561,
                laser_power=200,
                filter_wheel_index=0,
            ),
            notes="these are my notes",
        ),
    ],
)

acq.write_standard_file(prefix="exaspim")
