"""Example BarSEQ instrument schema"""

from datetime import date

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import SizeUnit

from aind_data_schema.components.coordinates import CoordinateSystemLibrary
from aind_data_schema.components.devices import (
    Camera,
    DAQDevice,
    Device,
    Filter,
    Laser,
    Microscope,
    Objective,
    Cooling,
    DataInterface,
    CameraChroma,
    BinMode
)
from aind_data_schema.core.instrument import Instrument


objectives = [
    Objective(
        name="20x Objective",
        numerical_aperture=0.70,
        magnification=20,
        immersion="air",
        manufacturer=Organization.NIKON,
        model="CFI S Plan Fluor LWD 20XC",
    ),
]

dichroics = [
    Filter(
        name="D1",
        filter_type="Multiband",
        manufacturer=Organization.SEMROCK,
        model="FF421/491/567/659/776-Di01",
        notes="DAPI/GFP/RFP/Cy5/Cy7 dichroic",
        center_wavelength=[421, 491, 567, 659, 776],
    ),
    Filter(
        name="D2",
        filter_type="Multiband",
        manufacturer=Organization.CHROMA,
        model="ZT405/514/635rpc",
        notes="DAPI/YFP/Rs Cy5 dichroic",
        center_wavelength=[405, 514, 635],
    ),
    Filter(
        name="D3",
        filter_type="Multiband",
        manufacturer=Organization.SEMROCK,
        model="FF421/491/572-Di01-25x36",
        notes="DAPI/GFP/TxRed dichroic",
        center_wavelength=[421, 491, 572],
    ),
]

emission_filters = [
    Filter(
        name="E1",
        filter_type="Multiband",
        manufacturer=Organization.SEMROCK,
        model="FF01-441/511/593/684/817",
        notes="DAPI/GFP/Red/Cy5/Cy7 - used with D1 and 405nm laser",
        center_wavelength=[441, 511, 593, 684, 817],
    ),
    Filter(
        name="E2",
        filter_type="Band pass",
        manufacturer=Organization.SEMROCK,
        model="FF01-565/24",
        notes="YFP - used with D2 and 520nm laser; bandwidth 24nm",
        center_wavelength=565,
    ),
    Filter(
        name="E3",
        filter_type="Band pass",
        manufacturer=Organization.SEMROCK,
        model="FF01-585/11",
        notes="RFP - used with D1 and 546nm laser; bandwidth 11nm",
        center_wavelength=585,
    ),
    Filter(
        name="E4",
        filter_type="Band pass",
        manufacturer=Organization.SEMROCK,
        model="FF01-676/29",
        notes="FarRed - used with D1 and 638nm laser; bandwidth 29nm",
        center_wavelength=676,
    ),
    Filter(
        name="E5",
        filter_type="Band pass",
        manufacturer=Organization.SEMROCK,
        model="FF01-775/140",
        notes="RS Cy5 - used with D2 and 638nm laser; bandwidth 140nm",
        center_wavelength=775,
    ),
    Filter(
        name="E6",
        filter_type="Multiband",
        manufacturer=Organization.SEMROCK,
        model="FF01-391/477/549/639/741-25",
        notes="YFP/Rs Cy5",
        center_wavelength=[391, 477, 549, 639, 741],
    ),
    Filter(
        name="E7",
        filter_type="Multiband",
        manufacturer=Organization.CHROMA,
        model="69401m",
        notes="DAPI/GFP/TxRed",
        center_wavelength=[440, 520, 600],
    ),
    Filter(
        name="E8",
        filter_type="Multiband",
        manufacturer=Organization.CHROMA,
        model="ZET532/640m",
        notes="Alexa532/Cy5(wide)",
        center_wavelength=[532, 640],
    ),
]

light_sources = [
    Laser(
        name="Lumencor Celesta 365nm",
        manufacturer=Organization.LUMENCOR,
        model="Celesta",
        wavelength=365,
    ),
    Laser(
        name="Lumencor Celesta 440nm",
        manufacturer=Organization.LUMENCOR,
        model="Celesta",
        wavelength=440,
    ),
    Laser(
        name="Lumencor Celesta 488nm",
        manufacturer=Organization.LUMENCOR,
        model="Celesta",
        wavelength=488,
    ),
    Laser(
        name="Lumencor Celesta 514nm",
        manufacturer=Organization.LUMENCOR,
        model="Celesta",
        wavelength=514,
    ),
    Laser(
        name="Lumencor Celesta 561nm",
        manufacturer=Organization.LUMENCOR,
        model="Celesta",
        wavelength=561,
    ),
    Laser(
        name="Lumencor Celesta 640nm",
        manufacturer=Organization.LUMENCOR,
        model="Celesta",
        wavelength=640,
    ),
    Laser(
        name="Lumencor Celesta 730nm",
        manufacturer=Organization.LUMENCOR,
        model="Celesta",
        wavelength=730,
    ),
]

camera = Camera(
    name="Camera-1",
    manufacturer=Organization.TELEDYNE_VISION_SOLUTIONS,
    model="01-KINETIX-M-C",
    data_interface=DataInterface.USB,
    cooling=Cooling.AIR,
    sensor_width=3200,
    sensor_height=3200,
    size_unit=SizeUnit.PX,
    chroma=CameraChroma.BW,
    immersion="air",
    bin_mode=BinMode.NO_BINNING,
    bit_depth=16,
    sensor_format="20.8 x 20.8",
    sensor_format_unit="mm",
    frame_rate=500,
    frame_rate_unit="hertz",
)

microscope = Microscope(
    name="Ti2-E__0",
    manufacturer=Organization.NIKON,
    model="Ti2-E",
)

spinning_disk = Device(
    name="XLIGHT Spinning Disk",
    manufacturer=Organization.CRESTOPTICS,
    model="X-Light V3",
    notes="Nipkow spinning disk confocal module",
)

daq = DAQDevice(
    name="DigitalIO",
    manufacturer=Organization.NATIONAL_INSTRUMENTS,
    model="NI-DAQ Dev1",
    data_interface="USB",
)

instrument = Instrument(
    location="243",
    instrument_id="Dogwood",
    modification_date=date(2024, 7, 9),
    coordinate_system=CoordinateSystemLibrary.IMAGE_XYZ,
    modalities=[Modality.BARSEQ],
    notes=(
        "BarSEQ imaging system with Nikon Ti2-E inverted microscope, X-Light V3 spinning disk confocal, "
        "and Lumencor Celesta light engine. Used for multi-channel fluorescence imaging of genetically "
        "modified tissue samples. Channel configurations: geneseq01/bcseq01 cycles use G/T/A/C/DAPI channels, "
        "other geneseq/bcseq cycles use GTAC channels, hyb cycles use GFP/G/TxRed/Cy5/DAPI/DIC channels. "
        "Camera pixel size: 0.33um. Stitch overlap: 23%. Hyb registration radius: 100um. "
        "Configuration date corresponds to chprofile20x_dogwood_20240709.mat and chshift20x_dogwood_20240709.mat"
    ),
    temperature_control=False,
    components=[
        microscope,
        *objectives,
        *dichroics,
        *emission_filters,
        *light_sources,
        camera,
        spinning_disk,
        daq,
    ],
)

if __name__ == "__main__":
    serialized = instrument.model_dump_json()
    deserialized = Instrument.model_validate_json(serialized)
    deserialized.write_standard_file(prefix="barseq")
