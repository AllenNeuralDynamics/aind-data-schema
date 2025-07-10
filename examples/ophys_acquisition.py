""" example fiber photometry acquisition """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality

from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    AcquisitionSubjectDetails,
)
from aind_data_schema.components.connections import Connection, ConnectionData, ConnectionDirection
from aind_data_schema.components.configs import Channel, DetectorConfig, PatchCordConfig, LaserConfig

t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

connections = [
    Connection(
        device_names=["Patch Cord A", "Fiber A"],
        connection_data={
            "Patch Cord A": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "Fiber A": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
        },
    ),
    Connection(
        device_names=["Patch Cord A", "Hamamatsu Camera"],
        connection_data={
            "Patch Cord A": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "Hamamatsu Camera": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["Patch Cord B", "Fiber B"],
        connection_data={
            "Patch Cord B": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
            "Fiber B": ConnectionData(
                direction=ConnectionDirection.SEND,
                port="ROI 0",
            ),
        },
    ),
    Connection(
        device_names=["Patch Cord B", "Hamamatsu Camera"],
        connection_data={
            "Patch Cord B": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "Hamamatsu Camera": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
                port="ROI 1",
            ),
        },
    ),
]

a = Acquisition(
    experimenters=["Scientist Smith"],
    acquisition_start_time=t,
    acquisition_end_time=t,
    subject_id="652567",
    acquisition_type="Parameter Testing",
    instrument_id="FIP1",
    ethics_review_id=["2115"],
    subject_details=AcquisitionSubjectDetails(
        mouse_platform_name="mouse_disc",
    ),
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.FIB],
            active_devices=[
                "Laser A",
                "Laser B",
                "Hamamatsu Camera",
                "Patch Cord A",
                "Patch Cord B",
            ],
            configurations=[
                LaserConfig(
                    device_name="Laser A",
                    wavelength=405,
                    wavelength_unit="nanometer",
                    power=10,
                    power_unit="milliwatt",
                ),
                PatchCordConfig(
                    device_name="Patch Cord A",
                    channels=[
                        Channel(
                            channel_name="Channel A",
                            intended_measurement="Dopamine",
                            detector=DetectorConfig(
                                device_name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal"
                            ),
                            light_sources=[
                                LaserConfig(
                                    device_name="Laser A",
                                    wavelength=405,
                                    wavelength_unit="nanometer",
                                    power=10,
                                    power_unit="milliwatt",
                                ),
                            ],
                        ),
                    ],
                ),
                PatchCordConfig(
                    device_name="Patch Cord B",
                    channels=[
                        Channel(
                            channel_name="Channel B",
                            intended_measurement="GCaMP",
                            detector=DetectorConfig(
                                device_name="Hamamatsu Camera", exposure_time=10, trigger_type="Internal"
                            ),
                            light_sources=[
                                LaserConfig(
                                    device_name="Laser B",
                                    wavelength=473,
                                    wavelength_unit="nanometer",
                                    power=7,
                                    power_unit="milliwatt",
                                ),
                            ],
                        )
                    ],
                ),
            ],
        )
    ],
)

if __name__ == "__main__":
    serialized = a.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="ophys")
