.. Doc Template documentation master file, created by
   sphinx-quickstart on Wed Aug 17 15:36:32 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to this repository's documentation!
===========================================
This repository describes the schema used to define metadata for Allen 
Institute for Neural Dynamics (AIND) data. All data is accompanied by 
a collection of JSON files that provide detailed information about the
data, how it was acquired, and how it was processed and analyzed. The 
goal of these files is to provide complete experimental details and 
documentation so that all users have a thorough understanding of the 
data.

A given data asset will have the following JSON files:

* **data_description**: Administrative metadata about the source of the data, relevant licenses, and restrictions on use.
* **subject**: Metadata about the subject used in the experiments, including genotype, age, sex, and source.
* **procedures**: Metadata about any procedures performed prior to data acquisition, including surgeries, behavior training, and tissue preparation.
* **rig** or **instrument**: Metadata describing the equipment used to acquire data, including part names, serial numbers, and configuration details.
* **session** or **acquisition**: Metadata describing how the data was acquired
* **processing**: Metadata describing how data has been processed into derived data assets, including information on what software was used.

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
