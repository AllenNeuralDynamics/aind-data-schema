""" example fiber photometry session """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.components.tile import Channel
from aind_data_schema.core.session import DetectorConfig, FiberConnectionConfig, LaserConfig, Session, Stream

t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

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
            fiber_connections=[
                FiberConnectionConfig(
                    patch_cord_name="Patch Cord A",
                    patch_cord_output_power=40,
                    output_power_unit="microwatt",
                    fiber_name="Fiber A",
                    channel=Channel(
                        channel_name="Channel A",
                        intended_measurement="Dopamine",
                        light_source_name="Laser A",
                        filter_names=["Excitation filter 410nm"],
                        detector_name="Green CMOS",
                        excitation_wavelength=410,
                        excitation_power=20,
                        emission_wavelength=600,
                    )
                ),
                FiberConnectionConfig(
                    patch_cord_name="Patch Cord B",
                    patch_cord_output_power=43,
                    output_power_unit="microwatt",
                    fiber_name="Fiber B",
                    channel=Channel(
                        channel_name="Channel B",
                        intended_measurement="Dopamine",
                        light_source_name="Laser B",
                        filter_names=["Excitation filter 520nm"],
                        detector_name="Red CMOS",
                        excitation_wavelength=520,
                        excitation_power=50,
                        emission_wavelength=700,
                    )
                ),
            ],
            notes="Internal trigger.",
        )
    ],
)
serialized = s.model_dump_json()
deserialized = Session.model_validate_json(serialized)
deserialized.write_standard_file(prefix="ophys")
