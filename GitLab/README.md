# GitLab CI/CD Integration for Network Automation

This directory contains configuration files for integrating with GitLab CI/CD pipelines. It includes Dockerfiles for setting up Ansible and pyATS runners, as well as the necessary components for executing tasks within the CI/CD framework.

## Features

- **Ansible Runner**: Provides a Docker environment for executing Ansible playbooks as part of the CI/CD process. It includes all necessary dependencies as specified in the requirements files.

- **pyATS Runner**: Offers a Docker environment tailored for running pyATS tests. This runner includes optional OpenConnect integration for accessing Cisco's dCloud, allowing for flexible test environment connectivity.

- **Pipeline Configuration**: Utilizes the Docker images to execute CI/CD tasks efficiently, ensuring consistent and repeatable builds within the GitLab CI/CD framework.

## Pipeline File: `.gitlab-ci.yml`

The `.gitlab-ci.yml` file defines the CI/CD pipeline for automating tasks such as site creation, switch onboarding, and testing. It includes stages for verification, deployment, and testing, leveraging Ansible playbooks and pyATS.

### Key Stages

- **Verify**: Executes dry-run Ansible playbooks to ensure configurations are correct before deployment.
- **Deploy**: Runs the actual Ansible playbooks to apply configurations, with manual execution and failure handling.
- **Test**: Uses pyATS for network testing, with optional VPN connection via OpenConnect for Cisco's dCloud.

### Hidden Jobs

The pipeline file contains hidden job templates (`.sites`, `.switches`) to manage environment-specific variables and scripts for different stages.

### Additional Information

For more information on building and pushing Docker images used in this pipeline, refer to the [GitLab Container Registry Documentation](https://docs.gitlab.com/ee/user/packages/container_registry/build_and_push_images.html).

## Known issues

Currently, there are no known issues. Please report any bugs or problems using the GitHub Issues section.

## Getting help

If you encounter any issues or need assistance, please create an issue in the GitHub repository for support.

## Getting involved

Contributions to this project are welcome! Please refer to the [CONTRIBUTING](../CONTRIBUTING.md) guidelines for instructions on how to contribute.

## Authors & Maintainers

This project was written and is maintained by the following individuals:

- Patrick Mosimann (<pamosima@cisco.com>)
- Tobias Spuhler (<tspuhler@cisco.com>)
- Luca Gubler (<luca.gubler@onway.ch>)

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](../LICENSE).

## Return to Main Menu

To return to the main menu, [click here](../README.md).
