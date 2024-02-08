"""Module for Organization definitions, including manufacturers, institutions, and vendors"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema.models.pid_names import PIDName
from aind_data_schema.models.registry import Registry, ResearchOrganizationRegistry


class _Organization(PIDName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class AAOptoElectronic(_Organization):
    """AAOptoElectronic"""

    name: Literal["AA Opto Electronic"] = "AA Opto Electronic"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Abcam(_Organization):
    """Abcam"""

    name: Literal["Abcam"] = "Abcam"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["02e1wjw63"] = "02e1wjw63"


class AilipuTechnologyCo(_Organization):
    """AilipuTechnologyCo"""

    name: Literal["Ailipu Technology Co"] = "Ailipu Technology Co"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class AllenInstitute(_Organization):
    """AllenInstitute"""

    name: Literal["Allen Institute"] = "Allen Institute"
    abbreviation: Literal["AI"] = "AI"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["03cpe7c52"] = "03cpe7c52"


class AllenInstituteForBrainScience(_Organization):
    """AllenInstituteForBrainScience"""

    name: Literal["Allen Institute for Brain Science"] = "Allen Institute for Brain Science"
    abbreviation: Literal["AIBS"] = "AIBS"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00dcv1019"] = "00dcv1019"


class AllenInstituteForNeuralDynamics(_Organization):
    """AllenInstituteForNeuralDynamics"""

    name: Literal["Allen Institute for Neural Dynamics"] = "Allen Institute for Neural Dynamics"
    abbreviation: Literal["AIND"] = "AIND"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["04szwah67"] = "04szwah67"


class Allied(_Organization):
    """Allied"""

    name: Literal["Allied"] = "Allied"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class AmsOsram(_Organization):
    """ams OSRAM"""

    name: Literal["ams OSRAM"] = "ams OSRAM"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["045d0h266"] = "045d0h266"


class AppliedScientificInstrumentation(_Organization):
    """AppliedScientificInstrumentation"""

    name: Literal["Applied Scientific Instrumentation"] = "Applied Scientific Instrumentation"
    abbreviation: Literal["ASI"] = "ASI"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Asus(_Organization):
    """Asus"""

    name: Literal["ASUS"] = "ASUS"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00bxkz165"] = "00bxkz165"


class ArecontVisionCostar(_Organization):
    """ArecontVisionCostar"""

    name: Literal["Arecont Vision Costar"] = "Arecont Vision Costar"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Basler(_Organization):
    """Basler"""

    name: Literal["Basler"] = "Basler"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class CambridgeTechnology(_Organization):
    """CambridgeTechnology"""

    name: Literal["Cambridge Technology"] = "Cambridge Technology"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class ChampalimaudFoundation(_Organization):
    """Champalimaud Foundation"""

    name: Literal["Champalimaud Foundation"] = "Champalimaud Foundation"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["03g001n57"] = "03g001n57"


class Chroma(_Organization):
    """Chroma"""

    name: Literal["Chroma"] = "Chroma"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class CoherentScientific(_Organization):
    """CoherentScientific"""

    name: Literal["Coherent Scientific"] = "Coherent Scientific"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["031tysd23"] = "031tysd23"


class ColumbiaUniversity(_Organization):
    """ColumbiaUniversity"""

    name: Literal["Columbia University"] = "Columbia University"
    abbreviation: Literal["Columbia"] = "Columbia"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00hj8s172"] = "00hj8s172"


class Computar(_Organization):
    """Computar"""

    name: Literal["Computar"] = "Computar"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Conoptics(_Organization):
    """Conoptics"""

    name: Literal["Conoptics"] = "Conoptics"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Custom(_Organization):
    """Custom"""

    name: Literal["Custom"] = "Custom"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Dodotronic(_Organization):
    """Dodotronic"""

    name: Literal["Dodotronic"] = "Dodotronic"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Doric(_Organization):
    """Doric"""

    name: Literal["Doric"] = "Doric"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["059n53q30"] = "059n53q30"


class Ealing(_Organization):
    """Ealing"""

    name: Literal["Ealing"] = "Ealing"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class EdmundOptics(_Organization):
    """EdmundOptics"""

    name: Literal["Edmund Optics"] = "Edmund Optics"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01j1gwp17"] = "01j1gwp17"


class Euresys(_Organization):
    """Euresys"""

    name: Literal["Euresys"] = "Euresys"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class TeledyneFLIR(_Organization):
    """TeledyneFLIR"""

    name: Literal["Teledyne FLIR"] = "Teledyne FLIR"
    abbreviation: Literal["FLIR"] = "FLIR"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01j1gwp17"] = "01j1gwp17"


class Fujinon(_Organization):
    """Fujinon"""

    name: Literal["Fujinon"] = "Fujinon"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Hamamatsu(_Organization):
    """Hamamatsu"""

    name: Literal["Hamamatsu"] = "Hamamatsu"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["03natb733"] = "03natb733"


class HuazhongUniversityOfScienceAndTechnology(_Organization):
    """HuazhongUniversityOfScienceAndTechnology"""

    name: Literal["Huazhong University of Science and Technology"] = "Huazhong University of Science and Technology"
    abbreviation: Literal["HUST"] = "HUST"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00p991c53"] = "00p991c53"


class TheImagingSource(_Organization):
    """TheImagingSource"""

    name: Literal["The Imaging Source"] = "The Imaging Source"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class InteruniversityMicroelectronicsCenter(_Organization):
    """InteruniversityMicroelectronicsCenter"""

    name: Literal["Interuniversity Microelectronics Center"] = "Interuniversity Microelectronics Center"
    abbreviation: Literal["IMEC"] = "IMEC"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["02kcbn207"] = "02kcbn207"


class InfinityPhotoOptical(_Organization):
    """InfinityPhotoOptical"""

    name: Literal["Infinity Photo-Optical"] = "Infinity Photo-Optical"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class ISLProductsInternational(_Organization):
    """ISLProductsInternational"""

    name: Literal["ISL Products International"] = "ISL Products International"
    abbreviation: Literal["ISL"] = "ISL"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class JacksonLaboratory(_Organization):
    """JacksonLaboratory"""

    name: Literal["Jackson Laboratory"] = "Jackson Laboratory"
    abbreviation: Literal["JAX"] = "JAX"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["021sy4w91"] = "021sy4w91"


class Julabo(_Organization):
    """Julabo"""

    name: Literal["Julabo"] = "Julabo"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class TheLeeCompany(_Organization):
    """TheLeeCompany"""

    name: Literal["The Lee Company"] = "The Lee Company"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Leica(_Organization):
    """Leica"""

    name: Literal["Leica"] = "Leica"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Lg(_Organization):
    """Lg"""

    name: Literal["LG"] = "LG"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["02b948n83"] = "02b948n83"


class LifeCanvas(_Organization):
    """LifeCanvas"""

    name: Literal["LifeCanvas"] = "LifeCanvas"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class MeadowlarkOptics(_Organization):
    """MeadowlarkOptics"""

    name: Literal["Meadowlark Optics"] = "Meadowlark Optics"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00n8qbq54"] = "00n8qbq54"


class IRRobotCo(_Organization):
    """IRRobotCo"""

    name: Literal["IR Robot Co"] = "IR Robot Co"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Mitutuyo(_Organization):
    """Mitutuyo"""

    name: Literal["Mitutuyo"] = "Mitutuyo"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class MKSNewport(_Organization):
    """MKSNewport"""

    name: Literal["MKS Newport"] = "MKS Newport"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["00k17f049"] = "00k17f049"


class Mpi(_Organization):
    """Mpi"""

    name: Literal["MPI"] = "MPI"
    abbreviation: Literal["MPI"] = "MPI"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class NationalInstituteOfNeurologicalDisordersAndStroke(_Organization):
    """NationalInstituteOfNeurologicalDisordersAndStroke"""

    name: Literal[
        "National Institute of Neurological Disorders and Stroke"
    ] = "National Institute of Neurological Disorders and Stroke"
    abbreviation: Literal["NINDS"] = "NINDS"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01s5ya894"] = "01s5ya894"


class NationalInstruments(_Organization):
    """NationalInstruments"""

    name: Literal["National Instruments"] = "National Instruments"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["026exqw73"] = "026exqw73"


class Navitar(_Organization):
    """Navitar"""

    name: Literal["Navitar"] = "Navitar"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class NewScaleTechnologies(_Organization):
    """NewScaleTechnologies"""

    name: Literal["New Scale Technologies"] = "New Scale Technologies"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class NewYorkUniversity(_Organization):
    """NewYorkUniversity"""

    name: Literal["New York University"] = "New York University"
    abbreviation: Literal["NYU"] = "NYU"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["0190ak572"] = "0190ak572"


class Nikon(_Organization):
    """Nikon"""

    name: Literal["Nikon"] = "Nikon"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["0280y9h11"] = "0280y9h11"


class OpenEphysProductionSite(_Organization):
    """OpenEphysProductionSite"""

    name: Literal["Open Ephys Production Site"] = "Open Ephys Production Site"
    abbreviation: Literal["OEPS"] = "OEPS"
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["007rkz355"] = "007rkz355"


class Olympus(_Organization):
    """Olympus"""

    name: Literal["Olympus"] = "Olympus"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["02vcdte90"] = "02vcdte90"


class Optotune(_Organization):
    """Optotune"""

    name: Literal["Optotune"] = "Optotune"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Oxxius(_Organization):
    """Oxxius"""

    name: Literal["Oxxius"] = "Oxxius"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Prizmatix(_Organization):
    """Prizmatix"""

    name: Literal["Prizmatix"] = "Prizmatix"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Quantifi(_Organization):
    """Quantifi"""

    name: Literal["Quantifi"] = "Quantifi"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class RaspberryPi(_Organization):
    """RaspberryPi"""

    name: Literal["Raspberry Pi"] = "Raspberry Pi"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class SecondOrderEffects(_Organization):
    """Second Order Effects"""

    name: Literal["Second Order Effects"] = "Second Order Effects"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Semrock(_Organization):
    """Semrock"""

    name: Literal["Semrock"] = "Semrock"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class SchneiderKreuznach(_Organization):
    """SchneiderKreuznach"""

    name: Literal["Schneider-Kreuznach"] = "Schneider-Kreuznach"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class SimonsFoundation(_Organization):
    """SimonsFoundation"""

    name: Literal["Simons Foundation"] = "Simons Foundation"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01cmst727"] = "01cmst727"


class Spinnaker(_Organization):
    """Spinnaker"""

    name: Literal["Spinnaker"] = "Spinnaker"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Tamron(_Organization):
    """Tamron"""

    name: Literal["Tamron"] = "Tamron"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Thermofisher(_Organization):
    """Thermofisher"""

    name: Literal["Thermo Fisher"] = "Thermo Fisher"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["03x1ewr52"] = Field("03x1ewr52")


class Thorlabs(_Organization):
    """Thorlabs"""

    name: Literal["Thorlabs"] = "Thorlabs"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["04gsnvb07"] = "04gsnvb07"


class TMC(_Organization):
    """TMC"""

    name: Literal["Technical Manufacturing Corporation"] = "Technical Manufacturing Corporation"
    abbreviation: Literal["TMC"] = "TMC"
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Tymphany(_Organization):
    """Tymphany"""

    name: Literal["Tymphany"] = "Tymphany"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Vieworks(_Organization):
    """Vieworks"""

    name: Literal["Vieworks"] = "Vieworks"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Vortran(_Organization):
    """Vortran"""

    name: Literal["Vortran"] = "Vortran"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class CarlZeiss(_Organization):
    """CarlZeiss"""

    name: Literal["Carl Zeiss"] = "Carl Zeiss"
    abbreviation: Literal[None] = Field(None)
    registry: Annotated[Union[ResearchOrganizationRegistry], Field(default=Registry.ROR, discriminator="name")]
    registry_identifier: Literal["01xk5xs43"] = "01xk5xs43"


class Other(_Organization):
    """Other"""

    name: Literal["Other"] = "Other"
    abbreviation: Literal[None] = Field(None)
    registry: Literal[None] = Field(None)
    registry_identifier: Literal[None] = Field(None)


class Organization:
    """Organization definitions"""

    AA_OPTO = AAOptoElectronic()
    ABCAM = Abcam()
    AILIPU = AilipuTechnologyCo()
    AI = AllenInstitute()
    AIBS = AllenInstituteForBrainScience()
    AIND = AllenInstituteForNeuralDynamics()
    ALLIED = Allied()
    ASI = AppliedScientificInstrumentation()
    ASUS = Asus()
    AVCOSTAR = ArecontVisionCostar()
    BASLER = Basler()
    CAMBRIDGE_TECHNOLOGY = CambridgeTechnology()
    CHAMPALIMAUD = ChampalimaudFoundation()
    CHROMA = Chroma()
    COHERENT_SCIENTIFIC = CoherentScientific()
    COLUMBIA = ColumbiaUniversity()
    COMPUTAR = Computar()
    CONOPTICS = Conoptics()
    CUSTOM = Custom()
    DODOTRONIC = Dodotronic()
    DORIC = Doric()
    EALING = Ealing()
    EDMUND_OPTICS = EdmundOptics()
    EURESYS = Euresys()
    FLIR = TeledyneFLIR()
    FUJINON = Fujinon()
    HAMAMATSU = Hamamatsu()
    HUST = HuazhongUniversityOfScienceAndTechnology()
    IMAGING_SOURCE = TheImagingSource()
    IMEC = InteruniversityMicroelectronicsCenter()
    INFINITY_PHOTO_OPTICAL = InfinityPhotoOptical()
    ISL = ISLProductsInternational()
    JAX = JacksonLaboratory()
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
    NINDS = NationalInstituteOfNeurologicalDisordersAndStroke()
    NIKON = Nikon()
    NYU = NewYorkUniversity()
    OEPS = OpenEphysProductionSite()
    OLYMPUS = Olympus()
    OPTOTUNE = Optotune()
    OSRAM = AmsOsram()
    OXXIUS = Oxxius()
    PRIZMATIX = Prizmatix()
    QUANTIFI = Quantifi()
    RASPBERRYPI = RaspberryPi()
    SEMROCK = Semrock()
    SCHNEIDER_KREUZNACH = SchneiderKreuznach()
    SIMONS = SimonsFoundation()
    SPINNAKER = Spinnaker()
    TAMRON = Tamron()
    THORLABS = Thorlabs()
    THERMOFISHER = Thermofisher()
    TMC = TMC()
    TYMPHANY = Tymphany()
    VIEWORKS = Vieworks()
    VORTRAN = Vortran()
    ZEISS = CarlZeiss()
    OTHER = Other()

    _ALL = tuple(_Organization.__subclasses__())
    ONE_OF = Annotated[Union[_ALL], Field(discriminator="name")]

    _abbreviation_map = {m().abbreviation: m() for m in _ALL}
    _name_map = {m().name: m() for m in _ALL}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        """Get class from abbreviation"""
        return cls._abbreviation_map[abbreviation]

    @classmethod
    def from_name(cls, name: str):
        """Get class from abbreviation"""
        return cls._name_map[name]

    @property
    def name_map(self) -> dict:
        """Dictionary of mapping from name to object"""
        return self._name_map

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
            SecondOrderEffects,
            Other,
        ],
        Field(discriminator="name"),
    ]
    LASER_MANUFACTURERS = Annotated[
        Union[CoherentScientific, Hamamatsu, Oxxius, Quantifi, Vortran, Other], Field(discriminator="name")
    ]
    LED_MANUFACTURERS = Annotated[Union[AmsOsram, Doric, Prizmatix, Thorlabs, Other], Field(discriminator="name")]
    MANIPULATOR_MANUFACTURERS = Annotated[Union[NewScaleTechnologies, Other], Field(discriminator="name")]
    MONITOR_MANUFACTURERS = Annotated[Union[Asus, Lg, Other], Field(discriminator="name")]
    SPEAKER_MANUFACTURERS = Annotated[Union[Tymphany, ISLProductsInternational, Other], Field(discriminator="name")]
    FUNDERS = Annotated[
        Union[AllenInstitute, NationalInstituteOfNeurologicalDisordersAndStroke, SimonsFoundation],
        Field(discriminator="name"),
    ]
    RESEARCH_INSTITUTIONS = Annotated[
        Union[
            AllenInstituteForBrainScience,
            AllenInstituteForNeuralDynamics,
            ColumbiaUniversity,
            HuazhongUniversityOfScienceAndTechnology,
            NewYorkUniversity,
            Other,
        ],
        Field(discriminator="name"),
    ]
    SUBJECT_SOURCES = Annotated[
        Union[
            AllenInstitute,
            ColumbiaUniversity,
            HuazhongUniversityOfScienceAndTechnology,
            JacksonLaboratory,
            NewYorkUniversity,
            Other,
        ],
        Field(discriminator="name"),
    ]
