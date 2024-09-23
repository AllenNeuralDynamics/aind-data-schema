# Quality control

**Q: What is the QualityControl object?**

Quality control is a collection of **evaluations** based on sets of **metrics** about the data. You build a QualityControl object by first building ``QCEvaluation`` objects and attaching them to the ``QualityControl`` object.

The QC object reflects the state of the entire data asset and its status is set based on the worst status of its evaluations.

Each ``QCEvaluation`` should be thought of as a single aspect of the data asset that can be evaluated. For example, a probe might move a lot during a recording (drift). This drift can be measured by various metrics, including qualititative ones made by a human observer, and then a judgment made about whether the drift is too large. Each evaluation has its own status, set based on the worst status of its metrics.

**Q: What is a metric?**

A metric is any single value or set of values that can be computed, or observed, about a set of data as part of an evaluation. These can have any type, but the QC apps we support expect you to use metrics that are numerical, string, bool, or arrays/dictionaries of these values.

All metrics have a required status object that should include both the evaluator (``"automated"`` or the evaluator's full name) and be timestamped correctly. If a metric gets re-evaluated by a second evaluator the new status should be appended to the end of the status list. 

**Q: How does QC status work?**

In our QC metadata status is always PASS, PENDING, or FAIL. When passing or failing assets the *rule* used to make that determination should be included in the QCMetric description. PENDING is used when the QC evaluation is not yet complete.

We enforce this minimal set of states to prevent ambiguity and to make it easier to build tools that can interpret the status of a data asset.

**Q: When does the state get set for the QualityControl and QCEvaluation objects?**

Call the ``QualityControl.evaluate_status()`` function to append a new status to the object. The status will be timestamped with the current time and reflect the worst status of the attached evaluations or metrics. It's best practice to evaluate the status anytime you add or update evaluations and/or metrics.

Note that while you can evaluate the status of ``QCEvaluation`` objects manually, this could lead to inconsistencies in the overall status of the ``QualityControl`` object.

## QC Portal

The QC Portal is a web application that allows users to view and interact with the QC metadata and to annotate ``PENDING`` metadata with qualitative evaluations. The portal is in testing, please get in touch with Dan to work on getting your data into the new format.

The portal works by pulling the metadata object from the Document Database (DocDB). Updates to the metadata are pushed up to DocDB when users submit their changes, along with a call to ``.evaluate_status()``. 