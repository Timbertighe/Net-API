"""
Manage routing functions (eg, routing table, OSPF)

Modules:
    3rd Party: None
    Internal: http_codes, api

Classes:

    Routing_Table
        Represents the /devices/:device_id/routing_table endpoint
    Ospf
        Represents the /devices/:device_id/ospf endpoint

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


class Routing_Table(api.ApiCall):
    '''
    Object to represent the /devices/:device_id/routing_table endpoint

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
        Handle a GET request to the /devices/:device_id/routing_table endpoint
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

        # Check for the 'route' parameter
        self.route = False
        if 'route' in self.args:
            self.route = self.args.getlist('route')

    def get(self):
        '''
        Handle a GET request to the /devices/:device_id/routing_table endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Check if we want a specific interface
        if self.route:
            pass

        # Build the response
        self.response = {
            "entry": [
                {
                    "route": " 10.1.1.0/24",
                    "next-hop": [
                        {
                            "hop": "10.2.2.2",
                            "protocol": "Static/5",
                            "interface": "vlan.29",
                            "metric": 0,
                            "active": True
                        }
                    ]
                }
            ]
        }

        self.code = http_codes.HTTP_OK


class Ospf(api.ApiCall):
    '''
    Object to represent the /devices/:device_id/ospf endpoint

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
        Handle a GET request to the /devices/:device_id/routing_table endpoint
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
        Handle a GET request to the /devices/:device_id/ospf endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Build the response
        self.response = {
            "id": "10.1.1.1",
            "reference": "100g",
            "areas": [
                {
                    "id": "0.0.0.10",
                    "type": "Not Stub",
                    "auth_type": "None",
                    "neighbors": 2
                }
            ],
            "neighbor": [
                {
                    "address": "172.1.1.1",
                    "interface": "st0.41",
                    "state": "Full",
                    "id": "10.2.2.2",
                    "area": "0.0.0.10"
                }
            ],
            "interface": [
                {
                    "name": "irb.10",
                    "state": "DRother",
                    "area": "0.0.0.10",
                    "neighbors": 0,
                    "mtu": 9192,
                    "cost": 8015,
                    "type": "P2MP",
                    "mask": "255.255.255.0",
                    "Auth_type": "None",
                    "passive": True
                }
            ]
        }

        self.code = http_codes.HTTP_OK

    def post(self):
        '''
        Handle a POST request to the /devices/:device_id/ospf/op endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Build the response
        self.response = {
            "id": "10.1.1.1",
            "reference": "100g",
            "areas": [
                {
                    "id": "0.0.0.10",
                    "type": "Not Stub",
                    "auth_type": "None",
                    "neighbors": 2
                }
            ],
            "neighbor": [
                {
                    "address": "172.2.2.2",
                    "interface": "st0.41",
                    "state": "Full",
                    "id": "10.2.2.2",
                    "area": "0.0.0.10"
                }
            ],
            "interface": [
                {
                    "name": "irb.10",
                    "state": "DRother",
                    "area": "0.0.0.10",
                    "neighbors": 0,
                    "mtu": 9192,
                    "cost": 8015,
                    "type": "P2MP",
                    "mask": "255.255.255.0",
                    "Auth_type": "None",
                    "passive": True
                }
            ]
        }

        self.code = http_codes.HTTP_OK
