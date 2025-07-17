""" example ExaSPIM acquisition """

from datetime import datetime, timezone

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.units import PowerUnit, SizeUnit
from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.configs import (
    Channel,
    DeviceConfig,
    LaserConfig,
    ImageSPIM,
    Immersion,
    ImagingConfig,
    DetectorConfig,
    SampleChamberConfig,
)
from aind_data_schema.components.coordinates import CoordinateSystemLibrary, Scale, Translation
from aind_data_schema.components.reagent import Reagent
from aind_data_schema.components.wrappers import AssetPath
from aind_data_schema.core.acquisition import Acquisition, DataStream
from aind_data_schema.components.measurements import Calibration, Maintenance

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

tile_scale = Scale(
    scale=[0.748, 0.748, 1],
)
tile_translation0 = Translation(
    translation=[0, 1, 2],
)

image0 = ImageSPIM(
    channel_name="488",
    file_name=AssetPath("tile_X_0000_Y_0000_Z_0000_CH_488.ims"),
    dimensions=Scale(scale=[512, 512, 256]),
    image_to_acquisition_transform=[tile_scale, tile_translation0],
)
image1 = ImageSPIM(
    channel_name="561",
    file_name=AssetPath("tile_X_0000_Y_0000_Z_0000_CH_561.ims"),
    dimensions=Scale(scale=[512, 512, 256]),
    image_to_acquisition_transform=[tile_scale, tile_translation0],
)

imaging_config = ImagingConfig(
    device_name="ExaSPIM",
    channels=[
        Channel(
            channel_name="488",
            intended_measurement="GFP signal",
            light_sources=[
                LaserConfig(
                    device_name="LAS_08308",
                    wavelength=488,
                    wavelength_unit=SizeUnit.NM,
                    power=200,
                    power_unit=PowerUnit.MW,
                ),
            ],
            emission_filters=[
                DeviceConfig(
                    device_name="Multiband filter",
                ),
            ],
            detector=DetectorConfig(
                device_name="PMT_1",
                exposure_time=1,
                trigger_type="Internal",
            ),
        ),
        Channel(
            channel_name="561",
            intended_measurement="TdTomato signal",
            light_sources=[
                LaserConfig(
                    device_name="539251",
                    wavelength=561,
                    wavelength_unit=SizeUnit.NM,
                    power=200,
                    power_unit=PowerUnit.MW,
                ),
            ],
            emission_filters=[
                DeviceConfig(
                    device_name="Multiband filter",
                )
            ],
            detector=DetectorConfig(
                device_name="PMT_1",
                exposure_time=1,
                trigger_type="Internal",
            ),
        ),
    ],
    images=[image0, image1],
    coordinate_system=CoordinateSystemLibrary.SPIM_RPI,
)

chamber_config = SampleChamberConfig(
    device_name="Sample chamber",
    chamber_immersion=Immersion(
        medium="PBS",
        refractive_index=1.33,
    ),
)


acq = Acquisition(
    experimenters=["John Smith"],
    specimen_id="123456-123",
    subject_id="123456",
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
            input=[100],
            input_unit=PowerUnit.PERCENT,
            output=[50],
            output_unit=PowerUnit.MW,
        )
    ],
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.SPIM],
            active_devices=[
                "LAS_08308",
                "539251",
            ],
            configurations=[
                imaging_config,
                chamber_config,
            ],
        )
    ],
    acquisition_start_time=t,
    acquisition_end_time=t,
    acquisition_type="ExaSPIM",
)

if __name__ == "__main__":
    serialized = acq.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="exaspim")
