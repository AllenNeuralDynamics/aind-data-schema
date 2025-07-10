""" example FIP ophys acquisition """

from datetime import datetime, timezone
from decimal import Decimal

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import TimeUnit, SizeUnit, PowerUnit, VolumeUnit

from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    StimulusEpoch,
    AcquisitionSubjectDetails,
    PerformanceMetrics,
)
from aind_data_schema.components.connections import Connection
from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    PatchCordConfig,
    LightEmittingDiodeConfig,
    TriggerType,
    SpeakerConfig,
    DeviceConfig,
)
from aind_data_schema_models.stimulus_modality import StimulusModality

# The session date from the JSON file is 2024-01-15 with timezone -08:00
t_start = datetime(2024, 1, 15, 15, 56, 28, tzinfo=timezone.utc)
t_end = t_start  # Set end time same as start since it's not specified in the JSON

# Define detector configurations
green_detector_config = DetectorConfig(
    device_name="Green CMOS",
    exposure_time=15350,
    exposure_time_unit=TimeUnit.US,
    trigger_type=TriggerType.INTERNAL,
)

red_detector_config = DetectorConfig(
    device_name="Red CMOS",
    exposure_time=15350,
    exposure_time_unit=TimeUnit.US,
    trigger_type=TriggerType.INTERNAL,
)

# Define light sources
blue_led_config = LightEmittingDiodeConfig(
    device_name="470nm LED",
    power=20,
    power_unit=PowerUnit.UW,
)

uv_led_config = LightEmittingDiodeConfig(
    device_name="415nm LED",
    power=20,
    power_unit=PowerUnit.UW,
)

yellow_led_config = LightEmittingDiodeConfig(
    device_name="565nm LED",
    power=20,
    power_unit=PowerUnit.UW,
)

# Define channel configurations for each fiber connection
# Fiber 0 channels
fiber0_red_channel = Channel(
    channel_name="Fiber 0_red",
    intended_measurement="dopamine",
    detector=red_detector_config,
    light_sources=[yellow_led_config],
    excitation_filters=[
        DeviceConfig(device_name="Excitation filter 560nm"),
    ],
    emission_filters=[
        DeviceConfig(device_name="Red emission bandpass filter"),
    ],
    emission_wavelength=590,
    emission_wavelength_unit=SizeUnit.NM,
    additional_device_names=None,
)

fiber0_green_channel = Channel(
    channel_name="Fiber 0_green",
    intended_measurement="calcium",
    detector=green_detector_config,
    light_sources=[blue_led_config],
    excitation_filters=[
        DeviceConfig(device_name="Excitation filter 470nm"),
    ],
    emission_filters=[
        DeviceConfig(device_name="Green emission bandpass filter"),
    ],
    emission_wavelength=510,
    emission_wavelength_unit=SizeUnit.NM,
    additional_device_names=None,
)

fiber0_isosbestic_channel = Channel(
    channel_name="Fiber 0_isosbestic",
    intended_measurement="control",
    detector=green_detector_config,
    light_sources=[uv_led_config],
    excitation_filters=[
        DeviceConfig(device_name="Excitation filter 410nm"),
    ],
    emission_filters=[
        DeviceConfig(device_name="Green emission bandpass filter"),
    ],
    emission_wavelength=510,
    emission_wavelength_unit=SizeUnit.NM,
    additional_device_names=None,
)

# Fiber 1 channels
fiber1_green_channel = Channel(
    channel_name="Fiber 1_green",
    intended_measurement="calcium",
    detector=green_detector_config,
    light_sources=[blue_led_config],
    excitation_filters=[
        DeviceConfig(device_name="Excitation filter 470nm"),
    ],
    emission_filters=[
        DeviceConfig(device_name="Green emission bandpass filter"),
        DeviceConfig(device_name="dual-edge standard epi-fluorescence dichroic beamsplitter"),
    ],
    emission_wavelength=510,
    emission_wavelength_unit=SizeUnit.NM,
    additional_device_names=None,
)

fiber1_isosbestic_channel = Channel(
    channel_name="Fiber 1_isosbestic",
    intended_measurement="control",
    detector=green_detector_config,
    light_sources=[uv_led_config],
    excitation_filters=[
        DeviceConfig(device_name="Excitation filter 410nm"),
    ],
    emission_filters=[
        DeviceConfig(device_name="Green emission bandpass filter"),
        DeviceConfig(device_name="dual-edge standard epi-fluorescence dichroic beamsplitter"),
    ],
    emission_wavelength=510,
    emission_wavelength_unit=SizeUnit.NM,
    additional_device_names=None,
)

# Define patch cord configs
patch_cord_a_config = PatchCordConfig(
    device_name="Patch Cord A",
    channels=[fiber0_red_channel, fiber0_green_channel, fiber0_isosbestic_channel],
)

patch_cord_b_config = PatchCordConfig(
    device_name="Patch Cord B",
    channels=[fiber1_green_channel, fiber1_isosbestic_channel],
)

patch_cord_c_config = PatchCordConfig(
    device_name="Patch Cord C",
    channels=[
        Channel(
            channel_name="disconnected",
            intended_measurement=None,
            detector=DetectorConfig(device_name="None", exposure_time=0, trigger_type=TriggerType.INTERNAL),
            light_sources=[],
            emission_wavelength=300,
            emission_wavelength_unit=SizeUnit.NM,
            additional_device_names=[],
        )
    ],
)

patch_cord_d_config = PatchCordConfig(
    device_name="Patch Cord D",
    channels=[
        Channel(
            channel_name="disconnected",
            intended_measurement=None,
            detector=DetectorConfig(device_name="None", exposure_time=0, trigger_type=TriggerType.INTERNAL),
            light_sources=[],
            emission_wavelength=300,
            emission_wavelength_unit=SizeUnit.NM,
            additional_device_names=[],
        )
    ],
)

# Define connections between patch cords, detectors, and implanted fibers
connections = [
    # Connection between Patch Cord A and Fiber 0 (implant) - bidirectional
    Connection(
        source_device="Patch Cord A",
        target_device="Fiber 0",
        send_and_receive=True,
    ),
    # Connection between Patch Cord B and Fiber 1 (implant) - bidirectional
    Connection(
        source_device="Patch Cord B",
        target_device="Fiber 1",
        send_and_receive=True,
    ),
    # Connections between Patch Cord A and detectors for different channels
    Connection(
        source_device="Patch Cord A",
        source_port="Fiber 0_red",
        target_device="Red CMOS",
    ),
    Connection(
        source_device="Patch Cord A",
        source_port="Fiber 0_green",
        target_device="Green CMOS",
    ),
    Connection(
        source_device="Patch Cord A",
        source_port="Fiber 0_isosbestic",
        target_device="Green CMOS",
        target_port="isosbestic",
    ),
    # Connections between Patch Cord B and detectors
    Connection(
        source_device="Patch Cord B",
        source_port="Fiber 1_green",
        target_device="Green CMOS",
    ),
    Connection(
        source_device="Patch Cord B",
        source_port="Fiber 1_isosbestic",
        target_device="Green CMOS",
        target_port="isosbestic",
    ),
    # Connections between LEDs and Patch Cord A
    Connection(
        source_device="470nm LED",
        target_device="Patch Cord A",
        target_port="Fiber 0_green",
    ),
    Connection(
        source_device="415nm LED",
        target_device="Patch Cord A",
        target_port="Fiber 0_isosbestic",
    ),
    Connection(
        source_device="565nm LED",
        target_device="Patch Cord A",
        target_port="Fiber 0_red",
    ),
    # Connections between LEDs and Patch Cord B
    Connection(
        source_device="470nm LED",
        target_device="Patch Cord B",
        target_port="Fiber 1_green",
    ),
    Connection(
        source_device="415nm LED",
        target_device="Patch Cord B",
        target_port="Fiber 1_isosbestic",
    ),
]

# Define stimulus epoch's speaker configuration
speaker_config = SpeakerConfig(
    device_name="Stimulus Speaker",
    volume=Decimal("72"),
    volume_unit="decibels",
)

# Create the data stream
data_stream = DataStream(
    stream_start_time=t_start,
    stream_end_time=t_end,
    modalities=[Modality.FIB],
    active_devices=[
        "Green CMOS",
        "Red CMOS",
        "Patch Cord A",
        "Patch Cord B",
        "Patch Cord C",
        "Patch Cord D",
        "470nm LED",
        "415nm LED",
        "565nm LED",
        "IR LED",
        "Fiber 0",
        "Fiber 1",  # Add implanted fibers to active devices
    ],
    configurations=[
        green_detector_config,
        red_detector_config,
        blue_led_config,
        uv_led_config,
        yellow_led_config,
        patch_cord_a_config,
        patch_cord_b_config,
        patch_cord_c_config,
        patch_cord_d_config,
    ],
    connections=connections,  # Add the connections to the data stream
    notes=(
        "Fib modality: fib mode: Normal This record has been updated to include intended measurements. Fiber "
        "connections are repeated for fibers with multiple channels. Disconnected fibers are marked with "
        "fiber_name 'disconnected'."
    ),
)

# Create the stimulus epoch
stimulus_epoch = StimulusEpoch(
    stimulus_start_time=t_start,
    stimulus_end_time=t_end,
    stimulus_name="CS - auditory conditioned stimuli",
    stimulus_modalities=[StimulusModality.AUDITORY],
    active_devices=["Stimulus Speaker"],
    configurations=[speaker_config],
    notes="The duration of CSs is 1s. The frequency set:5kHz, 8kHz, 13kHz, WhiteNoise.",
    performance_metrics=PerformanceMetrics(
        reward_consumed_during_epoch=Decimal("414"),
        reward_consumed_unit=VolumeUnit.UL,
        trials_total=418,
        trials_finished=418,
        trials_rewarded=207,
    ),
)

# Create the acquisition object
acquisition = Acquisition(
    experimenters=[
        "Bryan MacLennan",
        "Kenta Hagihara",
    ],
    subject_id="687582",
    acquisition_start_time=t_start,
    acquisition_end_time=t_end,
    acquisition_type="PavlovianConditioning",
    instrument_id="1_FIP1",
    protocol_id=[""],
    ethics_review_id=["2115"],
    subject_details=AcquisitionSubjectDetails(
        animal_weight_prior=None,
        animal_weight_post=None,
        mouse_platform_name="mouse_tube_foraging",
        reward_consumed_total=None,
        reward_consumed_unit=None,
    ),
    data_streams=[data_stream],
    stimulus_epochs=[stimulus_epoch],
    notes="",
)


if __name__ == "__main__":
    serialized = acquisition.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="fip_ophys")
