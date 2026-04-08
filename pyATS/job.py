"""
Copyright (c) 2026 Cisco and/or its affiliates.

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

import os
from pyats.contrib.creators.netbox import Netbox
from pyats.easypy import run
from genie import testbed


def _env_cli_credentials():
    """Prefer CATALYSTCENTER_CLI_*; fall back to legacy DNAC_CLI_*."""
    user = os.getenv("CATALYSTCENTER_CLI_USER") or os.getenv("DNAC_CLI_USER")
    password = os.getenv("CATALYSTCENTER_CLI_PASSWORD") or os.getenv("DNAC_CLI_PASSWORD")
    return user, password

def main(runtime):
    netbox_url = os.getenv("NETBOX_API")
    netbox_token = os.getenv("NETBOX_TOKEN")
    url_filter = "status=planned"

    cli_user, cli_password = _env_cli_credentials()

    nb_testbed = Netbox(
        netbox_url=netbox_url,
        user_token=netbox_token,
        def_user=cli_user,
        def_pass=cli_password,
        url_filter=url_filter,
        verify=False
    )

    tb = nb_testbed._generate()
    devices = testbed.load(tb)

    run(testscript="test_network.py", testbed=devices, runtime=runtime, netbox_url=netbox_url, netbox_token=netbox_token)
