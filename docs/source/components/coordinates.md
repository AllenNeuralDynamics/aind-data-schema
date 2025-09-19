# Coordinates

## Model definitions

### Affine

Definition of an affine transform 3x4 matrix

| Field | Type | Title (Description) |
|-------|------|-------------|
| `affine_transform` | `List[List[float]]` | Affine transform matrix  |


### Atlas

Definition an atlas

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | [AtlasName](../aind_data_schema_models/atlas.md#atlasname) | Atlas name  |
| `version` | `str` | Atlas version  |
| `size` | `List[float]` | Size  |
| `size_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `resolution` | `List[float]` | Resolution  |
| `resolution_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Resolution unit  |
| `origin` | [Origin](../aind_data_schema_models/coordinates.md#origin) | Origin (Defines the position of (0,0,0) in the coordinate system) |
| `axes` | List[[Axis](#axis)] | Axis names (Axis names and directions) |
| `axis_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |


### AtlasCoordinate

A point in an Atlas

| Field | Type | Title (Description) |
|-------|------|-------------|
| `coordinate_system` | [Atlas](#atlas) | Atlas  |
| `translation` | `List[float]` | Translation parameters  |


### Axis

Linked direction and axis

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | [AxisName](../aind_data_schema_models/coordinates.md#axisname) | Axis  |
| `direction` | [Direction](../aind_data_schema_models/coordinates.md#direction) | Direction (Direction of positive values along the axis) |


### CoordinateSystem

Definition of a coordinate system relative to a brain

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Name  |
| `origin` | [Origin](../aind_data_schema_models/coordinates.md#origin) | Origin (Defines the position of (0,0,0) in the coordinate system) |
| `axes` | List[[Axis](#axis)] | Axis names (Axis names and directions) |
| `axis_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |


### NonlinearTransform

Definition of a nonlinear transform

| Field | Type | Title (Description) |
|-------|------|-------------|
| `path` | `AssetPath` | Path to nonlinear transform file (Relative path from metadata json to file) |


### Rotation

Rotation

Rotations are applied as Euler angles in order X/Y/Z

Angles follow right-hand rule, with positive angles rotating counter-clockwise.

| Field | Type | Title (Description) |
|-------|------|-------------|
| `angles` | `List[float]` | Angles and axes in 3D space (Right-hand rule, positive angles rotate CCW) |
| `angles_unit` | [AngleUnit](../aind_data_schema_models/units.md#angleunit) | Angle unit  |


### Scale

Scale

| Field | Type | Title (Description) |
|-------|------|-------------|
| `scale` | `List[float]` | Scale parameters  |


### Translation

Translation

| Field | Type | Title (Description) |
|-------|------|-------------|
| `translation` | `List[float]` | Translation parameters  |


