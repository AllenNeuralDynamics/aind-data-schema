=================
Data organization
=================

``aind-data-schema`` validates and write JSON files containing metadata. We store those
JSON files in a particular directory structure to support our ability to rapidly and openly
share data. 
 
Core principles
===============

**Immutability**

Derived data cannot affect input data. This is essential for reproducibility.
All data, once produced, should be treated as “read only”. Derived processes 
cannot change input data. This means no appending information to input files, 
and no adding files to existing directories. 

**Acquisition sessions first**

The fundamental logical unit for primary data is the acquisition session (time).  

There are many ways to logically group data. We group all data acquired at the
same time. This is for two reasons:

First, it is helpful to logically group data that directly affect each other. The 
treadmill data stream is tightly coupled to the video capturing the body of the 
mouse, which naturally affects neural activity. Grouping these simultaneously 
collected data streams together helps users to understand the data they process 
and analyze. 

Second, organizing by session (time) facilitates immutable rapid sharing. Were 
we to share data at the project or dataset level, our ability to share would be 
dependent on difficult decisions that depend on the project’s intended use of the 
data. For example, waiting to release data that all meet the quality control 
criteria defined by a particular project assumes that those criteria apply to all
potential uses of the data.  

**Flat structure**

We avoid using hierarchies to encode metadata. Grouping data into hierarchies via 
directories - or implied hierarchies with complex ordered file naming conventions - is
a common practice to facilitate search. However, any type of hierarchy dramatically 
impacts how data can be used. Grouping data by project makes it difficult to find data
by modality. Grouping data by modality makes it difficult to find data by mouse.  

A flat structure organized by time is unopinionated about what metadata will be most 
useful. We will instead rely on flexible database queries to facilitate data discovery 
along any dimension, rather than biasing in favor of one field or another. 

**Processing is a session**

Processing sessions are analogous to primary data acquisition sessions.  Processed data 
files should therefore be logically grouped together, separate from primary data. 
Timestamping processed results allows us to flexibly reprocess without affecting primary
data. The generic term we use to describe acquisition sessions and processing sessions
is the data asset.  

We could consider separate data assets for different processing pipeline steps (e.g. one
asset for stitching transforms, one asset for fused results, one asset for segmented neurons, 
etc). However, at this point that seems like unnecessary complexity. 

**Standard processing, flexible analysis**

We define processing as basic feature extraction - spike sorting for electrophysiology, 
limb positions extracted from behavior videos, cell positions from light microscopy.  

Analysis is taking processed features and using them to answer a scientific question. 
For physiology, the NWB file is a key marker between processing and analysis. 

We separate data processing and analysis to facilitate flexible use of data. Whereas 
analytical use of processing features can vary widely, what features will be generally useful 
is often constrained and well-understood (though they are rarely easy to generate).   

Processing results must be represented in community-standard formats (NWB-Zarr, OME-Zarr). 
Analysis results can also be captured in standard formats, when applicable, and internally
consistent formats when standards don’t exist. 


Primary data conventions 
========================

All data acquired in a single acquisition session will be stored together. This
group needs a name, but it must be as simple as possible. It is critical that this
name be unique, but we should not use this name to encode essential metadata.  

All primary data assets have the following naming convention: 

    <platform-abbreviation>_<subject-id>_<acquisition-date>_<acquisition-time>

A platform is a standardized system for collecting one or more modalities of data. 

A few points: 

- ``<acquisition-date>``: yyyy-mm-dd at end of acquisition  
- ``<acquisition-time>``: hh-mm-ss at end of acquisition 
- Acquisition date and time are essential for uniqueness
- Acquisition date and time are in local time zone 
- Time-zone is documented in metadata 
- All tokens (e.g. ``<platform-abbreviation>``, ``<subject-id>``) must not contain underscores or illegal filename characters. 
- ``<platform-abbreviation>``: a less-than 10 character shorthand for a data acquisition platform 

Again, this name is strictly for uniqueness. We could use a GUID, but choose 
to have a relatively simple naming convention to facilitate casual browsing. 

Primary data assets are organized as follows:

    - <asset name>  
        - data_description.json (administrative information, funders, licenses, projects, etc) 
        - subject.json (species, sex, DOB, unique identifier, genotype, etc) 
        - procedures.json (subject surgeries, tissue preparation, water restriction, training protocols, etc) 
        - instrument.json/rig.json (static hardware components) 
        - acquisition.json/session.json (device settings that change acquisition-to-acquisition) 
        - <modality-1>  
            - <list of data files>  
        - <modality-2>  
            - <list of data files> 
        - <modality-n> 
            - <list of data files> 
        - derivatives (processed data generated during acquisition) 
            - <label> (e.g. MIP) 
                - <list of files>
        - logs (general log files generated by the instrument or rig that are not modality-specific) 
            - <list of files> 

Platform abbreviation and modality terms come from controlled vocabularies in aind-data-schema-models. 

Example for simultaneous electrophysiology with optotagging and fiber photometry:

    - EFIP_655568_2022-04-26_11-48-09
        - <metadata JSON files> 
        - FIB 
            - L415_2022-04-26T11_48_09.csv 
            - L470_2022-04-26T11_48_09.csv 
            - L560_2022-04-26T11_48_09.3024512-07_00 
            - Raw2022-04-26T11_48_09.csv 
            - TTL_2022-04-26T11_48_08.1780864-07_00 
            - TTL_TS2022-04-26T11_48_08.csv 
            - TimeStamp_2022-04-26T11_48_08.csv 
        - ecephys 
            - 220426114809_655568.opto.csv 
            - Record Node 104 
                - <files>
        - behavior-videos 
            - face_camera.mp4 
            - body_camera.mp4 

Example for lightsheet microscopy data acquired on the ExaSPIM platform:

    - exaSPIM_655568_2022-04-26_11-48-09
        - <metadata JSON files> 
        - SPIM 
            - SPIM.ome.zarr 
        - derivatives 
            - MIP  
                - <list of e.g. tiff files> 

Derived data conventions
========================

Anything computed in a single run should be logically grouped in a folder. The folder should be named: 

    <primary-asset-name>_<process-label>_<process-date>_<process-time>

For example:

- ``exaSPIM_ANM457202_2022-07-11_22-11-32_processed_2022-08-11_22-11-32``
- ``ecephys_595262_2022-02-21_15-18-07_processed_2022-08-11_22-11-32``

Processed outputs are usually the result of a multi-stage pipeline, so often <process-label> should 
just be “processed.” Other common process labels include: 

- ``curation`` - tags assigned to input data (e.g. merge/split/noise calls for ephys units) 
- ... 

Overlong names are difficult to read, so do not daisy-chain. The goal is to keep names as simple 
as possible while being readable, not to encode all metadata or the entire provenance chain. If 
various stages of processing are being performed manually over extended periods of time, anchor 
each derived asset on the primary data asset. 

Processed result folder organization is as follows:

    - <asset name> 
        - data_description.json 
        - processing.json (describes the code, input parameters, outputs) 
        - subject.json (copied from primary asset) 
        - procedures.json (copied from primary asset) 
        - instrument.json (copied from primary asset) 
        - acquisition.json (copied from primary asset) 
        - <process-label-1>  
            - <list of files> 
        - <process-label-2> 
            - <list of files> 
        - <process-label-n> 
            - <list of files> 

File name guidelines 
====================

When naming files, we should: 

- use terms from vocabularies defined in aind-data-schema, e.g. 
    - platform names and modalities behavior video file names 
    - use “yyyy-mm-dd" and “hh-mm-ss" in local time zone for dates and times 
- separate tokens with underscores, and not include underscores in tokens, e.g. 
    - Do this: ``EFIP_655568_2022-04-26_11-48-09``
    - Not this: ``EFIP-655568-2022_04_26-11_48_09``
- Do not include illegal filename characters in tokens 

