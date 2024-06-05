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

As experimental and analytical methods continue to develop, and new
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

   from datetime import datetime, timezone

   from aind_data_schema_models.organizations import Organization
   from aind_data_schema_models.species import Species

   from aind_data_schema.core.subject import BreedingInfo, Housing, Sex, Subject

   t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

   s = Subject(
      species=Species.MUS_MUSCULUS,
      subject_id="12345",
      sex=Sex.MALE,
      date_of_birth=t.date(),
      source=Organization.AI,
      breeding_info=BreedingInfo(
         breeding_group="Emx1-IRES-Cre(ND)",
         maternal_id="546543",
         maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
         paternal_id="232323",
         paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
      ),
      genotype="Emx1-IRES-Cre/wt;Camk2a-tTA/wt;Ai93(TITL-GCaMP6f)/wt",
      housing=Housing(home_cage_enrichment=["Running wheel"], cage_id="123"),
      background_strain="C57BL/6J",
   )
   serialized = s.model_dump_json()
   deserialized = Subject.model_validate_json(serialized)
   deserialized.write_standard_file()

yields JSON:

.. code-block:: json

   {
      "describedBy": "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/core/subject.py",
      "schema_version": "0.5.8",
      "subject_id": "12345",
      "sex": "Male",
      "date_of_birth": "2022-11-22",
      "genotype": "Emx1-IRES-Cre/wt;Camk2a-tTA/wt;Ai93(TITL-GCaMP6f)/wt",
      "species": {
         "name": "Mus musculus",
         "abbreviation": null,
         "registry": {
            "name": "National Center for Biotechnology Information",
            "abbreviation": "NCBI"
         },
         "registry_identifier": "10090"
      },
      "alleles": [],
      "background_strain": "C57BL/6J",
      "breeding_info": {
         "breeding_group": "Emx1-IRES-Cre(ND)",
         "maternal_id": "546543",
         "maternal_genotype": "Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
         "paternal_id": "232323",
         "paternal_genotype": "Ai93(TITL-GCaMP6f)/wt"
      },
      "source": {
         "name": "Allen Institute",
         "abbreviation": "AI",
         "registry": {
            "name": "Research Organization Registry",
            "abbreviation": "ROR"
         },
         "registry_identifier": "03cpe7c52"
      },
      "rrid": null,
      "restrictions": null,
      "wellness_reports": [],
      "housing": {
         "cage_id": "123",
         "room_id": null,
         "light_cycle": null,
         "home_cage_enrichment": [
            "Running wheel"
         ],
         "cohoused_subjects": []
      },
      "notes": null
   }


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   diagrams
   modules
   faq
      general
      data description
      subject
      procedures
      rig/instrument
      session
      acquisition
      processing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
