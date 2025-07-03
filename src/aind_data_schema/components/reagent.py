"""Classes to define reagents"""

from datetime import date
from typing import List, Optional, Union

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.species import Species
from aind_data_schema_models.units import MassUnit, SizeUnit
from aind_data_schema_models.reagent import StainType, FluorophoreType
from pydantic import Field

from aind_data_schema.base import DataModel, Discriminated


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
    lot_number: Optional[str] = Field(default=None, title="Lot number")
    expiration_date: Optional[date] = Field(default=None, title="Lot expiration date")


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


class ProteinProbe(DataModel):
    """Description of a protein probe including antibodies"""

    protein: PIDName = Field(..., title="Target protein name")
    species: Optional[Species.ONE_OF] = Field(default=None, title="Species of the probe")
    mass: float = Field(..., title="Mass of protein probe (ug)")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")
    sequence: Optional[str] = Field(default=None, title="Amino acid sequence of the probe")


class SmallMoleculeProbe(DataModel):
    """Description of a small molecule probe"""

    molecule: PIDName = Field(..., title="Target small molecule name")
    mass: float = Field(..., title="Mass of small molecule probe (ug)")
    mass_unit: MassUnit = Field(default=MassUnit.UG, title="Mass unit")


class ProbeReagent(Reagent):
    """Description of a probe used as a reagent"""

    target: Union[GeneProbe, ProteinProbe, SmallMoleculeProbe] = Field(..., title="Target")


class FluorescentStain(Reagent):
    """Description of a fluorescent stain"""

    probe: Discriminated[GeneProbe | ProteinProbe | SmallMoleculeProbe] = Field(..., title="Target of the stain")
    stain_type: StainType = Field(..., title="Stain type")
    fluorophore: Fluorophore = Field(..., title="Fluorophore used in the stain")
    initiator_name: Optional[str] = Field(default=None, title="Initiator for HCR probes")
