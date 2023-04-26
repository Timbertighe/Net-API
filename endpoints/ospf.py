"""
Manage OSPF

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_ospf
        Gets OSPF information
    post_ospf_op
        Performs operational tasks with OSPF

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_ospf(device_id):
    '''
    Handle a GET request to the /devices/:device_id/ospf endpoint

    Parameters:
        device_id : str
            The ID of the device

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

    code = http_codes.HTTP_OK

    return response, code


def post_ospf_op(device_id, body):
    '''
    Handle a POST request to the /devices/:device_id/ospf/op endpoint

    Parameters:
        device_id : str
            The ID of the device
        body : dict
            The body of the POST message, containing operational information

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

    code = http_codes.HTTP_OK

    return response, code
