# BRKOPS-2357 Demo Code (2026)

This repository contains demonstration code from the Cisco Live session BRKOPS-2357, titled "From NetDevOps to AI-Assisted Operations: Automating Networks with a Source of Truth," The demo illustrates modern techniques in network infrastructure management, showcasing how technologies like NetBox, Cisco Catalyst Center, and automation platforms can streamline network operations from configuration management to testing and verification.

For those who missed the session, you can watch the recording in the [Cisco Live On-Demand Library](https://www.ciscolive.com/on-demand/on-demand-library.html?zid=pp&search=brkops-2357#/s) (coming soon).

## Repository Components

- [Cisco Workflows Automation - Low-code/no-code automation for NetBox and Catalyst Center](./Workflows/README.md)
- [Automating Network Operations with Ansible, Catalyst Center, and NetBox](./Ansible/README.md)
- [GitLab CI/CD Integration for Network Automation](./GitLab/README.md)
- [NetBox Custom Scripts for Cisco Catalyst Center Site Creation and Plug-and-Play](./Netbox/README.md)
- [pyATS Network Testing Framework with NTP Testcase and NetBox Integration](./pyATS/README.md)

## Automation Approaches

This repository demonstrates multiple approaches to network automation:

| Approach | Use Case | Skills Required |
|----------|----------|-----------------|
| **Cisco Workflows** | Low-code/no-code automation with visual workflow builder | Basic understanding of APIs |
| **Ansible Playbooks** | Infrastructure as Code with YAML-based automation | Ansible, YAML, Jinja2 |
| **GitLab CI/CD** | Pipeline-driven automation with version control | Git, CI/CD concepts |
| **NetBox Custom Scripts** | Python-based automation integrated with NetBox | Python programming |

## Technologies & Frameworks Used

**Cisco Products & Services:**

- Cisco Catalyst Center
- Cisco Workflows

**Third-Party Products & Services:**

- NetBox
- Ansible
- GitLab CI/CD

**Tools & Frameworks:**

- pyATS
- Docker

## Known issues

Currently, there are no known issues. Please report any bugs or problems using the GitHub Issues section.

## Getting help

If you encounter any issues or need assistance, please create an issue in the GitHub repository for support.

## Getting involved

Contributions to this project are welcome! Please refer to the [CONTRIBUTING](./CONTRIBUTING.md) guidelines for instructions on how to contribute.

## Authors & Maintainers

This project was written and is maintained by the following individuals:

- Patrick Mosimann (<pamosima@cisco.com>)

## Credits

- Keith B for DNAC Template: [Platinum Onboarding Template](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/ONBOARDING/Platinum-Onboarding-Template-J2.json)
- Tobias Spuhler (<tspuhler@cisco.com>)
- Luca Gubler (<luca.gubler@onway.ch>)

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
