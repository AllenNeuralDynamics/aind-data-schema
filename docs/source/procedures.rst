Procedures
==========

The `procedures.json` file contains Procedures, anything done to the subject or specimen prior to data collection. This can include surgeries, injections, tissue processing, sectioning, immunolabeleing, etc.

**Subject** procedures are performed on a live subject (e.g. injections, surgeries, implants, perfusions, etc.) 
whereas **specimen** procedures are performed on tissue extracted after perfusion (e.g. tissue processing, 
immunolabeleing, sectioning, etc.). Sectioned specimens will have unique IDs (`subject_id-specimen_number`)

**Perfusions** are subject procedures that produce specimens and sectioning is a specimen procedure that produces new specimens.

**IACUC Protocol vs Protocol ID**

`iacuc_protocol` all experimental work with animals must follow an IACUC (Institute Animal Care Use Committee) protocol. The protocol ID refers to the DOI for a published protocol, for example those stored in the 
`AIND protocols.io workspace <https://www.protocols.io/workspaces/allen-institute-for-neural-dynamics>`_.
