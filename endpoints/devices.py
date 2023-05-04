"""
Return a list of all devices in the environment

Modules:
    3rd Party: None
    Internal: http_codes, sql, api, config

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
    Luke Robertson - May 2023
"""

import endpoints.http_codes as http_codes
import endpoints.api as api


SITE_TABLE = 'sites'


class Devices(api.ApiCall):
    '''
    Create an object to represent the Devices endpoint

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    request : flask.request
        The request object from Flask

    Methods
    -------
    get()
        Handle a GET request to the /devices/:device_id endpoint
    post()
        Handle a POST request to the /devices/:device_id endpoint
    patch()
        Handle a PATCH request to the /devices/:device_id endpoint
    '''

    def __init__(self, request, device_id):
        '''
        Class constructor

        Parameters:
            request : flask.request
                The request object from Flask

        Raises:
            None

        Returns:
            None
        '''

        # Call the superclass constructor
        super().__init__(request)

        # Store the device ID
        self.device_id = device_id

    def get(self):
        '''
        Handle a GET request to the /devices/:device_id endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Check if we're filtering by vendor or device type
        if self.vendor:
            pass

        if self.dev_type:
            pass

        if self.filter:
            pass

        # Build the response
        self.response = {
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

        self.code = http_codes.HTTP_OK

    def post(self):
        '''
        Handle a POST request to the /devices/:device_id/op endpoint

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
        if self.body is None:
            self.response = {
                "status": "error",
                "error": "Bad parameters"
            }
            self.code = http_codes.HTTP_BADREQUEST
            return

        # Build the response
        self.response = {
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

        self.code = http_codes.HTTP_OK

    def patch(self):
        '''
        Handle a PATCH request to the /devices/:device_id endpoint

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
        if self.body is None:
            self.response = {
                "status": "error",
                "error": "Bad parameters"
            }
            self.code = http_codes.HTTP_BADREQUEST
            return

        # Build the response
        self.response = {
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

        self.code = http_codes.HTTP_OK
