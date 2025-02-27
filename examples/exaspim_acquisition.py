""" example ExaSPIM acquisition """

from datetime import datetime, timezone

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.units import PowerUnit
from aind_data_schema_models.modalities import Modality

from aind_data_schema.components import tile
from aind_data_schema.components.coordinates import ImageAxis, Scale3dTransform, Translation3dTransform
from aind_data_schema.components.devices import Calibration, Maintenance
from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.acquisition import Acquisition, DataStream
from aind_data_schema.components.configs import Immersion, ImagingConfig
from aind_data_schema.core.procedures import Reagent

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)


acq = Acquisition(
    experimenters=[Person(name="John Smith")],
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
                    source=Organization.OTHER,
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
            input={"power_setting": 100.0, "power_unit": PowerUnit.PERCENT},
            output={
                "power_measurement": 50.0,
                "power_unit": PowerUnit.MW,
            },
        )
    ],
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.SPIM],
            active_devices=[],
            configurations=[
                ImagingConfig(
                    chamber_immersion=Immersion(
                        medium="PBS",
                        refractive_index=1.33,
                    ),
                    axes=[
                        ImageAxis(
                            name="X",
                            dimension=2,
                            direction="Left_to_right",
                        ),
                        ImageAxis(
                            name="Y",
                            dimension=1,
                            direction="Anterior_to_posterior",
                        ),
                        ImageAxis(
                            name="Z",
                            dimension=0,
                            direction="Inferior_to_superior",
                        ),
                    ],
                    tiles=[
                        tile.AcquisitionTile(
                            file_name="tile_X_0000_Y_0000_Z_0000_CH_488.ims",
                            coordinate_transformations=[
                                Scale3dTransform(scale=[0.748, 0.748, 1]),
                                Translation3dTransform(translation=[0, 0, 0]),
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
                                Scale3dTransform(scale=[0.748, 0.748, 1]),
                                Translation3dTransform(translation=[0, 0, 0]),
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
                ),
            ],
        )
    ],
    acquisition_start_time=t,
    acquisition_end_time=t,
    local_storage_directory="D:",
    external_storage_directory="Z:",
)

serialized = acq.model_dump_json()
deserialized = Acquisition.model_validate_json(serialized)
deserialized.write_standard_file(prefix="exaspim")
