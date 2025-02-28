""" example fiber photometry session """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import PowerUnit, SizeUnit, FrequencyUnit

from aind_data_schema.components.identifiers import Person
from aind_data_schema.core.acquisition import (
    Acquisition,
    DataStream,
    SubjectDetails,
)
from aind_data_schema.components.configs import FieldOfView, LaserConfig
from aind_data_schema_models.brain_atlas import CCFStructure

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

a = Acquisition(
    experimenters=[Person(name="John Smith")],
    acquisition_start_time=t,
    acquisition_end_time=t,
    subject_id="12345",
    acquisition_type="Mesoscope",
    instrument_id="MESO.1",
    ethics_review_id="12345",
    subject_details=SubjectDetails(
        mouse_platform_name="disc",
    ),
    data_streams=[
        DataStream(
            stream_start_time=t,
            stream_end_time=t,
            modalities=[Modality.POPHYS, Modality.BEHAVIOR_VIDEOS],
            active_devices=[
                "Mesoscope",
                "Eye",
                "Face",
                "Behavior",
                "Vasculature",
                "Laser A",
            ],
            configurations=[
                LaserConfig(
                    device_name="Laser A",
                    wavelength=920,
                    wavelength_unit="nanometer",
                    excitation_power=10,
                    excitation_power_unit=PowerUnit.MW,
                ),
                FieldOfView(
                    index=0,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=5,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=190,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=230,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=1,
                ),
                FieldOfView(
                    index=1,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=42,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=232,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=257,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=0,
                ),
                FieldOfView(
                    index=2,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=28,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=136,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=176,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=3,
                ),
                FieldOfView(
                    index=3,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=28,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=282,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=307,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=2,
                ),
                FieldOfView(
                    index=4,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=12,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=72,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=112,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=5,
                ),
                FieldOfView(
                    index=5,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=12,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=326,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=351,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=4,
                ),
                FieldOfView(
                    index=6,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=5,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=30,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=70,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=7,
                ),
                FieldOfView(
                    index=7,
                    fov_coordinate_ml=1.5,
                    fov_coordinate_ap=1.5,
                    fov_coordinate_unit=SizeUnit.UM,
                    fov_reference="Bregma",
                    fov_width=512,
                    fov_height=512,
                    fov_size_unit=SizeUnit.UM,
                    magnification="10x",
                    fov_scale_factor=0.78,
                    frame_rate=9.48,
                    frame_rate_unit=FrequencyUnit.HZ,
                    power=5,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=364,
                    targeted_structure=CCFStructure.VISP,
                    scanfield_z=389,
                    scanfield_z_unit=SizeUnit.UM,
                    coupled_fov_index=6,
                ),
            ],
        )
    ],
)
serialized = a.model_dump_json()
deserialized = Acquisition.model_validate_json(serialized)
deserialized.write_standard_file(prefix="multiplane_ophys")
