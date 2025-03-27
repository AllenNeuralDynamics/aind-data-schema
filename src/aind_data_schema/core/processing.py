"""schema for processing"""

from enum import Enum
from typing import List, Literal, Optional, Union
from pathlib import Path

from aind_data_schema_models.process_names import ProcessName
from aind_data_schema_models.units import MemoryUnit, UnitlessUnit
from pydantic import Field, SkipValidation, ValidationInfo, field_validator, model_validator

from aind_data_schema.base import (
    DataCoreModel,
    GenericModel,
    GenericModelType,
    DataModel,
    AwareDatetimeWithDefault,
)
from aind_data_schema.core.metadata import ExternalLinks
from aind_data_schema.components.identifiers import Person, Code
from aind_data_schema.utils.merge import merge_notes


class ProcessStage(str, Enum):
    """Stages of processing"""

    PROCESSING = "Processing"
    ANALYSIS = "Analysis"


class ResourceTimestamped(DataModel):
    """Description of resource usage at a moment in time"""

    timestamp: AwareDatetimeWithDefault = Field(..., title="Timestamp")
    usage: float = Field(..., title="Usage")


class ResourceUsage(DataModel):
    """Description of resources used by a process"""

    os: str = Field(..., title="Operating system")
    architecture: str = Field(..., title="Architecture")
    cpu: Optional[str] = Field(default=None, title="CPU name")
    cpu_cores: Optional[int] = Field(default=None, title="CPU cores")
    gpu: Optional[str] = Field(default=None, title="GPU name")
    system_memory: Optional[float] = Field(default=None, title="System memory")
    system_memory_unit: Optional[MemoryUnit] = Field(default=None, title="System memory unit")
    ram: Optional[float] = Field(default=None, title="System RAM")
    ram_unit: Optional[MemoryUnit] = Field(default=None, title="Ram unit")

    cpu_usage: Optional[List[ResourceTimestamped]] = Field(default=None, title="CPU usage")
    gpu_usage: Optional[List[ResourceTimestamped]] = Field(default=None, title="GPU usage")
    ram_usage: Optional[List[ResourceTimestamped]] = Field(default=None, title="RAM usage")
    usage_unit: str = Field(default=UnitlessUnit.PERCENT, title="Usage unit")


class DataAsset(DataModel):
    """Description of a single data asset"""

    url: str = Field(..., title="Asset location", description="URL pointing to the data asset")


class CombinedData(DataModel):
    """Description of multiple data assets"""

    assets: List[DataAsset] = Field(..., title="Data assets", min_items=1)
    name: Optional[str] = Field(default=None, title="Name")
    external_links: ExternalLinks = Field(
        default=dict(), title="External Links", description="Links to the Combined Data asset, if materialized."
    )
    description: Optional[str] = Field(
        default=None, title="Description", description="Intention or approach used to select group of assets"
    )


class Provenance(DataModel):
    """Description of provenance of processing results"""

    code: Code = Field(..., title="Code used for processing")
    inputs: List[Union[DataAsset, CombinedData, Path]] = Field(
        ...,
        title="Input locations",
        description=(
            "Inputs can be a single DataAsset, a CombinedData object, ",
            "and/or the name of a preceding DataProcess.",
        ),
    )


class DataProcess(DataModel):
    """Description of a single processing step"""

    type: ProcessName = Field(..., title="Process type")
    name: str = Field(
        default="",
        title="Name",
        description=("Unique name of the processing step.", " If not provided, the type will be used as the name."),
    )
    stage: ProcessStage = Field(..., title="Processing stage")
    provenance: Provenance = Field(..., title="Provenance")
    owners: List[Person] = Field(..., title="owners", description="People responsible for processing")
    pipeline_steps: Optional[List[str]] = Field(
        default=None,
        title="Pipeline steps",
        description=(
            "For pipeline processes (ProcessName.PIPELINE), steps should indicate the DataProcess objects",
            " that are part of the pipeline. Each object must show up in the data_processes list.",
        ),
    )
    start_date_time: AwareDatetimeWithDefault = Field(..., title="Start date time")
    end_date_time: AwareDatetimeWithDefault = Field(..., title="End date time")
    output_path: Optional[Path] = Field(
        default=None, title="Output path", description="Path to processing outputs, if stored."
    )
    output_parameters: GenericModelType = Field(
        default=GenericModel(), description="Output parameters", title="Outputs"
    )
    notes: Optional[str] = Field(default=None, title="Notes", validate_default=True)
    resources: Optional[ResourceUsage] = Field(default=None, title="Process resource usage")

    @field_validator("notes", mode="after")
    def validate_other(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validator for other/notes"""

        if info.data.get("type") == ProcessName.OTHER and not value:
            raise ValueError(
                "Notes cannot be empty if 'type' is Other. Describe the type of processing in the notes field."
            )
        return value

    @model_validator(mode="after")
    def fill_default_name(self) -> "DataProcess":
        """Fill in default name if not provided"""

        if not self.name:
            self.name = self.type
        return self


class Processing(DataCoreModel):
    """Description of all processes run on data"""

    _DESCRIBED_BY_URL: str = DataCoreModel._DESCRIBED_BY_BASE_URL.default + "aind_data_schema/core/processing.py"
    describedBy: str = Field(default=_DESCRIBED_BY_URL, json_schema_extra={"const": _DESCRIBED_BY_URL})
    schema_version: SkipValidation[Literal["2.0.25"]] = Field(default="2.0.25")

    data_processes: List[DataProcess] = Field(..., title="Data processing")
    notes: Optional[str] = Field(default=None, title="Notes")

    # why not mode="after"?
    @model_validator(mode="before")
    @classmethod
    def validate_pipeline_steps(cls, values):
        """Validator for pipeline_steps"""

        if not values.get("data_processes"):
            # No data processes, this is probably a test asset
            return values

        data_processes = values["data_processes"]
        # Coerce types if needed
        try:
            data_processes = [
                DataProcess(**process) if not isinstance(process, DataProcess) else process
                for process in data_processes
            ]
        except Exception as e:
            raise ValueError(f"data_processes should be a list of DataProcess objects or dictionaries. {e}")

        process_names = [process.name for process in data_processes]
        # Validate that all processes have a unique name
        if len(process_names) != len(set(process_names)):
            raise ValueError("data_processes must have unique names.")

        for process in data_processes:
            # For each process, make sure it's either a pipeline and has all its processes downstream

            if process.type == ProcessName.PIPELINE:

                if not hasattr(process, "pipeline_steps") or not process.pipeline_steps:
                    raise ValueError("Pipeline processes should have a pipeline_steps attribute.")

                # Validate that all steps show up in the data_processes list
                for step in process.pipeline_steps:
                    if step not in process_names:
                        raise ValueError(f"Pipeline step '{step}' not found in data_processes.")
            # Or make sure it doesn't have any pipeline steps
            elif hasattr(process, "pipeline_steps") and process.pipeline_steps:
                raise ValueError("pipeline_steps should only be provided for ProcessName.PIPELINE processes.")

        return values

    def __add__(self, other: "Processing") -> "Processing":
        """Combine two Processing objects"""

        # Check for incompatible schema_version
        if self.schema_version != other.schema_version:
            raise ValueError("Cannot add Processing objects with different schema versions.")

        return Processing(
            data_processes=self.data_processes + other.data_processes, notes=merge_notes(self.notes, other.notes)
        )
