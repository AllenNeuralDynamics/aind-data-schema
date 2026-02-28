"""example SLAP2 acquisition"""

import argparse
from datetime import datetime, timezone
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.slap2_acquisition_type import Slap2AcquisitionType
from aind_data_schema_models.units import PowerUnit, SizeUnit, FrequencyUnit, TimeUnit
from aind_data_schema_models.devices import FilterType
from aind_data_schema_models.organizations import Organization
from aind_data_schema.components.identifiers import Code
from aind_data_schema.components.devices import Filter
from aind_data_schema.components.coordinates import Translation, Scale, CoordinateSystemLibrary, Origin
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    StimulusEpoch,
)
from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    LaserConfig,
    TriggerType,
    ImagingConfig,
    Slap2Plane,
    PlanarImage,
    DeviceConfig,
)
from aind_data_schema_models.brain_atlas import CCFv3
from aind_data_schema_models.stimulus_modality import StimulusModality

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

instrument_components = [
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
    "w10dt714710",
    "VCO1_Behavior",
    "VCO1_CuttlefishCamTrigger",
    "VCO1_TimeStampGenerator",
    "MindScope Running Disc",
    "FaceCamera Assembly",
    "BodyCamera Assembly",
    "EyeCamera Assembly",
    "Stimulus Screen",
    "Photodiode",
]

harp_start_time = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)
harp_end_time = datetime(2022, 7, 12, 7, 30, 00, tzinfo=timezone.utc)

face_camera_exposure = 10
body_camera_exposure = 10
eye_camera_exposure = 10

project_name = "SLAP2"
acquisition_type = "multi-roi raster drifting gratings"

num_paths = 2
active_channels = ["Red", "Green"]

plane_depths = {"Path 1": [184, 160], "Path 2": [100, 105]}
hwp_laser_power = 75

x_dilations = {"Path 1": 9, "Path 2": 9}

channel_intended_measurements = {
    "Red": "RCaMP3",
    "Green": "iGluSnFR4s",
}

stage_offset_from_origin = None

imaging_target_name = "Neuron1"

slap2_plane_rois_raster = {
    "Path 1": [
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 1"][0],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.RASTER,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[100],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[5],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 1"],
            dilation_unit=SizeUnit.PX,
        ),
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 1"][1],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.RASTER,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[100],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[5],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 1"],
            dilation_unit=SizeUnit.PX,
        ),
    ],
    "Path 2": [
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 2"][0],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.RASTER,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[120],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[7],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 2"],
            dilation_unit=SizeUnit.PX,
        ),
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 2"][1],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.RASTER,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[120],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[7],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 2"],
            dilation_unit=SizeUnit.PX,
        ),
    ],
}

slap2_plane_rois_integration = {
    "Path 1": [
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 1"][0],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.INTEGRATION,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[200],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[9],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 1"],
            dilation_unit=SizeUnit.PX,
        ),
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 1"][1],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.INTEGRATION,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[200],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[9],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 1"],
            dilation_unit=SizeUnit.PX,
        ),
    ],
    "Path 2": [
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 2"][0],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.INTEGRATION,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[240],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[9],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 2"],
            dilation_unit=SizeUnit.PX,
        ),
        Slap2Plane(  # each fastZ plane will get its own Slap2Plane
            depth=plane_depths["Path 2"][1],
            depth_unit=SizeUnit.UM,
            power=hwp_laser_power,
            power_unit=PowerUnit.PERCENT,
            targeted_structure=CCFv3.VISPL2_3,
            target_name=imaging_target_name,
            slap2_acquisition_type=Slap2AcquisitionType.INTEGRATION,
            mask_image_path="path/to/mask.tif",
            unique_frame_rates=[240],
            frame_rate_unit=FrequencyUnit.HZ,
            frame_rate_image_path="path/to/frame_rate_image.tif",
            unique_y_dilations=[9],
            y_dilation_image_path="path/to/dilation_image.tif",
            x_dilation=x_dilations["Path 2"],
            dilation_unit=SizeUnit.PX,
        ),
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
            modalities=[Modality.SLAP2, Modality.BEHAVIOR_VIDEOS, Modality.BEHAVIOR],
            active_devices=instrument_components,
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
                        PlanarImage(
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
                            planes=[plane],
                        )
                        for path_idx in range(num_paths)
                        for plane in (
                            slap2_plane_rois_raster[f"Path {path_idx+1}"]
                            + slap2_plane_rois_integration[f"Path {path_idx+1}"]
                        )
                        for channel_color in active_channels
                    ],
                ),
                DetectorConfig(
                    device_name="FaceCamera",
                    exposure_time=face_camera_exposure,
                    exposure_time_unit=TimeUnit.MS,
                    trigger_type=TriggerType.EXTERNAL,
                ),
                DetectorConfig(
                    device_name="BodyCamera",
                    exposure_time=body_camera_exposure,
                    exposure_time_unit=TimeUnit.MS,
                    trigger_type=TriggerType.EXTERNAL,
                ),
                DetectorConfig(
                    device_name="EyeCamera",
                    exposure_time=eye_camera_exposure,
                    exposure_time_unit=TimeUnit.MS,
                    trigger_type=TriggerType.EXTERNAL,
                ),
            ],
        )
    ],
    stimulus_epochs=[
        StimulusEpoch(
            stimulus_start_time=harp_start_time,
            stimulus_end_time=harp_end_time,
            stimulus_name="Shuffled 8-direction drifting gratings",
            code=Code(
                url=(
                    "https://github.com/AllenNeuralDynamics/ophys-passive-visual-stim/"
                    "blob/main/src/RandomDriftingGratings_ContinuousTrials.bonsai"
                ),
                version="168e4ef1923c535f6c4d914a126526cc11168ac7",  # get git commit id
                name="RandomDriftingGratings_ContinuousTrials.bonsai",
                language="Bonsai",
                language_version="2.9.0",  # get from repo or code directly
                parameters={"CodeParameters": {
                        "Initial Spont Int": 28,
                        "Num Trials": 40,
                        "PortName": "COM7",
                        "Screen_BlueColor (0-1)": 1,
                        "Screen_GreenColor (0-1)": 0,
                        "Screen_RedColor (0-1)": 0,
                        "Subject": "000000",
                        "GratingTrialParametersFile": (
                            "ParameterFiles/8_direction_drifting_grating_params.csv"
                        ),
                    },
                    "GratingTrialParameters": {
                        "Contrast": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
                        "Delay": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                        "DelayUnit": "second",
                        "Diameter": [360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 360.0],
                        "DiameterUnit": "degree",
                        "Duration": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                        "DurationUnit": "second",
                        "Orientation": [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0, 359.0],
                        "OrientationUnit": "degree",
                        "SpatialFrequency": [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
                        "SpatialFrequencyUnit": "cycle/degree",
                        "TemporalFrequency": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                        "TemporalFrequencyUnit": "Hz",
                        "X": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "XUnit": "degree",
                        "Y": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        "YUnit": "degree",
                    },
                },
            ),
            stimulus_modalities=[StimulusModality.VISUAL],
            notes="",  # include description of stimulus here if code and/or parameters are not available
            active_devices=["Stimulus Screen"],
            configurations=[],
        ),
    ],
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON file")
    args = parser.parse_args()

    serialized = a.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="slap2", output_directory=args.output_dir)
