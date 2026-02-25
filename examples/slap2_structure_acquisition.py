"""example SLAP2 structure acquisition"""

import argparse
from datetime import datetime, timezone
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.slap2_acquisition_type import Slap2AcquisitionType
from aind_data_schema_models.units import PowerUnit, SizeUnit, FrequencyUnit
from aind_data_schema_models.devices import FilterType
from aind_data_schema_models.organizations import Organization
from aind_data_schema.components.devices import Filter
from aind_data_schema.components.coordinates import Translation, Scale, CoordinateSystemLibrary, Origin
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
)
from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    LaserConfig,
    TriggerType,
    ImagingConfig,
    Slap2Plane,
    PlanarImageStack,
    DeviceConfig,
    PowerFunction,
)
from aind_data_schema_models.brain_atlas import CCFv3

origin_ari = CoordinateSystemLibrary.BREGMA_ARI
origin_ari.name = "Arbitrary Origin ARI"
origin_ari.axis_unit = SizeUnit.UM
origin_ari.origin = Origin.ORIGIN

filter_red = Filter(
    name="Red Emission Filters",
    serial_number="None",
    manufacturer=Organization.SEMROCK,
    filter_type=FilterType.BANDPASS,
    cut_off_wavelength=725,
    cut_on_wavelength=585,
    center_wavelength=655,
    wavelength_unit=SizeUnit.NM,
    notes="Includes 585 dichroic mirror and 650/150 filter",
)

filter_green = Filter(
    name="Green Emission Filters",
    serial_number="None",
    manufacturer=Organization.SEMROCK,
    filter_type=FilterType.BANDPASS,
    cut_off_wavelength=580,
    cut_on_wavelength=500,
    center_wavelength=540,
    wavelength_unit=SizeUnit.NM,
    notes="Includes 585 dichroic mirror and 540/80 filter",
)

filters_by_name = {
    "Red Emission Filters": filter_red,
    "Green Emission Filters": filter_green,
}

harp_start_time = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)
harp_end_time = datetime(2022, 7, 12, 7, 30, 00, tzinfo=timezone.utc)

project_name = "SLAP2"
acquisition_type = "full-field raster structure"

num_paths = 2
active_channels = ["Red", "Green"]

plane_depths = {"Path 1": [x + 0.5 for x in range(-20, 30)], "Path 2": [x + 0.3 for x in range(0, 50)]}
hwp_laser_power = 75

x_dilations = {"Path 1": 9, "Path 2": 9}

channel_intended_measurements = {
    "Red": "RCaMP3",
    "Green": "iGluSnFR4s",
}

stage_offset_from_origin = None  # or [x, y] in um

imaging_target_name = "Neuron1"

slap2_plane_full_field_raster = {
    "Path 1": [
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=min(plane_depths["Path 1"]),
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.RASTER,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 1"],
            dilation_unit=SizeUnit.PX,
        )
    ],
    "Path 2": [
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=min(plane_depths["Path 2"]),
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.RASTER,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 2"],
            dilation_unit=SizeUnit.PX,
        )
    ],
}

monaco_laser_config = LaserConfig(
    device_name="Monaco 150",
    wavelength=1030,
    wavelength_unit=SizeUnit.NM,
    power=150,
    power_unit=PowerUnit.MW,
)

sipm_config = {
    "Red": DetectorConfig(
        device_name="Red SiPM",
        trigger_type=TriggerType.ANALOG,
    ),
    "Green": DetectorConfig(
        device_name="Green SiPM",
        trigger_type=TriggerType.ANALOG,
    ),
}


a = Acquisition(
    subject_id="12345",
    acquisition_start_time=harp_start_time,
    acquisition_end_time=harp_end_time,
    experimenters=["John Smith"],
    ethics_review_id=["2415"],
    instrument_id="SLAP2_1_VCO_1",
    acquisition_type=project_name + ": " + acquisition_type,
    notes="center back of cranial window is coordinate system origin",
    coordinate_system=origin_ari,
    calibrations=[],
    maintenance=[],
    data_streams=[
        DataStream(
            stream_start_time=harp_start_time,
            stream_end_time=harp_end_time,
            modalities=[Modality.SLAP2],
            active_devices=[
                "SLAP2-1-PC",
                "SLAP2_1",
                "SiPM Red",
                "SiPM Green",
                "Polygonal Scanner",
                "Pockels Cell",
                "Half-Wave Plate",
                "Leica Objective",
                "Monaco 150",
                "vDAQ",
                "Green Emission Filters",
                "Red Emission Filters",
                "DMD1",
                "DMD2",
            ],
            configurations=[
                ImagingConfig(
                    device_name="SLAP2_1",
                    channels=[
                        Channel(
                            channel_name=f"Path {path_idx + 1} {channel_color} channel",
                            intended_measurement=channel_intended_measurements[channel_color],
                            detector=sipm_config[channel_color],
                            light_sources=[monaco_laser_config],
                            additional_device_names=[
                                DeviceConfig(device_name=f"DMD{path_idx + 1}"),
                                DeviceConfig(device_name="Leica Objective"),
                                DeviceConfig(device_name="Half-Wave Plate"),
                                DeviceConfig(device_name="Polygonal Scanner"),
                            ],
                            emission_filters=[DeviceConfig(device_name=f"{channel_color} Emission Filters")],
                            emission_wavelength=filters_by_name[f"{channel_color} Emission Filters"].center_wavelength,
                            emission_wavelength_unit=filters_by_name[
                                f"{channel_color} Emission Filters"
                            ].wavelength_unit,
                        )
                        for path_idx in range(num_paths)
                        for channel_color in active_channels
                    ],
                    images=[
                        PlanarImageStack(
                            power_function=PowerFunction.CONSTANT,
                            depth_start=min(plane_depths[f"Path {path_idx+1}"]),
                            depth_end=max(plane_depths[f"Path {path_idx+1}"]),
                            depth_step=(
                                max(plane_depths[f"Path {path_idx+1}"]) - min(plane_depths[f"Path {path_idx+1}"])
                            )
                            / (len(plane_depths[f"Path {path_idx+1}"]) - 1),
                            depth_unit=SizeUnit.UM,
                            channel_name=f"Path {path_idx + 1} {channel_color} channel",
                            image_to_acquisition_transform=[
                                Scale(
                                    scale=[0.25, 0.25],
                                ),
                                *(
                                    [
                                        Translation(
                                            translation=stage_offset_from_origin,
                                        )
                                    ]
                                    if stage_offset_from_origin is not None
                                    else []
                                ),
                            ],
                            dimensions=Scale(
                                scale=[800, 1280],
                            ),
                            dimensions_unit=SizeUnit.PX,
                            planes=slap2_plane_full_field_raster[f"Path {path_idx+1}"],
                        )
                        for path_idx in range(num_paths)
                        for channel_color in active_channels
                    ],
                ),
            ],
        )
    ],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = a.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="slap2_structure", output_directory=args.output_dir)
