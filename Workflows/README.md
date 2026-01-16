# Cisco Workflows - NetBox and Catalyst Center Integration

This directory contains automation workflows for integrating **NetBox** as the source of truth with **Cisco Catalyst Center** for network infrastructure provisioning and device onboarding.

## Operation Types

### Site Management Operations

Workflows designed for network site provisioning including:

- Site and building hierarchy creation in both NetBox and Catalyst Center
- Floor/location management with GPS coordinate lookup
- Automatic synchronization between NetBox and Catalyst Center

### Device Onboarding Operations

Workflows specifically designed for switch onboarding including:

- Device registration in NetBox with proper attributes
- IP address management and prefix creation
- Plug and Play (PnP) device claiming in Catalyst Center
- Network validation testing with pyATS

## Directory Structure

```text
Workflows/
├── README.md
├── Atomic_GetDataFromNetBox.json
├── Atomic_GetGPSFromGoogleAPI.json
├── Atomic_PatchDataInNetBox.json
├── Atomic_PostDataToNetBox.json
├── Master_CreateSite.json
├── Master_OnboardSwitch.json
├── Sub_Onboard_AddSwitchesToSite.json
├── Sub_Onboard_CreatePrefixesAndIPs.json
├── Sub_Onboard_RunPyATSTests.json
├── Sub_Onboard_SwitchViaPnP.json
├── Sub_Site_CreateHierarchy.json
├── Sub_Site_CreateInNetBox.json
└── Demo_CreateSiteViaScript.json
```

## Current Workflows

The following workflows are available in this repository:

### Atomic Workflows

| Workflow Name | Description | Type |
|---------------|-------------|------|
| Get Data from NetBox | Generic GET requests to NetBox API with query parameter support | Atomic |
| Post Data to NetBox | Generic POST requests to create objects in NetBox | Atomic |
| Patch Data in NetBox | Generic PATCH requests to update existing objects in NetBox | Atomic |
| Get GPS from Google API | Geocoding via Google Maps API for site address lookup | Atomic |

### Master Workflows

| Workflow Name | Description | Type |
|---------------|-------------|------|
| Create Site | Creates a new site in both NetBox and Catalyst Center with floor locations | Master |
| Onboard Switch | Complete switch onboarding process from NetBox to Catalyst Center | Master |

### Site Management Workflows

| Workflow Name | Description | Type |
|---------------|-------------|------|
| Create in NetBox | Creates site and floor locations in NetBox with GPS coordinates | Sub |
| Create Hierarchy in CCC | Creates site hierarchy in Catalyst Center from NetBox data | Sub |

### Demo Workflows

| Workflow Name | Description | Type |
|---------------|-------------|------|
| Create Site via NetBox Script | Demonstrates calling a NetBox custom script to create sites | Demo |

### Device Onboarding Workflows

| Workflow Name | Description | Type |
|---------------|-------------|------|
| Add Switches to Site | Adds switch devices to a site in NetBox with auto-naming | Sub |
| Create Prefixes and IPs | Creates IP prefixes and addresses from Catalyst Center PnP data | Sub |
| Claim Device via PnP | Claims devices in Catalyst Center via Plug and Play API | Sub |
| Run pyATS Tests | Runs pyATS network tests to validate device configuration | Sub |

## Workflow Dependencies

```text
Master_CreateSite
├── Sub_Site_CreateInNetBox
│   ├── Atomic_GetDataFromNetBox
│   ├── Atomic_PostDataToNetBox
│   └── Atomic_GetGPSFromGoogleAPI
└── Sub_Site_CreateHierarchy
    ├── Atomic_GetDataFromNetBox
    └── Atomic_PatchDataInNetBox

Master_OnboardSwitch
├── Sub_Onboard_AddSwitchesToSite
│   ├── Atomic_GetDataFromNetBox
│   ├── Atomic_PostDataToNetBox
│   └── Atomic_PatchDataInNetBox
├── Sub_Onboard_CreatePrefixesAndIPs
│   ├── Atomic_GetDataFromNetBox
│   ├── Atomic_PostDataToNetBox
│   └── Atomic_PatchDataInNetBox
├── Sub_Onboard_SwitchViaPnP
│   ├── Atomic_GetDataFromNetBox
│   └── Atomic_PatchDataInNetBox
└── Sub_Onboard_RunPyATSTests
```

## Target Configuration

Workflows use a **Target Group** with **Global Variables** for dynamic target selection, making them portable across environments.

### Target Group

Create a target group named `BRKOPS-2357` containing:

| Target Type | Description |
|-------------|-------------|
| `netbox.endpoint` | NetBox API endpoint |
| `catalystcenter.endpoint` | Catalyst Center API endpoint |
| `terminal.unix_linux_endpoint` | SSH host for pyATS tests |
| `web-service.endpoint` | Google Maps API |

### Global Variables

Create these global variables to control target selection:

| Variable Name | Type | Value | Description |
|---------------|------|-------|-------------|
| `Target_NetBox` | String | `NetBox` | Display name of NetBox target |
| `Target_CatC` | String | `dCloud Catalyst Center` | Display name of Catalyst Center target |
| `Target_Docker` | String | `dCloud Docker` | Display name of SSH host target for pyATS |
| `Target_GoogleMapsAPI` | String | `Google Maps API` | Display name of Google API target |
| `Google API Key` | Secure String | `*****` | Google Maps Geocoding API key |

### How It Works

Each workflow activity uses target group criteria to select the appropriate target:

```json
"target": {
  "override_workflow_target_group_criteria": true,
  "target_group": {
    "use_criteria": {
      "choose_target_using_algorithm": "choose_first_with_matching_criteria",
      "conditions": [{
        "left_operand": "$targetgroup.display_name$",
        "operator": "eq",
        "right_operand": "$global.variable.Target_NetBox$"
      }]
    }
  }
}
```

This allows you to:
- Change targets by updating global variables (no workflow edits needed)
- Use different targets for different environments
- Share workflows without exposing environment-specific details

## Prerequisites

### NetBox Access

- NetBox instance with API access enabled
- API token with read/write privileges
- Configured tenants, regions, device types, and device roles

### Catalyst Center Access

- Catalyst Center platform with appropriate licensing
- API credentials with sufficient privileges
- Network connectivity to Catalyst Center instance
- Pre-configured site hierarchy (tenant and region levels)

### NetBox Custom Fields

Devices require the following custom fields for Catalyst Center integration:

| Field | Description |
|-------|-------------|
| `ccc_pid` | Catalyst Center Product ID |
| `ccc_template_name` | Day-0 template name in Catalyst Center |
| `ccc_location` | Floor/location name for site path construction |
| `ccc_ip` | Management IP in CIDR notation |

### pyATS Testing Requirements

- SSH host with Python 3 and pyATS installed in a virtual environment
- pyATS venv at `{pyATS Scripts Path}/venv`
- Network connectivity to devices under test
- `.env` file with credentials (NETBOX_API, NETBOX_TOKEN, DNAC_CLI_USER, DNAC_CLI_PASSWORD)

## Import Order

When importing workflows, follow this order:

1. **Create Target Group** and add your targets
2. **Create Global Variables** for target selection
3. **Import Atomic Workflows** (no dependencies)
4. **Import Sub-Workflows** (depend on Atomic workflows)
5. **Import Master Workflows** (depend on Sub-Workflows)

## Usage

### Create a New Site

1. Run **[Master] Create Site**
2. Select tenant and region from dropdowns
3. Enter site name, address, and floor configuration
4. Workflow creates site in NetBox and Catalyst Center automatically

### Onboard Switches

1. Ensure switches have contacted Catalyst Center (visible in PnP)
2. Run **[Master] Onboard Switch**
3. Select tenant, site, device type, and role from dropdowns
4. Enter comma-separated serial numbers
5. Workflow handles device creation, IP assignment, PnP claiming, and validation

## Security

All credentials are properly masked (`*****`) in exported workflows:

| Credential Type | Status |
|-----------------|--------|
| NetBox API tokens | ✅ Masked |
| Catalyst Center passwords | ✅ Masked |
| SSH passwords | ✅ Masked |
| Google API key | ✅ Masked |

**Note:** After importing, you must reconfigure:
- Runtime user credentials
- Target endpoint addresses
- Global variable values

---

*For more Catalyst Center workflows, see the [CiscoDevNet/CiscoWorkflowsAutomation](https://github.com/CiscoDevNet/CiscoWorkflowsAutomation/tree/main/Catalyst_Center) repository.*
