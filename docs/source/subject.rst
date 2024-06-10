Subject schema
==============

**Q: What is a subject?**

A: The animal from which data is obtained.

**Q: What does the subject file contain?**

A: Information regarding the background of the subject such as sex, species, genotype, any identifiers, where it was 
sourced from, breeding background, etc.

**Q: How do I create a subject file?**
A: The metadata service (http://aind-metadata-service/) pulls metadata from LabTracks about our mice. If you are using 
a subject that is not from our animal facility, you will need to create this manually. You can either use the GUI 
(https://metadata-entry.allenneuraldynamics.org/) or write python code that imports aind-data-schema.
