"""
Return a list of all devices in the environment

Modules:
    3rd Party: None
    Internal: http_codes, api, config

Classes:

    Devices
        Handle a GET request to the /devices endpoint
    Hardware
        Represents the /devices/:device_id/hardware endpoint

Functions

    None

Exceptions:

    None

Misc Variables:

    SITE_TABLE : str
        The name of the table in the database that stores site information

Author:
    Luke Robertson - May 2023
"""

import endpoints.http_codes as http_codes
import endpoints.api as api
import config
from sql.sql import SqlServer


SITE_TABLE = 'sites'


class Devices(api.ApiCall):
    '''
    Create an object to represent the Devices endpoint

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    request : flask.request
        The request object from Flask
    device_id : str
        The device ID to query

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
            device_id : str
                The device ID to query

        Raises:
            None

        Returns:
            None
        '''

        # Call the superclass constructor
        super().__init__(request)

        # Store the device ID
        self.device_id = device_id

        # Look up the device in the database
        with SqlServer(
            server=config.SQL_SERVER['db_server'],
            db=config.SQL_SERVER['db_name'],
            table=config.SQL_SERVER['device_table']
        ) as site_sql:
            output = site_sql.read(
                field='id',
                value=device_id
            )[0]
        self.device_vendor = output[3]

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

        # Find the correct plugin to use
        for plugin in config.PLUGINS['loaded']:
            if self.device_vendor == plugin.vendor:
                # Get the device information from the plugin
                self.response = plugin.device(device_id=self.device_id)
                break

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


class Hardware(api.ApiCall):
    '''
    Create an object to represent the /devices/:device_id/hardware endpoint

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    request : flask.request
        The request object from Flask
    device_id : str
        The device ID to query

    Methods
    -------
    get()
        Handle a GET request to the /devices/:device_id/hardware endpoint
    '''

    def __init__(self, request, device_id):
        '''
        Class constructor

        Parameters:
            request : flask.request
                The request object from Flask
            device_id : str
                The device ID to query

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
        Handle a GET request to the /devices/:device_id/hardware endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Check if we're filtering in any way
        if self.filter:
            pass

        # Build the response
        self.response = {
            "cpu": {
                "used": 10,
                "idle": 90,
                "1_min": 5,
                "5_min": 1,
                "15_min": 1
            },
            "memory": {
                "total": 1024,
                "used": 123
            },
            "disk": [
                {
                    "disk": "/edv/da0s1a",
                    "size": 597,
                    "used": 424
                }
            ],
            "temperature": {
                "cpu": 69,
                "chassis": 42
            },
            "fan": [
                {
                    "fan": "SRX345 Chassis fan 0",
                    "status": "ok",
                    "rpm": 3840,
                    "detail": "spinning at normal speed"
                }
            ]
        }

        self.code = http_codes.HTTP_OK
