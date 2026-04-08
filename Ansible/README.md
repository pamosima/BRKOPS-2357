# Automating Network Operations with Ansible, Cisco Catalyst Center, and NetBox

This directory contains a collection of Ansible playbooks designed to automate network operations with Cisco Catalyst Center and NetBox.

Playbooks use the **[`cisco.catalystcenter`](https://galaxy.ansible.com/ui/repo/published/cisco/catalystcenter/)** Ansible collection (not the legacy `cisco.dnac` collection). The control node needs **`catalystcentersdk`** from `pip install -r requirements.txt` at the repository root (or the same file under `GitLab/container/ansible/` in CI images).

## Features

- Configuring general global settings in Catalyst Center
- Adding data to NetBox
- Creating site hierarchies (areas, buildings, and floors) in Catalyst Center
- Creating site hierarchies in Catalyst Center based on NetBox data
- Onboarding planned switches defined in NetBox
- Provisioning planned switches defined in NetBox
- Removing switches and cleaning up settings in Catalyst Center

## Usage

**Load credentials in the same shell before any playbook** so `inventory/group_vars/brkops2357.yml` can read them from the environment (`lookup('env', ...)`):

```bash
cd /path/to/brkops-2357
source .bash-script.sh
cd Ansible
```

Without this, Catalyst Center API calls fail with **`AccessTokenError`** / missing username and password—the Python SDK (`catalystcentersdk`) and Ansible both need credentials, either via **`CATALYSTCENTER_USER`** / **`CATALYSTCENTER_PASSWORD`** (and **`CATALYSTCENTER_HOST`**) or the SDK-style names **`CATALYST_CENTER_USERNAME`** / **`CATALYST_CENTER_PASSWORD`**.

To use the playbooks in this repository, follow these commands:

- **First navigate to the Ansible directory** (after sourcing `.bash-script.sh` as above):

  ```bash
  cd Ansible
  ```

- **Configure Global Settings in Catalyst Center**

  ```bash
  ansible-playbook playbooks/00_setup/01_ccc_config.yml -i inventory/ccc_inventory.yml
  ```

- **Add Example Data to NetBox**

  ```bash
  ansible-playbook -i localhost, playbooks/00_setup/02_nb_config.yml
  ```

  The play uses **`connection: local`** (no SSH to `localhost`). Ensure **`NETBOX_API`** and **`NETBOX_TOKEN`** are set (for example `source` the repo `.bash-script.sh` first).

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

   This installs **ansible-core**, **catalystcentersdk** (required by `cisco.catalystcenter` modules), and other Python dependencies.

6. **Configure environment variables** (for example by creating or editing **`.bash-script.sh`** in the repository root):

   ```bash
   nano .bash-script.sh
   ```

   Adjust the values as needed. Example:

   ```bash
   export NETBOX_API="<my-netbox-url>"
   export NETBOX_TOKEN="<my-netbox-token>"
   export GOOGLE_API_KEY="<my-googlemaps-token>"
   export GITLAB_URL="<my-gitlab-url>"
   export GITLAB_TRIGGER_TOKEN="<my-gitlab-token>"
   export CATALYSTCENTER_HOST="<my-catalyst-center-hostname-or-ip>"
   export CATALYSTCENTER_USER="<my-catalyst-center-api-user>"
   export CATALYSTCENTER_PASSWORD="<my-catalyst-center-api-password>"
   export CATALYSTCENTER_CLI_USER="<my-device-cli-user>"
   export CATALYSTCENTER_CLI_PASSWORD="<my-device-cli-password>"
   export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
   ```

   **`CATALYSTCENTER_HOST`**, **`CATALYSTCENTER_USER`**, and **`CATALYSTCENTER_PASSWORD`** are the preferred environment variables read by **`Ansible/inventory/group_vars/brkops2357.yml`**. They populate `catalystcenter_host`, `catalystcenter_username`, and `catalystcenter_password`. For backward compatibility, **`DNAC_HOST`**, **`DNAC_USER`**, and **`DNAC_PASSWORD`** are still used if the `CATALYSTCENTER_*` API variables are unset. **`CATALYSTCENTER_CLI_USER`** and **`CATALYSTCENTER_CLI_PASSWORD`** supply device CLI credentials to Ansible (`catalystcenter_cli_user` / `catalystcenter_cli_password`) and to pyATS; **`DNAC_CLI_USER`** / **`DNAC_CLI_PASSWORD`** remain supported as fallbacks. If neither set is present, the literals in `brkops2357.yml` apply for Ansible.

7. **Source the `.bash-script.sh` file to apply the environment variables:**

   ```bash
   source .bash-script.sh
   ```

8. **Install Ansible Galaxy collections** into the project so `ansible.cfg` can find them:

   ```bash
   ansible-galaxy collection install -r Ansible/requirements.yml -p Ansible/collections
   ```

   This pulls **`cisco.catalystcenter`**, **`netbox.netbox`**, and **`ansible.utils`**. The checked-in **`Ansible/ansible.cfg`** sets `collections_path` to `./collections` and `~/.ansible/collections`.

9. **Run playbooks from the `Ansible/` directory** (so Ansible loads `ansible.cfg`). Example:

   ```bash
   cd Ansible
   ansible-playbook -i inventory/ccc_inventory.yml playbooks/01_demo_ccc/01_create-site-hierarchy.yml
   ```

   If you run from the repo root without `cd Ansible`, Ansible may not find `cisco.catalystcenter` unless you set `ANSIBLE_CONFIG=Ansible/ansible.cfg` or export collection paths.

10. **Adjust the following inventory and group variable files:**

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
