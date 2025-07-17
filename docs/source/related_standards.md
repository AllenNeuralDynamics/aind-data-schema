# Related Standards

There are an overwhelming number of data standards across the life sciences aligned to various biological subdomains and communities. While it may be clear how any particular piece of data aligns with these standards, no standard spans the diversity and scale of data being collected at the Allen Institute.

`aind-data-schema` is intentionally unopinionated about how images, arrays, time series, and data frames should be represented in files. Because it decouples metadata representation from data representation, `aind-data-schema` is able to integrate with other formats in the field easily. We designed `aind-data-schema` to specifically align well with Neurodata Without Borders (NWB), OME-NGFF, and the Brain Imaging Data Structure (BIDS).

## NWB

[Neurodata Without Borders (NWB)](https://nwb.org/) is a data standard for neurophysiology, providing neuroscientists with a common standard to share, archive, use, and build common analysis tools for neurophysiology data. The NWB standard describes how neurophysiology data should be organized in array file formats (either HDF5 or Zarr) and provides locations for a limited amount of metadata to describe experimental conditions.

`aind-data-schema` describes significantly more metadata. We are actively developing an NWB extension ([ndx-aind-metadata](https://github.com/AllenNeuralDynamics/ndx-aind-metadata)) that can directly package aind-data-schema metadata into NWB.

## OME-NGFF

[OME-NGFF](https://ngff.openmicroscopy.org/) is an imaging format specification designed to support massively parallel reading and writing of petascale image data. The OME-NGFF standard describes how imaging data should be arranged in files, including multiresolution image pyramids. OME-NGFF also contains a metadata standard that focuses on microscope configuration.

`aind-data-schema` describes significantly more metadata. We plan to develop a utility for packaging aind-data-schema metadata into OME-NGFF files, setting common fields as appropriate.

## BIDS

The [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/) is a file and folder naming convention and a metadata standard. AIND organizes our files similarly to the BIDS organization, and many of our metadata concepts align with BIDS.

The primary reason we cannot use BIDS directly is that the file organization is inherently mutable. As new acquisitions are produced, many metadata files must change as they describe the entire group. aind-data-schema is scoped specifically to a single data acquisition.

## Croissant

[Croissant](https://mlcommons.org/working-groups/data/croissant/) is a metadata format that describes how data (arrays, time series, tables) are laid out in files in such a way that they can be easily read into common machine learning frameworks like PyTorch, TensorFlow, and JAX. It contains a few unconstrained metadata fields to describe fields, columns, etc.

`aind-data-schema` contains fields that align with array field names (for example, the name of a fiber implanted in a certain location is in procedures.json, and that name will also show up in photometry readout files), but `aind-data-schema` avoids describing the outer and inner layouts of files and focuses instead on broader experimental metadata.

## Hugging Face

[Hugging Face](https://huggingface.co/) is a platform for hosting and running machine learning models. It has a schema for model metadata that is used to facilitate model discovery and visualization on their web page. The `aind-data-schema` model schema extends the core concepts there to cover more detailed descriptions of model architecture, training conditions, and more.