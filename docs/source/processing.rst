Processing
==========

**Q: What is processing?**

This file captures the data processing and analysis steps that have been carried out – mostly for derived data assets. 
This tracks what code was used for each step, when it was run, what the input and outputs where, what parameters were 
set. This includes things like spike sorting, image alignment, cell segmentation. It also includes manual annotation, 
quality control, and data analysis. This file should be appended with each subsequent stage of processing or analysis.

Questions for AIND users
------------------------

**Q: How do I create a processing file?**

You can create a procedure file using our `metadata entry web application <https://metadata-entry.allenneuraldynamics.org>`_. 
The internal `data transfer service <http://aind-data-transfer-service>`_ creates a processing.json file when
it performs data compression or other preprocessing prior to upload. When derived data assets are created, they should have 
a processing.json files that has appended new processing steps to that original file. This needs to be done using python code
that imports `aind-data-schema <https://github.com/allenNeuralDynamics/aind-data-schema>`_.
