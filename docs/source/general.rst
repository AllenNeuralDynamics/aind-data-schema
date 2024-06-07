General metadata
================

**Q: What is metadata?**

Metadata is data about data. This documents the information about the data that enables us to be able to analyze and 
interpret it well. We use our metadata to document the entire process of creating data, the provenance of that data as 
it moves through processing and analysis workflows, and the quality of the data. We use this metadata to keep track of 
the data assets and to communicate the embodied context of those data.

**Q: What metadata files are needed for each data asset?**

Each data asset needs:

* Data description
* Subject
* Procedures
* Instrument or Rig
* Acqusition or Session
* Processing

The contents of these will get compiled into a metadata.nd.json file by the data transfer service.

**Q: Which fields do I have to provide within these?**

All required (non-optional) fields must be completed to create a “valid model”. 

**Q: Can I skip fields that are optional?**

Optional fields should be included whenever possible but are not required. The reason some fields are optional is 
usually because they aren’t universal, and so the pertinent question is whether those fields apply to your 
experiments/devices/etc and not about whether you can ignore things because you don’t want to provide them.

**Q: If I don’t know something (e.g. the serial number of my device) can I just make something up?**

A: No. Fake metadata is harmful. 

**Q: Who is responsible for making sure the metadata is accurate?**

You are. Even with metadata service and tools, you need to make sure the information attached to your data is 
accurate and that any issues get resolved. Please reach out with questions if you are unclear about the schema, 
but you are responsibile for the content.

**Q: Whom should I contact with questions or issues?**

Questions about the schema should be directed to Saskia de Vries. If you have github issues you can add them to the 
repo for the Data Infrastructure team to review and address. Questions about correcting errors in metadata that 
you've already attached to your data should be directed to David Feng.

**Q: What are the registries that are referenced in the schema?**

When possible, we use persistent identifiers (PIDs) to specify metadata features. This affords precision and clarity 
and allows richer information in public databases to be accessible. Our list of registries will grow as we incorporate 
more ontologies into our schema. We currently use:

* NCBI Taxonomy to specify species
* Research Organization Registry (ROR) to specify organizations (including manufacturer, funders, research organizations)
* Open Researcher and Contributor ID (ORCID) to identify investigators
* Research Resource Identifiers (RRID) to identify reagents and other resources
* Addgene to identify viruses and plasmids
* Mouse Genome Informatics (MGI) to identify transgenic alleles
