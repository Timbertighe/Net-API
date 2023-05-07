"""
Interface information

Modules:
    3rd Party: None
    Internal: http_codes, api

Classes:

    Interfaces
        Represents the /devices/:device_id/interfaces endpoint

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - May 2023
"""

import endpoints.http_codes as http_codes
import endpoints.api as api


class Interfaces(api.ApiCall):
    '''
    Create an object to represent the /devices/:device_id/interfaces endpoint

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
        Handle a GET request to the /devices/:device_id/interfaces endpoint
    patch()
        Handle a PATCH request to the /devices/:device_id/interfaces endpoint
    post()
        Handle a POST request to the /devices/:device_id/interfaces/op endpoint
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

        # Extract parameters from the request
        self.interface = False
        self.summary = False

        # Check for the 'interface' parameter
        if 'interface' in self.args:
            self.interface = self.args.getlist('interface')

        # Check for the 'summary' parameter
        if 'summary' in self.args:
            self.summary = self.args.getlist('summary')

    def get(self):
        '''
        Handle a GET request to the /devices/:device_id/interfaces endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Check if we want a specific interface
        if self.interface:
            pass

        # Check if we want a summary only
        if self.summary:
            pass

        # Build the response
        self.response = {
            "interfaces": [
                {
                    "name": "ge-0/0/0",
                    "mac": "4c:6d:58:00:00:00",
                    "description": "Workstations",
                    "family": "",
                    "address": "",
                    "native_vlan": 1,
                    "speed": 1000,
                    "counters": {
                        "bps_in": 550800,
                        "bps_out": 682184,
                        "bytes_in": 4755699005,
                        "bytes_out": 629507153,
                        "pps_in": 51088,
                        "pps_out": 74936,
                        "packets_in": 3979923,
                        "packets_out": 2173825
                    },
                    "subinterfaces": [
                        {
                            "subinterface": "unit 0",
                            "family": "ethernet",
                            "address": "204",
                            "description": "Workstation"
                        }
                    ],
                    "poe": {
                        "admin": True,
                        "operational": True,
                        "max": 15.4,
                        "used": 11.8
                    }
                }
            ]
        }

        self.code = http_codes.HTTP_OK

    def patch(self):
        '''
        Handle a PATCH request to the /devices/:device_id/interfaces endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Build the response
        self.response = {
            "interfaces": [
                {
                    "name": "ge-0/0/0",
                    "mac": "4c:6d:58:00:00:00",
                    "description": "Workstations",
                    "family": "",
                    "address": "",
                    "native_vlan": 1,
                    "speed": 1000,
                    "counters": {
                        "bps_in": 550800,
                        "bps_out": 682184,
                        "bytes_in": 4755699005,
                        "bytes_out": 629507153,
                        "pps_in": 51088,
                        "pps_out": 74936,
                        "packets_in": 3979923,
                        "packets_out": 2173825
                    },
                    "subinterfaces": [
                        {
                            "subinterface": "unit 0",
                            "family": "ethernet",
                            "address": "204",
                            "description": "Workstation"
                        }
                    ],
                    "poe": {
                        "admin": True,
                        "operational": True,
                        "max": 15.4,
                        "used": 11.8
                    }
                }
            ]
        }

        self.code = http_codes.HTTP_CREATED

    def post(self):
        '''
        Handle a POST request to the /devices/:device_id/interfaces/op endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Build the response
        self.response = {
            "interfaces": [
                {
                    "name": "ge-0/0/0",
                    "mac": "4c:6d:58:00:00:00",
                    "description": "Workstations",
                    "family": "",
                    "address": "",
                    "native_vlan": 1,
                    "speed": 1000,
                    "counters": {
                        "bps_in": 550800,
                        "bps_out": 682184,
                        "bytes_in": 4755699005,
                        "bytes_out": 629507153,
                        "pps_in": 51088,
                        "pps_out": 74936,
                        "packets_in": 3979923,
                        "packets_out": 2173825
                    },
                    "subinterfaces": [
                        {
                            "subinterface": "unit 0",
                            "family": "ethernet",
                            "address": "204",
                            "description": "Workstation"
                        }
                    ],
                    "poe": {
                        "admin": True,
                        "operational": True,
                        "max": 15.4,
                        "used": 11.8
                    }
                }
            ]
        }

        self.code = http_codes.HTTP_OK
