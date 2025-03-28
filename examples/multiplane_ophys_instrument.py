"""Generates an example instrument JSON for a multiplane-ophys session"""

from datetime import date
from decimal import Decimal

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import FrequencyUnit, SizeUnit

from aind_data_schema.components.coordinates import (
    Transform,
    Affine,
    Translation,
    CoordinateSystemLibrary,
    AnatomicalRelative,
)
from aind_data_schema.components.devices import (
    BinMode,
    Camera,
    CameraAssembly,
    Cooling,
    DAQChannel,
    DaqChannelType,
    DAQDevice,
    DataInterface,
    Detector,
    Device,
    Disc,
    Filter,
    Laser,
    Lens,
    PockelsCell,
    Software,
    Monitor,
    Computer,
    Objective,
    CameraTarget,
)
from aind_data_schema.core.instrument import (
    Instrument,
    Connection,
    ConnectionData,
    ConnectionDirection,
)

monitor = Monitor(
    name="Stimulus Screen",
    manufacturer=Organization.ASUS,
    model="PA248Q",
    notes=(
        "viewing distance is from screen normal to bregma, Rotation and translation here are "
        "inaccurate, they are not in BREGMA_ARI but in FACE_XYZ for the monitor, needs to be "
        "translated",
    ),
    refresh_rate=60,
    width=1920,
    height=1200,
    size_unit="pixel",
    viewing_distance=Decimal("15.5"),
    viewing_distance_unit="centimeter",
    relative_position=[AnatomicalRelative.ANTERIOR, AnatomicalRelative.LEFT, AnatomicalRelative.SUPERIOR],
    position=Transform(
        system_name="BREGMA_ARI",
        transforms=[
            Affine(
                affine_transform=[
                    [-0.80914, -0.58761, 0, 0],
                    [-0.12391, 0.17063, 0.97751, 0],
                    [-0.5744, 0.79095, -0.21087, 0],
                    [0, 0, 0, 1],
                ]
            ),
            Translation(translation=[0.08751, -0.12079, 0.02298]),
        ],
    ),
)

connections = [
    Connection(
        device_names=["Behavior Camera", "Eye Camera", "Face Camera", "Video Monitor"],
        connection_data={
            "Behavior Camera": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "Eye Camera": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "Face Camera": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "Video Monitor": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["SYNC DAQ", "MESO1SYNC"],
        connection_data={
            "SYNC DAQ": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "MESO1SYNC": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
    Connection(
        device_names=["STIM DAQ", "VBEB DAQ", "MESO1STIM"],
        connection_data={
            "STIM DAQ": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "VBEB DAQ": ConnectionData(
                direction=ConnectionDirection.SEND,
            ),
            "MESO1STIM": ConnectionData(
                direction=ConnectionDirection.RECEIVE,
            ),
        },
    ),
]

cameras = [
    CameraAssembly(
        name="Behavior Camera Assembly",
        target=CameraTarget.BODY,
        relative_position=[AnatomicalRelative.ANTERIOR],
        camera=Camera(
            name="Behavior Camera",
            manufacturer=Organization.ALLIED,
            model="Mako G-32B",
            detector_type="Camera",
            data_interface="Ethernet",
            cooling=Cooling.NONE,
            frame_rate=Decimal("60"),
            frame_rate_unit=FrequencyUnit.HZ,
            chroma="Monochrome",
            sensor_width=658,
            sensor_height=492,
            size_unit=SizeUnit.IN,
            sensor_format="1/3",
            sensor_format_unit=SizeUnit.IN,
            bit_depth=8,
            bin_mode=BinMode.NONE,
            bin_unit=SizeUnit.PX,
            gain=Decimal("4"),
            recording_software=Software(
                name="MultiVideoRecorder",
                version="1.1.7",
            ),
            driver="Vimba",
            driver_version="Vimba GigE Transport Layer 1.6.0",
        ),
        lens=Lens(
            name="Behavior Camera Lens",
            manufacturer=Organization.THORLABS,
            model="MVL6WA",
            focal_length=Decimal("6"),
            focal_length_unit=SizeUnit.MM,
            max_aperture="f/1.4",
        ),
        filter=Filter(
            name="Behavior Camera Filter",
            manufacturer=Organization.SEMROCK,
            model="FF01-747/33-25",
            filter_type="Band pass",
            size_unit=SizeUnit.MM,
            cut_off_wavelength=780,
            cut_on_wavelength=714,
            center_wavelength=747,
            wavelength_unit=SizeUnit.NM,
        ),
        position=Transform(
            system_name="BREGMA_ARI",
            transforms=[
                Affine(
                    affine_transform=[
                        [-1, 0, 0, 0],
                        [0, 0, -1, 0],
                        [0, -3, 0, 0],
                        [0, 0, 0, 1],
                    ]
                ),
                Translation(translation=[-0.03617, 0.23887, -0.02535]),
            ],
        ),
    ),
    CameraAssembly(
        name="Eye Camera Assembly",
        target=CameraTarget.EYE,
        relative_position=[AnatomicalRelative.ANTERIOR],
        camera=Camera(
            name="Eye Camera",
            manufacturer=Organization.ALLIED,
            model="Mako G-32B",
            detector_type="Camera",
            data_interface="Ethernet",
            cooling=Cooling.NONE,
            frame_rate=Decimal("60"),
            frame_rate_unit=FrequencyUnit.HZ,
            chroma="Monochrome",
            sensor_width=658,
            sensor_height=492,
            size_unit=SizeUnit.IN,
            sensor_format="1/3",
            sensor_format_unit=SizeUnit.IN,
            bit_depth=8,
            bin_mode=BinMode.NONE,
            bin_unit=SizeUnit.PX,
            gain=Decimal("22"),
            recording_software=Software(
                name="MultiVideoRecorder",
                version="1.1.7",
            ),
            driver="Vimba",
            driver_version="Vimba GigE Transport Layer 1.6.0",
        ),
        lens=Lens(
            name="Eye Camera Lens",
            manufacturer=Organization.INFINITY_PHOTO_OPTICAL,
            model="213073",
        ),
        filter=Filter(
            name="Eye Camera Filter",
            manufacturer=Organization.SEMROCK,
            model="FF01-850/10-25",
            filter_type="Band pass",
            size_unit=SizeUnit.MM,
            cut_off_wavelength=860,
            cut_on_wavelength=840,
            center_wavelength=850,
            wavelength_unit=SizeUnit.NM,
        ),
        position=Transform(
            system_name="BREGMA_ARI",
            transforms=[
                Affine(
                    affine_transform=[
                        [-0.5, -0.86603, 0, 0],
                        [-0.366, 0.21131, -0.90631, 0],
                        [0.78489, -0.45315, -0.42262, 0],
                        [0, 0, 0, 1],
                    ]
                ),
                Translation(translation=[-0.14259, 0.06209, -0.09576]),
            ],
        ),
    ),
    CameraAssembly(
        name="Face Camera Assembly",
        target=CameraTarget.FACE,
        relative_position=[AnatomicalRelative.ANTERIOR],
        camera=Camera(
            name="Face Camera",
            manufacturer=Organization.ALLIED,
            model="Mako G-32B",
            detector_type="Camera",
            data_interface="Ethernet",
            cooling=Cooling.NONE,
            frame_rate=Decimal("60"),
            frame_rate_unit=FrequencyUnit.HZ,
            chroma="Monochrome",
            sensor_width=658,
            sensor_height=492,
            size_unit=SizeUnit.IN,
            sensor_format="1/3",
            sensor_format_unit=SizeUnit.IN,
            bit_depth=8,
            bin_mode=BinMode.NONE,
            bin_unit=SizeUnit.PX,
            gain=Decimal("13"),
            recording_software=Software(
                name="MultiVideoRecorder",
                version="1.1.7",
            ),
            driver="Vimba",
            driver_version="Vimba GigE Transport Layer 1.6.0",
        ),
        lens=Lens(
            name="Face Camera Lens",
            manufacturer=Organization.EDMUND_OPTICS,
            model="86-604",
            focal_length=Decimal("8.5"),
            focal_length_unit=SizeUnit.MM,
            max_aperture="f/8",
        ),
        filter=Filter(
            name="Face Camera Filter",
            manufacturer=Organization.SEMROCK,
            model="FF01-715/LP-25",
            filter_type="Long pass",
            size_unit=SizeUnit.MM,
            cut_on_wavelength=715,
            wavelength_unit=SizeUnit.NM,
        ),
        position=Transform(
            system_name="BREGMA_ARI",
            transforms=[
                Affine(
                    affine_transform=[
                        [-0.17365, 0.98481, 0, 0],
                        [0.44709, 0.07883, -0.89101, 0],
                        [-0.87747, -0.15472, -0.45399, 0],
                        [0, 0, 0, 1],
                    ]
                ),
                Translation(translation=[0.154, 0.03078, 0.06346]),
            ],
        ),
    ),
]


instrument = Instrument(
    instrument_id="429_mesoscope_20220321",
    modification_date=date(2024, 10, 16),
    coordinate_system=CoordinateSystemLibrary.BREGMA_ARI,
    components=[
        Disc(
            name="MindScope Running Disc",
            manufacturer=Organization.AIND,
            surface_material="Kittrich Magic Cover Solid Grip Liner",
            radius=Decimal("8.255"),
            radius_unit="centimeter",
            output="Digital Output",
            encoder="CUI Devices AMT102-V 0000 Dip Switch 2048 ppr",
            decoder="LS7366R",
            encoder_firmware=Software(
                name="ls7366r_quadrature_counter",
                version="0.1.6",
            ),
        ),
        monitor,
        *cameras,
        Laser(
            name="Axon 920-2 TPC",
            wavelength=920,
            wavelength_unit=SizeUnit.NM,
            serial_number="GDP.1007S.3490",
            manufacturer=Organization.COHERENT_SCIENTIFIC,
        ),
        Detector(
            name="H11706-40",
            detector_type="Photomultiplier Tube",
            manufacturer=Organization.HAMAMATSU,
            data_interface=DataInterface.PCIE,
        ),
        Objective(
            name="Mesoscope JenOptik Objective",
            numerical_aperture=0.8,
            magnification=3.6,
            manufacturer=Organization.THORLABS,
            immersion="water",
            notes="Part from JenOptik: 14163000",
            serial_number="110",
        ),
        PockelsCell(
            name="Pockels Cell 1",
            polygonal_scanner="",
            on_time=12.0,
            off_time=13.0,
            manufacturer=Organization.CONOPTICS,
            model="350-80",
            serial_number="354683BK",
        ),
        Computer(name="Video Monitor"),
        Computer(name="MESO1STIM"),
        Device(name="MESO1SYNC"),
        DAQDevice(
            name="VBEB DAQ",
            manufacturer=Organization.NATIONAL_INSTRUMENTS,
            model="USB-6001",
            data_interface="USB",
        ),
        DAQDevice(
            name="SYNC DAQ",
            manufacturer=Organization.NATIONAL_INSTRUMENTS,
            model="PCIe-6612",
            data_interface="PCIe",
            channels=[
                DAQChannel(
                    channel_name="P0.3",
                    channel_type=DaqChannelType.DI,
                    port=0,
                    channel_index=3,
                    sample_rate=100.0,
                    sample_rate_unit=FrequencyUnit.KHZ,
                )
            ],
        ),
        DAQDevice(
            name="STIM DAQ",
            manufacturer=Organization.NATIONAL_INSTRUMENTS,
            model="PCIe-6321",
            data_interface="PCIe",
        ),
    ],
    connections=connections,
    modalities=[Modality.POPHYS],
)

serialized = instrument.model_dump_json()
deserialized = Instrument.model_validate_json(serialized)
deserialized.write_standard_file(prefix="multiplane_ophys")
