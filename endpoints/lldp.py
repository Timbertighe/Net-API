"""
LLDP neighbour information

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_lldp
        Gets interface information

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_lldp(device_id, interface):
    '''
    Handle a GET request to the /devices/:device_id/lldp endpoint

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

    # Check if we want a specific interface
    if interface:
        pass

    # Build the response
    response = {
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

    code = http_codes.HTTP_OK

    return response, code
