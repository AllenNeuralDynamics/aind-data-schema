""" example fiber photometry session """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema.components.coordinates import Coordinates3d
from aind_data_schema.core.session import DetectorConfig, FiberConnectionConfig, LaserConfig, Session, Stream, FiberModule, StimulusEpoch, StimulusModality

t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

fiber_coordinates = Coordinates3d(x=30.5, y=70, z=180)
stimulus_epoch = StimulusEpoch(
    stimulus_start_time=t,
    stimulus_end_time=t,
    stimulus_name="Some Stimulus Name",
    stimulus_modalities=[StimulusModality.AUDITORY],
    stimulus_device_names=["Stimulus Device A", "Stimulus Device B"]
)

s = Session(
    experimenter_full_name=["John Doe"],
    session_start_time=t,
    session_end_time=t,
    subject_id="652567",
    session_type="Parameter Testing",
    iacuc_protocol="2115",
    rig_id="ophys_rig",
    mouse_platform_name="Disc",
    active_mouse_platform=False,
    data_streams=[
        Stream(
            stream_start_time=t,
            stream_end_time=t,
            stream_modalities=[Modality.FIB],
            light_sources=[
                LaserConfig(
                    name="Laser A",
                    wavelength=405,
                    wavelength_unit="nanometer",
                    excitation_power=10,
                    excitation_power_unit="milliwatt",
                ),
                LaserConfig(
                    name="Laser B",
                    wavelength=473,
                    wavelength_unit="nanometer",
                    excitation_power=7,
                    excitation_power_unit="milliwatt",
                ),
            ],
            detectors=[DetectorConfig(name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal")],
            fiber_modules=[
                FiberModule(
                    assembly_name="Fiber Module A",
                    arc_angle=30,
                    module_angle=180,
                    primary_targeted_structure="Structure A",
                    manipulator_coordinates=fiber_coordinates,
                )
            ],
            fiber_connections=[
                FiberConnectionConfig(
                    patch_cord_name="Patch Cord A",
                    patch_cord_output_power=40,
                    output_power_unit="microwatt",
                    fiber_name="Fiber A",
                ),
                FiberConnectionConfig(
                    patch_cord_name="Patch Cord B",
                    patch_cord_output_power=43,
                    output_power_unit="microwatt",
                    fiber_name="Fiber B",
                ),
            ],
            notes="Internal trigger. GRAB-DA2m shows signal. Unclear about GRAB-rAC",
        )
    ],
    stimulus_epochs=[stimulus_epoch]
)
