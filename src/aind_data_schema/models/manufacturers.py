"""Module for Manufacturers definitions"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.registry import Registry, ResearchOrganizationRegistry


class _Manufacturer(PIDName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class AAOptoElectronic(_Manufacturer):
    """AAOptoElectronic"""

    name: Literal["AA Opto Electronic"] = "AA Opto Electronic"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class AilipuTechnologyCo(_Manufacturer):
    """AilipuTechnologyCo"""

    name: Literal["Ailipu Technology Co"] = "Ailipu Technology Co"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Allied(_Manufacturer):
    """Allied"""

    name: Literal["Allied"] = "Allied"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class AllenInstituteForNeuralDynamics(_Manufacturer):
    """AllenInstituteForNeuralDynamics"""

    name: Literal["Allen Institute for Neural Dynamics"] = "Allen Institute for Neural Dynamics"
    abbreviation: Literal["AIND"] = "AIND"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["04szwah67"] = "04szwah67"


class AppliedScientificInstrumentation(_Manufacturer):
    """AppliedScientificInstrumentation"""

    name: Literal["Applied Scientific Instrumentation"] = "Applied Scientific Instrumentation"
    abbreviation: Literal["ASI"] = "ASI"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Asus(_Manufacturer):
    """Asus"""

    name: Literal["ASUS"] = "ASUS"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00bxkz165"] = "00bxkz165"


class ArecontVisionCostar(_Manufacturer):
    """ArecontVisionCostar"""

    name: Literal["Arecont Vision Costar"] = "Arecont Vision Costar"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Basler(_Manufacturer):
    """Basler"""

    name: Literal["Basler"] = "Basler"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class CambridgeTechnology(_Manufacturer):
    """CambridgeTechnology"""

    name: Literal["Cambridge Technology"] = "Cambridge Technology"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class ChampalimaudFoundation(_Manufacturer):
    """Champalimaud Foundation"""

    name: Literal["Champalimaud Foundation"] = "Champalimaud Foundation"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["03g001n57"] = "03g001n57"


class Chroma(_Manufacturer):
    """Chroma"""

    name: Literal["Chroma"] = "Chroma"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class CoherentScientific(_Manufacturer):
    """CoherentScientific"""

    name: Literal["Coherent Scientific"] = "Coherent Scientific"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["031tysd23"] = "031tysd23"


class Conoptics(_Manufacturer):
    """Conoptics"""

    name: Literal["Conoptics"] = "Conoptics"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Computar(_Manufacturer):
    """Computar"""

    name: Literal["Computar"] = "Computar"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Custom(_Manufacturer):
    """Custom"""

    name: Literal["Custom"] = "Custom"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Doric(_Manufacturer):
    """Doric"""

    name: Literal["Doric"] = "Doric"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["059n53q30"] = "059n53q30"


class Ealing(_Manufacturer):
    """Ealing"""

    name: Literal["Ealing"] = "Ealing"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class EdmundOptics(_Manufacturer):
    """EdmundOptics"""

    name: Literal["Edmund Optics"] = "Edmund Optics"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01j1gwp17"] = "01j1gwp17"


class Euresys(_Manufacturer):
    """Euresys"""

    name: Literal["Euresys"] = "Euresys"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class TeledyneFLIR(_Manufacturer):
    """TeledyneFLIR"""

    name: Literal["Teledyne FLIR"] = "Teledyne FLIR"
    abbreviation: Literal["FLIR"] = "FLIR"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01j1gwp17"] = "01j1gwp17"


class Fujinon(_Manufacturer):
    """Fujinon"""

    name: Literal["Fujinon"] = "Fujinon"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Hamamatsu(_Manufacturer):
    """Hamamatsu"""

    name: Literal["Hamamatsu"] = "Hamamatsu"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["03natb733"] = "03natb733"


class TheImagingSource(_Manufacturer):
    """TheImagingSource"""

    name: Literal["The Imaging Source"] = "The Imaging Source"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class InteruniversityMicroelectronicsCenter(_Manufacturer):
    """InteruniversityMicroelectronicsCenter"""

    name: Literal["Interuniversity Microelectronics Center"] = "Interuniversity Microelectronics Center"
    abbreviation: Literal["IMEC"] = "IMEC"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["02kcbn207"] = "02kcbn207"


class InfinityPhotoOptical(_Manufacturer):
    """InfinityPhotoOptical"""

    name: Literal["Infinity Photo-Optical"] = "Infinity Photo-Optical"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class ISLProductsInternational(_Manufacturer):
    """ISLProductsInternational"""

    name: Literal["ISL Products International"] = "ISL Products International"
    abbreviation: Literal["ISL"] = "ISL"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Julabo(_Manufacturer):
    """Julabo"""

    name: Literal["Julabo"] = "Julabo"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class TheLeeCompany(_Manufacturer):
    """TheLeeCompany"""

    name: Literal["The Lee Company"] = "The Lee Company"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Leica(_Manufacturer):
    """Leica"""

    name: Literal["Leica"] = "Leica"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Lg(_Manufacturer):
    """Lg"""

    name: Literal["LG"] = "LG"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["02b948n83"] = "02b948n83"


class LifeCanvas(_Manufacturer):
    """LifeCanvas"""

    name: Literal["LifeCanvas"] = "LifeCanvas"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class MeadowlarkOptics(_Manufacturer):
    """MeadowlarkOptics"""

    name: Literal["Meadowlark Optics"] = "Meadowlark Optics"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00n8qbq54"] = "00n8qbq54"


class IRRobotCo(_Manufacturer):
    """IRRobotCo"""

    name: Literal["IR Robot Co"] = "IR Robot Co"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Mitutuyo(_Manufacturer):
    """Mitutuyo"""

    name: Literal["Mitutuyo"] = "Mitutuyo"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class MKSNewport(_Manufacturer):
    """MKSNewport"""

    name: Literal["MKS Newport"] = "MKS Newport"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00k17f049"] = "00k17f049"


class Mpi(_Manufacturer):
    """Mpi"""

    name: Literal["MPI"] = "MPI"
    abbreviation: Literal["MPI"] = "MPI"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class NationalInstruments(_Manufacturer):
    """NationalInstruments"""

    name: Literal["National Instruments"] = "National Instruments"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["026exqw73"] = "026exqw73"


class Navitar(_Manufacturer):
    """Navitar"""

    name: Literal["Navitar"] = "Navitar"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class NewScaleTechnologies(_Manufacturer):
    """NewScaleTechnologies"""

    name: Literal["New Scale Technologies"] = "New Scale Technologies"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Nikon(_Manufacturer):
    """Nikon"""

    name: Literal["Nikon"] = "Nikon"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["0280y9h11"] = "0280y9h11"


class OpenEphysProductionSite(_Manufacturer):
    """OpenEphysProductionSite"""

    name: Literal["Open Ephys Production Site"] = "Open Ephys Production Site"
    abbreviation: Literal["OEPS"] = "OEPS"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["007rkz355"] = "007rkz355"


class Olympus(_Manufacturer):
    """Olympus"""

    name: Literal["Olympus"] = "Olympus"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["02vcdte90"] = "02vcdte90"


class Optotune(_Manufacturer):
    """Optotune"""

    name: Literal["Optotune"] = "Optotune"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Oxxius(_Manufacturer):
    """Oxxius"""

    name: Literal["Oxxius"] = "Oxxius"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Prizmatix(_Manufacturer):
    """Prizmatix"""

    name: Literal["Prizmatix"] = "Prizmatix"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Quantifi(_Manufacturer):
    """Quantifi"""

    name: Literal["Quantifi"] = "Quantifi"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class RaspberryPi(_Manufacturer):
    """RaspberryPi"""

    name: Literal["Raspberry Pi"] = "Raspberry Pi"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class SecondOrderEffects(_Manufacturer):
    """Second Order Effects"""

    name: Literal["Second Order Effects"] = "Second Order Effects"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Semrock(_Manufacturer):
    """Semrock"""

    name: Literal["Semrock"] = "Semrock"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class SchneiderKreuznach(_Manufacturer):
    """SchneiderKreuznach"""

    name: Literal["Schneider-Kreuznach"] = "Schneider-Kreuznach"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Spinnaker(_Manufacturer):
    """Spinnaker"""

    name: Literal["Spinnaker"] = "Spinnaker"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Tamron(_Manufacturer):
    """Tamron"""

    name: Literal["Tamron"] = "Tamron"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Thorlabs(_Manufacturer):
    """Thorlabs"""

    name: Literal["Thorlabs"] = "Thorlabs"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["04gsnvb07"] = "04gsnvb07"


class TMC(_Manufacturer):
    """TMC"""

    name: Literal["Technical Manufacturing Corporation"] = "Technical Manufacturing Corporation"
    abbreviation: Literal["TMC"] = "TMC"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Tymphany(_Manufacturer):
    """Tymphany"""

    name: Literal["Tymphany"] = "Tymphany"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Vieworks(_Manufacturer):
    """Vieworks"""

    name: Literal["Vieworks"] = "Vieworks"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Vortran(_Manufacturer):
    """Vortran"""

    name: Literal["Vortran"] = "Vortran"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class CarlZeiss(_Manufacturer):
    """CarlZeiss"""

    name: Literal["Carl Zeiss"] = "Carl Zeiss"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01xk5xs43"] = "01xk5xs43"


class Other(_Manufacturer):
    """Other"""

    name: Literal["Other"] = "Other"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


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
    CHAMPALIMAUD = ChampalimaudFoundation()
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
    TMC = TMC()
    TYMPHANY = Tymphany()
    VIEWORKS = Vieworks()
    VORTRAN = Vortran()
    ZEISS = CarlZeiss()
    OTHER = Other()

    _ALL = tuple(_Manufacturer.__subclasses__())
    ONE_OF = Annotated[Union[_ALL], Field(discriminator="name")]

    DETECTOR_MANUFACTURERS = Annotated[
        Union[
            AilipuTechnologyCo,
            Allied,
            Basler,
            EdmundOptics,
            Hamamatsu,
            Spinnaker,
            TeledyneFLIR,
            TheImagingSource,
            Thorlabs,
            Vieworks,
            Other,
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
        Union[
            AllenInstituteForNeuralDynamics,
            ChampalimaudFoundation,
            NationalInstruments,
            InteruniversityMicroelectronicsCenter,
            OpenEphysProductionSite,
            Other,
            SecondOrderEffects,
        ],
        Field(discriminator="name"),
    ]
    LASER_MANUFACTURERS = Annotated[
        Union[CoherentScientific, Hamamatsu, Oxxius, Quantifi, Vortran, Other], Field(discriminator="name")
    ]
    LED_MANUFACTURERS = Annotated[Union[Doric, Prizmatix, Thorlabs, Other], Field(discriminator="name")]
    MANIPULATOR_MANUFACTURERS = Annotated[Union[NewScaleTechnologies], Field(discriminator="name")]
    MONITOR_MANUFACTURERS = Annotated[Union[Asus, Lg], Field(discriminator="name")]
    SPEAKER_MANUFACTURERS = Annotated[Union[Tymphany, ISLProductsInternational], Field(discriminator="name")]
