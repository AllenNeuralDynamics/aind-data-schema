# Subject_procedures

## Model definitions

### GenericSubjectProcedure

Description of a non-surgical procedure performed on a subject

| Field | Type | Description |
|-------|------|-------------|
| `start_date` | `datetime.date` |  |
| `experimenters` | `Optional[List[str]]` |  |
| `ethics_review_id` | `str` |  |
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `description` | `str` |  |
| `notes` | `Optional[str]` |  |


### Surgery

Description of subject procedures performed at one time

| Field | Type | Description |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | DOI for protocols.io |
| `start_date` | `datetime.date` |  |
| `experimenters` | `Optional[List[str]]` |  |
| `ethics_review_id` | `Optional[str]` |  |
| `animal_weight_prior` | `Optional[float]` | Animal weight before procedure |
| `animal_weight_post` | `Optional[float]` | Animal weight after procedure |
| `weight_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) |  |
| `anaesthesia` | Optional[[Anaesthetic](surgery_procedures.md#anaesthetic)] |  |
| `workstation_id` | `Optional[str]` |  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Only required when the Surgery.coordinate_system is different from the Procedures.coordinate_system |
| `measured_coordinates` | Optional[Dict[[Origin](../aind_data_schema_models/coordinates.md#origin), [Translation](coordinates.md#translation)]] | Coordinates measured during the procedure, for example Bregma and Lambda |
| `procedures` | List[[CatheterImplant](surgery_procedures.md#catheterimplant) or [Craniotomy](surgery_procedures.md#craniotomy) or [ProbeImplant](surgery_procedures.md#probeimplant) or [Headframe](surgery_procedures.md#headframe) or [BrainInjection](surgery_procedures.md#braininjection) or [Injection](injection_procedures.md#injection) or [MyomatrixInsertion](surgery_procedures.md#myomatrixinsertion) or [GenericSurgeryProcedure](surgery_procedures.md#genericsurgeryprocedure) or [Perfusion](surgery_procedures.md#perfusion) or [SampleCollection](surgery_procedures.md#samplecollection)] |  |
| `notes` | `Optional[str]` |  |


### TrainingProtocol

Description of an animal training protocol

| Field | Type | Description |
|-------|------|-------------|
| `training_name` | `str` |  |
| `protocol_id` | `Optional[str]` |  |
| `start_date` | `datetime.date` |  |
| `end_date` | `Optional[datetime.date]` |  |
| `curriculum_code` | Optional[[Code](identifiers.md#code)] | Code describing the directed graph used for the training curriculum |
| `notes` | `Optional[str]` |  |


### WaterRestriction

Description of a water restriction procedure

| Field | Type | Description |
|-------|------|-------------|
| `ethics_review_id` | `str` |  |
| `target_fraction_weight` | `int` |  |
| `target_fraction_weight_unit` | [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) |  |
| `minimum_water_per_day` | `float` |  |
| `minimum_water_per_day_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) |  |
| `baseline_weight` | `float` | Weight at start of water restriction |
| `weight_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) |  |
| `start_date` | `datetime.date` |  |
| `end_date` | `Optional[datetime.date]` |  |


