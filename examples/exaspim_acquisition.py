""" example ExaSPIM acquisition """

from datetime import datetime

from aind_data_schema.core import acquisition
from aind_data_schema.core.procedures import Reagent
from aind_data_schema.imaging import tile
from aind_data_schema.models.devices import Calibration, Maintenance
from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.registry import Registry
from aind_data_schema.models.units import PowerValue

t = datetime(2022, 11, 22, 8, 43, 00)

acq = acquisition.Acquisition(
    experimenter_full_name=["###"],
    specimen_id="###",
    subject_id="###",
    instrument_id="###",
    maintenance=[
        Maintenance(
            maintenance_date=t,
            device_name="Chamber",
            description="Clean chamber",
            reagents=[
                Reagent(
                    name="reagent1",
                    source="xxx",
                    rrid=PIDName(name="xxx", abbreviation="xx", registry=Registry.RRID, registry_identifier="100"),
                    lot_number="xxx",
                    expiration_date=t.date(),
                ),
            ],
        )
    ],
    calibrations=[
        Calibration(
            calibration_date=t,
            device_name="Laser_1",
            description="Laser power calibration",
            input={"power_setting": PowerValue(value=100.0, unit="percent")},
            output={"power_measurement": PowerValue(value=50.0, unit="milliwatt")},
        )
    ],
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
                excitation_wavelength=488,
                excitation_power=200,
                light_source_name="Ex_488",
                filter_names=["Em_600"],
                detector_name="PMT_1",
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
                excitation_wavelength=561,
                excitation_power=200,
                light_source_name="Ex_561",
                filter_names=["Em_600"],
                detector_name="PMT_1",
                filter_wheel_index=0,
            ),
            notes="these are my notes",
        ),
    ],
)

acq.write_standard_file(prefix="exaspim")
