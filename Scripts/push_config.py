#!/usr/bin/env python3
"""
Push configuration to network devices via SSH using Netmiko.

This script is designed to be called from XDR Workflows via SSH.
Credentials are loaded from environment variables for security.

Usage:
    python3 push_config.py <device_ip> <device_type> <config_commands>

Environment Variables Required:
    DEVICE_USERNAME - SSH username for network devices
    DEVICE_PASSWORD - SSH password for network devices
    DEVICE_ENABLE   - Enable password (optional, for IOS devices)

Example:
    export DEVICE_USERNAME=admin
    export DEVICE_PASSWORD=cisco123
    python3 push_config.py 192.168.1.1 cisco_ios "hostname TEST,interface gi0/1,description Test"
"""

import os
import sys
import json
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def get_credentials():
    """Load credentials from environment variables."""
    username = os.environ.get('DEVICE_USERNAME')
    password = os.environ.get('DEVICE_PASSWORD')
    enable = os.environ.get('DEVICE_ENABLE', '')
    
    if not username or not password:
        raise ValueError(
            "Missing credentials. Set DEVICE_USERNAME and DEVICE_PASSWORD environment variables."
        )
    
    return username, password, enable


def push_config(device_ip: str, device_type: str, config_commands: list) -> dict:
    """
    Push configuration commands to a network device.
    
    Args:
        device_ip: IP address or hostname of the device
        device_type: Netmiko device type (cisco_ios, cisco_xe, cisco_nxos, etc.)
        config_commands: List of configuration commands to send
        
    Returns:
        dict with status, output, and any errors
    """
    username, password, enable = get_credentials()
    
    device = {
        'device_type': device_type,
        'host': device_ip,
        'username': username,
        'password': password,
        'secret': enable if enable else password,
        'timeout': 30,
        'session_timeout': 60,
    }
    
    result = {
        'status': 'success',
        'device': device_ip,
        'device_type': device_type,
        'commands_sent': len(config_commands),
        'output': '',
        'error': None
    }
    
    try:
        with ConnectHandler(**device) as conn:
            if device_type in ['cisco_ios', 'cisco_xe'] and enable:
                conn.enable()
            
            output = conn.send_config_set(config_commands)
            result['output'] = output
            
            save_output = conn.save_config()
            result['save_output'] = save_output
            
    except NetmikoTimeoutException as e:
        result['status'] = 'failed'
        result['error'] = f"Connection timeout: {str(e)}"
    except NetmikoAuthenticationException as e:
        result['status'] = 'failed'
        result['error'] = f"Authentication failed: {str(e)}"
    except Exception as e:
        result['status'] = 'failed'
        result['error'] = f"Unexpected error: {str(e)}"
    
    return result


def main():
    if len(sys.argv) < 4:
        print(json.dumps({
            'status': 'failed',
            'error': 'Usage: push_config.py <device_ip> <device_type> <config_commands>'
        }))
        sys.exit(1)
    
    device_ip = sys.argv[1]
    device_type = sys.argv[2]
    config_input = sys.argv[3]
    
    if config_input.startswith('['):
        config_commands = json.loads(config_input)
    else:
        config_commands = [cmd.strip() for cmd in config_input.split(',')]
    
    result = push_config(device_ip, device_type, config_commands)
    
    print(json.dumps(result, indent=2))
    
    if result['status'] == 'failed':
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
