# Coordinate Systems

The metadata schema supports flexible definitions of coordinate systems, both relative to anatomy and devices. This allows us to store the positions of devices, insertion coordinates, etc, all with one standardized system of metadata.

Unlike many parts of the metadata schema it is important to understand **how coordinate systems are stored** to be able to use them properly. There are just two rules to be aware of:

1. Each [Instrument](instrument.md), [Acquisition](acquisition.md), and [Procedures](procedures.md) has its own `.coordinate_system` field. These can be identical, or different, depending on your needs.
2. Any transform (i.e. a [Translation](components/coordinates.md#translation), [Rotation](components/coordinates.md#rotation), or [Scale](components/coordinates.md#scale)) defined for a device or configuration of a device **must be defined in it's core file's coordinate system**. To help you avoid mistakes, transform fields are paired with a `.coordinate_system_name` field and the coordinate system name must match the name of the coordinate system defined in the metadata.

For a few special cases like coordinates in an [Atlas](components/coordinates.md#atlas) the coordinate system and transform are defined at the same time. For these configurations the new coordinate system overrides the one defined in the core file.

## CoordinateSystem

A [CoordinateSystem](components/coordinates.md#coordinatesystem) is defined by an [Origin](aind_data_schema_models/coordinates.md#origin) and a list of axis and direction pairs. The name of a coordinate system is created by combining the origin and positive directions of the axes. For example, `BREGMA_ARI` is a coordinate system with an origin at bregma and three axes pointing anterior, right, and inferior. This is made explicit in the full definition:

```{code} python
CoordinateSystem(
    name="BREGMA_ARI",
    origin=Origin.BREGMA,
    axis_unit=SizeUnit.UM,
    axes=[
        Axis(name=AxisName.AP, direction=Direction.PA),
        Axis(name=AxisName.ML, direction=Direction.LR),
        Axis(name=AxisName.SI, direction=Direction.SI),
    ],
)
```

This matches the image below:

<div align="center">
    <img src="_static/coordinates2.png" alt="BREGMA_ARI Coordinate System" width="50%">
</div>

## Origin

An [Origin](aind_data_schema_models/coordinates.md#origin) is a point in space, often relative to the mouse's anatomy but it can also be a point on a device. Standard anatomical references are positions like Bregma or Lambda

<div align="center">
    <img src="_static/bregma_and_lambda2.png" alt="BREGMA_ARI Coordinate System" width="50%">
</div>

## Axis definitions

Each [Axis](components/coordinates.md#axis) is a combination of an [AxisName](aind_data_schema_models/coordinates.md#axisname) and [Direction](aind_data_schema_models/coordinates.md#direction).

## CoordinateSystemLibrary

We know that allowing complete flexibility with coordinate systems will be a source of confusion. With that in mind, we encourage everybody to use the `CoordinateSystemLibrary` class, which comes with a pre-defined set of standard coordinate systems. For example, you can import the `BREGMA_ARI` coordinate system and then re-use it as follows:

```{code} python
from aind_data_schema.components.coordinates import CoordinateSystemLibrary

...

coordinate_system = CoordinateSystemLibrary.BREGMA_ARI
coordinate_system_name = CoordinateSystemLibrary.BREGMA_ARI.name
```

You can request additions to the library by opening an [issue](https://github.com/AllenNeuralDynamics/aind-data-schema/issues).
