===================
Metadata in general
===================

**Q: What is metadata?**

Metadata is data about data. This documents information about acquired data that enables us to be able to analyze and 
interpret it well. We use our metadata to document the entire process of creating data, the provenance of that data as 
it moves through processing and analysis workflows, and the quality of the data. We use this metadata to keep track of 
the data assets and to communicate the embodied context of those data.

**Q: My data files already contain some of this metadata. Why store this in additional JSON files?**

How acquisition software represents metadata evolves over time and often does not capture 
everything we need to know to interpret data. These JSON files represent our ground truth 
viewpoint on what is essential to know about our data in a single location. 

Additionally, JSON files are trivially both human- and machine-readable. They are viewable on 
any system without additional software to be installed (a text editor is fine). They are easy 
to parse from code without any heavy dependencies (IGOR, H5PY, pynwb, etc). 

**Q: Why JSON rather than CSV, YAML, or a SQL database?**

There are many ways to store metadata. JSON is a common format, as are CSV, YAML, and others.
CSV is ubiquitous but its tabular structure makes it difficult to represent complex biological
data with many relationships. YAML is perhaps more human-readable than JSON, but the tooling
around YAML is a bit less mature than JSON. 

Databases are very important for reliable and performant querying, however they are 
also barriers to external interpretability and reproducibility. They have complex schema with 
extraneous information that make them difficult to interpret. They have query languages 
(e.g. SQL) that require training to use properly. Information becomes distributed across 
different locations and platforms. They may have security policies that make them difficult 
to share with the public.  

Files, particularly in cloud storage, are reliable and more persistent. By storing metadata 
essential to interpreting an acquisition session alongside the acquisition in a human- and machine-readable 
format, there will always be an interpretable record of what happened even if e.g. the 
database stops working. 

**Q: Which fields do I have to provide within these core schemas?**

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
