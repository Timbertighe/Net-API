"""
Return hardware information for a device

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    hardware
        Get hardware information for a device

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_hardware(device_id, query):
    '''
    Handle a GET request to the /devices/:device_id/hardware endpoint

    Parameters:
        device_id : str
            The ID of the device
        query : list
            Parameters to filter the output

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check if we're filtering in any way
    if query:
        pass

    # Build the response
    response = {
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

    code = http_codes.HTTP_OK

    return response, code
