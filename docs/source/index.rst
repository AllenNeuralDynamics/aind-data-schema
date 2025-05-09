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

Controlled vocabularies
-----------------------

``aind-data-schema`` relies on controlled vocabularies. We store these controlled vocabularies in a separate repository: `aind-data-schema-models <https://github.com/AllenNeuralDynamics/aind-data-schema-models>`_.

Flexibility, versioning, and upgrading
--------------------------------------

``aind-data-schema`` is versioned using `Semantic Versioning <https://semver.org/>`_. The core schemas listed above 
also have their own version numbers, which are documented in the ``schema_version`` field of any JSON file 
they are used to generate.

When new versions of schemas are released, data collectors can decide if they want to update the metadata
from their existing data assets to the new schema. Metadata upgrading capabilities can be found in 
`aind-metadata-upgrader <https://github.com/allenneuraldynamics/aind-metadata-upgrader>`_.

Related metadata standards
--------------------------

Community standards like NWB, OME, and BIDS are essential. ``aind-data-schema`` complements these standards, adding new concepts and detail as needed to support AIND's discovery science. 


.. toctree::
   :caption: Data and Metadata
   :hidden:
   :maxdepth: 1

   general
   data_organization
   


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
   :caption: Getting Started
   :hidden:
   :maxdepth: 1
   
   example_workflow/example_workflow


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
