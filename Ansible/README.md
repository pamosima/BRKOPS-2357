# Automating Network Operations with Ansible, Cisco Catalyst Center, and NetBox

This directory contains a collection of Ansible playbooks designed to automate network operations with Cisco Catalyst Center and NetBox.

## Features

- Configuring general global settings in Catalyst Center
- Adding data to NetBox
- Creating site hierarchies (areas, buildings, and floors) in Catalyst Center
- Creating site hierarchies in Catalyst Center based on NetBox data
- Onboarding planned switches defined in NetBox
- Provisioning planned switches defined in NetBox
- Removing switches and cleaning up settings in Catalyst Center

## Usage

To use the playbooks in this repository, follow these commands:

- **First navigate to the Ansible directory:**

  ```bash
  cd Ansible
  ```

- **Configure Global Settings in Catalyst Center**

  ```bash
  ansible-playbook playbooks/00_setup/01_ccc_config.yml -i inventory/ccc_inventory.yml
  ```

- **Add Example Data to NetBox**

  ```bash
  ansible-playbook playbooks/00_setup/02_nb_config.yml
  ```

- **Create Site Hierarchy in Catalyst Center (without NetBox Data)**

  ```bash
  ansible-playbook playbooks/01_demo_ccc/01_create-site-hierarchy.yml -i inventory/ccc_inventory.yml
  ```

- **Create Site Hierarchy in Catalyst Center from NetBox Data**

  ```bash
  ansible-playbook playbooks/02_demo_nb-ccc/01_create-site-hierarchy.yml -i inventory/ccc_inventory.yml
  ```

- **Onboard Planned Switches Defined in NetBox**

  ```bash
  ansible-playbook playbooks/02_demo_nb-ccc/02_switch-onboarding.yml -i inventory/nb_inventory.yml
  ```

- **Provision Planned Switches Defined in NetBox**

  ```bash
  ansible-playbook playbooks/02_demo_nb-ccc/03_provision-switch.yml -i inventory/nb_inventory.yml
  ```

- **Clean Up Catalyst Center**
  ```bash
  ansible-playbook playbooks/99_clean-up/01_ccc_clean-up.yml -i inventory/ccc_inventory.yml
  ```

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/pamosima/brkops-2357 brkops-2357
   ```

2. **Navigate to the repository directory:**

   ```bash
   cd brkops-2357
   ```

3. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   ```

4. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

5. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Configure environment variables by creating the `.bash-script.sh` file:**

   ```bash
   nano .bash-script.sh
   ```

   Adjust the environment variables as needed. Example:

   ```bash
   export NETBOX_API="<my-netbox-url>"
   export NETBOX_TOKEN="<my-netbox-token>"
   export GOOGLE_API_KEY="<my-googlemaps-token>"
   export GITLAB_URL="<my-gitlab-url>"
   export GITLAB_TRIGGER_TOKEN="<my-gitlab-token>"
   export DNAC_HOST="<my-ccc-url>"
   export DNAC_USER="<my-ccc-user>"
   export DNAC_PASSWORD="<my-ccc-password>"
   export DNAC_CLI_USER="<my-device-user>"
   export DNAC_CLI_PASSWORD="<my-device-password>"
   export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
   ```

7. **Source the `.bash-script.sh` file to apply the environment variables:**

   ```bash
   source .bash-script.sh
   ```

8. **Install Ansible Galaxy collections:**

   ```bash
   ansible-galaxy collection install -r Ansible/requirements.yml
   ```

9. **Adjust the following inventory and group variable files:**

   - `Ansible/inventory/ccc_inventory.yml`
   - `Ansible/inventory/nb_inventory.yml`
   - `Ansible/inventory/group_vars/brkops2357.yml`

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

## Credits

- Keith B for DNAC Template: [Platinum Onboarding Template](https://github.com/kebaldwi/DNAC-TEMPLATES/blob/master/ONBOARDING/Platinum-Onboarding-Template-J2.json)

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](../LICENSE).

## Return to Main Menu

To return to the main menu, [click here](../README.md).
