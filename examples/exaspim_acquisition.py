""" example ExaSPIM acquisition """

import datetime

from aind_data_schema.imaging import acquisition

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

acq = acquisition.Acquisition(
    experimenter_full_name="###",
    subject_id="###",
    instrument_id="###",
    session_start_time=t,
    session_end_time=t,
    local_storage_directory="D:",
    external_storage_directory="Z:",
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
        acquisition.Tile(
            file_name="tile_X_0000_Y_0000_Z_0000_CH_488.ims",
            voxel_size=acquisition.VoxelSize(
                size_x=0.748, size_y=0.748, size_z=1.000
            ),
            position=acquisition.TilePosition(
                x_start=0,
                x_end=100,
                y_start=0,
                y_end=100,
                z_start=0,
                z_end=100,
            ),
            channel=acquisition.Channel(
                channel_name="488",
                laser_wavelength=488,
                laser_power=200,
                filter_wheel_index=0,
            ),
            daq_params=dict(
                etl_buffer_time_ms=5.0,
                etl_amplitude_volt=0.2,
                etl_offest_volt=1.77,
            ),
            notes="these are my notes",
        ),
        acquisition.Tile(
            file_name="tile_X_0000_Y_0000_Z_0000_CH_561.ims",
            voxel_size=acquisition.VoxelSize(
                size_x=0.748, size_y=0.748, size_z=1.000
            ),
            position=acquisition.TilePosition(
                x_start=0,
                x_end=100,
                y_start=0,
                y_end=100,
                z_start=0,
                z_end=100,
            ),
            channel=acquisition.Channel(
                channel_name="561",
                laser_wavelength=561,
                laser_power=200,
                filter_wheel_index=0,
            ),
            daq_params=dict(
                etl_buffer_time_ms=5.0,
                etl_amplitude_volt=0.2,
                etl_offest_volt=1.77,
            ),
            notes="these are my notes",
        ),
    ],
)

acq.write_standard_file(prefix="exaspim")
