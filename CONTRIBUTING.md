# Contributor Guidelines
This repository defines the schemas needed to ingest and validate metadata. As a core service, it is used across multiple teams and services. Therefore, any contributions must follow certain rules to ensure stability and organization.
This document will go through best practices for contributing to this project

## Issues and Feature Requests
Questions, feature requests and bug reports are all welcome as [discussions or issues](https://github.com/AllenNeuralDynamics/aind-metadata-mapper/issues). Please use the provided [templates](https://github.com/AllenNeuralDynamics/aind-metadata-mapper/issues/new/choose) to ensure we have enough information to work with.

NOTE: If your package requires upgrading pydantic, create a separate ticket and a dedicated engineer will handle the upgrade.
## Installation and Development
To develop the software, *clone* the repository and create a new branch for your changes.
Please do not fork this repository unless you are an external developer.
```bash
git clone git@github.com:AllenNeuralDynamics/aind-metadata-mapper.git
git checkout -b my-new-feature-branch
``` 
Then in bash, run
```bash
pip install -e .[dev]
```
to set up your environment. Once these steps are complete, you can get developing🚀.
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

There are several libraries used to run linters and check documentation. We've included these in the development package. You can run them as described [here](https://github.com/AllenNeuralDynamics/aind-metadata-mapper/blob/main/README.md#linters-and-testing). 

## Pull Requests
When you are ready to open a pull request, please link any relevant issues and request a review. Thanks for contributing!