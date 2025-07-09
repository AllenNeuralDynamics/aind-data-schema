# Generating metadata

## Why

We are gathering this metadata so that our assets will be FAIR (findable, accessible, interoperable, and re-usable).

After completing this tutorial you will be able to:
- Build the data description, subject, and procedures metadata for your asset using Python code and pydantic.
- Describe how a simple set of metadata for a few assets get converted into individual metadata records.
- Navigate the documentation

## Identify metadata sources

In practice, key metadata is usually distributed into many data sources. They could be spreadsheets, databases, TIFF file headers, or even file names. 

In this example, let's say that our basic subject and surgical procedure metadata are stored in an excel workbook with three sheets: `mice`, `sessions`, and `procedures`. 

Let's say they look like this:

`mice`:

```
id  dam_id  sire_id  genotype                                               dob         sex
1                    Vip-IRES-Cre/wt                                        9/22/2023   F
2                    Ai32(RCL-ChR2(H134R)_EYFP)/Ai32(RCL-ChR2(H134R)_EYFP)  9/15/2023   M
3   1       2        Vip-IRES-Cre/wt;Ai32(RCL-ChR2(H134R)_EYFP)/wt          12/1/2023   F
```

`procedures`:

```
mouse_id    injection_date  protocol                brain_area  virus_name           virus_titer  injection_volume  injection_coord     perfusion_date
3	        1/2/2024 7:00   injection-perfusion-v1  VISp        AAV2-Flex-ChrimsonR  2300000000   200               03.8,-0.87,-3.3,10  1/31/2024 10:22
```

`sessions`:

```
mouse_id  start_time       end_time
3         1/26/2024 15:00  1/26/2024 15:30
3         1/27/2024 15:00  1/27/2024 15:30
3         1/28/2024 15:00  1/28/2024 15:30
```

In this example you can see that we recorded three sessions from one mouse, 
which has a viral injection and a perfusion procedure. All mice are C57BL/6J, 
were bred locally, and were housed with a running wheel in their cage. Download 
[example_workflow.xlsx](example_workflow.xlsx) and 
[example_workflow.py](example_workflow.py) to follow along.

## Setup Python environment

First, we'll set up the Python environment and define some shared variables.

```{literalinclude} example_workflow.py
:language: python
:lines: 1-39
```

### How did we know which `aind-data-schema` classes to import?

Our general recommendation for metadata is to navigate the documentation starting from the core class you are working on. So for the data description you would go to that page: [DataDescription](../data_description.md). The import for any object can be read from the URL of the page, core classes are found in the core subfolder `from aind_data_schema.core import DataDescription`.

One of the objects you'll need to build is going to be the [Person](../components/identifiers.md#person). From the [DataDescription](../data_description.md) page you can click-through (we recommend you ctrl+click or command+click to open the link in a new tab) to the [Person](../components/identifiers.md#person) page. Again read the URL to know where to import the file, in this case we're in a subfolder components in the file identifiers `from aind_data_schema.components.identifiers import Person`. After importing the class and populating it in your Python code you can close the extra tab.

Let's move on to build the actual data description now.

## Data description

The data description schema contains basic administrative metadata. Who collected the data, 
how was it funded, etc. We'll define a function to generate this, and re-use it for each of the three sessions.

```{literalinclude} example_workflow.py
:language: python
:lines: 40-55
```

A few of the fields in the data description required us to use enumerated variables, like [DataLevel](../aind_data_schema_models/data_name_patterns.md#datalevel). Controlled vocabularies like this one are used to standardize the metadata and make it easier for people to search across assets from different experiments. We also use controlled vocabularies that are linked to external registries, like for [Organization](../aind_data_schema_models/organizations.md#organization)

## Subject

To create the subject metadata we'll pull some information from the excel spreadsheet and pass it to a function which will return the validated [Subject](../subject.md#subject) object.

Some of the required metadata, like the `cage_id` wasn't available to us. We'll put `"unknown"` in the metadata for that field. Never invent metadata!

```{literalinclude} example_workflow.py
:language: python
:lines: 56-90
```

## Procedures

We'll next write a function that will construct the [Procedures](../procedures.md#procedures) about two surgeries that were performed: a brain injection at a target depth and later (after data acquisition) a perfusion.

```{literalinclude} example_workflow.py
:language: python
:lines: 91-169
```

This is the point at which we need to also discuss the [coordinate systems](../coordinate_systems.md). To know the position of an object or procedure across experiments we need to record position, rotation, and scale information in a standardized system. This step in metadata creation can be a bit intimidating but know that we've created tools to help simplify it! The two things to think about are:

- What was the origin that you used as a reference coordinate? For many animal experiments it's probably bregma on the skull.
- How did you go from the origin to your target coordinate? For many animal experiments you likely used a stereotax and should know the exact anterior-posterior, left-to-right (or medial-lateral), and superior-to-inferior position you went to, plus the depth you moved down along the injection axis. Make sure to also note any rotation you performed and which axis you rotated around.

For most mouse experiments like the one here, the coordinate system used had the origin at Bregma and the axes pointing anterior, right, and inferior (or ventral), plus a depth coordinate. To make your life easier you can import this coordinate system from the library so that you don't have to worry about constructing it yourself.

```
from aind_data_schema.coordinates.components import CoordinateSystemLibrary

coordinate_system = CoordinateSystemLibrary.BREGMA_ARID
```

## Generating metadata

Finally, we're ready to generate all the metadata files. We'll loop over the sessions listed in the excel spreadsheet and use our functions to build the JSON files. The `write_standard_file()` function will take care of writing the files to disk.

```{literalinclude} example_workflow.py
:language: python
:lines: 170-251
```

## Instrument and Acquisition and other metadata

The remaining metadata files needed for an experimental data asset ([Instrument](../../instrument) and [Acquisition](../../acquisition)) follow the same pattern: extract the relevant information from a data source, transform it into the schema, and use the `write_standard_file()` function to construct the output JSON file that will be kept alongside your data asset.

During processing and analysis, you will also generate metadata files for [Processing](../../processing) and [QualityControl](../../quality_control), and possibly a [Model](../../model).
