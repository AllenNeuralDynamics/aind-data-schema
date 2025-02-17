Procedures
==========

**Q: What are procedures?**

Procedures are things that are done to the subject or specimen prior to data collection. This can include surgeries, 
injections, tissue processing, sectioning, immunolabeleing, etc.

**Q: What's the difference between subject and specimen procedures?**

Subject procedures are procedures performed to a live subject (e.g. injections, surgeries, implants, perfusions, etc.) 
whereas <b>specimen procedures</b> are procedures performed on tissue extracted after perfusion (e.g. tissue processing, 
immunolabeleing, sectioning, etc.). Perfusions are subject procedures that produce specimens (removing tissue from a 
subject to create specimens) and sectioning is a specimen procedure that produces new specimens.

**Q: What’s the difference between subject id and specimen id? Are these always the same?**

The subject id is the id of an animal, and the specimen id is the id of a piece of tissue. When the tissue is an intact 
brain, it will usually be the same number as the subject id. If the tissue is sectioned, new specimen ids will be 
created. E.g. if the subject_id of an animal is 123456 and it is perfused the brain has specimen_id of 123456. When 
that brain is sectioned into 3 sections, they will have specimen_ids of 123456-001, 123456-002, and 123456-003.

**Q: What is “iacuc_protocol”? How is this different from “protocol_id”?**

An IACUC protocol is a protocol for experiments approved by the IACUC (Institute Animal Care and Use Committee) that 
assures that our procedures and experiments comply with our animal care policies. All experimental work with animals 
must happen under an IACUC protocol. Typically, the same IACUC protocol covers all the in vivo procedures/experiments 
used for a given project/set of projects. The protocol_id is a doi to a protocol published on protocols.io, which 
contains the step-by-step protocol for a specific procedure.

Questions for AIND users
------------------------

**Q: Where do I find the protocol_id for my procedure?**

You can find AIND's protocols on our `protocols.io workspace <https://www.protocols.io/workspaces/allen-institute-for-neural-dynamics>`_
or in this list of our `published protocols <https://app.smartsheet.com/sheets/3XQgWWrXW3mh46xmXCw5Q9GfqQmmP4xwF9Cjfqg1?view=grid>`_.

**Q: How do I create a procedure file?**

You can create a procedure file using our `metadata entry web application <https://metadata-entry.allenneuraldynamics.org>`_. You can also use 
the Allen-internal `metadata service <http://aind-metadata-service/>`_, which automatically pulls subject 
procedure information from our Neurosurgery and Behavior database and Lab Animal Services database, capturing most surgeries, injections
and perfusions. As our SLIMS system continues to develop, this service will be able to pull more procedure information from SLIMS,
but presently any additional surgeries must be documented manually. Note that this service is automatically used to pull procedure metadata
any time data is uploaded with the `data transfer service <http://aind-data-transfer-service>`_.
