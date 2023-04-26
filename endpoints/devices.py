"""
Return a list of all devices in the environment

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_devices
        Get a list of devices in a site
    get_device
        Get a list of devices
    patch_device
        Update the config on a device
    post_device
        Run an operational command on a device

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_devices(vendor, dev_type):
    '''
    Handle a GET request to the /devices endpoint

    Parameters:
        None

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check if we're filtering by vendor or device type
    if vendor:
        pass

    if dev_type:
        pass

    # Build the response
    response = {
        "device_id": "acde070d-8c4c-4f0d-9d8a-162843c10444",
        "hostname": "hq-sw01",
        "vendor": "juniper",
        "type": "switch"
    }
    code = http_codes.HTTP_OK

    return response, code


def get_device(device_id, site_id, vendor, dev_type, query):
    '''
    Handle a GET request to the /devices/:device_id endpoint
    Handle a GET request to the /sites/:site_id/:device_id endpoint

    Parameters:
        None

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check if we're filtering by vendor or device type
    if vendor:
        pass

    if dev_type:
        pass

    if query:
        pass

    # Build the response
    response = {
        "device_id": "acde070d-8c4c-4f0d-9d8a-162843c10444",
        "hostname": "hq-sw01",
        "vendor": "juniper",
        "type": "switch",
        "serial": "CWxxxxxxxxxx",
        "uptime": 1502870,
        "licenses": [
            {
                "lic_id": " JUNOSxxxxxxxxx",
                "name": "wf_key_websense_ewf",
                "expiry": "2023-03-20 11:00:00 EST"
            }
        ],
        "radius-servers": [
            {
                "server": "10.1.1.1",
                "port": 1812,
                "acc_port": 1813,
                "timeout": 5,
                "retry": 3,
                "source": "10.10.10.10"
            }
        ],
        "syslog-servers": [
            {
                "server": "10.1.1.1",
                "facilities": "any",
                "level": "notice",
                "source": "10.10.10.10",
                "prefix": "hq-sw01"
            }
        ],
        "ntp-servers": [
            {
                "server": "10.1.1.1",
                "prefer": False
            }
        ],
        "dns-servers": [
            {
                "server": "10.1.1.1",
                "source": False,
                "domain": "mydomain.com"
            }
        ],
        "snmp": {
            "name": "hq-sw01",
            "contact": "John Smith",
            "description": "first floor switch",
            "communities": [
                {
                    "community": "SNMPCommunity",
                    "auth": "RO",
                    "clients": [
                        "10.1.1.1",
                        "10.1.1.2"
                    ]
                }
            ]
        }
    }

    code = http_codes.HTTP_OK

    return response, code


def patch_device(device_id, site_id, body):
    '''
    Handle a PATCH request to the /devices/:device_id endpoint
    Handle a PATCH request to the /sites/:site_id/:device_id endpoint

    This is used to update config on a device

    Parameters:
        None

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check that there's a body
    if body is False:
        response = {
            "status": "error",
            "error": "Bad parameters"
        }
        code = http_codes.HTTP_BADREQUEST
        return response, code

    # Build the response
    response = {
        "device_id": " acde070d-8c4c-4f0d-9d8a-162843c10444",
        "hostname": "hq-sw01",
        "vendor": "juniper",
        "type": "switch",
        "serial": "CWxxxxxxxxxx",
        "uptime": 1502870,
        "licenses": [
            {
                "lic_id": " JUNOSxxxxxxxxx",
                "name": "wf_key_websense_ewf",
                "expiry": "2023-03-20 11:00:00 EST"
            }
        ],
        "radius-servers": [
            {
                "server": "10.1.1.1",
                "port": 1812,
                "acc_port": 1813,
                "timeout": 5,
                "retry": 3,
                "source": "10.10.10.10"
            }
        ],
        "syslog-servers": [
            {
                "server": "10.1.1.1",
                "facilities": "any",
                "level": "notice",
                "source": "10.10.10.10",
                "prefix": "hq-sw01"
            }
        ],
        "ntp-servers": [
            {
                "server": "10.1.1.1",
                "prefer": False
            }
        ],
        "dns-servers": [
            {
                "server": "10.1.1.1",
                "source": False,
                "domain": "mydomain.com"
            }
        ],
        "snmp": {
            "name": "hq-sw01",
            "contact": "John Smith",
            "description": "first floor switch",
            "communities": [
                {
                    "community": "SNMPCommunity",
                    "auth": "RO",
                    "clients": [
                        "10.1.1.1",
                        "10.1.1.2"
                    ]
                }
            ]
        }
    }

    code = http_codes.HTTP_OK

    return response, code


def post_device(device_id, site_id, body):
    '''
    Handle a POST request to the /devices/:device_id/op endpoint
    Handle a POST request to the /sites/:site_id/:device_id/op endpoint

    This is used to run operational commands on a device

    Parameters:
        None

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check that there's a body
    if body is False:
        response = {
            "status": "error",
            "error": "Bad parameters"
        }
        code = http_codes.HTTP_BADREQUEST
        return response, code

    # Build the response
    response = {
        "device_id": " acde070d-8c4c-4f0d-9d8a-162843c10444",
        "hostname": "hq-sw01",
        "vendor": "juniper",
        "type": "switch",
        "serial": "CWxxxxxxxxxx",
        "uptime": 1502870,
        "licenses": [
            {
                "lic_id": " JUNOSxxxxxxxxx",
                "name": "wf_key_websense_ewf",
                "expiry": "2023-03-20 11:00:00 EST"
            }
        ],
        "radius-servers": [
            {
                "server": "10.1.1.1",
                "port": 1812,
                "acc_port": 1813,
                "timeout": 5,
                "retry": 3,
                "source": "10.10.10.10"
            }
        ],
        "syslog-servers": [
            {
                "server": "10.1.1.1",
                "facilities": "any",
                "level": "notice",
                "source": "10.10.10.10",
                "prefix": "hq-sw01"
            }
        ],
        "ntp-servers": [
            {
                "server": "10.1.1.1",
                "prefer": False
            }
        ],
        "dns-servers": [
            {
                "server": "10.1.1.1",
                "source": False,
                "domain": "mydomain.com"
            }
        ],
        "snmp": {
            "name": "hq-sw01",
            "contact": "John Smith",
            "description": "first floor switch",
            "communities": [
                {
                    "community": "SNMPCommunity",
                    "auth": "RO",
                    "clients": [
                        "10.1.1.1",
                        "10.1.1.2"
                    ]
                }
            ]
        }
    }

    code = http_codes.HTTP_OK

    return response, code
