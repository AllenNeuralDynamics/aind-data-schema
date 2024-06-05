# aind-data-schema

[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
![Code Style](https://img.shields.io/badge/code%20style-black-black)
[![Documentation Status](https://readthedocs.org/projects/aind-data-schema/badge/?version=latest)](https://aind-data-schema.readthedocs.io/en/latest/?badge=latest)

A library that defines [AIND](https://alleninstitute.org/what-we-do/brain-science/research/allen-institute-neural-dynamics/) data schema and validates JSON files. 

User documentation available on [readthedocs](https://aind-data-schema.readthedocs.io/en/latest/).

## Overview

This repository contains the schemas needed to ingest and validate metadata that are essential to ensuring [AIND](https://alleninstitute.org/what-we-do/brain-science/research/allen-institute-neural-dynamics/) data collection is completely reproducible. Our general approach is to semantically version core schema classes and include those version numbers in serialized metadata so that we can flexibly evolve the schemas over time without requiring difficult data migrations. In the future, we will provide a browsable list of these classes rendered to [JSON Schema](https://json-schema.org/), including all historic versions.

Be aware that this package is still under heavy preliminary development. Expect breaking changes regularly, although we will communicate these through semantic versioning.

A simple example:

```python
import datetime

from aind_data_schema.core.subject import BreedingInfo, Housing, Subject
from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.species import Species

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

s = Subject(
   species=Species.MUS_MUSCULUS,
   subject_id="12345",
   sex="Male",
   date_of_birth=t.date(),
   genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
   housing=Housing(home_cage_enrichment=["Running wheel"], cage_id="123"),
   background_strain="C57BL/6J",
   source=Organization.AI,
   breeding_info=BreedingInfo(
         breeding_group="Emx1-IRES-Cre(ND)",
         maternal_id="546543",
         maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
         paternal_id="232323",
         paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
   ),
)

s.write_standard_file() # writes subject.json
```

```json
{
   "describedBy": "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/core/subject.py",
   "schema_version": "0.5.6",
   "subject_id": "12345",
   "sex": "Male",
   "date_of_birth": "2022-11-22",
   "genotype": "Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
   "species": {
      "name": "Mus musculus",
      "abbreviation": null,
      "registry": {
         "name": "National Center for Biotechnology Information",
         "abbreviation": "NCBI"
      },
      "registry_identifier": "10090"
   },
   "alleles": [],
   "background_strain": "C57BL/6J",
   "breeding_info": {
      "breeding_group": "Emx1-IRES-Cre(ND)",
      "maternal_id": "546543",
      "maternal_genotype": "Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
      "paternal_id": "232323",
      "paternal_genotype": "Ai93(TITL-GCaMP6f)/wt"
   },
   "source": {
      "name": "Allen Institute",
      "abbreviation": "AI",
      "registry": {
         "name": "Research Organization Registry",
         "abbreviation": "ROR"
      },
      "registry_identifier": "03cpe7c52"
   },
   "rrid": null,
   "restrictions": null,
   "wellness_reports": [],
   "housing": {
      "cage_id": "123",
      "room_id": null,
      "light_cycle": null,
      "home_cage_enrichment": [
         "Running wheel"
      ],
      "cohoused_subjects": []
   },
   "notes": null
}
```

## Installing and Upgrading

To install the latest version:
```
pip install aind-data-schema
```

Every merge to the `main` branch is automatically tagged with a new major/minor/patch version and uploaded to PyPI. To upgrade to the latest version:
```
pip install aind-data-schema --upgrade
```

## Issues and Discussions
If you've found a bug in the schemas or would like to make a minor change, open an [issue](https://github.com/AllenNeuralDynamics/aind-data-schema/issues) and please use the provided [templates](https://github.com/AllenNeuralDynamics/aind-metadata-mapper/issues/new/choose).
If you'd like to propose a large change or addition, or generally have a question about how things work, head start a new [Discussion](https://github.com/AllenNeuralDynamics/aind-data-schema/discussions)!

## Controlled Vocabularies

Controlled vocabularies and other enumerated lists are maintained in a separate repository: [aind-data-schema-models](https://github.com/AllenNeuralDynamics/aind-data-schema-models). This allows us to specify these lists without changing aind-data-schema. Controlled vocabularies include lists of organizations, manufacturers, species, modalities, platforms, units, harp devices, and registries.

To upgrade to the latest data models version:
```
pip install aind-data-schema-models --upgrade
```

## Contributing
Contributions are more than welcome for this project! If you'd like to develop the code, please follow the standards outlined in the [contribution guide](https://github.com/AllenNeuralDynamics/aind-data-schema/blob/main/CONTRIBUTING.md).


### Documentation

To generate the rst files source files for documentation, run:

```
sphinx-apidoc -o docs/source/ src
```

Then to create the documentation html files, run:
```
sphinx-build -b html docs/source/ docs/build/html
```

More info on sphinx installation can be found here: https://www.sphinx-doc.org/en/master/usage/installation.html
