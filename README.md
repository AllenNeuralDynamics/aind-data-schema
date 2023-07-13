# aind-data-schema

[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
![Code Style](https://img.shields.io/badge/code%20style-black-black)
[![Documentation Status](https://readthedocs.org/projects/aind-data-schema/badge/?version=latest)](https://aind-data-schema.readthedocs.io/en/latest/?badge=latest)

A library that defines [AIND](https://alleninstitute.org/what-we-do/brain-science/research/allen-institute-neural-dynamics/) data schema and validates JSON files. 

User documentation available on [readthedocs](https://aind-data-schema.readthedocs.io/en/latest/).

## Overview

This repository contains the schemas needed to ingest and validate metadata that are essential to ensuring [AIND](https://alleninstitute.org/what-we-do/brain-science/research/allen-institute-neural-dynamics/) data collection is completely reproducible. Our general approach is to semantically version core schema classes and include those version numbers in serialized metadata so that we can flexibly evolve the schemas over time without requiring difficult data migrations. In the future, we will provide a browsable list of these classes rendered to [JSONschema](https://json-schema.org/), including all historic versions.

Be aware that this package is still under heavy preliminary development. Expect breaking changes regularly, although we will communicate these through semantic versioning.

A simple example:

```python
import datetime

from aind_data_schema.subject import Housing, Subject

t = datetime.datetime(2022, 11, 22, 8, 43, 00)

s = Subject(
    species="Mus musculus",
    subject_id="12345",
    sex="Male",
    date_of_birth=t.date(),
    genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
    housing=Housing(home_cage_enrichment=["Running wheel"], cage_id="123"),
    background_strain="C57BL/6J",
)

s.write_standard_file() # writes subject.json
```

```json
{
   "describedBy": "https://raw.githubusercontent.com/AllenNeuralDynamics/aind-data-schema/main/src/aind_data_schema/subject.py",
   "schema_version": "0.3.0",
   "species": "Mus musculus",
   "subject_id": "12345",
   "sex": "Male",
   "date_of_birth": "2022-11-22",
   "genotype": "Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)",
   "mgi_allele_ids": null,
   "background_strain": "C57BL/6J",
   "source": null,
   "rrid": null,
   "restrictions": null,
   "breeding_group": null,
   "maternal_id": null,
   "maternal_genotype": null,
   "paternal_id": null,
   "paternal_genotype": null,
   "wellness_reports": null,
   "housing": {
      "cage_id": "123",
      "room_id": null,
      "light_cycle": null,
      "home_cage_enrichment": [
         "Running wheel"
      ],
      "cohoused_subjects": null
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

To develop the code, check out this repo and run the following in the cloned directory: 
```
pip install -e .[dev]
```

## Contributing

If you've found a bug in the schemas or would like to make a minor change, open an [Issue](https://github.com/AllenNeuralDynamics/aind-data-schema/issues) on this repository. If you'd like to propose a large change or addition, or generally have a question about how things work, head start a new [Discussion](https://github.com/AllenNeuralDynamics/aind-data-schema/discussions)!


### Linters and testing

There are several libraries used to run linters, check documentation, and run tests.

- To run tests locally, navigate to AIND-DATA-SCHEMA directory in terminal and run (this will not run any on-line only tests):

```
python -m unittest
```

- Please test your changes using the **coverage** library, which will run the tests and log a coverage report:

```
coverage run -m unittest discover && coverage report
```

- To test any of the following modules, conda/pip install the relevant package (interrogate, flake8, black, isort), navigate to relevant directory, and run any of the following commands in place of [command]:

```
[command] -v . 
```

- Use **interrogate** to check that modules, methods, etc. have been documented thoroughly:

```
interrogate .
```

- Use **flake8** to check that code is up to standards (no unused imports, etc.):

```
flake8 .
```

- Use **black** to automatically format the code into PEP standards:

```
black .
```

- Use **isort** to automatically sort import statements:

```
isort .
```

### Pull requests

For internal members, please create a branch. For external members, please fork the repo and open a pull request from the fork. We'll primarily use [Angular](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit) style for commit messages. Roughly, they should follow the pattern:
```
<type>(<scope>): <short summary>
```

where scope (optional) describes the packages affected by the code changes and type (mandatory) is one of:

- **build**: Changes that affect the build system or external dependencies (example scopes: pyproject.toml, setup.py)
- **ci**: Changes to our CI configuration files and scripts (examples: .github/workflows/ci.yml)
- **docs**: Documentation only changes
- **feat**: A new feature
- **fix**: A bug fix
- **perf**: A code change that improves performance
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **test**: Adding missing tests or correcting existing tests

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
