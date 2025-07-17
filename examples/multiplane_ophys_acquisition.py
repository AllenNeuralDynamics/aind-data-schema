""" example fiber photometry acquisition """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import PowerUnit, SizeUnit, FrequencyUnit

from aind_data_schema.components.coordinates import Translation, Scale, CoordinateSystemLibrary
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    AcquisitionSubjectDetails,
)
from aind_data_schema.components.configs import (
    Channel,
    DetectorConfig,
    LaserConfig,
    TriggerType,
    ImagingConfig,
    CoupledPlane,
    PlanarImage,
    SamplingStrategy,
)
from aind_data_schema_models.brain_atlas import CCFv3

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

# Define the sampling strategy
sampling_strategy = SamplingStrategy(
    frame_rate=9.48,
    frame_rate_unit=FrequencyUnit.HZ,
)

a = Acquisition(
    experimenters=["John Smith"],
    acquisition_start_time=t,
    acquisition_end_time=t,
    subject_id="12345",
    acquisition_type="Mesoscope",
    instrument_id="MESO.1",
    ethics_review_id=["1234"],
    subject_details=AcquisitionSubjectDetails(
        mouse_platform_name="disc",
    ),
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
            active_devices=["Mesoscope", "Eye", "Face", "Behavior", "Vasculature", "Laser A", "PMT 1"],
            configurations=[
                ImagingConfig(
                    device_name="Mesoscope",
                    channels=[
                        Channel(
                            channel_name="Green channel",
                            intended_measurement="GCaMP",
                            detector=DetectorConfig(
                                device_name="PMT 1", exposure_time=0.1, trigger_type=TriggerType.INTERNAL
                            ),
                            light_sources=[
                                LaserConfig(
                                    device_name="Laser A",
                                    wavelength=920,
                                    wavelength_unit=SizeUnit.NM,
                                    power=10,
                                    power_unit=PowerUnit.MW,
                                ),
                            ],
                        ),
                    ],
                    images=[
                        PlanarImage(
                            channel_name="Green channel",
                            image_to_acquisition_transform=[
                                Translation(
                                    translation=[1500, 1500],
                                ),
                            ],
                            dimensions=Scale(
                                scale=[512, 512],
                            ),
                            planes=[
                                CoupledPlane(
                                    plane_index=0,
                                    depth=190,
                                    depth_unit=SizeUnit.UM,
                                    power=5,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=1,
                                    power_ratio=0.12,
                                ),
                                CoupledPlane(
                                    plane_index=1,
                                    depth=232,
                                    depth_unit=SizeUnit.UM,
                                    power=42,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=0,
                                    power_ratio=8.4,
                                ),
                                CoupledPlane(
                                    plane_index=2,
                                    depth=136,
                                    depth_unit=SizeUnit.UM,
                                    power=28,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=3,
                                    power_ratio=1.0,
                                ),
                                CoupledPlane(
                                    plane_index=3,
                                    depth=282,
                                    depth_unit=SizeUnit.UM,
                                    power=28,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=2,
                                    power_ratio=1.0,
                                ),
                                CoupledPlane(
                                    plane_index=4,
                                    depth=72,
                                    depth_unit=SizeUnit.UM,
                                    power=12,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=5,
                                    power_ratio=1.0,
                                ),
                                CoupledPlane(
                                    plane_index=5,
                                    depth=326,
                                    depth_unit=SizeUnit.UM,
                                    power=12,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=4,
                                    power_ratio=1.0,
                                ),
                                CoupledPlane(
                                    plane_index=6,
                                    depth=30,
                                    depth_unit=SizeUnit.UM,
                                    power=5,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=7,
                                    power_ratio=1.0,
                                ),
                                CoupledPlane(
                                    plane_index=7,
                                    depth=364,
                                    depth_unit=SizeUnit.UM,
                                    power=5,
                                    power_unit=PowerUnit.PERCENT,
                                    targeted_structure=CCFv3.VISP,
                                    coupled_plane_index=6,
                                    power_ratio=1.0,
                                ),
                            ],
                        ),
                    ],
                    sampling_strategy=sampling_strategy,
                ),
            ],
        )
    ],
)

if __name__ == "__main__":
    serialized = a.model_dump_json()
    deserialized = Acquisition.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="multiplane_ophys")
