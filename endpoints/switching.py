"""
Switching information

Modules:
    3rd Party: None
    Internal: http_codes, api

Classes:

    Vlans
        Represents the /devices/:device_id/vlans endpoint
    Mac
        Represents the /devices/:device_id/mac_table endpoint
    Lldp
        Represents the /devices/:device_id/lldp endpoint

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


class Vlans(api.ApiCall):
    '''
    Create an object to represent the /devices/:device_id/vlans endpoint

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
        Handle a GET request to the /devices/:device_id/vlans endpoint
    patch()
        Handle a PATCH request to the /devices/:device_id/vlans endpoint
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

        # Check for the 'vlan' parameter
        self.vlan = False
        if 'vlan' in self.args:
            self.vlan = self.args.getlist('vlan')

    def get(self):
        '''
        Handle a GET request to the /devices/:device_id/vlans endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Check if we want a specific vlan
        if self.vlan:
            pass

        # Build the response
        self.response = {
            "vlans": [
                {
                    "id": 44,
                    "name": "Internet",
                    "description": " Internet access for the public",
                    "irb": "irb.44"
                }
            ]
        }

        self.code = http_codes.HTTP_OK

    def patch(self):
        '''
        Handle a PATCH request to the /devices/:device_id/vlans endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Build the response
        self.response = {
            "vlans": [
                {
                    "id": 44,
                    "name": "Internet",
                    "description": " Internet access for the public",
                    "irb": "irb.44"
                }
            ]
        }

        self.code = http_codes.HTTP_CREATED


class Mac(api.ApiCall):
    '''
    Create an object to represent the /devices/:device_id/mac_table endpoint

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
        Handle a GET request to the /devices/:device_id/mac_table endpoint
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

        # Check for the 'interface' parameter
        self.interface = False
        if 'interface' in self.args:
            self.interface = self.args.getlist('interface')

        # Check for the 'mac' parameter
        self.mac = False
        if 'mac' in self.args:
            self.mac = self.args.getlist('mac')

    def get(self):
        '''
        Handle a GET request to the /devices/:device_id/vlans endpoint

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

        # Check if we want a specific mac
        if self.mac:
            pass

        # Build the response
        self.response = {
            "entry": [
                {
                    "mac": "1c:7d:22:000:00:00",
                    "vlan": "Workstations",
                    "interface": "ge-0/0/5.0"
                }
            ]
        }

        self.code = http_codes.HTTP_OK


class Lldp(api.ApiCall):
    '''
    Create an object to represent the /devices/:device_id/lldp endpoint

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
        Handle a GET request to the /devices/:device_id/lldp endpoint
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

        # Check for the 'interface' parameter
        self.interface = False
        if 'interface' in self.args:
            self.interface = self.args.getlist('interface')

    def get(self):
        '''
        Handle a GET request to the /devices/:device_id/lldp endpoint

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

        # Build the response
        self.response = {
            "interfaces": [
                {
                    "name": "ge-0/0/0",
                    "mac": "18:66:da:00:00:00",
                    "system": "WAP-1",
                    "port_name": "ETH0",
                    "ip": "10.1.1.1",
                    "vendor": "Mist Systems.",
                    "description": "Mist Systems 802.11ax Access Point.",
                    "model": "AP43-WW",
                    "serial": "Axxxxxxxxxxxx"
                }
            ]
        }

        self.code = http_codes.HTTP_OK
