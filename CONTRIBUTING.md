# Contributor Guidelines
This repository defines the schemas needed to validate and document metadata. As a core service, it is used across multiple teams and services. Therefore, any contributions must follow certain rules to ensure stability and organization.
This document will go through best practices for contributing to this project

## Issues and Feature Requests
Feature requests and bug reports are all welcome as [issues](https://github.com/AllenNeuralDynamics/aind-data-schema/issues). Create a ticket using the provided [templates](https://github.com/AllenNeuralDynamics/aind-metadata-mapper/issues/new/choose) to ensure we have enough information to work with.
Our team will review, assign, and address the ticket. If the ticket is urgent, you may tag a dedicated engineer in the issue but please refrain from assigning it.

If you have a broader suggestion or a question about how things work, start a new [Discussion](https://github.com/AllenNeuralDynamics/aind-data-schema/discussions)!

NOTE: If your request requires upgrading pydantic, create a separate ticket and a dedicated engineer will handle the upgrade.

## Installation and Development
To develop the software, *clone* the repository and create a new branch for your changes.
Please do not fork this repository unless you are an external developer.
```bash
git clone git@github.com:AllenNeuralDynamics/aind-metadata-mapper.git
git checkout -b my-new-feature-branch
``` 
Then run the following command in the checked out directory. 
```bash
pip install -e .[dev]
```

### Testing
Testing is required to open a PR in this repository to ensure robustness and reliability of our codebase.
- **1:1 Correspondence:** Structure unit tests in a manner that mirrors the module structure. 
  - For every package in the src directory, there should be a corresponding test package.
  - For every module in a package, there should be a corresponding unit test module.
  - For every method in a module, there should be a corresponding unit test.
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

## Documentation and Style Guide
Documentation is required for contributing to this project. We have settled on using Numpy's conventions as a default: [Numpy docstring standards](https://numpydoc.readthedocs.io/en/latest/format.html)


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