Data description
================

The `data_description.json` file tracks administrative information about a data asset, including affiliated researchers/organizations, projects,
data modalities, dates of collection, and more.

**Q: What is the difference between modality and platform?**

Modalities are types of data being collected. A platform is a standardized way of collecting one or more modalities of 
data that we give a name. Platform standardization -- of file formats, hardware setup, etc -- enables us automatically 
and reliably process data with centrally managed data pipelines. 

    Example 1: the behavior platform leverages Harp and Bonsai to run behavioral experiments and acquire multiple 
    modalities of data (behavior videos, electrophysiology, photometry, etc). 

    Example 2: We use SmartSPIM lightsheet microscopes to collect whole-mesoscale whole brain neuroanatomy data. This 
    is a single-modality (SPIM) platform (mesoscale anatomy, SmartSPIM colloquially).
