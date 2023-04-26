"""
Interface information

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_interfaces
        Gets interface information
    patch_interfaces
        Updates interface configuration
    post_interfaces_op
        Performs operational tasks on an interface

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_interfaces(device_id, interface, summary):
    '''
    Handle a GET request to the /devices/:device_id/interfaces endpoint

    Parameters:
        device_id : str
            The ID of the device
        interface : str
            A specific interface to query
        summary : bool
            True if we want just a simple summary, not all details

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check if we want a specific interface
    if interface:
        pass

    # Check if we want a summary only
    if summary:
        pass

    # Build the response
    response = {
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

    code = http_codes.HTTP_OK

    return response, code


def patch_interfaces_op(device_id, body):
    '''
    Handle a PATCH request to the /devices/:device_id/interfaces endpoint

    Parameters:
        device_id : str
            The ID of the device
        body : dict
            The operational request

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Build the response
    response = {
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

    code = http_codes.HTTP_CREATED

    return response, code


def post_interfaces_op(device_id, body):
    '''
    Handle a POST request to the /devices/:device_id/interfaces/op endpoint

    Parameters:
        device_id : str
            The ID of the device
        body : dict
            The operational request

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Build the response
    response = {
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

    code = http_codes.HTTP_OK

    return response, code
