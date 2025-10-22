# Metadata in general

Metadata is data about data. Metadata documents information about acquired data that enables us to be able to analyze and interpret it well. We use our metadata to document the entire process of creating data, the provenance of that data as it moves through processing and analysis workflows, and the quality of the data.

In capturing metadata we have two goals:

1. Rigorously define the properties of data assets necessary for further data analysis and interpretation.
2. Create searchable records that make it easy to group data assets (by project, modality, quality control status, etc).

To learn more about why we are developing our own schema, see the [related_standards](related_standards.md) page.

## Meta-decisions

### Why should we enforce a rigorous schema?

Metadata captured by acquisition software evolves over time and often does not capture 
everything we need to know to interpret data. These JSON files represent our ground truth 
viewpoint on what is essential to know about our data in a single location. 

Additionally, JSON files are both human- and machine-readable. They are viewable on 
any system without additional software to be installed (a text editor is fine). They are easy 
to parse from code without any heavy dependencies (IGOR, H5PY, pynwb, etc). 

### Why did we choose to save metadata in JSON files?

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

## Data organization

Learn more about about [AIND data organization](https://docs.allenneuraldynamics.org/en/latest/metadata/philosophy.html) philosophy and the rules we use to standardize asset naming.

## FAQs

**Q: Which fields do I have to provide within these core schemas?**

All required (non-optional) fields must be completed to create a "valid model". 

**Q: Can I skip fields that are optional?**

Optional fields should be included whenever possible but are not required. The reason some fields are optional is 
usually because they aren't universal, and so the pertinent question is whether those fields apply to your 
experiments/devices/etc and not about whether you can ignore things because you don't want to provide them.

**Q: If I don't know something (e.g. the serial number of my device) can I just make something up?**

A: No. Fake metadata is harmful. 

**Q: Who is responsible for making sure the metadata is accurate?**

You are. Even with metadata service and tools, you need to make sure the information attached to your data is 
accurate and that any issues get resolved. Please reach out with questions if you are unclear about the schema, 
but you are responsible for the content.

**Q: Whom should I contact with questions or issues?**

Questions about the schema should be directed to Saskia de Vries. [Issues](https://github.com/AllenNeuralDynamics/aind-data-schema/issues) can be opened on our GitHub repository. Questions about correcting errors in existing metadata can be directed to the [data migration repository](https://github.com/AllenNeuralDynamics/aind-data-migration-scripts/issues).

**Q: What are the registries and atlases that are referenced in the schema?**

When possible, we use persistent identifiers (PIDs) to specify metadata features. This affords precision and clarity 
and allows richer information in public databases to be accessible. Our list of registries will grow as we incorporate 
more ontologies into our schema. We currently use:

* NCBI Taxonomy to specify species
* NBCI Gene
* Research Organization Registry (ROR) to specify organizations (including manufacturer, funders, research organizations)
* Open Researcher and Contributor ID (ORCID) to identify experimenters
* Research Resource Identifiers (RRID) to identify reagents and other resources
* Addgene to identify viruses and plasmids
* Mouse Genome Informatics (MGI) to identify transgenic alleles
* Edinburgh Mouse Atlas Project (EMAPA), mouse anatomy
* Mouse Common Coordinate Framework (CCF), mouse brain anatomy

## Flexibility, versioning, and upgrading

`aind-data-schema` is versioned using [Semantic Versioning](https://semver.org/). The core schemas listed above 
also have their own version numbers, which are documented in the `schema_version` field of any JSON file 
they are used to generate.

When new versions of schemas are released, data collectors can decide if they want to update the metadata
from their existing data assets to the new schema. Metadata upgrading capabilities can be found in 
[aind-metadata-upgrader](https://github.com/allenneuraldynamics/aind-metadata-upgrader).
