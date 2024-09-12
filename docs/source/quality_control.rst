Quality control
==========

**Q: What is quality control?**

Quality control is a collection of **evaluations** based on sets of **metrics** about the data. Quality control has a status: it must pass, fail, or be pending waiting for manual evaluation.

**Q: What is an evaluation?**

An evaluation is a qualitative or quantitative judgement about the state of a set of metrics. For example, a probe might move a lot during a recording (drift). This drift can be measured by various metrics, including qualititative ones made by a human observer, and then a judgment made about whether the drift is too large. Each evaluation has its own status.

**Q: What is a metric?**

A metric is any single value that can be computed (or observed) about a set of data as part of an evaluation. These can have any type, but the QC apps we support expect you to use metrics that are numerical, string, or bool.
