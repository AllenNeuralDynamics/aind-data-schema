import aind_data_schema.ophys.ophys_rig as ophr
import aind_data_schema.device as d

r = ophr.OphysRig(
    rig_id="347_FIP1_1",
    patch_cords=[
        ophr.Patch(
            name="Bundle Branching Fiber-optic Patch Cord",
            manufacturer=d.Manufacturer.DORIC,
            model="BBP(4)_200/220/900-0.37_Custom_FCM-4xMF1.25",
            core_diameter=200,
            numerical_aperture=0.37
        )
    ],
    light_sources=[
        d.LightEmittingDiode(
            name="470nm LED",
            manufacturer=d.Manufacturer.THORLABS,
            model="M470F3",
            wavelength=470
        ),
        d.LightEmittingDiode(
            name="415nm LED",
            manufacturer=d.Manufacturer.THORLABS,
            model="M415F3",
            wavelength=415
        ),
        d.LightEmittingDiode(
            name="565nm LED",
            manufacturer=d.Manufacturer.THORLABS,
            model="M565F3",
            wavelength=415
        ),
    ],
    detectors=[
        ophr.Detector(
            name="FLIR CMOS for Green Channel",
            serial_number="21396991",
            manufacturer=d.Manufacturer.FLIR,
            model="BFS-U3-20S40M",
            notes="4*4 binning (additive), 200*200pixels, Mono16, Gain2",
            detector_type="Camera",
            data_interface="USB",
            cooling="air",
            immersion="air"
        ),
        ophr.Detector(
            name="FLIR CMOS for Red Channel",
            serial_number="21396991",
            manufacturer=d.Manufacturer.FLIR,
            model="BFS-U3-20S40M",
            notes="4*4 binning (additive), 200*200pixels, Mono16, Gain2",
            detector_type="Camera",
            data_interface="USB",
            cooling="air",
            immersion="air"
        )
    ],
    objectives=[
        ophr.Objective(
            name="Nikon 10x Objective",
            serial_number="128022336",
            manufacturer=d.Manufacturer.NIKON,
            model="CFI Plan Apochromat Lambda D 10x",
            numerical_aperture=0.45,
            magnification=10,
            immersion="air"
        )
    ],
    filters=[
        d.Filter(
            name="Green emission bandpass filter",
            manufacturer=d.Manufacturer.SEMROCK,
            model="FF01-520/35-25",
            filter_type="Band pass",
            center_wavelength=520,
            diameter=25
        ),
        d.Filter(
            name="Red emission bandpass filter",
            manufacturer=d.Manufacturer.SEMROCK,
            model="FF01-600/37-25",
            filter_type="Band pass",
            center_wavelength=600,
            diameter=25
        ),
        d.Filter(
            name="Emission Dichroic",
            model="FF562-Di03-25x36",
            manufacturer=d.Manufacturer.SEMROCK,
            filter_type="Dichroic",
            height=25,
            width=36,
            cut_off_wavelength=562
        ),
        d.Filter(
            name="dual-edge standard epi-fluorescence dichroic beamsplitter",
            model="FF493/574-Di01-25x36",
            manufacturer=d.Manufacturer.SEMROCK,
            notes="493/574 nm BrightLine® dual-edge standard epi-fluorescence dichroic beamsplitter",
            filter_type="Multiband",
            width=36,
            height=24
        ),
        d.Filter(
            name="Excitation filter 410nm",
            manufacturer=d.Manufacturer.THORLABS,
            model="FB410-10",
            filter_type="Band pass",
            diameter=25,
            center_wavelength=410
        ),
        d.Filter(
            name="Excitation filter 470nm",
            manufacturer=d.Manufacturer.THORLABS,
            model="FB470-10",
            filter_type="Band pass",
            center_wavelength=470,
            diameter=25
        ),
        d.Filter(
            name="Excitation filter 560nm",
            manufacturer=d.Manufacturer.THORLABS,
            model="FB560-10",
            filter_type="Band pass",
            diameter=25,
            center_wavelength=560
        ),
        d.Filter(
            name="450nm, 25.2 x 35.6mm, Dichroic Longpass Filter",
            manufacturer=d.Manufacturer.EDMUND_OPTICS,            
            model="#69-898",
            filter_type="Dichroic",
            cut_off_wavelength=450,
            width=35.6,
            height=25.2
        ),
        d.Filter(
            name="500nm, 25.2 x 35.6mm, Dichroic Longpass Filter",
            manufacturer=d.Manufacturer.EDMUND_OPTICS,            
            model="#69-899",
            filter_type="Dichroic",
            width=35.6,
            height=23.2
        )
    ],
    lenses=[
        d.Lens(
            manufacturer=d.Manufacturer.THORLABS,
            model="AC254-080-A-ML",
            name="Image focusing lens",
            focal_length=80,
            size=1
        )
    ],
    daqs=[
        d.DAQDevice(
            name="USB DAQ",
            manufacturer=d.Manufacturer.NATIONAL_INSTRUMENTS,
            model="USB-6212",
            notes="To record behavior events and licks via AnalogInput node in Bonsai",
            data_interface="USB",
            computer_name="W10DTJK7N0M3",
            channels=[
                d.DAQChannel(
                    event_based_sampling=False,
                    channel_name="AI0",
                    device_name="Bpod DO",
                    channel_type="Analog Input",
                    port=0,
                    channel_index=0,
                    sample_rate=1000
                ),
                d.DAQChannel(
                    event_based_sampling=False,
                    channel_name="AI1",
                    device_name="Janelia lick-o-meter circuit board, Left",
                    channel_type="Analog Input",
                    port=1,
                    channel_index=1,
                    sample_rate=1000
                ),
                d.DAQChannel(
                    event_based_sampling=False,
                    channel_name="AI2",
                    device_name="Janelia lick-o-meter circuit board, Right",
                    channel_type="Analog Input",
                    port=2,
                    channel_index=2,
                    sample_rate= 1000
                )
            ]
        )
    ],
    mouse_platform=d.Tube(
        diameter=5,
        name="Mouse Tube for Dynamic Foraging"
    )
)

r.write_standard_file()
