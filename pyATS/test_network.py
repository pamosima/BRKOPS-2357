"""
Copyright (c) 2025 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from pyats import aetest
from genie.testbed import load
import logging
import pynetbox
import os
from subprocess import call

logging.basicConfig(level=logging.INFO)

import subprocess

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        """
        Connect to all devices in the testbed
        """
        logging.info("Connecting to devices...")
        for device_name, device in testbed.devices.items():
            try:
                device.connect()
                logging.info(f"Connected to {device_name}")
            except Exception as e:
                logging.error(f"Failed to connect to {device_name}: {str(e)}")
                self.failed(f"Failed to connect to {device_name}: {str(e)}")

class TestcaseNTP(aetest.Testcase):
    
    must_pass=True
    
    @aetest.test
    
    def verify_ntp_peer(self, testbed, steps):
        """
        Verify that the expected NTP peer is configured 
        and synchronized
        """
        expected_ntp_peer = "198.18.133.141"
        for device_name, device in testbed.devices.items():
            with steps.start(f"Checking NTP peer configuration on {device_name}") as step:
                try:
                    ntp_output = device.parse("show ntp associations")
                    associations = ntp_output.get("peer", {})
                    system_status = ntp_output.get("clock_state", {}).get("system_status", {})

                    # Check if expected NTP peer is configured
                    if expected_ntp_peer in associations:
                        peer_info = associations[expected_ntp_peer]

                        # Check if the peer is the system's synchronized peer
                        if system_status.get("associations_address") == expected_ntp_peer and system_status.get("clock_state") == "synchronized":
                            step.passed(f"Expected NTP peer {expected_ntp_peer} is configured and synchronized on {device_name}")
                        else:
                            step.failed(f"NTP peer {expected_ntp_peer} is configured but not synchronized on {device_name} (clock_state: {system_status})")
                    else:
                        step.failed(f"Expected NTP peer {expected_ntp_peer} not found on {device_name}")

                except Exception as e:
                    step.failed(f"Failed to parse NTP configuration on {device_name}: {str(e)}")
                    
class NetboxUpdate(aetest.Testcase):
    @aetest.test
    def update_device_status(self, testbed, netbox_url, netbox_token):
        """
        Update device status in Netbox from "planned" to "active"
        if the test was successful.
        """
        if not netbox_token or not netbox_url:
            self.failed("NetBox API credentials are not set in the environment variables.")

        logging.info("Updating device statuses in NetBox...")
        nb = pynetbox.api(url=netbox_url, token=netbox_token)

        for device_name, _ in testbed.devices.items():
            logging.info(f"Updating status for device: {device_name}")
            try:
                device = nb.dcim.devices.get(name=device_name)
                if device:
                    try:
                        device.update({"status": "active"})
                        logging.info(f"Device '{device_name}' status updated to 'active'.")
                    except pynetbox.core.query.RequestError as e:
                        logging.error(f"Failed to update device '{device_name}' status: {e}")
                        self.failed(f"Failed to update device '{device_name}' status: {e}")
                else:
                    logging.warning(f"Device '{device_name}' not found in NetBox.")
            except Exception as e:
                logging.error(f"Error retrieving device '{device_name}' from NetBox: {str(e)}")
                self.failed(f"Error retrieving device '{device_name}' from NetBox: {str(e)}")

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        logging.info("Disconnecting from devices...")
        for device_name, device in testbed.devices.items():
            try:
                device.disconnect()
                logging.info(f"Disconnected from {device_name}")
            except Exception as e:
                logging.error(f"Failed to disconnect from {device_name}: {str(e)}")
                self.failed(f"Failed to disconnect from {device_name}: {str(e)}")

if __name__ == "__main__":
    testbed = load("testbed.yml")
    aetest.main(testbed=testbed)