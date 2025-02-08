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

from extras.scripts import Script, ObjectVar, StringVar
from dcim.models import Site, Device, DeviceType, DeviceRole, Interface, InterfaceTemplate
from tenancy.models import Tenant
from scripts import CreateIps
import requests
import re



class AddSwitchesToSite(Script):
    """
    Script to add one or more switches to an existing site in NetBox.
    """

    class Meta:
        """
        Meta options for the script, including its name, description,
        and the order of the fields in the form.
        """

        name = "Add Switches to Site"
        description = "Script to add one or more switches to an existing site."
        field_order = ["tenant", "site", "device_type", "device_role","device_uplink","serial_numbers"]

    # Input variables
    tenant = ObjectVar(
        model=Tenant, label="Tenant", description="Select the tenant for the new site."
    )

    site = ObjectVar(
        model=Site,
        label="Site",
        description="Select the site to which the switches will be added.",
    )

    device_type = ObjectVar(
        model=DeviceType,
        label="Device Type",
        description="Select the type of the switches to add.",
    )

    device_role = ObjectVar(
        model=DeviceRole,
        label="Device Role",
        description="Select the role of the devices to add.",
    )
    
    device_uplink = ObjectVar(
        model=InterfaceTemplate,
        label="Device Uplink",
        description="Select uplink inteface.",
    )

    serial_numbers = StringVar(
        label="Serial Numbers",
        description="Enter one or more serial numbers, separated by commas.",
    )

    def run(self, data, commit):
        """
        Main execution method for adding switches to the site.

        :param data: Form data submitted by the user.
        :param commit: Whether to commit changes to the database.
        """

        tenant = data["tenant"]
        site = data["site"]
        device_type = data["device_type"]
        device_role = data["device_role"]
        device_uplink = data["device_uplink"]
        
        # Load the environment vars from JSON file
        vars_data = self.load_json('vars.json')
        GITLAB_API = vars_data.get("GITLAB_API")
        GITLAB_URL = vars_data.get("GITLAB_URL")
        GITLAB_TRIGGER_TOKEN = vars_data.get("GITLAB_TRIGGER_TOKEN") 
        NETBOX_URL = vars_data.get("NETBOX_API")
        
        # Extract the site number from the site's name
        site_number_match = re.search(r"\d+$", site.name)
        site_number = site_number_match.group() if site_number_match else "unknown"

        # Parse serial numbers from the input
        serial_numbers = [sn.strip() for sn in data["serial_numbers"].split(",")]

        if not serial_numbers:
            self.log_warning("No serial numbers provided. Nothing to add.")
            return

        # Get existing devices at the site to determine the next available index
        existing_devices = Device.objects.filter(
            site=site, name__startswith=f"sw{site_number}-"
        )
        existing_indices = [
            int(re.search(r"-(\d+)$", dev.name).group(1))
            for dev in existing_devices
            if re.search(r"-(\d+)$", dev.name)
        ]
        next_index = max(existing_indices, default=0) + 1

        # Loop through the provided serial numbers and create devices
        for serial_number in serial_numbers:
            # Check if the serial number already exists in the database
            if Device.objects.filter(serial=serial_number).exists():
                self.log_warning(
                    f"A device with serial number {serial_number} already exists. Skipping."
                )
                continue

            # Attempt to create the device
            try:
                device = Device.objects.create(
                    name=f"sw{site_number}-{next_index}",
                    tenant=tenant,
                    site=site,
                    device_type=device_type,
                    role=device_role,
                    serial=serial_number,
                    status="planned",
                    custom_field_data={"ccc_template_name": "Ansible_Day0-Template","ccc_pid":device_type.part_number},
                )
                # Fetch the existing interface
                interface = Interface.objects.get(device=device, name=device_uplink.name)
                # Update the label of the interface
                interface.label = "Uplink"
                interface.save()

                self.log_success(
                    f"Added switch with serial number [{serial_number}]({NETBOX_URL}/dcim/devices/{device.id}) to site [{site.name}]({NETBOX_URL}/dcim/sites/{site.id})."
                )
                next_index += 1
            except Exception as e:
                self.log_failure(
                    f"Failed to add switch with serial number {serial_number}: {e} uplink: {device_uplink}."
                )
                continue

            # Execute the CreateIps script
            self.log_info("Running the CreateIps script...")
            try:
                create_ips = CreateIps.CreateIps()
                create_ips.run({"tenant": tenant}, commit=commit)
                self.log_success("CreateIps script executed successfully.")
            except Exception as e:
                self.log_failure(f"Failed to execute CreateIps script: {e}")


        """
        If the `commit` flag is set, a GitLab pipeline will be automatically triggered.
        This pipeline performs a dry run for the site creation in Catalyst Center.
        Any subsequent deployment to production must be manually triggered in GitLab.
        """
        
        if commit:
            self.log_info("Commit is set. Triggering GitLab pipeline...")
            url = GITLAB_API
            token = GITLAB_TRIGGER_TOKEN
            
            params = {
                "token": token,
                "variables[SWITCH_PIPELINE]": "true"
            }

            try:
                response = requests.post(url, params=params)
                response.raise_for_status()

                if response.status_code == 201:
                    self.log_success(f"[Pipeline]({GITLAB_URL}/-/pipelines/) triggered successfully.")
                else:
                    self.log_warning(
                        f"Unexpected response status: {response.status_code}. Response: {response.text}"
                    )
            except requests.exceptions.RequestException as e:
                self.log_failure(f"Failed to trigger pipeline: {e}")
        else:
            self.log_info("Commit is not set. Skipping GitLab pipeline trigger.")


        self.log_success("Finished adding switches to the site.")
