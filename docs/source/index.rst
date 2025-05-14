Welcome to aind-data-schema 
===========================

Data acquired at the Allen Institute for Neural Dynamics (AIND) is accompanied by metadata describing how it was acquired, processed, and analyzed. This metadata is stored in JSON files according to the schema defined in this library. Our goal in capturing this metadata is to make our data findable and understandable.

Data assets acquired from a live subject or in vivo specimen must contain the following JSON files:

- :doc:`data_description <data_description>`: Administrative metadata about the source of the data, funding, relevant licenses, and restrictions on use.
- :doc:`subject <subject>`: Species, genotype, age, sex, and source.
- :doc:`procedures <procedures>`: Metadata about any procedures performed prior to data acquisition, including subject procedures (surgeries, behavior training, etc.) and specimen procedures (tissue preparation, staining, etc.).
- :doc:`instrument <instrument>`: Metadata describing the equipment used to acquire data, including part names, serial numbers.
- :doc:`acquisition <acquisition>`: Metadata describing what devices were active during acquisition and their configuration.

After data analysis, additional quality control and processing metadata is captured:

- :doc:`processing <processing>`: Metadata describing how data has been processed and analyzed into derived data assets, including information on the software and parameters used.
- :doc:`quality_control <quality_control>`: Evaluations and metrics describing the quality of a data asset.

The metadata also covers models that are derived from data or used to analyze data:

- :doc:`model <model>`: Metadata describing how the data has been evaluated for quality control.

I want to...
------------

- :doc:`Create metadata for my data assets <example_workflow/example_workflow>`. 
- :doc:`Query metadata<query>`.
- :doc:`Learn about the philosophy behind aind-data-schema<general>`.


Components and Registries
-------------------------

``aind-data-schema`` relies on many individual components as well as controlled vocabularies. The components are stored in their own files. We store these controlled vocabularies in a separate repository: `aind-data-schema-models <https://github.com/AllenNeuralDynamics/aind-data-schema-models>`_.

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
   

.. toctree::
   :caption: Components
   :hidden:
   :maxdepth: 2

   components

.. toctree::
   :caption: Registries
   :hidden:
   :maxdepth: 2

   registries


.. toctree::
   :caption: Data and Metadata
   :hidden:
   :maxdepth: 1

   general
   data_organization
