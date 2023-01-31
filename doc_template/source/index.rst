.. Doc Template documentation master file, created by
   sphinx-quickstart on Wed Aug 17 15:36:32 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aind-data-schema: 
============================

This repository contains the schema used to define metadata for Allen 
Institute for Neural Dynamics (AIND) data. All data is accompanied by 
a collection of JSON files that include the metadata that provide detailed 
information about the data, how it was acquired, and how it was processed 
and analyzed. The metadata also including administrative information 
including licenses and restrictions on publication. The purpose of these 
files is to provide complete experimental details and documentation so 
that all users have a thorough understanding of the data. 

As experimental and anaytical methods continue to develop, and new 
experiments and projects are added to the AIND portfolio, these schema
will continue to evolve in order to capture the full range of our work.

A given data asset will have the following JSON files:

* **data_description**: Administrative metadata about the source of the data, relevant licenses, and restrictions on use.
* **subject**: Metadata about the subject used in the experiments, including genotype, age, sex, and source.
* **procedures**: Metadata about any procedures performed prior to data acquisition, including surgeries, behavior training, and tissue preparation.
* **rig** or **instrument**: Metadata describing the equipment used to acquire data, including part names, serial numbers, and configuration details.
* **session** or **acquisition**: Metadata describing how the data was acquired
* **processing**: Metadata describing how data has been processed into derived data assets, including information on what software was used.

Example
=======

An example subject file:

.. code-block:: python

   from aind_data_schema import Subject
   import datetime

   t = datetime.datetime(2022, 11, 22, 8, 43, 00)

   s = Subject(
      species="Mus musculus",
      subject_id="12345",
      sex="Male",
      date_of_birth=t.date(),
      genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
      home_cage_enrichment="other",
      background_strain="C57BL/6J",
   )

   with open("subject.json", "w") as f:
      f.write(s.json(indent=3))

yields JSON:

.. code-block:: json

   {
      "describedBy": "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/subject.py",
      "schema_version": "0.2.2",
      "species": "Mus musculus",
      "subject_id": "12345",
      "sex": "Male",
      "date_of_birth": "2022-11-22",
      "genotype": "Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
      "mgi_allele_ids": null,
      "background_strain": "C57BL/6J",
      "source": null,
      "rrid": null,
      "restrictions": null,
      "breeding_group": null,
      "maternal_id": null,
      "maternal_genotype": null,
      "paternal_id": null,
      "paternal_genotype": null,
      "light_cycle": null,
      "home_cage_enrichment": "other",
      "wellness_reports": null,
      "notes": null
   }

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   opendata

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
