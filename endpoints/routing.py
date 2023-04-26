"""
Routing table

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_routes
        Gets routing table entries

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_routes(device_id, route):
    '''
    Handle a GET request to the /devices/:device_id/routing_table endpoint

    Parameters:
        device_id : str
            The ID of the device
        route : str
            A specific route to search for

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
    if route:
        pass

    # Build the response
    response = {
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

    code = http_codes.HTTP_OK

    return response, code
