================
Example Workflow
================

This tutorial walks through a hypothetical example of how to generate metadata
for a cellular 2-photon imaging session. This won't focus on session or rig
metadata for now, but will expand in the future.

The example metadata here is intentionally simple. The names and values don't 
perfectly align with ``aind-data-schema`` so as to show examples of mapping from
local conventions to the schema. 

You will see through this example that creating
these metadata JSON files reveals that some important data that were not being
tracked in the original metadata sources. This is common and usually things that a
single person keeps track of implicitly in their head. This information must be entered
somewhere, either by updating the data sources or hard-coding values in the 
generation script - this is not avised but what what we do here in this example.


Identify metadata sources
-------------------------

In practice, key metadata is usually distributed into many data sources. They
could be spreadsheets, databases, TIFF file headers, or even file names. 

In this example, let's assume that our basic subject and surgical procedure 
metadata are stored in and excel workbook with three sheets: ``mice``, ``sessions``, and ``procedures``. 

Let's say they look like this:

``mice``::

    id  dam_id  sire_id  genotype                                               dob         sex
	1                    Emx1-IRES-Cre/wt;Camk2a-tTA/wt;Ai93(TITL-GCaMP6f)/wt   5/1/2024    F
	2                    Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA                1/1/2024    M
	3   1       2        Ai93(TITL-GCaMP6f)/wt                                  1/4/2024    F


``procedures``::

    mouse_id    injection_date  protocol  brain_area  virus_name           virus_titer  injection_volume  injection_coord     perfusion_date
    3	        7/12/2022 7:00  2109      VISp        AAV2-Flex-ChrimsonR  2300000000   200               03.8,-0.87,-3.3,10  9/23/2022 10:22


``sessions``::

    mouse_id  start_time      end_time
    3         3/13/2024 3:00  3/13/2024 3:30
    3         3/14/2024 3:00  3/14/2024 3:30
    3         3/15/2024 3:00  3/15/2024 3:30
    

In this example you can see that we recorded three sessions from one mouse, 
which has a viral injection and a perfusion procedure.


Make data description
---------------------

The data description schema contains basic administrative metadata. Who collected the data, 
how was it funded, etc.

.. literalinclude:: example_workflow/example_workflow.py
    :lines: 1-43


Make subject
------------

The subject metadata is a bit more complex. In this case, certain fields 
are required but we simply didn't keep track. As a best practice, we acknowledge
that this information is unavailable by saying it is ``unknown``.

.. literalinclude:: example_workflow/example_workflow.py
    :lines: 45-71


Make procedures
---------------

While it's best practice to store each surgery as a separate record, in our
example we instead have one row per mouse. The different procedures are 
stored in separate columns. This makes it harder to represent lists of 
procedures, but because our hypothetical protocol is always the same -
one injection at one depth followed by a perfusion at a later date - we can
get away with this simplification.

.. literalinclude:: example_workflow/example_workflow.py
    :lines: 73-

And there you have it. More metadata to come!


   