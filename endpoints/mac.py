"""
MAC address table

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_mac
        Gets mac entries

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_mac(device_id, interface, mac):
    '''
    Handle a GET request to the /devices/:device_id/mac_table endpoint

    Parameters:
        device_id : str
            The ID of the device
        mac : str
            A specific mac to search for

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

    # Check if we want a specific mac
    if mac:
        pass

    # Build the response
    response = {
        "entry": [
            {
                "mac": "1c:7d:22:000:00:00",
                "vlan": "Workstations",
                "interface": "ge-0/0/5.0"
            }
        ]
    }

    code = http_codes.HTTP_OK

    return response, code
