"""
Handle queries devices within a site

Modules:
    3rd Party: None
    Internal: http_codes

Classes:

    None

Functions

    get_site_devices
        Get a list of devices in a site
    post_site_devices
        Create a new device in a site

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes


def get_site_devices(site_id, vendor, dev_type):
    '''
    Handle a GET request to the /sites/:site_id endpoint

    Parameters:
        None

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check if we're filtering by vendor or device type
    if vendor:
        pass

    if dev_type:
        pass

    # Build the response
    response = {
        "device_id": "acde070d-8c4c-4f0d-9d8a-162843c10444",
        "hostname": "hq-sw01",
        "vendor": "juniper",
        "type": "switch"
    }
    code = http_codes.HTTP_OK

    return response, code


def post_site_devices(site_id, body):
    '''
    Handle a POST request to the /sites/:site_id endpoint

    Parameters:
        None

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # If there are fields missing, return an error
    if ('hostname' not in body or
            'vendor' not in body or
            'type' not in body):
        response = {
            "status": "error",
            "error": "Bad parameters"
        }
        code = http_codes.HTTP_BADREQUEST

    # Create the device in the site
    else:
        response = {
            "device_id": "acde070d-8c4c-4f0d-9d8a-162843c10444",
            "hostname": "hq-sw01",
            "vendor": "juniper",
            "type": "switch"
        }
        code = http_codes.HTTP_CREATED

    return response, code
