################
Open Data Access
################

The Allen Institute for Neural Dynamics (AIND) is committed to FAIR, Open, 
and Reproducible science. We therefore share all of the data we collect publicly 
with rich metadata as near to the time of collection as possible. We share data 
at all stages of the data lifecycle, including preliminary data collected 
during methods development, processed data that we are actively improving,
or highly curated data used in a publication.

In addition to sharing curated datasets with modality-specific NIH data archives 
like `DANDI <https://dandiarchive.org/>`_ and `BIL <https://www.brainimagelibrary.org/>`_, 
we are also excited to share all of our data in one public S3 bucket generously 
hosted by the `Registry of Open Data on AWS <https://registry.opendata.aws/>`_. 

All data is stored here: ``s3://aind-open-data``

*******************
Bucket Organization
*******************

AIND's mission to share data early with full reproducibility has significant 
implications on how data and metadata should be organized and represented. Specifically:

* derived data should not be stored in the same path or directory as source data
* metadata should be represented in simple human- and machine-readable files
* metadata should be adjacent to the data it describes
* data should be stored in cloud-friendly formats (e.g. Zarr), preferably at time of acquisition

Based on these principles, ``s3://aind-open-data`` is organized as a flat list of
data assets, where a data asset is simply a logical collection of files. Raw data assets 
are named:

``<modality>_<subject-id>_<acquisition-date>_<acquisition-time>``

Derived data assets are named:

``<source-data-asset-name>_<label>_<acquisition-date>_<acquisition-time>``

Inspired by `BIDS <https://bids.neuroimaging.io/>`_ and the 
`HCA metadata schema <https://data.humancellatlas.org/metadata/structure>`_, metadata 
describing a data asset is stored as sidecar JSON files that conform to the schemas 
defined in ``aind-data-schema``. 

A raw extracellular ephys asset would look like this:

.. code-block:: text

    ecephys_123456_2022-12-12_05-06-07/
        ecephys/<ephys data>
        behavior/<video data>
        data_description.json
        subject.json
        procedures.json
        processing.json
        rig.json
        acquisition.json

A spike-sorting result asset would look like this:

.. code-block:: text

    ecephys_123456_2022-12-12_05-06-07_sorted-ks25_2022-12-12_06-07-08/
        sorted/<sorted ephys data>
        data_description.json
        subject.json
        procedures.json
        processing.json
        rig.json
        acquisition.json







