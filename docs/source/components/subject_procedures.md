# Subject_procedures

## Model definitions

### GenericSubjectProcedure

Description of a non-surgical procedure performed on a subject

| Field | Type | Title (Description) |
|-------|------|-------------|
| `start_date` | `datetime.date` | Start date  |
| `experimenters` | `Optional[List[str]]` | experimenter(s)  |
| `ethics_review_id` | `str` | Ethics review ID  |
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `description` | `str` | Description  |
| `notes` | `Optional[str]` | Notes  |


### Surgery

Description of subject procedures performed at one time

| Field | Type | Title (Description) |
|-------|------|-------------|
| `protocol_id` | `Optional[str]` | Protocol ID (DOI for protocols.io) |
| `start_date` | `datetime.date` | Start date  |
| `experimenters` | `Optional[List[str]]` | experimenter(s)  |
| `ethics_review_id` | `Optional[str]` | Ethics review ID  |
| `animal_weight_prior` | `Optional[float]` | Animal weight (g) (Animal weight before procedure) |
| `animal_weight_post` | `Optional[float]` | Animal weight (g) (Animal weight after procedure) |
| `weight_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) | Weight unit  |
| `anaesthesia` | Optional[[Anaesthetic](surgery_procedures.md#anaesthetic)] | Anaesthesia  |
| `workstation_id` | `Optional[str]` | Workstation ID  |
| `coordinate_system` | Optional[[CoordinateSystem](coordinates.md#coordinatesystem)] | Surgery coordinate system (Only required when the Surgery.coordinate_system is different from the Procedures.coordinate_system) |
| `measured_coordinates` | Optional[Dict[[Origin](../aind_data_schema_models/coordinates.md#origin), [Translation](coordinates.md#translation)]] | Measured coordinates (Coordinates measured during the procedure, for example Bregma and Lambda) |
| `procedures` | List[[CatheterImplant](surgery_procedures.md#catheterimplant) or [Craniotomy](surgery_procedures.md#craniotomy) or [ProbeImplant](surgery_procedures.md#probeimplant) or [Headframe](surgery_procedures.md#headframe) or [BrainInjection](surgery_procedures.md#braininjection) or [Injection](injection_procedures.md#injection) or [MyomatrixInsertion](surgery_procedures.md#myomatrixinsertion) or [GenericSurgeryProcedure](surgery_procedures.md#genericsurgeryprocedure) or [Perfusion](surgery_procedures.md#perfusion) or [SampleCollection](surgery_procedures.md#samplecollection)] | Procedures  |
| `notes` | `Optional[str]` | Notes  |


### TrainingProtocol

Description of an animal training protocol

| Field | Type | Title (Description) |
|-------|------|-------------|
| `training_name` | `str` | Training protocol name  |
| `protocol_id` | `Optional[str]` | Training protocol ID  |
| `start_date` | `datetime.date` | Training protocol start date  |
| `end_date` | `Optional[datetime.date]` | Training protocol end date  |
| `curriculum_code` | Optional[[Code](identifiers.md#code)] | Curriculum code (Code describing the directed graph used for the training curriculum) |
| `notes` | `Optional[str]` | Notes  |


### WaterRestriction

Description of a water restriction procedure

| Field | Type | Title (Description) |
|-------|------|-------------|
| `ethics_review_id` | `str` | Ethics review ID  |
| `target_fraction_weight` | `int` | Target fraction weight (%)  |
| `target_fraction_weight_unit` | [UnitlessUnit](../aind_data_schema_models/units.md#unitlessunit) | Target fraction weight unit  |
| `minimum_water_per_day` | `float` | Minimum water per day (mL)  |
| `minimum_water_per_day_unit` | [VolumeUnit](../aind_data_schema_models/units.md#volumeunit) | Minimum water per day unit  |
| `baseline_weight` | `float` | Baseline weight (g) (Weight at start of water restriction) |
| `weight_unit` | [MassUnit](../aind_data_schema_models/units.md#massunit) | Weight unit  |
| `start_date` | `datetime.date` | Water restriction start date  |
| `end_date` | `Optional[datetime.date]` | Water restriction end date  |


