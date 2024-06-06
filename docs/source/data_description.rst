FAQ: Data description
=====================

**Q: What is the data description file?**

This tracks administrative information about a data asset, including affiliated researchers/organizations, projects,
data modalities, dates of collection, and more.

**Q: How do I create the data description?**

The data description is created during data transfer based on information you provide to that service and pulling 
information from internal resources.

**Q: What is the difference between modality and platform?**

Modalities are types of data being collected. A platform is a standardized way of collecting one or more modalities of 
data that we give a name. Platform standardization -- of file formats, hardware setup, etc -- enables us automatically 
and reliably process data with centrally managed data pipelines. 

    Example 1: the behavior platform leverages Harp and Bonsai to run behavioral experiments and acquire multiple 
    modalities of data (behavior videos, electrophysiology, photometry, etc). 

    Example 2: We use SmartSPIM lightsheet microscopes to collect whole-mesoscale whole brain neuroanatomy data. This 
    is a single-modality (SPIM) platform (mesoscale anatomy, SmartSPIM colloquially).

**Q: What platform should I use?**

There is a controlled vocabulary in aind-data-schema-models. Pick the one that most closely aligns with how you have
collected data. If none exists, talk to Saskia de Vries or David Feng.

**Q: This data is for a AIND project and not part of a grant. Shouldn’t the funder be AIND?**

No. The funding for internally funded AIND or AIBS work is listed as “Allen Institute”.

**Q: I got a new grant! How do I make sure this grant information will get integrated into the metadata?**

Congratulations! The funding information is pulled from the Funding Smartsheet that Shelby maintains. Work with Shelby 
to make sure your grant is on that sheet.
    