# Model

[Link to code](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/dev/src/aind_data_schema/core/model.py)

The Model metadata schema is an extension of the Processing schema tailored to model weights and other data and code artifacts underlying machine learning models - these may be trained on one dataset and evaluated on others, and may be intended to undergo further training iteratively in future versions.

Thus new evaluations and training steps can easily be appended for new model versions. This metadata should be documented for any models that see widespread internal use or public release, in order to facilitate model reuse and document provenance.
