# pyATS Network Testing Framework with NTP Testcase and NetBox Integration

This directory contains scripts for network testing using the Cisco pyATS framework. These scripts are designed to validate network configurations and ensure operational integrity within the Cisco BRKOPS-2357 project.

## Files Included

- **job.py**: This script defines the pyATS job, specifying the sequence of tasks and their execution. It uses the NetBox integration to dynamically generate a testbed from devices marked as "planned" in NetBox and runs the specified test scripts.

  Key Features:

  - Integrates with NetBox to retrieve device configurations using the API.
  - Filters devices based on their status to focus on "planned" devices.
  - Dynamically generates a testbed for pyATS from the NetBox data.
  - Executes the `test_network.py` script to perform network tests.

- **test_network.py**: Contains the test scripts used by pyATS to perform various network checks. This file includes specific test cases and scenarios tailored for validating the network environment.

  Key Features:

  - **CommonSetup**: Establishes connections to all devices in the testbed.
  - **TestcaseNTP**: Verifies that the expected NTP peer is configured and synchronized on each device.
  - **NetboxUpdate**: Updates device status in NetBox from "planned" to "active" if tests are successful.
  - **CommonCleanup**: Disconnects from all devices in the testbed after tests are completed.

## Usage

To execute the pyATS tests, ensure you have the pyATS environment set up and follow these steps:

1. **Activate the virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

2. **Navigate to the pyATS directory:**

   ```bash
   cd pyATS
   ```

3. **Run the pyATS job:**

   ```bash
   pyats run job job.py
   ```

This command will initiate the testing process, executing the test cases defined in test_network.py.

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
