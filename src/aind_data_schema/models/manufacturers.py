"""Module for Manufacturers definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import BaseName, PIDName
from aind_data_schema.models.registry import ROR


class _Manufacturer(PIDName):
    """Base model config"""
    model_config = ConfigDict(frozen=True)


class AAOptoElectronic(_Manufacturer):
    name: Literal["AA Opto Electronic"] = "AA Opto Electronic"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class AilipuTechnologyCo(_Manufacturer):
    name: Literal["Ailipu Technology Co"] = "Ailipu Technology Co"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Allied(_Manufacturer):
    name: Literal["Allied"] = "Allied"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class AppliedScientificInstrumentation(_Manufacturer):
    name: Literal["Applied Scientific Instrumentation"] = "Applied Scientific Instrumentation"
    abbreviation: Literal["ASI"] = "ASI"
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Asus(_Manufacturer):
    name: Literal["ASUS"] = "ASUS"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["00bxkz165"] = "00bxkz165"


class ArecontVisionCostar(_Manufacturer):
    name: Literal["Arecont Vision Costar"] = "Arecont Vision Costar"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Basler(_Manufacturer):
    name: Literal["Basler"] = "Basler"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class CambridgeTechnology(_Manufacturer):
    name: Literal["Cambridge Technology"] = "Cambridge Technology"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Chroma(_Manufacturer):
    name: Literal["Chroma"] = "Chroma"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class CoherentScientific(_Manufacturer):
    name: Literal["Coherent Scientific"] = "Coherent Scientific"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["031tysd23"] = "031tysd23"


class Conoptics(_Manufacturer):
    name: Literal["Conoptics"] = "Conoptics"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Computar(_Manufacturer):
    name: Literal["Computar"] = "Computar"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Custom(_Manufacturer):
    name: Literal["Custom"] = "Custom"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Doric(_Manufacturer):
    name: Literal["Doric"] = "Doric"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["059n53q30"] = "059n53q30"


class Ealing(_Manufacturer):
    name: Literal["Ealing"] = "Ealing"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class EdmundOptics(_Manufacturer):
    name: Literal["Edmund Optics"] = "Edmund Optics"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["01j1gwp17"] = "01j1gwp17"


class Euresys(_Manufacturer):
    name: Literal["Euresys"] = "Euresys"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class TeledyneFLIR(_Manufacturer):
    name: Literal["Teledyne FLIR"] = "Teledyne FLIR"
    abbreviation: Literal["FLIR"] = "FLIR"
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["01j1gwp17"] = "01j1gwp17"


class Fujinon(_Manufacturer):
    name: Literal["Fujinon"] = "Fujinon"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Hamamatsu(_Manufacturer):
    name: Literal["Hamamatsu"] = "Hamamatsu"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["03natb733"] = "03natb733"


class TheImagingSource(_Manufacturer):
    name: Literal["The Imaging Source"] = "The Imaging Source"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class InteruniversityMicroelectronicsCenter(_Manufacturer):
    name: Literal["Interuniversity Microelectronics Center"] = "Interuniversity Microelectronics Center"
    abbreviation: Literal["IMEC"] = "IMEC"
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["02kcbn207"] = "02kcbn207"


class InfinityPhotoOptical(_Manufacturer):
    name: Literal["Infinity Photo-Optical"] = "Infinity Photo-Optical"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class ISLProductsInternational(_Manufacturer):
    name: Literal["ISL Products International"] = "ISL Products International"
    abbreviation: Literal["ISL"] = "ISL"
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Julabo(_Manufacturer):
    name: Literal["Julabo"] = "Julabo"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class TheLeeCompany(_Manufacturer):
    name: Literal["The Lee Company"] = "The Lee Company"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Leica(_Manufacturer):
    name: Literal["Leica"] = "Leica"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Lg(_Manufacturer):
    name: Literal["LG"] = "LG"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["02b948n83"] = "02b948n83"


class LifeCanvas(_Manufacturer):
    name: Literal["LifeCanvas"] = "LifeCanvas"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class MeadowlarkOptics(_Manufacturer):
    name: Literal["Meadowlark Optics"] = "Meadowlark Optics"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["00n8qbq54"] = "00n8qbq54"


class IRRobotCo(_Manufacturer):
    name: Literal["IR Robot Co"] = "IR Robot Co"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Mitutuyo(_Manufacturer):
    name: Literal["Mitutuyo"] = "Mitutuyo"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class MKSNewport(_Manufacturer):
    name: Literal["MKS Newport"] = "MKS Newport"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["00k17f049"] = "00k17f049"


class Mpi(_Manufacturer):
    name: Literal["MPI"] = "MPI"
    abbreviation: Literal["MPI"] = "MPI"
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class NationalInstruments(_Manufacturer):
    name: Literal["National Instruments"] = "National Instruments"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["026exqw73"] = "026exqw73"


class Navitar(_Manufacturer):
    name: Literal["Navitar"] = "Navitar"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class NewScaleTechnologies(_Manufacturer):
    name: Literal["New Scale Technologies"] = "New Scale Technologies"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Nikon(_Manufacturer):
    name: Literal["Nikon"] = "Nikon"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["0280y9h11"] = "0280y9h11"


class OpenEphysProductionSite(_Manufacturer):
    name: Literal["Open Ephys Production Site"] = "Open Ephys Production Site"
    abbreviation: Literal["OEPS"] = "OEPS"
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["007rkz355"] = "007rkz355"


class Olympus(_Manufacturer):
    name: Literal["Olympus"] = "Olympus"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["02vcdte90"] = "02vcdte90"


class Optotune(_Manufacturer):
    name: Literal["Optotune"] = "Optotune"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Oxxius(_Manufacturer):
    name: Literal["Oxxius"] = "Oxxius"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Prizmatix(_Manufacturer):
    name: Literal["Prizmatix"] = "Prizmatix"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Quantifi(_Manufacturer):
    name: Literal["Quantifi"] = "Quantifi"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class RaspberryPi(_Manufacturer):
    name: Literal["Raspberry Pi"] = "Raspberry Pi"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Semrock(_Manufacturer):
    name: Literal["Semrock"] = "Semrock"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class SchneiderKreuznach(_Manufacturer):
    name: Literal["Schneider-Kreuznach"] = "Schneider-Kreuznach"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Spinnaker(_Manufacturer):
    name: Literal["Spinnaker"] = "Spinnaker"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Tamron(_Manufacturer):
    name: Literal["Tamron"] = "Tamron"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Thorlabs(_Manufacturer):
    name: Literal["Thorlabs"] = "Thorlabs"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["04gsnvb07"] = "04gsnvb07"


class TechnicalManufacturingCorporation(_Manufacturer):
    name: Literal["Technical Manufacturing Corporation"] = "Technical Manufacturing Corporation"
    abbreviation: Literal["TMC"] = "TMC"
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Tymphany(_Manufacturer):
    name: Literal["Tymphany"] = "Tymphany"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Vieworks(_Manufacturer):
    name: Literal["Vieworks"] = "Vieworks"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Vortran(_Manufacturer):
    name: Literal["Vortran"] = "Vortran"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class CarlZeiss(_Manufacturer):
    name: Literal["Carl Zeiss"] = "Carl Zeiss"
    abbreviation: Literal[None] = None
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Literal["01xk5xs43"] = "01xk5xs43"


class Other(_Manufacturer):
    name: Literal["Other"] = "Other"
    abbreviation: Literal[None] = None
    registry: Literal[None] = None
    registry_identifier: Literal[None] = None


class Manufacturer:

    AA_OPTO = AAOptoElectronic()
    AILIPU = AilipuTechnologyCo()
    ALLIED = Allied()
    ASI = AppliedScientificInstrumentation()
    ASUS = Asus()
    AVCOSTAR = ArecontVisionCostar()
    BASLER = Basler()
    CAMBRIDGE_TECHNOLOGY = CambridgeTechnology()
    CHROMA = Chroma()
    COHERENT_SCIENTIFIC = CoherentScientific()
    CONOPTICS = Conoptics()
    COMPUTAR = Computar()
    CUSTOM = Custom()
    DORIC = Doric()
    EALING = Ealing()
    EDMUND_OPTICS = EdmundOptics()
    EURESYS = Euresys()
    FLIR = TeledyneFLIR()
    FUJINON = Fujinon()
    HAMAMATSU = Hamamatsu()
    IMAGING_SOURCE = TheImagingSource()
    IMEC = InteruniversityMicroelectronicsCenter()
    INFINITY_PHOTO_OPTICAL = InfinityPhotoOptical()
    ISL = ISLProductsInternational()
    JULABO = Julabo()
    LEE = TheLeeCompany()
    LEICA = Leica()
    LG = Lg()
    LIFECANVAS = LifeCanvas()
    MEADOWLARK = MeadowlarkOptics()
    MIGHTY_ZAP = IRRobotCo()
    MITUTUYO = Mitutuyo()
    MKS_NEWPORT = MKSNewport()
    MPI = Mpi()
    NATIONAL_INSTRUMENTS = NationalInstruments()
    NAVITAR = Navitar()
    NEW_SCALE_TECHNOLOGIES = NewScaleTechnologies()
    NIKON = Nikon()
    OEPS = OpenEphysProductionSite()
    OLYMPUS = Olympus()
    OPTOTUNE = Optotune()
    OXXIUS = Oxxius()
    PRIZMATIX = Prizmatix()
    QUANTIFI = Quantifi()
    RASPBERRYPI = RaspberryPi()
    SEMROCK = Semrock()
    SCHNEIDER_KREUZNACH = SchneiderKreuznach()
    SPINNAKER = Spinnaker()
    TAMRON = Tamron()
    THORLABS = Thorlabs()
    TMC = TechnicalManufacturingCorporation()
    TYMPHANY = Tymphany()
    VIEWORKS = Vieworks()
    VORTRAN = Vortran()
    ZEISS = CarlZeiss()
    OTHER = Other()

    ALL = tuple(_Manufacturer.__subclasses__())
    ONE_OF = Annotated[Union[ALL], Field(discriminator="name")]

    CAMERA_MANUFACTURERS = Annotated[
        Union[
            AilipuTechnologyCo, Allied, Basler, EdmundOptics, Spinnaker, TeledyneFLIR, TheImagingSource, Thorlabs, Other
        ],
        Field(discriminator="name"),
    ]
    FILTER_MANUFACTURERS = Annotated[Union[Chroma, EdmundOptics, Semrock, Thorlabs, Other], Field(discriminator="name")]
    LENS_MANUFACTURERS = Annotated[
        Union[
            Computar,
            EdmundOptics,
            Hamamatsu,
            InfinityPhotoOptical,
            Leica,
            Mitutuyo,
            Navitar,
            Nikon,
            Olympus,
            SchneiderKreuznach,
            Thorlabs,
            CarlZeiss,
            Other,
        ],
        Field(discriminator="name"),
    ]
    DAQ_DEVICE_MANUFACTURERS = Annotated[
        Union[NationalInstruments, InteruniversityMicroelectronicsCenter, OpenEphysProductionSite, Other],
        Field(discriminator="name"),
    ]
    LASER_MANUFACTURERS = Annotated[
        Union[CoherentScientific, Hamamatsu, Oxxius, Quantifi, Vortran, Other], Field(discriminator="name")
    ]
    LED_MANUFACTURERS = Annotated[Union[Doric, Prizmatix, Thorlabs, Other], Field(discriminator="name")]
    MANIPULATOR_MANUFACTURERS = Annotated[Union[NewScaleTechnologies], Field(discriminator="name")]
    MONITOR_MANUFACTURERS = Annotated[Union[Asus, Lg], Field(discriminator="name")]
    SPEAKER_MANUFACTURERS = Annotated[Union[Tymphany, ISLProductsInternational], Field(discriminator="name")]
