===================
Generating metadata
===================

This tutorial walks through a hypothetical example of how to generate metadata
for a cellular 2-photon imaging session. This won't focus on acquisition or instrument
metadata, instead you can find examples of those in their respective sections.

The example metadata here is intentionally simple, our intention is to give you a sense of how to generate the pydantic models, navigate the documentation, and write the metadata files.

Identify metadata sources
-------------------------

In practice, key metadata is usually distributed into many data sources. They could be spreadsheets, databases, TIFF file headers, or even file names. 

In this example, let's say that our basic subject and surgical procedure metadata are stored in excel workbook with three sheets: ``mice``, ``sessions``, and ``procedures``. 

Let's say they look like this:

``mice``::

    id  dam_id  sire_id  genotype                                               dob         sex
    1                    Vip-IRES-Cre/wt                                        9/22/2023   F
    2                    Ai32(RCL-ChR2(H134R)_EYFP)/Ai32(RCL-ChR2(H134R)_EYFP)  9/15/2023   M
    3   1       2        Vip-IRES-Cre/wt;Ai32(RCL-ChR2(H134R)_EYFP)/wt          12/1/2023   F


``procedures``::

    mouse_id    injection_date  protocol                brain_area  virus_name           virus_titer  injection_volume  injection_coord     perfusion_date
    3	        1/2/2024 7:00   injection-perfusion-v1  VISp        AAV2-Flex-ChrimsonR  2300000000   200               03.8,-0.87,-3.3,10  1/31/2024 10:22


``sessions``::

    mouse_id  start_time       end_time
    3         1/26/2024 15:00  1/26/2024 15:30
    3         1/27/2024 15:00  1/27/2024 15:30
    3         1/28/2024 15:00  1/28/2024 15:30
    

In this example you can see that we recorded three sessions from one mouse, 
which has a viral injection and a perfusion procedure. All mice are C57BL/6J, 
were bred locally, and were housed with a running wheel in their cage. Download 
:download:`example_workflow.xlsx <example_workflow.xlsx>` and 
:download:`example_workflow.py <example_workflow.py>` to follow along.


Setup Python environment
----------------------------

First, we'll set up the Python environment and define some shared variables.

.. literalinclude:: example_workflow.py
    :lines: 1-42

Data description
---------------------

The data description schema contains basic administrative metadata. Who collected the data, 
how was it funded, etc. We'll define a function to generate this, and re-use it for each session.

.. literalinclude:: example_workflow.py
    :lines: 47-60

Subject
------------

To create the subject metadata we'll pull some information from the excel spreadsheet.

Some of the required metadata, like the `cage_id` wasn't available to us. We'll put `"unknown"`` in the metadata for that field.

.. literalinclude:: example_workflow.py
    :lines: 63-86


Procedures
---------------

While it's best practice to store each surgery as a separate record, in our
example we instead have one row per mouse. The different procedures are 
stored in separate columns. This makes it harder to represent lists of 
procedures, but because our hypothetical protocol is always the same -
one injection at one depth followed by a perfusion at a later date - we can
get away with this simplification.

.. literalinclude:: example_workflow.py
    :lines: 89-136


Generating metadata
--------------------

Finally, we're ready to generate all the metadata files. We'll loop over the sessions listed in the excel spreadsheet and use our functions to build the JSON files. The `write_standard_file()` function will take care of writing the files to disk.

.. literalinclude:: example_workflow.py
    :lines: 139-162


Other metadata
-----------------

The remaining metadata files (:doc:`Instrument<../instrument.md>` and `Acquisition<../acquisition.md>`_) follow the same pattern: extract the relevant information from a data source, transform it into the schema, and use the `write_standard_file()` function to write the file. Follow the links above to the relevant sections for more information on these files.

.. _Instrument: ../instrument.md

During processing and analysis, you will also generate the `Processing<../processing.md>`_, `Quality Control<../quality_control.md>`_, and possibly a `Model<../model.md>`_ metadata file.
   