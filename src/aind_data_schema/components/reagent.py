"""Classes to define reagents"""

from datetime import date
from enum import Enum
from typing import List, Optional

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.species import Species
from aind_data_schema_models.units import ConcentrationUnit, MassUnit, SizeUnit
from pydantic import Field

from aind_data_schema.base import DataModel, Discriminated


class ImmunolabelClass(str, Enum):
    """Type of antibodies"""

    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    CONJUGATE = "Conjugate"


class StainType(str, Enum):
    """Stain types for probes describing what is being labeled"""

    RNA = "RNA"
    NUCLEAR = "Nuclear"
    FILL = "Fill"


class FluorophoreType(str, Enum):
    """Fluorophores types"""

    ALEXA = "Alexa Fluor"
    ATTO = "Atto"
    CF = "CF"
    CYANINE = "Cyanine"
    DYLIGHT = "DyLight"


class Fluorophore(DataModel):
    """Flurophore used in HCR, Immunolabeling, etc"""

    fluorophore_type: FluorophoreType = Field(..., title="Fluorophore type")
    excitation_wavelength: int = Field(..., title="Excitation wavelength (nm)")
    excitation_wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Excitation wavelength unit")


class Reagent(DataModel):
    """Description of reagent used in procedure"""

    name: str = Field(..., title="Name")
    source: Organization.ONE_OF = Field(..., title="Source")
    rrid: Optional[PIDName] = Field(default=None, title="Research Resource ID")
    lot_number: str = Field(..., title="Lot number")
    expiration_date: Optional[date] = Field(default=None, title="Lot expiration date")


# Gene-targeting oligonucleotide probes


class OligoProbe(DataModel):
    """Description of an oligonucleotide probe"""

    name: str = Field(..., title="Name")
    sequence: str = Field(..., title="Sequence")


class GeneProbe(DataModel):
    """Description of a set of oligonucleotide probes targeting a specific gene"""

    gene: PIDName = Field(..., title="Gene name")
    probes: Optional[List[OligoProbe]] = Field(default=None, title="Probes")


class GeneProbeSet(Reagent):
    """set of probes used in BarSEQ"""

    gene_probes: List[GeneProbe] = Field(..., title="Gene probes")


class ProteinProbe(Reagent):
    """Description of a protein probe including antibodies"""

    protein: PIDName = Field(..., title="Target protein name")
    mass: float = Field(..., title="Mass of protein probe (ug)")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")
    sequence: Optional[str] = Field(default=None, title="Amino acid sequence of the probe")


class SmallMoleculeProbe(Reagent):
    """Description of a small molecule probe"""

    molecule: PIDName = Field(..., title="Target small molecule name")
    mass: float = Field(..., title="Mass of small molecule probe (ug)")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")


class FluorescentStain(Reagent):
    """Description of a fluorescent stain"""

    target: Discriminated[GeneProbe | ProteinProbe | SmallMoleculeProbe] = Field(..., title="Target of the stain")
    stain_type: StainType = Field(..., title="Stain type")
    fluorophore: Fluorophore = Field(..., title="Fluorophore used in the stain")
    species: Optional[Species] = Field(default=None, title="Species targeted by the stain")