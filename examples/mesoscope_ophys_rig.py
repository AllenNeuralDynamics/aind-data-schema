from datetime import date
from decimal import Decimal

from aind_data_schema.core.rig import (
    Rig, 
    Monitor
)
from aind_data_schema.core.instrument import DAQDevice
from aind_data_schema.models.organizations import (
    AllenInstitute, 
    Asus,
    Allied,
    Thorlabs,
    Semrock,
    InfinityPhotoOptical,
    EdmundOptics,
    NationalInstruments
)
from aind_data_schema.models.devices import (
    Camera,
    CameraAssembly,
    Disc,
    Software,
    Lens,
    Filter,
    Cooling,
    BinMode
)
from aind_data_schema.models.coordinates import (
    RelativePosition,
    Rotation3dTransform,
    Translation3dTransform,
    Axis
)
from aind_data_schema.models.units import (
    SizeUnit,
    FrequencyUnit
)
from aind_data_schema.models.registry import ResearchOrganizationRegistry
from aind_data_schema.base import AindGeneric 


rig = Rig(
        describedBy='https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/core/rig.py', 
        schema_version='0.3.3', 
        rig_id='MESO.2', 
        modification_date=date(2024, 4, 2), 
        mouse_platform=Disc(
            device_type='Disc', 
            name='MindScope Running Disk', 
            serial_number=None, 
            manufacturer=AllenInstitute(
                name='Allen Institute', 
                abbreviation='AI', 
                registry=ResearchOrganizationRegistry(
                    name='Research Organization Registry', 
                    abbreviation='ROR'), 
                    registry_identifier='03cpe7c52'), 
                    model=None, 
                    path_to_cad=None, 
                    port_index=None, 
                    additional_settings=AindGeneric(), 
                    notes=None, 
                    surface_material='Kittrich Magic Cover Solid Grip Liner', 
                    date_surface_replaced=None, 
                    radius=Decimal(
                        '8.255'
                        ), 
                    radius_unit='centimeter', 
                    output='Digital Output', 
                    encoder='CUI Devices AMT102-V 0000 Dip Switch 2048 ppr', 
                    decoder='LS7366R', 
                    encoder_firmware=Software(
                        name='ls7366r_quadrature_counter', 
                        version='0.1.6', 
                        url='https://eng-gitlab/hardware/ls7366r_quadrature_counter', 
                        parameters=AindGeneric()
                        )
                    ), 
                    stimulus_devices=[
                        Monitor(
                            device_type='Monitor', 
                            name='Stimulus Screen', 
                            serial_number=None, 
                            manufacturer=Asus(
                                name='ASUS', 
                                abbreviation=None, 
                                registry=ResearchOrganizationRegistry(
                                    name='Research Organization Registry', 
                                    abbreviation='ROR'), 
                                    registry_identifier='00bxkz165'
                                    ), 
                                model='PA248Q', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes='viewing distance is from screen normal to bregma', 
                                refresh_rate=60, 
                                width=1920, 
                                height=1200, 
                                size_unit='pixel', 
                                viewing_distance=Decimal('15.5'), 
                                viewing_distance_unit='centimeter', 
                                position=RelativePosition(
                                    device_position_transformations=[
                                        Rotation3dTransform(
                                            type='rotation', 
                                            rotation=[
                                                Decimal('-0.80914'), 
                                                Decimal('-0.58761'), 
                                                Decimal('0'), 
                                                Decimal('-0.12391'), 
                                                Decimal('0.17063'), 
                                                Decimal('0.97751'), 
                                                Decimal('-0.5744'), 
                                                Decimal('0.79095'), 
                                                Decimal('-0.21087')
                                                ]
                                            ), 
                                            Translation3dTransform(
                                                type='translation', 
                                                translation=[
                                                    Decimal('0.08751'), 
                                                    Decimal('-0.12079'), 
                                                    Decimal('0.02298')
                                                    ]
                                                )], 
                                                device_origin='Center of Screen on Face', 
                                                device_axes=[
                                                    Axis(
                                                        name='Z', 
                                                        direction='Away from screen'
                                                    ), 
                                                    Axis(
                                                        name='Y', 
                                                        direction='Pointing to the top of the screen'
                                                    ), 
                                                    Axis(
                                                        name='X', 
                                                        direction='Oriented parallel to the long edge of the screen'
                                                    )
                                                ], 
                                                notes=None
                                                ), 
                                            contrast=None, 
                                            brightness=None
                                        )
                        ], 
                    cameras=[
                        CameraAssembly(
                            name='Behavior Camera', 
                            camera_target='Body', 
                            camera=Camera(
                                device_type='Detector', 
                                name='Behavior Camera', 
                                serial_number=None, 
                                manufacturer=Allied(
                                    name='Allied', 
                                    abbreviation=None, 
                                    registry=None, 
                                    registry_identifier=None
                                    ), 
                                model='Mako G-32B', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, 
                                detector_type='Camera', 
                                data_interface='Ethernet', 
                                cooling=Cooling.NONE, 
                                computer_name='Video Monitor', 
                                max_frame_rate=Decimal('60'),
                                frame_rate_unit=FrequencyUnit.HZ, 
                                immersion=None, 
                                chroma='Monochrome', 
                                sensor_width=658, 
                                sensor_height=492, 
                                size_unit=SizeUnit.IN, 
                                sensor_format='1/3', 
                                sensor_format_unit=SizeUnit.IN, 
                                bit_depth=8, 
                                bin_mode=BinMode.NONE, 
                                bin_width=None, 
                                bin_height=None, 
                                bin_unit=SizeUnit.PX, 
                                gain=Decimal('4'), 
                                crop_width=None, 
                                crop_height=None, 
                                crop_unit=SizeUnit.PX, 
                                recording_software=Software(
                                    name='MultiVideoRecorder', 
                                    version='1.1.7', 
                                    url=None, 
                                    parameters=AindGeneric()
                                    ), 
                                driver='Vimba', 
                                driver_version='Vimba GigE Transport Layer 1.6.0',
                            ),
                            lens=Lens(
                                device_type='Lens', 
                                name='Behavior Camera Lens', 
                                serial_number=None, 
                                manufacturer=Thorlabs(
                                    name='Thorlabs', 
                                    abbreviation=None, 
                                    registry=ResearchOrganizationRegistry(
                                        name='Research Organization Registry', 
                                        abbreviation='ROR'
                                        ), 
                                    registry_identifier='04gsnvb07'
                                    ), 
                                model='MVL6WA', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, 
                                focal_length=Decimal('6'), 
                                focal_length_unit=SizeUnit.MM, 
                                size=None, 
                                lens_size_unit=SizeUnit.IN, 
                                optimized_wavelength_range=None, 
                                wavelength_unit=SizeUnit.NM, 
                                max_aperture='f/1.4'
                                ), 
                            filter=Filter(
                                device_type='Filter', 
                                name='Behavior Camera Filter', 
                                serial_number=None, 
                                manufacturer=Semrock(
                                    name='Semrock', 
                                    abbreviation=None, 
                                    registry=None, 
                                    registry_identifier=None
                                    ), 
                                model='FF01-747/33-25', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, 
                                filter_type='Band pass', 
                                diameter=None, 
                                width=None, 
                                height=None, 
                                size_unit=SizeUnit.MM, 
                                thickness=None, 
                                thickness_unit=SizeUnit.MM, 
                                filter_wheel_index=None, 
                                cut_off_wavelength=780, 
                                cut_on_wavelength=714, 
                                center_wavelength=747, 
                                wavelength_unit=SizeUnit.NM, 
                                description=None
                                ), 
                            position=RelativePosition(
                                device_position_transformations=[
                                    Rotation3dTransform(
                                        type='rotation', 
                                        rotation=[
                                            Decimal('-1'), 
                                            Decimal('0'), 
                                            Decimal('0'), 
                                            Decimal('0'), 
                                            Decimal('0'), 
                                            Decimal('-1'), 
                                            Decimal('0'), 
                                            Decimal('-3'), 
                                            Decimal('0')
                                            ]
                                        ), 
                                    Translation3dTransform(
                                        type='translation', 
                                        translation=[
                                            Decimal('-0.03617'), 
                                            Decimal('0.23887'), 
                                            Decimal('-0.02535')
                                            ]
                                        )
                                    ], 
                            device_origin='Located on face of the lens mounting surface in its center', 
                            device_axes=[
                                Axis(
                                    name='Z', 
                                    direction='moving away from the sensor towards the object'
                                    ), 
                                Axis(
                                    name='Y', 
                                    direction='pointing to the bottom edge of the sensor'
                                    ), 
                                Axis(
                                    name='X', 
                                    direction='parallel to the bottom edge of the sensor'
                                    )
                                ], 
                            notes=None
                            )
                        ), 
                        CameraAssembly(
                            name='Eye Camera', 
                            camera_target='Eye', 
                            camera=Camera(
                                device_type='Detector', 
                                name='Eye Camera', 
                                serial_number=None, 
                                manufacturer=Allied(
                                    name='Allied', 
                                    abbreviation=None, 
                                    registry=None, 
                                    registry_identifier=None
                                    ), 
                                model='Mako G-32B', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, 
                                detector_type='Camera', 
                                data_interface='Ethernet', 
                                cooling=Cooling.NONE, 
                                computer_name='Video Monitor', 
                                max_frame_rate=Decimal('60'), 
                                frame_rate_unit=FrequencyUnit.HZ, 
                                immersion=None, 
                                chroma='Monochrome', 
                                sensor_width=658, 
                                sensor_height=492, 
                                size_unit=SizeUnit.IN, 
                                sensor_format='1/3', 
                                sensor_format_unit=SizeUnit.IN, 
                                bit_depth=8, 
                                bin_mode=BinMode.NONE, 
                                bin_width=None, 
                                bin_height=None, 
                                bin_unit=SizeUnit.PX, 
                                gain=Decimal('4'), 
                                crop_width=None, 
                                crop_height=None, 
                                crop_unit=SizeUnit.PX, 
                                recording_software=Software(
                                    name='MultiVideoRecorder', 
                                    version='1.1.7', 
                                    url=None, 
                                    parameters=AindGeneric()
                                    ), 
                                driver='Vimba', 
                                driver_version='Vimba GigE Transport Layer 1.6.0'
                            ),
                            lens=Lens(
                                device_type='Lens', 
                                name='Eye Camera Lens', 
                                serial_number=None, 
                                manufacturer=InfinityPhotoOptical(
                                    name='Infinity Photo-Optical', 
                                    abbreviation=None, 
                                    registry=None, 
                                    registry_identifier=None
                                    ), 
                                model='213073', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, focal_length=None, 
                                focal_length_unit=SizeUnit.MM, 
                                size=None, 
                                lens_size_unit=SizeUnit.IN, 
                                optimized_wavelength_range=None, 
                                wavelength_unit=SizeUnit.NM, 
                                max_aperture=None
                                ), 
                                filter=Filter(
                                    device_type='Filter', 
                                    name='Eye Camera Filter', 
                                    serial_number=None, 
                                    manufacturer=Semrock(
                                        name='Semrock', 
                                        abbreviation=None, 
                                        registry=None, 
                                        registry_identifier=None
                                        ), 
                                    model='FF01-850/10-25', 
                                    path_to_cad=None, 
                                    port_index=None, 
                                    additional_settings=AindGeneric(), 
                                    notes=None, 
                                    filter_type='Band pass', 
                                    diameter=None, 
                                    width=None, 
                                    height=None, 
                                    size_unit=SizeUnit.MM, 
                                    thickness=None, 
                                    thickness_unit=SizeUnit.MM, 
                                    filter_wheel_index=None, 
                                    cut_off_wavelength=860, 
                                    cut_on_wavelength=840, 
                                    center_wavelength=850, 
                                    wavelength_unit=SizeUnit.NM, 
                                    description=None
                                    ), 
                                position=RelativePosition(
                                    device_position_transformations=[
                                        Rotation3dTransform(
                                            type='rotation', 
                                            rotation=[
                                                Decimal('-0.5'), 
                                                Decimal('-0.86603'), 
                                                Decimal('0'), 
                                                Decimal('-0.366'), 
                                                Decimal('0.21131'), 
                                                Decimal('-0.90631'), 
                                                Decimal('0.78489'), 
                                                Decimal('-0.45315'), 
                                                Decimal('-0.42262')
                                                ]
                                            ), 
                                        Translation3dTransform(
                                            type='translation', 
                                            translation=[
                                                Decimal('-0.14259'), 
                                                Decimal('0.06209'), 
                                                Decimal('-0.09576')
                                                ]
                                            )
                                        ], 
                                    device_origin='Located on face of the lens mounting surface in its center', 
                                    device_axes=[
                                        Axis(
                                            name='Z', 
                                            direction='moving away from the sensor towards the object'
                                            ), 
                                        Axis(
                                            name='Y', 
                                            direction='pointing to the bottom edge of the sensor'
                                            ), 
                                        Axis(
                                            name='X', 
                                            direction='parallel to the bottom edge of the sensor'
                                            )
                                        ], 
                                    notes=None
                                )
                                ), 
                        CameraAssembly(
                            name='Face Camera', 
                            camera_target='Face forward', 
                            camera=Camera(
                                device_type='Detector', 
                                name='Face Camera', 
                                serial_number=None, 
                                manufacturer=Allied(
                                    name='Allied', 
                                    abbreviation=None, 
                                    registry=None, 
                                    registry_identifier=None
                                    ), 
                                model='Mako G-32B', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, 
                                detector_type='Camera', 
                                data_interface='Ethernet', 
                                cooling=Cooling.NONE, 
                                computer_name='Video Monitor', 
                                max_frame_rate=Decimal('60'), 
                                frame_rate_unit=FrequencyUnit.HZ, 
                                immersion=None, 
                                chroma='Monochrome', 
                                sensor_width=658, 
                                sensor_height=492, 
                                size_unit=SizeUnit.IN, 
                                sensor_format='1/3', 
                                sensor_format_unit=SizeUnit.IN, 
                                bit_depth=8, 
                                bin_mode=BinMode.NONE, 
                                bin_width=None, 
                                bin_height=None, 
                                bin_unit=SizeUnit.PX, 
                                gain=Decimal('4'), 
                                crop_width=None, 
                                crop_height=None, 
                                crop_unit=SizeUnit.PX, 
                                recording_software=Software(
                                    name='MultiVideoRecorder', 
                                    version='1.1.7', 
                                    url=None, 
                                    parameters=AindGeneric()), 
                                    driver='Vimba', 
                                    driver_version='Vimba GigE Transport Layer 1.6.0'), 
                                    lens=Lens(
                                        device_type='Lens', 
                                        name='Face Camera Lens', 
                                        serial_number=None, 
                                        manufacturer=EdmundOptics(
                                            name='Edmund Optics', 
                                            abbreviation=None, 
                                            registry=ResearchOrganizationRegistry(
                                                name='Research Organization Registry', 
                                                abbreviation='ROR'
                                                ), 
                                            registry_identifier='01j1gwp17'
                                            ), 
                                        model='86-604', 
                                        path_to_cad=None, 
                                        port_index=None, 
                                        additional_settings=AindGeneric(), 
                                        notes=None, 
                                        focal_length=Decimal('8.5'), 
                                        focal_length_unit=SizeUnit.MM, 
                                        size=None, 
                                        lens_size_unit=SizeUnit.IN, 
                                        optimized_wavelength_range=None, 
                                        wavelength_unit=SizeUnit.NM, max_aperture='f/8'), 
                                        filter=Filter(
                                            device_type='Filter', 
                                            name='Face Camera Filter', 
                                            serial_number=None, 
                                            manufacturer=Semrock(
                                                name='Semrock', 
                                                abbreviation=None, 
                                                registry=None, 
                                                registry_identifier=None
                                                ), 
                                            model='FF01-715/LP-25', 
                                            path_to_cad=None, 
                                            port_index=None, 
                                            additional_settings=AindGeneric(), 
                                            notes=None, 
                                            filter_type='Long pass', 
                                            diameter=None, 
                                            width=None, 
                                            height=None, 
                                            size_unit=SizeUnit.MM, 
                                            thickness=None, 
                                            thickness_unit=SizeUnit.MM, 
                                            filter_wheel_index=None, 
                                            cut_off_wavelength=None, 
                                            cut_on_wavelength=715, 
                                            center_wavelength=None, 
                                            wavelength_unit=SizeUnit.NM, 
                                            description=None
                                        ), 
                                position=RelativePosition(
                                    device_position_transformations=[
                                        Rotation3dTransform(
                                            type='rotation', 
                                            rotation=[
                                                Decimal('-0.17365'), 
                                                Decimal('0.98481'), 
                                                Decimal('0'), 
                                                Decimal('0.44709'), 
                                                Decimal('0.07883'), 
                                                Decimal('-0.89101'), 
                                                Decimal('-0.87747'), 
                                                Decimal('-0.15472'), 
                                                Decimal('-0.45399')
                                                ]
                                            ), 
                                        Translation3dTransform(
                                            type='translation', 
                                            translation=[
                                                Decimal('0.154'), 
                                                Decimal('0.03078'), 
                                                Decimal('0.06346')
                                                ]
                                            )
                                        ], 
                                    device_origin='Located on face of the lens mounting surface in its center', 
                                    device_axes=[
                                        Axis(
                                            name='Z', 
                                            direction='moving away from the sensor towards the object'
                                            ), 
                                        Axis(
                                            name='Y', 
                                            direction='pointing to the bottom edge of the sensor'
                                            ), 
                                        Axis(
                                            name='X', 
                                            direction='parallel to the bottom edge of the sensor'
                                            )
                                        ], 
                                    notes=None
                                    )
                                )
                            ], 
                    enclosure=None, 
                    ephys_assemblies=[], 
                    fiber_assemblies=[], 
                    stick_microscopes=[], 
                    laser_assemblies=[], 
                    patch_cords=[], 
                    light_sources=[], 
                    detectors=[], 
                    objectives=[], 
                    filters=[], 
                    lenses=[], 
                    digital_micromirror_devices=[], 
                    polygonal_scanners=[], 
                    pockels_cells=[], 
                    additional_devices=[], 
                    daqs=[
                        DAQDevice(
                            device_type='DAQ Device', 
                            name='VBEB DAQ', 
                            serial_number=None, 
                            manufacturer=NationalInstruments(
                                name='National Instruments', 
                                abbreviation=None, 
                                registry=ResearchOrganizationRegistry(
                                    name='Research Organization Registry', 
                                    abbreviation='ROR'), 
                                    registry_identifier='026exqw73'
                                    ), 
                                model='USB-6001', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, 
                                data_interface='USB', 
                                computer_name='STIM', 
                                channels=[], 
                                firmware_version=None, 
                                hardware_version=None
                            ), 
                        DAQDevice(
                            device_type='DAQ Device', 
                            name='SYNC DAQ', 
                            serial_number=None, 
                            manufacturer=NationalInstruments(
                                name='National Instruments', 
                                abbreviation=None, 
                                registry=ResearchOrganizationRegistry(
                                    name='Research Organization Registry', 
                                    abbreviation='ROR'), 
                                    registry_identifier='026exqw73'
                                ), model='PCIe-6612', 
                                path_to_cad=None, 
                                port_index=None, 
                                additional_settings=AindGeneric(), 
                                notes=None, 
                                data_interface='PCIe', 
                                computer_name='SYNC', 
                                channels=[], 
                                firmware_version=None, 
                                hardware_version=None
                            ), 
                        DAQDevice(
                            device_type='DAQ Device', 
                            name='STIM DAQ', 
                            serial_number=None, 
                            manufacturer=NationalInstruments(
                                name='National Instruments', 
                                abbreviation=None, 
                                registry=ResearchOrganizationRegistry(
                                    name='Research Organization Registry', 
                                    abbreviation='ROR'
                                    ), 
                                registry_identifier='026exqw73'
                            ), 
                            model='PCIe-6321', 
                            path_to_cad=None, 
                            port_index=None, 
                            additional_settings=AindGeneric(), 
                            notes=None, 
                            data_interface='PCIe', 
                            computer_name='STIM', 
                            channels=[], 
                            firmware_version=None, 
                            hardware_version=None
                        )
                    ], 
                    calibrations=[], 
                    ccf_coordinate_transform=None, 
                    origin='Bregma', 
                    rig_axes=[
                        Axis(
                            name='X', 
                            direction='lays on the Mouse Sagittal Plane, Positive direction is towards the nose of the mouse'
                            ), 
                        Axis(
                            name='Z', 
                            direction='positive pointing UP opposite the direction from the force of gravity'
                            ), 
                        Axis(
                            name='Y', 
                            direction='defined by the right hand rule and the other two axis'
                            )
                        ], 
                    modalities=set(), 
                    notes=None
            )

serialized = rig.model_dump_json()
deserialized = Rig.model_validate_json(serialized)
deserialized.write_standard_file(prefix="mesoscope_ophys")