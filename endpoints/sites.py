"""
Handle queries about sites

Modules:
    3rd Party: uuid, traceback
    Internal: http_codes

Classes:

    None

Functions

    get_sites
        Get a list of sites
    post_sites
        Add a new site
    patch_sites
        Update a site
    delete_sites
        Delete a site
    get_site_devices
        Get a list of devices in a site
    post_site_devices
        Create a new device in a site
    patch_site_devices
        Update a device's information
    delete_site_devices
        Delete a device

Exceptions:

    None

Misc Variables:

    SITE_TABLE : str
        The SQL table name for sites
    DEVICE_TABLE : str
        The SQL table name for devices

To Do:
    PATCH device should only update the fields provided

Author:
    Luke Robertson - April 2023
"""

import endpoints.http_codes as http_codes
import config
from sql.sql import SqlServer
import uuid


SITE_TABLE = 'sites'
DEVICE_TABLE = 'devices'


def get_sites():
    '''
    Handle a GET request to the /sites endpoint

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

    # Connect to the database and get a list of all sites
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=SITE_TABLE
    ) as site_sql:
        # Empty field and value mean 'get all records'
        output = site_sql.read(
            field='',
            value=''
        )

    # if there was a response, build it into a list of entries
    if output:
        response = []
        for record in output:
            entry = {
                "site_id": record[0],
                "site_name": record[1]
            }
            response.append(entry)
            code = http_codes.HTTP_OK

    else:
        response = ''
        code = http_codes.HTTP_NOTFOUND

    return response, code


def post_sites(body):
    '''
    Handle a POST request to the /sites endpoint

    Parameters:
        body : json
            The body of the request

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Check if the site name already exists
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=SITE_TABLE
    ) as site_sql:
        output = site_sql.read(
            field='name',
            value=body['site_name']
        )

    # If there was a response, return an error
    if output:
        response = {
            "status": "error",
            "error": "Site name already exists"
        }
        code = http_codes.HTTP_CONFLICT
        return response, code

    # Generate a UUID
    site_id = uuid.uuid4()

    # Build a dictionary of fields
    fields = {
        'id': site_id,
        'name': body['site_name']
    }

    # Connect to the database and add a new site record
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=SITE_TABLE
    ) as site_sql:
        output = site_sql.add(
            fields=fields,
        )

    # If there was an error, return it
    if not output:
        response = {
            "status": "error",
            "error": "SQL error"
        }
        code = http_codes.HTTP_BADREQUEST

    else:
        response = {
            "site_id": site_id,
            "site_name": body['site_name']
        }
        code = http_codes.HTTP_CREATED

    return response, code


def patch_sites(body):
    '''
    Handle a PATCH request to the /sites endpoint

    Parameters:
        body : json
            The body of the request

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    # Build a dictionary of fields
    fields = {
        'name': body['site_name']
    }

    # Connect to the database and update the site record
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=SITE_TABLE
    ) as site_sql:
        output = site_sql.update(
            field='id',
            value=body['site_id'],
            body=fields,
        )

    # If there was an error, return it
    if not output:
        response = {
            "status": "error",
            "error": "SQL error"
        }
        code = http_codes.HTTP_BADREQUEST

    else:
        response = {
            "site_id": body['site_id'],
            "site_name": body['site_name']
        }
        code = http_codes.HTTP_OK

    return response, code


def delete_sites(body):
    '''
    Handle a DELETE request to the /sites endpoint

    Parameters:
        body : json
            The body of the request

    Raises:
        None

    Returns:
        response : str
            Return an empty string for a DELETE
        code : int
            The HTTP response code
    '''

    # Connect to the database and delete the site record
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=SITE_TABLE
    ) as site_sql:
        output = site_sql.delete(
            field='id',
            value=body['site_id'],
        )

    # If there was an error, return it
    if not output:
        response = {
            "status": "error",
            "error": "SQL error"
        }
        code = http_codes.HTTP_BADREQUEST

    else:
        response = ''
        code = http_codes.HTTP_NOCONTENT

    return response, code


def get_site_devices(site_id, vendor, dev_type):
    '''
    Handle a GET request to the /sites/:site_id endpoint

    Parameters:
        site_id : str
            The UUID of the site
        vendor : str
            The device vendor (eg, 'juniper')
        dev_type : str
            The type of a device (eg, 'switch')

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

    # Connect to the database and get a list devices in a site
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=DEVICE_TABLE
    ) as site_sql:
        output = site_sql.read(
            field='site',
            value=site_id
        )

    # If there was an error, return it
    if not output:
        response = {
            "status": "error",
            "error": ("Site ID is incorrect, "
                      "or there are no devices in the site")
        }
        code = http_codes.HTTP_BADREQUEST

    # Otherwise, build the response
    else:
        response = []
        for record in output:
            entry = {
                "device_id": record[0],
                "hostname": record[1],
                "site": record[2],
                "vendor": record[3],
                "type": record[4],
                "auth_type": record[5],
                "username": record[6],
                "secret": record[7],
                "salt": record[8],
                "token": record[9],
            }
            response.append(entry)
        code = http_codes.HTTP_OK

    return response, code


def post_site_devices(site_id, body):
    '''
    Handle a POST request to the /sites/:site_id endpoint

    Parameters:
        site_id : str
            The UUID of the site
        body : json
            The body of the request

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
            'auth_type' not in body or
            'type' not in body):
        response = {
            "status": "error",
            "error": "Bad parameters"
        }
        code = http_codes.HTTP_BADREQUEST

        return response, code

    # Check if the site exists
    if not site_exists(site_id):
        response = {
            "status": "error",
            "error": "Site ID is incorrect"
        }
        code = http_codes.HTTP_BADREQUEST

        return response, code

    # Check if the device already exists
    if device_exists(
        site_id=site_id,
        device_id=body['device_id'],
        hostname=body['hostname']
    ):
        response = {
            "status": "error",
            "error": "Device already exists"
        }
        code = http_codes.HTTP_BADREQUEST

        return response, code

    # Generate a UUID
    device_id = uuid.uuid4()

    # Build a dictionary of fields
    fields = {
        'id': device_id,
        'name': body['hostname'],
        'site': site_id,
        'vendor': body['vendor'],
        'type': body['type'],
        'auth_type': body['auth_type'],
    }

    # Handle auth_type
    if body['auth_type'] == 'secret':
        fields['secret'] = body['secret']
        fields['username'] = body['username']
        fields['salt'] = body['salt']
    elif body['auth_type'] == 'token':
        fields['token'] = body['token']
    else:
        response = {
            "status": "error",
            "error": "Wrong auth_type"
        }
        code = http_codes.HTTP_BADREQUEST
        return response, code

    # Connect to the database and add a new device record
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=DEVICE_TABLE
    ) as site_sql:
        output = site_sql.add(
            fields=fields,
        )

    # If there was an error, return it
    if not output:
        response = {
            "status": "error",
            "error": "SQL error"
        }
        code = http_codes.HTTP_BADREQUEST

    # Otherwise, return the new device
    else:
        response = {
            "device_id": device_id,
            "hostname": body['hostname'],
            "site": site_id,
            "vendor": body['vendor'],
            "type": body['type'],
            "auth_type": body['auth_type'],
            "username": body['username'],
            "secret": body['secret'],
            "salt": body['salt'],
            "token": body['token']
        }
        code = http_codes.HTTP_CREATED

    return response, code


def patch_site_devices(site_id, body):
    '''
    Handle a PATCH request to the /sites/:site_id endpoint

    Parameters:
        site_id : str
            The UUID of the site
        body : json
            The body of the request

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the updated object
        code : int
            The HTTP response code
    '''

    # If there are fields missing, return an error
    if 'device_id' not in body:
        response = {
            "status": "error",
            "error": "Bad parameters"
        }
        code = http_codes.HTTP_BADREQUEST

        return response, code

    # Check if the site exists
    if not site_exists(site_id):
        response = {
            "status": "error",
            "error": "Site ID is incorrect"
        }
        code = http_codes.HTTP_BADREQUEST

        return response, code

    # Build a dictionary of fields
    #   Only include fields that are in the body
    fields = {
        'id': body['device_id'],
        'site': site_id,
    }

    if 'hostname' in body:
        fields['name'] = body['hostname']

    if 'vendor' in body:
        fields['vendor'] = body['vendor']

    if 'type' in body:
        fields['type'] = body['type']

    if 'auth_type' in body:
        fields['auth_type'] = body['auth_type']

    if 'username' in body:
        fields['username'] = body['username']

    if 'secret' in body:
        fields['secret'] = body['secret']

    if 'salt' in body:
        fields['salt'] = body['salt']

    if 'token' in body:
        fields['token'] = body['token']

    # Send the fields to the database
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=DEVICE_TABLE
    ) as site_sql:
        output = site_sql.update(
            field='id',
            value=body['device_id'],
            body=fields
        )

    # If there was an error, return it
    if not output:
        response = {
            "status": "error",
            "error": "SQL error"
        }
        code = http_codes.HTTP_BADREQUEST

    # Otherwise, return the updated device
    else:
        # Read the device from the database
        with SqlServer(
            server=config.SQLSERVER,
            db=config.DATABASE,
            table=DEVICE_TABLE
        ) as site_sql:
            output = site_sql.read(
                field='id',
                value=body['device_id']
            )

        response = {
            "device_id": output[0][0],
            "hostname": output[0][1],
            "site": output[0][2],
            "vendor": output[0][3],
            "type": output[0][4],
            "auth_type": output[0][5],
            "username": output[0][6],
            "secret": output[0][7],
            "salt": output[0][8],
            "token": output[0][9],
        }
        code = http_codes.HTTP_CREATED

    return response, code


def delete_site_devices(site_id, body):
    '''
    Handle a DELETE request to the /sites/:site_id endpoint

    Parameters:
        site_id : str
            The UUID of the site
        body : json
            The body of the request

    Raises:
        None

    Returns:
        response : str
            An empty string, or JSON error
        code : int
            The HTTP response code
    '''

    # If there are fields missing, return an error
    if 'device_id' not in body:
        response = {
            "status": "error",
            "error": "Bad parameters"
        }
        code = http_codes.HTTP_BADREQUEST

        return response, code

    # Check if the site exists
    if not site_exists(site_id):
        response = {
            "status": "error",
            "error": "Site ID is incorrect"
        }
        code = http_codes.HTTP_BADREQUEST

        return response, code

    # Delete the device in the site
    # Send the fields to the database
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=DEVICE_TABLE
    ) as site_sql:
        output = site_sql.delete(
            field='id',
            value=body['device_id']
        )

    # If there was an error, return it
    if not output:
        response = {
            "status": "error",
            "error": "SQL error"
        }
        code = http_codes.HTTP_BADREQUEST

    # Otherwise, return an empty string
    else:
        response = ''
        code = http_codes.HTTP_NOCONTENT

    return response, code


def site_exists(site_id):
    '''
    Check if a site exists

    Parameters:
        site_id : str
            The UUID of the site

    Raises:
        None

    Returns:
        response : bool
            True if the site exists, False otherwise
    '''

    # Check if the site exists
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=SITE_TABLE
    ) as site_sql:
        output = site_sql.read(
            field='id',
            value=site_id
        )

    # If there was an error (no site), return it
    if not output:
        return False

    return True


def device_exists(site_id, device_id, hostname):
    '''
    Check if a device exists by id and hostname, and is in the right site

    Parameters:
        site_id : str
            The UUID of the site
        device_id : str
            The UUID of the device

    Raises:
        None

    Returns:
        response : bool
            True if the device does not exist, False otherwise
    '''

    # Check if the device exists
    with SqlServer(
        server=config.SQLSERVER,
        db=config.DATABASE,
        table=DEVICE_TABLE
    ) as site_sql:
        output = site_sql.read(
            field='id',
            value=device_id
        )

    # If there was an error (no device), return it
    if not output:
        return False

    # If the site ID doesn't match, return False
    if output[0]['site'] != site_id:
        return False

    # If the hostname already exists, return False
    if output[0]['hostname'] == hostname:
        return False

    return True
