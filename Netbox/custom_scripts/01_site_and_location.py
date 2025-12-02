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

from extras.scripts import Script, ObjectVar, StringVar, IntegerVar
from tenancy.models import Tenant
from dcim.models import Site, Location, Region
from django.utils.text import slugify
import requests


class CreateSiteAndLocations(Script):
    """
    Script to create a new site and associated floors as locations in NetBox.
    """

    class Meta:
        """
        Meta options for the script, including its name, description,
        and the order of the fields.
        """

        name = "Create Site and Locations"
        description = "Script to create a new site and associated floors as locations."
        field_order = [
            "tenant",
            "region",
            "site_name",
            "address",
            "number_of_floors",
            "lowest_floor",
        ]

    # Input variables
    tenant = ObjectVar(
        model=Tenant, label="Tenant", description="Select the tenant for the new site."
    )
    region = ObjectVar(
        model=Region, label="Region", description="Select the region for the new site."
    )
    site_name = StringVar(
        label="Site Name", description="Enter the name of the new site."
    )
    address = StringVar(
        label="Address",
        description="Enter the physical address of the site to fetch GPS coordinates.",
    )
    number_of_floors = IntegerVar(
        label="Number of Floors",
        description="Enter the total number of floors to create.",
    )
    lowest_floor = IntegerVar(
        label="Lowest Floor", description="Enter the starting floor number (e.g., -2)."
    )

    def get_coordinates(self, api_key, address):
        """
        Fetches GPS coordinates for the provided address using Google Maps API.

        :param api_key: Google Maps API key.
        :param address: The physical address for which coordinates are fetched.
        :return: Tuple of latitude and longitude, or None if the request fails.
        """

        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": api_key}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "OK" and data.get("results"):
                location = data["results"][0]["geometry"]["location"]
                return location["lat"], location["lng"]
            else:
                self.log_warning(
                    f"Google API error: {data.get('status')} - {data.get('error_message', 'No message')}"
                )
                return None, None
        except requests.RequestException as e:
            self.log_warning(f"HTTP error while querying Google API: {e}")
            return None, None

    def run(self, data, commit):
        """
        Executes the script to create the site and associated floors.

        :param data: Input data from the script form.
        :param commit: Whether to commit changes to the database.
        """

        self.log_info("Starting the script...")

        # Load the environment vars from JSON file
        vars_data = self.load_json('vars.json')
        GOOGLE_API_KEY = vars_data.get("GOOGLE_API_KEY")
        GITLAB_URL = vars_data.get("GITLAB_URL")
        GITLAB_API = vars_data.get("GITLAB_API")
        GITLAB_TRIGGER_TOKEN = vars_data.get("GITLAB_TRIGGER_TOKEN")
        NETBOX_URL = vars_data.get("NETBOX_API")

        # Handle tenant and region - convert IDs to objects if needed
        # When called via API, these might be integers; when via UI, they're objects
        tenant = data["tenant"]
        if isinstance(tenant, int) or (isinstance(tenant, str) and tenant.isdigit()):
            tenant = Tenant.objects.get(id=int(tenant))
        
        region = data["region"]
        if isinstance(region, int) or (isinstance(region, str) and region.isdigit()):
            region = Region.objects.get(id=int(region))

        # Fetch GPS coordinates
        latitude, longitude = self.get_coordinates(GOOGLE_API_KEY, data["address"])

        if latitude is None or longitude is None:
            self.log_warning("Failed to fetch GPS coordinates. Aborting...")
            return

        self.log_success(
            f"Retrieved GPS coordinates: Latitude={latitude}, Longitude={longitude}"
        )

        # Create the site
        site = Site.objects.create(
            name=data["site_name"],
            slug=slugify(data["site_name"]),
            tenant=tenant,
            region=region,
            status="planned",
            physical_address=data["address"],
            latitude=latitude,
            longitude=longitude,
        )
        self.log_success(f"Created site: [{site.name}]({NETBOX_URL}/dcim/sites/{site.id}).")

        # Create the floors as locations
        lowest_floor = data["lowest_floor"]
        number_of_floors = data["number_of_floors"]
        floor_numbers = range(lowest_floor, lowest_floor + number_of_floors)

        for floor in floor_numbers:
            location_name = f"{site.name}-{floor}"

            # Use a different slug format for negative floors
            if floor < 0:
                location_slug = slugify(f"{site.name}-neg{-floor}")
            else:
                location_slug = slugify(f"{site.name}-{floor}")

            # Create the location object
            location = Location.objects.create(
                name=location_name,
                slug=location_slug,
                site=site,
                tenant=tenant,
                status="planned",
                custom_field_data={
                    "ccc_rf_model": "Cubes And Walled Offices",
                    "ccc_floor_height": 10.0,
                    "ccc_floor_length": 100.0,
                    "ccc_floor_width": 100.0,
                    "ccc_floor_units": "feet",
                    "ccc_floor_number": floor
                },
            )
            self.log_success(
                f"Created location: [{location.name}]({NETBOX_URL}/dcim/locations/{location.id}) with slug: {location.slug}."
            )

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
                "variables[SITE_PIPELINE]": "true"
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

        self.log_success("All locations and site successfully created!")