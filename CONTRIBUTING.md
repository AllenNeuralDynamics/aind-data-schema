# Contributor Guidelines

Contributions to `aind-data-schema` must follow certain rules to ensure stability and organization. This document will go through best practices for contributing to this project

## Issues and Feature Requests

Feature requests and bug reports are all welcome as [issues](https://github.com/AllenNeuralDynamics/aind-data-schema/issues). Create a ticket using the provided [templates](https://github.com/AllenNeuralDynamics/aind-metadata-mapper/issues/new/choose) to ensure we have enough information to work with.
Our team will review, assign, and address the ticket. If the ticket is urgent, you may tag a dedicated engineer in the issue but please refrain from assigning it.

If you have a broader suggestion or a question about how things work, start a new [Discussion](https://github.com/AllenNeuralDynamics/aind-data-schema/discussions)!

## Installation and Development

To develop the software, *clone* the repository and create a new branch for your changes.
Please do not fork this repository unless you are an external developer.

```bash
git clone git@github.com:AllenNeuralDynamics/aind-data-schema.git
cd aind-data-schema
git checkout -b my-new-feature-branch
```

It's recommended you work in an isolated virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate  # (unix)
```

Then run the following command in the checked out directory.

```bash
pip install -e .[dev]
```

### Upgrades

Starting with the v2.0 release all changes must be accompanied by an [upgrader](https://github.com/AllenNeuralDynamics/aind-metadata-upgrader/) that converts valid metadata from the latest version tag of `aind-data-schema` to valid metadata in the version tag where your changes are introduced. Breaking changes are exempt from this requirement.

### Documentation

**Note**: The core files (`docs/source/acquisition.md`, etc) are auto-generated from the base files in the folder `docs/base/core` with the model definitions appended. You must modify the **base** file or your changes will be overwritten when you run the documentation generators.

To generate the source files for the documentation and model class links, run:

```python
python src/aind_data_schema/utils/docs/model_generator.py
python src/aind_data_schema/utils/docs/registries_generator.py
python src/aind_data_schema/utils/docs/doc_generator.py
```

Then to create the documentation html files, run:

```bash
sphinx-build -b html docs/source/ docs/build/html
```

More info on sphinx installation can be found here: https://www.sphinx-doc.org/en/master/usage/installation.html

### Testing

Testing is required to open a PR in this repository to ensure robustness and reliability of our codebase.
- **1:1 Correspondence:** Structure unit tests in a manner that mirrors the module structure. 
  - For every package in the src directory, there should be a corresponding test package.
  - For every module in a package, there should be a corresponding unit test module.
  - For every method in a module, there should be a corresponding unit test.
  - For complicated functions, keep unit test functions small and interpretable.
- **Test Coverage:** Aim for comprehensive test coverage to validate all critical paths and edge cases within the module. To open a PR, you will need at least 80% coverage. 
  - Please test your changes using the **coverage** library, which will run the tests and log a coverage report:

    ```bash
    coverage run -m unittest discover && coverage report
    ```

    To open the coverage report in a browser, you can run

    ```bash
    coverage html
    ```
    and find the report in the htmlcov/index.html.

To run a single unit test file you can use

```bash
coverage run -m unittest tests/your_test.py
```

### Linters

There are several libraries used to run linters and check documentation. We've included these in the development package. You can run them as described [here](https://github.com/AllenNeuralDynamics/aind-metadata-mapper/blob/main/README.md#linters-and-testing).

- To run tests locally, navigate to AIND-DATA-SCHEMA directory in terminal and run (this will not run any on-line only tests):

  ```
  python -m unittest
  ```
- To test any of the following modules, conda/pip install the relevant package (interrogate, flake8, black, isort), navigate to relevant directory, and run any of the following commands in place of [command]:

  ```
  [command] -v . 
  ```

- Use **interrogate** to check that modules, methods, etc. have been documented thoroughly:

  ```
  interrogate .
  ```
  For more information you can run
  ```interrogate --verbose .```

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
**NOTE**: Please note that these linters are automatically run in github actions when a PR is opened. These linters must pass for a PR to merge. 

### Units
Unit types (i.e. anything from [aind_data_schema_models.units](https://github.com/AllenNeuralDynamics/aind-data-schema-models/blob/main/src/aind_data_schema_models/units.py)) should always be paired with a variable in one of two patterns.

When you have a single `variable` with a unit, you should add the `_unit` suffix on the name of the unit:

```python
variable: type = Field(...)
variable_unit: XUnit = Field(...)
```

If the variable is `Optional[]` the unit should also be marked as optional.

If you have multiple variables that map onto a single unit type, start each `variable` with the same prefix. The prefix should be unique within the class (watch out for inherited fields). 

```python
fov_width: type = Field(...)
fov_height: type = Field(...)
fov_unit: XUnit = Field(...)
```

### Docstrings

Docstrings are required for contributing to this project. We have settled on using Numpy's conventions as a default: [Numpy docstring standards](https://numpydoc.readthedocs.io/en/latest/format.html)

## Pull Requests

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
to set up your environment.

When you are ready to open a pull request, please link any relevant issues and request a review. Thanks for contributing!

## Release

- From dev, create a branch called release-vX.Y.Z
- Manually increment the version number in the aind_data_schema/__init__.py file to match
- Manually increment the major/minor/patch versions of the core files as needed
- Push the branch and open a PR into main
- After this push, any last minute changes to the release-vX.Y.Z will have to done to via a PR
- After review, use a merge commit to merge into main
- Open a PR from main back into dev so they're synced again
- Create a Github release with the corresponding tag, modify the auto-generated release notes to focus on the major changes that occurred
