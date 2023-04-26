"""
VLAN information

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_vlans
        Gets vlan information
    patch_vlans
        Updates vlan configuration

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_vlans(device_id, vlan):
    '''
    Handle a GET request to the /devices/:device_id/vlans endpoint

    Parameters:
        device_id : str
            The ID of the device
        interface : str
            A specific interface to query

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check if we want a specific vlan
    if vlan:
        pass

    # Build the response
    response = {
        "vlans": [
            {
                "id": 44,
                "name": "Internet",
                "description": " Internet access for the public",
                "irb": "irb.44"
            }
        ]
    }

    code = http_codes.HTTP_OK

    return response, code


def patch_vlans(device_id, body):
    '''
    Handle a PATCH request to the /devices/:device_id/vlans endpoint

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
        "vlans": [
            {
                "id": 44,
                "name": "Internet",
                "description": " Internet access for the public",
                "irb": "irb.44"
            }
        ]
    }

    code = http_codes.HTTP_CREATED

    return response, code
