"""Module for Manufacturers definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.base import Constant
from aind_data_schema.models.pid_names import BaseName, PIDName
from aind_data_schema.models.registry import ROR


class _Manufacturer(PIDName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class AAOptoElectronic(_Manufacturer):
    """AAOptoElectronic"""

    name: Constant("AA Opto Electronic")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class AilipuTechnologyCo(_Manufacturer):
    """AilipuTechnologyCo"""

    name: Constant("Ailipu Technology Co")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Allied(_Manufacturer):
    """Allied"""

    name: Constant("Allied")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class AppliedScientificInstrumentation(_Manufacturer):
    """AppliedScientificInstrumentation"""

    name: Constant("Applied Scientific Instrumentation")
    abbreviation: Constant("ASI")
    registry: Constant(None)
    registry_identifier: Constant(None)


class Asus(_Manufacturer):
    """Asus"""

    name: Constant("ASUS")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("00bxkz165")


class ArecontVisionCostar(_Manufacturer):
    """ArecontVisionCostar"""

    name: Constant("Arecont Vision Costar")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Basler(_Manufacturer):
    """Basler"""

    name: Constant("Basler")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class CambridgeTechnology(_Manufacturer):
    """CambridgeTechnology"""

    name: Constant("Cambridge Technology")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Chroma(_Manufacturer):
    """Chroma"""

    name: Constant("Chroma")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class CoherentScientific(_Manufacturer):
    """CoherentScientific"""

    name: Constant("Coherent Scientific")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("031tysd23")


class Conoptics(_Manufacturer):
    """Conoptics"""

    name: Constant("Conoptics")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Computar(_Manufacturer):
    """Computar"""

    name: Constant("Computar")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Custom(_Manufacturer):
    """Custom"""

    name: Constant("Custom")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Doric(_Manufacturer):
    """Doric"""

    name: Constant("Doric")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("059n53q30")


class Ealing(_Manufacturer):
    """Ealing"""

    name: Constant("Ealing")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class EdmundOptics(_Manufacturer):
    """EdmundOptics"""

    name: Constant("Edmund Optics")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("01j1gwp17")


class Euresys(_Manufacturer):
    """Euresys"""

    name: Constant("Euresys")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class TeledyneFLIR(_Manufacturer):
    """TeledyneFLIR"""

    name: Constant("Teledyne FLIR")
    abbreviation: Constant("FLIR")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("01j1gwp17")


class Fujinon(_Manufacturer):
    """Fujinon"""

    name: Constant("Fujinon")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Hamamatsu(_Manufacturer):
    """Hamamatsu"""

    name: Constant("Hamamatsu")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("03natb733")


class TheImagingSource(_Manufacturer):
    """TheImagingSource"""

    name: Constant("The Imaging Source")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class InteruniversityMicroelectronicsCenter(_Manufacturer):
    """InteruniversityMicroelectronicsCenter"""

    name: Constant("Interuniversity Microelectronics Center")
    abbreviation: Constant("IMEC")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("02kcbn207")


class InfinityPhotoOptical(_Manufacturer):
    """InfinityPhotoOptical"""

    name: Constant("Infinity Photo-Optical")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class ISLProductsInternational(_Manufacturer):
    """ISLProductsInternational"""

    name: Constant("ISL Products International")
    abbreviation: Constant("ISL")
    registry: Constant(None)
    registry_identifier: Constant(None)


class Julabo(_Manufacturer):
    """Julabo"""

    name: Constant("Julabo")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class TheLeeCompany(_Manufacturer):
    """TheLeeCompany"""

    name: Constant("The Lee Company")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Leica(_Manufacturer):
    """Leica"""

    name: Constant("Leica")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Lg(_Manufacturer):
    """Lg"""

    name: Constant("LG")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("02b948n83")


class LifeCanvas(_Manufacturer):
    """LifeCanvas"""

    name: Constant("LifeCanvas")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class MeadowlarkOptics(_Manufacturer):
    """MeadowlarkOptics"""

    name: Constant("Meadowlark Optics")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("00n8qbq54")


class IRRobotCo(_Manufacturer):
    """IRRobotCo"""

    name: Constant("IR Robot Co")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Mitutuyo(_Manufacturer):
    """Mitutuyo"""

    name: Constant("Mitutuyo")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class MKSNewport(_Manufacturer):
    """MKSNewport"""

    name: Constant("MKS Newport")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("00k17f049")


class Mpi(_Manufacturer):
    """Mpi"""

    name: Constant("MPI")
    abbreviation: Constant("MPI")
    registry: Constant(None)
    registry_identifier: Constant(None)


class NationalInstruments(_Manufacturer):
    """NationalInstruments"""

    name: Constant("National Instruments")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("026exqw73")


class Navitar(_Manufacturer):
    """Navitar"""

    name: Constant("Navitar")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class NewScaleTechnologies(_Manufacturer):
    """NewScaleTechnologies"""

    name: Constant("New Scale Technologies")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Nikon(_Manufacturer):
    """Nikon"""

    name: Constant("Nikon")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("0280y9h11")


class OpenEphysProductionSite(_Manufacturer):
    """OpenEphysProductionSite"""

    name: Constant("Open Ephys Production Site")
    abbreviation: Constant("OEPS")
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("007rkz355")


class Olympus(_Manufacturer):
    """Olympus"""

    name: Constant("Olympus")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("02vcdte90")


class Optotune(_Manufacturer):
    """Optotune"""

    name: Constant("Optotune")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Oxxius(_Manufacturer):
    """Oxxius"""

    name: Constant("Oxxius")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Prizmatix(_Manufacturer):
    """Prizmatix"""

    name: Constant("Prizmatix")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Quantifi(_Manufacturer):
    """Quantifi"""

    name: Constant("Quantifi")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class RaspberryPi(_Manufacturer):
    """RaspberryPi"""

    name: Constant("Raspberry Pi")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Semrock(_Manufacturer):
    """Semrock"""

    name: Constant("Semrock")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class SchneiderKreuznach(_Manufacturer):
    """SchneiderKreuznach"""

    name: Constant("Schneider-Kreuznach")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Spinnaker(_Manufacturer):
    """Spinnaker"""

    name: Constant("Spinnaker")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Tamron(_Manufacturer):
    """Tamron"""

    name: Constant("Tamron")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Thorlabs(_Manufacturer):
    """Thorlabs"""

    name: Constant("Thorlabs")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("04gsnvb07")


class TechnicalManufacturingCorporation(_Manufacturer):
    """TechnicalManufacturingCorporation"""

    name: Constant("Technical Manufacturing Corporation")
    abbreviation: Constant("TMC")
    registry: Constant(None)
    registry_identifier: Constant(None)


class Tymphany(_Manufacturer):
    """Tymphany"""

    name: Constant("Tymphany")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Vieworks(_Manufacturer):
    """Vieworks"""

    name: Constant("Vieworks")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Vortran(_Manufacturer):
    """Vortran"""

    name: Constant("Vortran")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class CarlZeiss(_Manufacturer):
    """CarlZeiss"""

    name: Constant("Carl Zeiss")
    abbreviation: Constant(None)
    registry: BaseName = Field(ROR, json_schema_extra={"const": True})
    registry_identifier: Constant("01xk5xs43")


class Other(_Manufacturer):
    """Other"""

    name: Constant("Other")
    abbreviation: Constant(None)
    registry: Constant(None)
    registry_identifier: Constant(None)


class Manufacturer:
    """Manufacturer definitions"""

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
