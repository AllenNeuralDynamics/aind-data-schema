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
| `handedness` | Optional[[Handedness](#handedness)] | Handedness (Whether the coordinate system is right-handed or left-handed) |


### AtlasCoordinate

A point in an Atlas

| Field | Type | Title (Description) |
|-------|------|-------------|
| `coordinate_system` | [Atlas](#atlas) | Atlas  |
| `translation` | `List[float]` | Translation parameters  |
| `frame` | [TransformFrame](#transformframe) | Reference frame (Extrinsic applies in the global frame; intrinsic applies in the local device frame) |


### Axis

Linked direction and axis

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | [AxisName](../aind_data_schema_models/coordinates.md#axisname) | Axis  |
| `direction` | [Direction](../aind_data_schema_models/coordinates.md#direction) | Direction (Direction of positive values along the axis) |


### CoordinateSystem

Definition of a coordinate system

| Field | Type | Title (Description) |
|-------|------|-------------|
| `name` | `str` | Name  |
| `origin` | [Origin](../aind_data_schema_models/coordinates.md#origin) | Origin (Defines the position of (0,0,0) in the coordinate system) |
| `axes` | List[[Axis](#axis)] | Axis names (Axis names and directions) |
| `axis_unit` | [SizeUnit](../aind_data_schema_models/units.md#sizeunit) | Size unit  |
| `handedness` | Optional[[Handedness](#handedness)] | Handedness (Whether the coordinate system is right-handed or left-handed) |


### Handedness

Coordinate system handedness

| Name | Value |
|------|-------|
| `RIGHT` | `right` |
| `LEFT` | `left` |


### NonlinearTransform

Definition of a nonlinear transform

| Field | Type | Title (Description) |
|-------|------|-------------|
| `path` | `AssetPath` | Path to nonlinear transform file (Relative path from metadata json to file) |


### Rotation

Rotation

Rotations are applied as Euler angles in the specified axis order.

The default convention is extrinsic (fixed global axes), right-hand rule (positive angles rotate
counter-clockwise when looking along the positive axis), xyz axis order, pivoting around the global origin.

| Field | Type | Title (Description) |
|-------|------|-------------|
| `angles` | `List[float]` | Angles and axes in 3D space (Right-hand rule, positive angles rotate CCW) |
| `angles_unit` | [AngleUnit](../aind_data_schema_models/units.md#angleunit) | Angle unit  |
| `axis_order` | `str` | Axis order (Order of rotation axes as a string (e.g. 'xyz', 'zyx'). Must match the length of angles.) |
| `frame` | [TransformFrame](#transformframe) | Reference frame (Extrinsic applies around fixed global axes; intrinsic applies around the rotating local axes) |
| `rotation_direction` | [RotationDirection](#rotationdirection) | Rotation direction (Right-hand rule: positive angles rotate CCW when looking along the positive axis) |
| `pivot` | [RotationPivot](#rotationpivot) | Rotation pivot (Whether to rotate around the global origin or the local origin of the device) |


### RotationDirection

Rotation direction convention

| Name | Value |
|------|-------|
| `RIGHT_HAND` | `right_hand` |
| `LEFT_HAND` | `left_hand` |


### RotationPivot

Rotation pivot point

| Name | Value |
|------|-------|
| `GLOBAL_ORIGIN` | `global_origin` |
| `LOCAL_ORIGIN` | `local_origin` |


### Scale

Scale

| Field | Type | Title (Description) |
|-------|------|-------------|
| `scale` | `List[float]` | Scale parameters  |


### TransformFrame

Reference frame for applying transforms

| Name | Value |
|------|-------|
| `EXTRINSIC` | `extrinsic` |
| `INTRINSIC` | `intrinsic` |


### Translation

Translation

| Field | Type | Title (Description) |
|-------|------|-------------|
| `translation` | `List[float]` | Translation parameters  |
| `frame` | [TransformFrame](#transformframe) | Reference frame (Extrinsic applies in the global frame; intrinsic applies in the local device frame) |


