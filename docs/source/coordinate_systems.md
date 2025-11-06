# Coordinate systems

The metadata schema supports flexible definitions of coordinate systems, both relative to anatomy and devices. This allows us to store the positions of devices, insertion coordinates, etc, all with one standardized system.

Unlike many parts of the metadata schema where fields are just floats or strings, it is critical to understand **how coordinate systems are stored in the schema** to be able to use them properly. There are two rules to be aware of:

1. Each [Instrument](instrument.md), [Acquisition](acquisition.md), and [Procedures](procedures.md) has its own `.coordinate_system` field. In most assets, the coordinate system is the same in all three files.
2. Any transform (i.e. a [Translation](components/coordinates.md#translation), [Rotation](components/coordinates.md#rotation), or [Scale](components/coordinates.md#scale)) defined for a device or configuration of a device **must be defined in it's core file's coordinate system**. To help you avoid mistakes, transform fields are paired with a `.coordinate_system_name` field and the coordinate system name must match the name of the coordinate system defined in the core file.

The top-level coordinate systems in the instrument, acquisition, and procedures are generally defined in *in vivo* space, usually relative to an origin on an animal's skull. Often when targeting coordinates in the brain we plan our experiments in a **standardized atlas** like the mouse common coordinate framework. When you encounter a field that that requires an atlas transform (i.e. a point or vector in an atlas), you'll see that an [Atlas](components/coordinates.md#atlas) will have to be defined alongside that transform. An Atlas library is available in `aind_data_schema.components.coordinates.AtlasLibrary` for your convenience.

## CoordinateSystem

A [CoordinateSystem](components/coordinates.md#coordinatesystem) is defined by an [Origin](aind_data_schema_models/coordinates.md#origin) and a list of [AxisName](aind_data_schema_models/coordinates.md#axisname) and [Direction](aind_data_schema_models/coordinates.md#direction) pairs. The name of a coordinate system is created by combining the origin and positive directions of the axes. For example, `BREGMA_ARI` is a coordinate system with an origin at bregma and three axes pointing anterior, right, and inferior. This is made explicit in the full definition:

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

### Origin

An [Origin](aind_data_schema_models/coordinates.md#origin) is a point in space, often relative to the mouse's anatomy but it can also be a point on a device. Standard anatomical references are positions like Bregma or Lambda

<div align="center">
    <img src="_static/bregma_and_lambda2.png" alt="BREGMA_ARI Coordinate System" width="50%">
</div>

### Axis

Each [Axis](components/coordinates.md#axis) is a combination of an [AxisName](aind_data_schema_models/coordinates.md#axisname) and [Direction](aind_data_schema_models/coordinates.md#direction).

### Units

Each [CoordinateSystem](components/coordinates.md#coordinatesystem) defines its origin, axis direction, and units. All of this information is inherited by the [Translation](components/coordinates.md#translation), [Rotation](components/coordinates.md#rotation), and [Scale](components/coordinates.md#scale) transforms that are applied. The only exception is for rotations, where we ask you to specify for each rotation the units (degrees or radians). 

#### 3D vs 4D and Depth

Because skull shapes vary across animals the most useful coordinates to re-create insertions across animals are often the AP/ML position of the entry coordinate and then the "depth", i.e. the insertion distance of the tip of the inserted device from the brain (or dura) surface, whether a probe, fiber, needle, whatever. To support these kinds of insertions we include a depth axis option.

In most cases users should report the coordinates of the *entry coordinate* at the brain/dura surface using the first three (AP, ML, SI) values and then the depth *from the brain/dura surface* in the fourth depth coordinate. Recording all three coordinates disambiguates between the two ways that a probe can be "dropped" to the brain surface (either along the SI axis or down the probe depth axis). You can also use a 3-dimensional coordinate system (AP, ML, Depth) but we don't recommend it, since you need to either report in a protocol or in the notes how you dropped from the AP/ML plane down to the brain surface.

Note that in general, the process by which you perform an insertion should be recorded in a protocol, especially if there are specific details a user would need to know about how to interpret coordinates.

### CoordinateSystemLibrary

We know that allowing complete flexibility with coordinate systems will be a source of confusion. With that in mind, we encourage everybody to use the `CoordinateSystemLibrary` class, which comes with a pre-defined set of standard coordinate systems. For example, you can import the `BREGMA_ARI` coordinate system and then re-use it as follows:

```{code} python
from aind_data_schema.components.coordinates import CoordinateSystemLibrary

...

coordinate_system = CoordinateSystemLibrary.BREGMA_ARI
coordinate_system_name = CoordinateSystemLibrary.BREGMA_ARI.name
```

You can always define your own coordinate system. If you find yourself re-using a coordinate system that isn't available in the library across multiple projects, please request an update to the library by opening an [issue](https://github.com/AllenNeuralDynamics/aind-data-schema/issues).

## Measured Coordinates

During a [Surgery](components/subject_procedures.md#surgery) requiring stereotaxic coordinates the surgeon will typically reference the stereotax or insertion device to a known coordinate, almost always Bregma. It's useful at this time to also measure the relative position of other known landmarks, like Lambda. The `Surgery.measured_coordinates` field is intended to store this data, for example for a surgery in the BREGMA_ARI coordinate system and where Lambda is measured 4.1 mm posterior to Bregma you would include:

```{code} python
measured_coordinates = {
    Origin.LAMBDA: Translation(translation=[-4.1, 0, 0])
}
```

Some notes: the position is *negative* because in BREGMA_ARI the AP axis points positive in the anterior direction, the other two axes are zero because this skull has apparently already been leveled, and finally no units are included in the translation itself because they are implied by the coordinate system, see [units](#units) above.

## Rotations

Rotations are applied using the [scipy Euler angle conventions](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html#scipy.spatial.transform.Rotation.from_euler), in "xyz" order. Positive angles rotate counter-clockwise.

It can be complicated to translate your rotations into the default conventions in situations where you aren't in control of the coordinate system definition. In that situation, it is preferable to construct an affine rotation matrix directly and pass it using the [Affine](components/coordinates.md#affine) object.

## Device transforms

To understand the position and orientation of a **device** in an instrument requires knowing three things: (1) the coordinate system for the instrument, (2) the coordinate system for the device, and (3) the coordinate system transform i.e. how a point in one coordinate system is translated, rotated, and scaled to the other. For example, a [CameraAssembly](components/devices.md#cameraassembly) is a positioned device: it has three special fields `relative_position`, `coordinate_system`, and `transform`. The relative position is required for all positioned devices while the transform and coordinate system are only required when a device's exact position will have an impact on the interpretation/analysis of data.

### Relative Position

For devices where the exact position is not important or is unknown, simply tell us where the device is *roughly* relative to the origin. By combining several [AnatomicalRelative](aind_data_schema_models/coordinates.md#anatomicalrelative) directions in a list, for example `[AnatomicalRelative.ANTERIOR, AnatomicalRelative.SUPERIOR]`, etc, you can describe the position.

### Exact Position

The transform we require for devices is the device to instrument transform. I.e. given the origin of the device (0, 0, 0) and the three axis directions, what will be the position of the origin and what direction will the three axes point in the instrument's coordinate system.

#### Building an exact position from scratch

The easiest way to construct the exact position is to start by drawing two pictures of your device. First, draw your device in the instrument coordinate system at the origin. Define a "neutral" position: for example, a monitor at neutral might be facing posterior as if the mouse is looking at it. Select an origin coordinate for the device, a logical point for a monitor is the center of the screen. Then, define this device coordinate system by adding axis direction information matching the picture you drew so that the X, Y, and Z axes are matched between your instrument coordinate system and the device. Assuming that our instrument coordinate system is BREGMA_ARI, i.e. +X = +Anterior, +Y = +Right, and +Z = +Inferior, then our monitor should be defined as:

```{code} python
CoordinateSystem(
    name="MONITOR_BRU",
    origin=Origin.FRONT_CENTER,
    axis_unit=SizeUnit.MM,
    axes=[
        Axis(name=AxisName.X, direction=Direction.FB),
        Axis(name=AxisName.Y, direction=Direction.LR),
        Axis(name=AxisName.Z, direction=Direction.DU),
    ],
)
```

The device is now defined in the instrument coordinate system, but at a physically impossible location overlapping the mouse. Now draw a second picture, which is the actual location of your mouse. In our case, lets assume that this monitor is facing the mouse's right eye, at a 45 degree angle (i.e. the eye to monitor vector is perpendicular to the monitor surface.), and at a viewing distance of 100 mm.

To do this we first translate the monitor to the correct position by applying `Translation(translation=70.7, 70.7, 0)`. Then, we rotate *clockwise* around the Z axis by applying `Rotation(angles=[0, 0, -45], angles_unit=AngleUnit.DEG)`.
