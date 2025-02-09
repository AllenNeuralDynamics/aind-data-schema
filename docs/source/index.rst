.. Doc Template documentation master file, created by
   sphinx-quickstart on Wed Aug 17 15:36:32 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aind-data-schema 
===========================

This repository contains the schema used to define metadata for Allen 
Institute for Neural Dynamics (AIND) data. All data is accompanied by 
a collection of JSON files that include the metadata that provide detailed 
information about the data, how it was acquired, and how it was processed 
and analyzed. The metadata also including administrative information 
including licenses and restrictions on publication. The purpose of these 
files is to provide complete experimental details and documentation so 
that all users have a thorough understanding of the data. 

As experimental and analytical methods continue to develop, and new
experiments and projects are added to the AIND portfolio, these schema
will continue to evolve in order to capture the full range of our work.

A given data asset will have the following JSON files:

- :doc:`data_description <data_description>`: Administrative metadata about the source of the data, funding, relevant licenses, and restrictions on use.
- :doc:`subject <subject>`: Metadata about the subject used in the experiments, including genotype, age, sex, and source.
- :doc:`procedures <procedures>`: Metadata about any procedures performed prior to data acquisition, including subject procedures (surgeries, behavior training, etc.) and specimen procedures (tissue preparation, staining, etc.).
- :doc:`rig <rig>` or :doc:`instrument <rig>`: Metadata describing the equipment used to acquire data, including part names, serial numbers, and configuration details.
- :doc:`session <session>` or :doc:`acquisition <acquisition>`: Metadata describing how the data was acquired
- :doc:`processing <processing>`: Metadata describing how data has been processed and analyzed into derived data assets, including information on the software and parameters used for processing and analysis.
- :doc:`quality_control <quality_control>`: Metadata describing how the data has been evaluated for quality control.

Example
=======

An example subject file:

.. literalinclude:: ../../examples/subject.py
   :language: python
   :caption: Example JSON File

yields JSON:

.. literalinclude:: ../../examples/subject.json
   :language: json
   :caption: Example JSON File

Flexibility, versioning, and upgrading
--------------------------------------

``aind-data-schema`` is versioned using `Semantic Versioning <https://semver.org/>`_. The core schemas listed above 
also have their own version numbers, which are documented in the ``schema_version`` field of any JSON file 
they are used to generate. Documenting the schema version in this way allows users to know
how to interpret the files. 

Schema versioning in this way is essential for flexibility. As science evolves, new concepts and nomenclature
will emerge or replace existing terms. By versioning the schema, we can ensure that data assets are always
tagged with the appropriate metadata at the time they were acquired. 

When a new version of a schema is released, data collectors can decide if they want to update the metadata
from their existing data assets to the new schema. As needed we add metadata upgrading capabilities to 
`aind-metadata-upgrader <https://github.com/allenneuraldynamics/aind-metadata-upgrader>`_. This python library
is not comprehensive - it contains only the upgrade functions that have been needed to date.

Controlled vocabularies
-----------------------

``aind-data-schema`` relies heavily on controlled vocabularies to validate metadata. Because these grow over time,
we don't want adding e.g. a manufacturer to constitute a new revision of the schema. We therefore store many 
controlled vocabularies in a separate repository: `aind-data-schema-models <https://github.com/AllenNeuralDynamics/aind-data-schema-models>`_.

Related metadata standards
--------------------------

Community standards like NWB, OME, and BIDS are essential. ``aind-data-schema`` intends to complement these standards,
adding new concepts or detail as needed to support AIND's discovery science. 

As ``aind-data-schema`` stabilizes we will build dedicated integrations with community standards. For example, we would 
build NWB extension that easily embeds metadata not covered by the core NWB schema. 


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
   rig
   session
   acquisition
   processing
   quality_control


.. toctree::
   :caption: Getting Started
   :hidden:
   :maxdepth: 1
   
   example_workflow/example_workflow


.. toctree::
   :caption: API Reference
   :hidden:
   :maxdepth: 1

   diagrams
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
