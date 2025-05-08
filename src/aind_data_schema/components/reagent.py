"""Classes to define reagents"""

from datetime import date
from enum import Enum
from typing import List, Optional

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.species import Species
from aind_data_schema_models.units import ConcentrationUnit, MassUnit, SizeUnit
from pydantic import Field

from aind_data_schema.base import DataModel


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


class Readout(Reagent):
    """Description of a readout"""

    fluorophore: Fluorophore = Field(..., title="Fluorophore")
    excitation_wavelength: int = Field(..., title="Excitation wavelength (nm)")
    excitation_wavelength_unit: SizeUnit = Field(default=SizeUnit.NM, title="Excitation wavelength unit")
    stain_type: StainType = Field(..., title="Stain type")


class HCRReadout(Readout):
    """Description of a readout for HCR"""

    initiator_name: str = Field(..., title="Initiator name")
    stain_type: StainType = Field(..., title="Stain type")


class OligoProbe(Reagent):
    """Description of an oligonucleotide probe"""

    species: Species.ONE_OF = Field(..., title="Species")
    gene: PIDName = Field(..., title="Gene name, accession number, and registry")
    probe_sequences: List[str] = Field(..., title="Probe sequences")
    readout: Readout = Field(..., title="Readout")


class HCRProbe(OligoProbe):
    """Description of an oligo probe used for HCR"""

    initiator_name: str = Field(..., title="Initiator name")
    readout: HCRReadout = Field(..., title="Readout")


class Stain(Reagent):
    """Description of a non-oligo probe stain"""

    concentration: float = Field(..., title="Concentration")
    concentration_unit: ConcentrationUnit = Field(default=ConcentrationUnit.UM, title="Concentration unit")


class Antibody(Reagent):
    """Description of an antibody used in immunolableing"""

    immunolabel_class: ImmunolabelClass = Field(..., title="Immunolabel class")
    fluorophore: Optional[Fluorophore] = Field(default=None, title="Fluorophore")
    mass: float = Field(..., title="Mass of antibody")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")
    notes: Optional[str] = Field(default=None, title="Notes")
