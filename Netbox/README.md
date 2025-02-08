# NetBox Custom Scripts for Cisco Catalyst Center Site Creation, and Plug-and-Play

This directory contains custom scripts designed to import data into NetBox, facilitating the automation of network operations within the Cisco BRKOPS-2357 project.

## Custom Scripts

The custom scripts provided in this directory enable the importation of site, location, and switch data into NetBox. These scripts are essential for setting up and managing network configurations effectively.

### Scripts Included

- **01_site_and_location.py**: This script creates a new site and associated floors as locations in NetBox. It uses Google Maps API to fetch GPS coordinates based on the physical address provided. Upon successful creation of sites and locations, it can optionally trigger a GitLab pipeline for further actions.

  Key Features:

  - Input fields for tenant, region, site name, address, number of floors, and lowest floor.
  - Fetches GPS coordinates using the Google Maps API.
  - Creates site and location entries in NetBox.
  - Optionally triggers a GitLab pipeline for additional automation steps.

- **02_switches.py**: This script adds one or more switches to an existing site in NetBox. It handles device creation, assigns interfaces, and can trigger a GitLab pipeline for further processing.

  Key Features:

  - Input fields for tenant, site, device type, device role, uplink interface, and serial numbers.
  - Creates switch devices based on serial numbers and device type.
  - Assigns uplink interfaces to devices and updates interface labels.
  - Optionally triggers a GitLab pipeline for additional automation steps.
  - Integrates with the `CreateIps` script to manage IP assignments.

- **CreateIps.py**: This script creates prefixes, interfaces, and assigns primary IPs for devices in NetBox. It integrates with Cisco Catalyst Center to retrieve device IPs and updates the network configuration in NetBox.

  Key Features:

  - Retrieves device IP addresses from Cisco Catalyst Center using the device serial number.
  - Creates VLAN interfaces and assigns management IPs to devices.
  - Generates new prefixes if they do not exist and associates them with the correct VLAN and tenant.
  - Sets primary IPv4 addresses for devices in NetBox.

## Installation

To install and run these scripts in NetBox, follow the instructions outlined in the [Getting Started with NetBox Custom Scripts](https://netboxlabs.com/blog/getting-started-with-netbox-custom-scripts/) blog post. This resource provides detailed guidance on how to import and execute custom scripts within NetBox.

## Configuration

Before running the scripts, you need to create a `vars.json` file with the following content, which contains essential configuration parameters:

```json
{
  "GOOGLE_API_KEY": "<your-google-api-key>",
  "GITLAB_API": "<your-gitlab-api-url>",
  "GITLAB_URL": "<your-gitlab-url>",
  "GITLAB_TRIGGER_TOKEN": "<your-gitlab-trigger-token>",
  "DNAC_HOST": "<your-dnac-host>",
  "DNAC_USER": "<your-dnac-user>",
  "DNAC_PASSWORD": "<your-dnac-password>",
  "NETBOX_API": "<your-netbox-api-url>"
}
```

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
