Welcome to aind-data-schema 
===========================

`Code repository <https://github.com/allenNeuralDynamics/aind-data-schema>`_


Data acquired at the Allen Institute for Neural Dynamics (AIND) is accompanied by metadata describing how it was acquired, processed, and analyzed. This metadata is stored in JSON files according to the schema defined in this library. Our goal in capturing this metadata is to make our data findable and understandable.

Data assets acquired from a live subject or in vivo specimen must contain the following *core* metadata files:

- :doc:`data_description <data_description>`: Administrative metadata about the source of the data, funding, relevant licenses, and restrictions on use.
- :doc:`subject <subject>`: Species, genotype, age, sex, and source.
- :doc:`procedures <procedures>`: Metadata about any procedures performed prior to data acquisition, including subject procedures (surgeries, behavior training, etc.) and specimen procedures (tissue preparation, staining, etc.).
- :doc:`instrument <instrument>`: Metadata describing the equipment used to acquire data, including part names, serial numbers.
- :doc:`acquisition <acquisition>`: Metadata describing what devices were active during acquisition and their configuration.

After data analysis, additional processing and quality control metadata is captured:

- :doc:`processing <processing>`: Metadata describing how data has been processed and analyzed into derived data assets, including information on the software and parameters used.
- :doc:`quality_control <quality_control>`: Evaluations and metrics describing the quality of a data asset.
- :doc:`model <model>`: Metadata describing machine learning models created from or used to analyze data assets.

Finally the *core* files are pulled together into a single `metadata.json` file:

- :doc:`metadata <metadata>`: The combined set of core files, plus the asset location (e.g. on S3).

The *core* files are built from many smaller schema objects. These are stored in the components and registries. Registries are specifically used for schema objects that are part of a controlled vocabulary. Some registries are linked to external standards.

- :doc:`components <components>`: Component schemas used to build up the core files (devices, configurations, etc).
- :doc:`registries <registries>`: Component schemas that are part of a controlled vocabulary.

I want to...
------------

- :doc:`Create metadata for my data assets <example_workflow/example_workflow>`. 
- :doc:`Create metadata using the AIND metadata-mapper <todo>`. 
- :doc:`Learn about the philosophy behind aind-data-schema<general>`.
- :doc:`Learn about how coordinate systems work<coordinate_systems>`.
- `Report an issue or request an addition to the metadata schema <https://github.com/AllenNeuralDynamics/aind-data-schema/issues>`_.
- `Build my own changes to the metadata schema <https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/CONTRIBUTING.md>`_.


.. toctree::
   :caption: Getting Started
   :hidden:
   :maxdepth: 1
   
   example_workflow/example_workflow
   

.. toctree::
   :caption: Core Schemas
   :hidden:
   :maxdepth: 1

   data_description
   subject
   procedures
   instrument
   acquisition
   processing
   quality_control
   model
   metadata
   

.. toctree::
   :caption: Component Schemas
   :hidden:
   :maxdepth: 2

   components
   registries


.. toctree::
   :caption: Philosophy
   :hidden:
   :maxdepth: 1

   general
   coordinate_systems
   related_standards
