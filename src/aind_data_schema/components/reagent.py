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


class Fluorophore(str, Enum):
    """Fluorophores used in HCR and Immunolabeling"""

    ALEXA_405 = "Alexa Fluor 405"
    ALEXA_488 = "Alexa Fluor 488"
    ALEXA_546 = "Alexa Fluor 546"
    ALEXA_568 = "Alexa Fluor 568"
    ALEXA_594 = "Alexa Fluor 594"
    ALEXA_633 = "Alexa Fluor 633"
    ALEXA_647 = "Alexa Fluor 647"
    ATTO_488 = "ATTO 488"
    ATTO_565 = "ATTO 565"
    ATTO_643 = "ATTO 643"
    CY3 = "Cyanine Cy 3"


class Reagent(DataModel):
    """Description of reagent used in procedure"""

    name: str = Field(..., title="Name")
    source: Organization.ONE_OF = Field(..., title="Source")
    rrid: Optional[PIDName] = Field(default=None, title="Research Resource ID")
    lot_number: str = Field(..., title="Lot number")
    expiration_date: Optional[date] = Field(default=None, title="Lot expiration date")


class Stain(Reagent):
    """Description of a non-oligo probe stain"""

    stain_type: StainType = Field(..., title="Stain type")
    concentration: float = Field(..., title="Concentration")
    concentration_unit: ConcentrationUnit = Field(default=ConcentrationUnit.UM, title="Concentration unit")


class Antibody(Reagent):
    """Description of an antibody used in immunolableing"""

    immunolabel_class: ImmunolabelClass = Field(..., title="Immunolabel class")
    fluorophore: Optional[Fluorophore] = Field(default=None, title="Fluorophore")
    mass: float = Field(..., title="Mass of antibody")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")
    notes: Optional[str] = Field(default=None, title="Notes")


# Gene-targeting oligonucleotide probes


class OligoProbe(DataModel):
    """Description of an oligonucleotide probe"""

    name: str = Field(..., title="Name")
    sequence: str = Field(..., title="Sequence")


class GeneProbes(DataModel):
    """Description of a set of oligonucleotide probes targeting a specific gene"""

    gene: PIDName = Field(..., title="Gene name")
    probes: List[OligoProbe] = Field(..., title="Probes")


class OligoProbeSet(Reagent):
    """set of probes used in BarSEQ"""

    gene_probes: List[GeneProbes] = Field(..., title="Gene probes")
    # IDT scale stuff?


class Readout(Reagent):
    """Description of a readout"""

    fluorophore: Fluorophore = Field(..., title="Fluorophore")
    excitation_wavelength: int = Field(..., title="Excitation wavelength (nm)")
    excitation_wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Excitation wavelength unit")
    stain_type: StainType = Field(..., title="Stain type")


class HCRReadout(Readout):
    """Description of a readout for HCR"""

    initiator_name: str = Field(..., title="Initiator name")


class GeneticStain(Reagent):
    """Description of an oligonucleotide probe(s) targeting a gene and readout"""

    gene_probe: GeneProbes = Field(..., title="Gene probe")
    readout: Discriminated[Readout | HCRReadout] = Field(..., title="Readout")
    species: Species.ONE_OF = Field(..., title="Species")
