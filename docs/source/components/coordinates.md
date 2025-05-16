# Coordinates

## Model definitions

### Affine

Definition of an affine transform 3x4 matrix

| Field | Type | Description |
|-------|------|-------------|
| `affine_transform` | `List[List[float]]` |  |


### AngleUnit

Enumeration of Angle Measurements

| Name | Value |
|------|-------|
| `RAD` | `radians` |
| `DEG` | `degrees` |


### Atlas

Definition an atlas

| Field | Type | Description |
|-------|------|-------------|
| `name` | [AtlasName](../aind_data_schema_models/atlas.md#atlasname) |  |
| `version` | `str` |  |
| `size` | `List[float]` |  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `resolution` | `List[float]` |  |
| `resolution_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |
| `origin` | [Origin](../aind_data_schema_models/#origin) | Defines the position of (0,0,0) in the coordinate system |
| `axes` | List[[Axis](#axis)] | Axis names and directions |
| `axis_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |


### AtlasCoordinate

A point in an Atlas

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system` | [Atlas](#atlas) |  |
| `translation` | `List[float]` |  |


### AtlasName

Atlas names

| Name | Value |
|------|-------|
| `CCF` | `CCF` |
| `CUSTOM` | `CUSTOM` |


### Axis

Linked direction and axis

| Field | Type | Description |
|-------|------|-------------|
| `name` | [AxisName](../aind_data_schema_models/#axisname) |  |
| `direction` | [Direction](../aind_data_schema_models/#direction) | Direction of positive values along the axis |


### AxisName

Axis name

| Name | Value |
|------|-------|
| `X` | `X` |
| `Y` | `Y` |
| `Z` | `Z` |
| `AP` | `AP` |
| `ML` | `ML` |
| `SI` | `SI` |
| `DEPTH` | `Depth` |


### CoordinateSystem

Definition of a coordinate system relative to a brain

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `origin` | [Origin](../aind_data_schema_models/#origin) | Defines the position of (0,0,0) in the coordinate system |
| `axes` | List[[Axis](#axis)] | Axis names and directions |
| `axis_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |


### Direction

Local and anatomical directions

| Name | Value |
|------|-------|
| `LR` | `Left_to_right` |
| `RL` | `Right_to_left` |
| `AP` | `Anterior_to_posterior` |
| `PA` | `Posterior_to_anterior` |
| `IS` | `Inferior_to_superior` |
| `SI` | `Superior_to_inferior` |
| `FB` | `Front_to_back` |
| `BF` | `Back_to_front` |
| `UD` | `Up_to_down` |
| `DU` | `Down_to_up` |
| `OTHER` | `Other` |
| `POS` | `Positive` |
| `NEG` | `Negative` |


### NonlinearTransform

Definition of a nonlinear transform

| Field | Type | Description |
|-------|------|-------------|
| `path` | `aind_data_schema.components.wrappers.AssetPath` | Relative path from metadata json to file |


### Origin

Origin positions for coordinate systems

| Name | Value |
|------|-------|
| `ORIGIN` | `Origin` |
| `BREGMA` | `Bregma` |
| `LAMBDA` | `Lambda` |
| `C1` | `C1` |
| `C2` | `C2` |
| `C3` | `C3` |
| `C4` | `C4` |
| `C5` | `C5` |
| `C6` | `C6` |
| `C7` | `C7` |
| `TIP` | `Tip` |
| `FRONT_CENTER` | `Front_center` |
| `ARENA_CENTER` | `Arena_center` |
| `ARENA_FRONT_LEFT` | `Arena_front_left` |
| `ARENA_FRONT_RIGHT` | `Arena_front_right` |
| `ARENA_BACK_LEFT` | `Arena_back_left` |
| `ARENA_BACK_RIGHT` | `Arena_back_right` |


### Rotation

Rotation

Rotations are applied as Euler angles in order X/Y/Z

Angles follow right-hand rule, with positive angles rotating counter-clockwise.

| Field | Type | Description |
|-------|------|-------------|
| `angles` | `List[float]` | Right-hand rule, positive angles rotate CCW |
| `angles_unit` | [AngleUnit](../aind_data_schema_models/units.md#angleunit) |  |


### Scale

Scale

| Field | Type | Description |
|-------|------|-------------|
| `scale` | `List[float]` |  |


### SizeUnit

Enumeration of Length Measurements

| Name | Value |
|------|-------|
| `M` | `meter` |
| `CM` | `centimeter` |
| `MM` | `millimeter` |
| `UM` | `micrometer` |
| `NM` | `nanometer` |
| `IN` | `inch` |
| `PX` | `pixel` |


### Translation

Translation

| Field | Type | Description |
|-------|------|-------------|
| `translation` | `List[float]` |  |


