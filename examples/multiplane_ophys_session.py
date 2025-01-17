""" example fiber photometry session """

from datetime import datetime, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.units import PowerUnit, SizeUnit

from aind_data_schema.core.session import FieldOfView, LaserConfig, Session, Stream

# If a timezone isn't specified, the timezone of the computer running this
# script will be used as default
t = datetime(2022, 7, 12, 7, 00, 00, tzinfo=timezone.utc)

s = Session(
    experimenter_full_name=["John Doe"],
    session_start_time=t,
    session_end_time=t,
    subject_id="12345",
    session_type="Mesoscope",
    iacuc_protocol="12345",
    rig_id="429_mesoscope_20220321",
    mouse_platform_name="MindScope Running Disc",
    active_mouse_platform=True,
    data_streams=[
        Stream(
            stream_start_time=t,
            stream_end_time=t,
            stream_modalities=[
                Modality.POPHYS,
                Modality.BEHAVIOR_VIDEOS,
            ],
            daq_names=["NI PCIe-6612", "NI PCIe-6321", "NI USB-6001", "NI OEM-6001"],
            camera_names=[
                "Behavior Camera",
                "Eye Camera",
                "Face Camera",
            ],
            light_sources=[
                LaserConfig(
                    name="Axon 920-2 TPC",
                    wavelength=920,
                    wavelength_unit="nanometer",
                    excitation_power=10,
                    excitation_power_unit="milliwatt",
                ),
            ],
            ophys_fovs=[
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
                    power=5,
                    power_unit=PowerUnit.PERCENT,
                    scanimage_roi_index=0,
                    imaging_depth=190,
                    targeted_structure="VISp",
                    scanfield_z=230,
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
                    power=42,
                    scanimage_roi_index=0,
                    imaging_depth=232,
                    targeted_structure="VISp",
                    scanfield_z=257,
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
                    power=28,
                    scanimage_roi_index=0,
                    imaging_depth=136,
                    targeted_structure="VISp",
                    scanfield_z=176,
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
                    power=28,
                    scanimage_roi_index=0,
                    imaging_depth=282,
                    targeted_structure="VISp",
                    scanfield_z=307,
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
                    power=12,
                    scanimage_roi_index=0,
                    imaging_depth=72,
                    targeted_structure="VISp",
                    scanfield_z=112,
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
                    power=12,
                    scanimage_roi_index=0,
                    imaging_depth=326,
                    targeted_structure="VISp",
                    scanfield_z=351,
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
                    power=5,
                    scanimage_roi_index=0,
                    imaging_depth=30,
                    targeted_structure="VISp",
                    scanfield_z=70,
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
                    power=5,
                    scanimage_roi_index=0,
                    imaging_depth=364,
                    targeted_structure="VISp",
                    scanfield_z=389,
                    coupled_fov_index=6,
                ),
            ],
        )
    ],
)
serialized = s.model_dump_json()
deserialized = Session.model_validate_json(serialized)
deserialized.write_standard_file(prefix="multiplane_ophys")
