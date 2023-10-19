"""Enum of Manufacturers for use in the AIND data schema."""

from enum import Enum

from aind_data_schema.base import BaseNameEnumMeta, PIDName, Registry


class Manufacturer(Enum, metaclass=BaseNameEnumMeta):
    """Device manufacturer name"""

    AA_OPTO = PIDName(name="AA Opto Electronic")
    AILIPU = PIDName(name="Ailipu Technology Co")
    ALLIED = PIDName(name="Allied")
    ASI = PIDName(
        name="Applied Scientific Instrumentation",
        abbreviation="ASI",
    )
    AVCOSTAR = PIDName(name="Arecont Vision Costar")
    BASLER = PIDName(name="Basler")
    CAMBRIDGE_TECHNOLOGY = PIDName(name="Cambridge Technology")
    CHROMA = PIDName(name="Chroma")
    COHERENT_SCIENTIFIC = PIDName(
        name="Coherent Scientific",
        registry=Registry.ROR,
        registry_identifier="031tysd23",
    )
    CONOPTICS = PIDName(name="Conoptics")
    COMPUTAR = PIDName(name="Computar")
    CUSTOM = PIDName(name="Custom")
    DORIC = PIDName(
        name="Doric",
        registry=Registry.ROR,
        registry_identifier="059n53q30",
    )
    EALING = PIDName(name="Ealing")
    EDMUND_OPTICS = PIDName(
        name="Edmund Optics",
        registry=Registry.ROR,
        registry_identifier="01j1gwp17",
    )
    EURESYS = PIDName(name="Euresys")
    FLIR = PIDName(
        name="Teledyne FLIR",
        abbreviation="FLIR",
        registry=Registry.ROR,
        registry_identifier="01j1gwp17",
    )
    FUJINON = PIDName(name="Fujinon")
    HAMAMATSU = PIDName(
        name="Hamamatsu",
        registry=Registry.ROR,
        registry_identifier="03natb733",
    )
    IMAGING_SOURCE = PIDName(name="The Imaging Source")
    IMEC = PIDName(
        name="Interuniversity Microelectronics Center",
        abbreviation="IMEC",
        registry=Registry.ROR,
        registry_identifier="02kcbn207",
    )
    INFINITY_PHOTO_OPTICAL = PIDName(name="Infinity Photo-Optical")
    JULABO = PIDName(name="Julabo")
    LEE = PIDName(name="The Lee Company")
    LEICA = PIDName(name="Leica")
    LG = PIDName(
        name="LG",
        registry=Registry.ROR,
        registry_identifier="02b948n83",
    )
    LIFECANVAS = PIDName(name="LifeCanvas")
    MEADOWLARK = PIDName(
        name="Meadowlark Optics",
        registry=Registry.ROR,
        registry_identifier="00n8qbq54",
    )
    MIGHTY_ZAP = PIDName(name="IR Robot Co")
    MITUTUYO = PIDName(name="Mitutuyo")
    MKS_NEWPORT = PIDName(
        name="MKS Newport",
        registry=Registry.ROR,
        registry_identifier="00k17f049",
    )
    MPI = PIDName(name="MPI", abbreviation="MPI")
    NATIONAL_INSTRUMENTS = PIDName(
        name="National Instruments",
        registry=Registry.ROR,
        registry_identifier="026exqw73",
    )
    NEW_SCALE_TECHNOLOGIES = PIDName(name="New Scale Technologies")
    NIKON = PIDName(
        name="Nikon",
        registry=Registry.ROR,
        registry_identifier="0280y9h11",
    )
    OEPS = PIDName(
        name="Open Ephys Production Site",
        abbreviation="OEPS",
        registry=Registry.ROR,
        registry_identifier="007rkz355",
    )
    OLYMPUS = PIDName(
        name="Olympus",
        registry=Registry.ROR,
        registry_identifier="02vcdte90",
    )
    OPTOTUNE = PIDName(name="Optotune")
    OXXIUS = PIDName(name="Oxxius")
    PRIZMATIX = PIDName(name="Prizmatix")
    QUANTIFI = PIDName(name="Quantifi")
    RASPBERRYPI = PIDName(name="Raspberry Pi")
    SEMROCK = PIDName(name="Semrock")
    SCHNEIDER_KREUZNACH = PIDName(name="Schneider-Kreuznach")
    TAMRON = PIDName(name="Tamron")
    THORLABS = PIDName(
        name="Thorlabs",
        registry=Registry.ROR,
        registry_identifier="04gsnvb07",
    )
    TMC = PIDName(name="Technical Manufacturing Corporation", abbreviation="TMC")
    TYMPHANY = PIDName(name="Tymphany")
    VIEWORKS = PIDName(name="Vieworks")
    VORTRAN = PIDName(name="Vortran")
    ZEISS = PIDName(name="Carl Zeiss", registry=Registry.ROR, registry_identifier="01xk5xs43")
    OTHER = PIDName(name="Other")
