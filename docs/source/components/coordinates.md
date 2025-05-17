# Coordinates

## Model definitions

### Affine

Definition of an affine transform 3x4 matrix

| Field | Type | Description |
|-------|------|-------------|
| `affine_transform` | `List[List[float]]` |  |


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
| `origin` | [Origin](../aind_data_schema_models/coordinates.md#origin) | Defines the position of (0,0,0) in the coordinate system |
| `axes` | List[[Axis](#axis)] | Axis names and directions |
| `axis_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |


### AtlasCoordinate

A point in an Atlas

| Field | Type | Description |
|-------|------|-------------|
| `coordinate_system` | [Atlas](#atlas) |  |
| `translation` | `List[float]` |  |


### Axis

Linked direction and axis

| Field | Type | Description |
|-------|------|-------------|
| `name` | [AxisName](../aind_data_schema_models/coordinates.md#axisname) |  |
| `direction` | [Direction](../aind_data_schema_models/coordinates.md#direction) | Direction of positive values along the axis |


### CoordinateSystem

Definition of a coordinate system relative to a brain

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` |  |
| `origin` | [Origin](../aind_data_schema_models/coordinates.md#origin) | Defines the position of (0,0,0) in the coordinate system |
| `axes` | List[[Axis](#axis)] | Axis names and directions |
| `axis_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) |  |


### NonlinearTransform

Definition of a nonlinear transform

| Field | Type | Description |
|-------|------|-------------|
| `path` | `AssetPath` | Relative path from metadata json to file |


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


### Translation

Translation

| Field | Type | Description |
|-------|------|-------------|
| `translation` | `List[float]` |  |


