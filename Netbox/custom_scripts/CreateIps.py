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

from extras.scripts import Script, ObjectVar
from dcim.models import Device, Interface
from ipam.models import IPAddress, Prefix, VLAN
from tenancy.models import Tenant
import requests
from requests.auth import HTTPBasicAuth
import logging

class Dnac:
    """
    Class to manage interactions with Cisco Catalyst Center (DNAC) using the requests library.
    Provides methods to retrieve device information, such as IP addresses.
    """

    def __init__(self, host, user, password) -> None:
        """
        Initialize DNAC session using provided credentials.
        """
        self.host = host
        self.user = user
        self.password = password
        self.base_url = f"https://{self.host}/dna/intent/api/v1"
        self.token = self.get_token()
        self.session = requests.Session()
        self.session.headers.update({"x-auth-token": self.token})
        self.session.verify = False  # Consider enabling SSL verification
        logging.basicConfig(level=logging.INFO)

    def get_token(self) -> str:
        url = f"https://{self.host}/dna/system/api/v1/auth/token"
        try:
            response = requests.post(url, auth=HTTPBasicAuth(self.user, self.password), verify=False)  # Change verify to True with valid certificates
            response.raise_for_status()
            return response.json()["Token"]
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTPError: {e} - Response: {e.response.text}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    def get_device_ip_address(self, device_serial: str) -> str:
        """
        Retrieve the IP address of a device by its serial number.

        :param device_serial: The serial number of the device.
        :return: The IP address as a string, or an empty string if not found.
        """
        ip_address = ""
        try:
            url = f"{self.base_url}/onboarding/pnp-device"
            params = {"serialNumber": device_serial}

            # Perform the GET request using the session with token in headers
            response = self.session.get(url, params=params)

            response.raise_for_status()  # Raises an HTTPError for bad responses

            devices = response.json()
            if devices:
                # Extract IP address from the device's HTTP headers
                ip_address = next(
                    header["value"]
                    for header in devices[0]["deviceInfo"]["httpHeaders"]
                    if "value" in header
                )

        except requests.exceptions.HTTPError as e:
            logging.error(f"Failed to get device list for {device_serial}: {e} - Response: {e.response.text}")
        except Exception as e:
            logging.error(f"Error getting IP address for device {device_serial}: {e}")

        return ip_address


class CreateIps(Script):
    """
    Script to create prefixes, interfaces, and assign primary IPs for devices in NetBox.
    """

    class Meta:
        """
        Metadata for the script, including its name and description.
        """

        name = "Create Prefixes and Interfaces"
        description = (
            "Script to create new prefixes, interfaces and set primary IPs in NetBox."
        )

    tenant = ObjectVar(
        model=Tenant, label="Tenant", description="Select the tenant for the new site."
    )

    def run(self, data, commit):
        """
        Main execution method to process devices and assign network settings.

        :param data: Form data submitted by the user.
        :param commit: Whether to commit changes to the database.
        """

        self.log_info("Starting the script...")

        # Load configuration from JSON file
        vars_data = self.load_json('vars.json')
        dnac_host = vars_data.get("DNAC_HOST")
        dnac_user = vars_data.get("DNAC_USER")
        dnac_password = vars_data.get("DNAC_PASSWORD")

        # Initialize DNAC instance with credentials
        dnac = Dnac(dnac_host, dnac_user, dnac_password)

        devices = Device.objects.filter(status="planned", primary_ip4=None)
        tenant = data["tenant"]

        vlan = VLAN.objects.get(name="MGMT")

        for device in devices:
            # Get the device's IP address from DNAC using the correct argument
            ip_address = dnac.get_device_ip_address(device.serial)

            if ip_address:
                self.log_info(f"Found IP address {ip_address} for device {device.name}")

                parent_interface = Interface.objects.get(device=device, label="Uplink")

                interface = Interface.objects.create(
                    device=device,
                    name="Vlan1",
                    type="virtual",
                    label="MGMT",
                    enabled=True,
                    parent=parent_interface,
                )

                parent_prefix = f"{'.'.join(ip_address.split('.')[:3])}.0/24"

                if Prefix.objects.filter(prefix=parent_prefix).exists():
                    self.log_info(f"Prefix {parent_prefix} already exists.")
                else:
                    Prefix.objects.create(
                        prefix=parent_prefix,
                        tenant=tenant,
                        vlan=vlan,
                        status="active",
                    )
                    self.log_success(f"Created parent prefix {parent_prefix}.")

                ip_obj = IPAddress.objects.create(
                    address=f"{ip_address}/24",
                    assigned_object=interface,
                    tenant=tenant,
                )

                device.primary_ip4 = ip_obj
                device.save()

                self.log_success(f"Set primary IPv4 address {ip_address} for device {device.name}.")
                self.log_success(f"Created MGMT SVI with IP {ip_address} for device {device.name}.")
            else:
                self.log_warning(f"No IP address found for device {device.name}")

        self.log_success("Script completed successfully!")