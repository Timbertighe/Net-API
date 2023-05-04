"""
Handle queries about sites

Modules:
    3rd Party: uuid
    Internal: http_codes

Classes:

    Sites
        Handle queries about sites
    SiteDevices
        Handle queries about devices in a site

Functions

    None

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
import endpoints.api as api
import config
from sql.sql import SqlServer

import uuid


SITE_TABLE = 'sites'
DEVICE_TABLE = 'devices'


class Sites(api.ApiCall):
    '''
    Create an object to represent the Sites endpoint

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    request : flask.request
        The request object from Flask

    Methods
    -------
    get()
        Handle a GET request to the /sites endpoint
    post()
        Handle a POST request to the /sites endpoint
    patch()
        Handle a PATCH request to the /sites endpoint
    delete()
        Handle a DELETE request to the /sites endpoint
    '''

    def __init__(self, request):
        '''
        Class constructor

        Parameters:
            request : flask.request
                The request object from Flask

        Raises:
            None

        Returns:
            None
        '''

        # Call the superclass constructor
        super().__init__(request)

    def get(self):
        '''
        Handle a GET request to the /sites endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
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
            self.response = []
            for record in output:
                entry = {
                    "site_id": record[0],
                    "site_name": record[1]
                }
                self.response.append(entry)
                self.code = http_codes.HTTP_OK

        else:
            self.response = ''
            self.code = http_codes.HTTP_NOTFOUND

    def post(self):
        '''
        Handle a POST request to the /sites endpoint

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

        # Check if the site name already exists
        with SqlServer(
            server=config.SQLSERVER,
            db=config.DATABASE,
            table=SITE_TABLE
        ) as site_sql:
            output = site_sql.read(
                field='name',
                value=self.body['site_name']
            )

        # If there was a response, return an error
        if output:
            self.response = {
                "status": "error",
                "error": "Site name already exists"
            }
            self.code = http_codes.HTTP_CONFLICT
            return

        # Generate a UUID
        site_id = uuid.uuid4()

        # Build a dictionary of fields
        fields = {
            'id': site_id,
            'name': self.body['site_name']
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
            self.response = {
                "status": "error",
                "error": "SQL error"
            }
            self.code = http_codes.HTTP_BADREQUEST

        else:
            self.response = {
                "site_id": str(site_id),
                "site_name": self.body['site_name']
            }
            self.code = http_codes.HTTP_CREATED

    def patch(self):
        '''
        Handle a PATCH request to the /sites endpoint

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

        # Build a dictionary of fields
        fields = {
            'name': self.body['site_name']
        }

        # Connect to the database and update the site record
        with SqlServer(
            server=config.SQLSERVER,
            db=config.DATABASE,
            table=SITE_TABLE
        ) as site_sql:
            output = site_sql.update(
                field='id',
                value=self.body['site_id'],
                body=fields,
            )

        # If there was an error, return it
        if not output:
            self.response = {
                "status": "error",
                "error": "SQL error"
            }
            self.code = http_codes.HTTP_BADREQUEST

        else:
            self.response = {
                "site_id": self.body['site_id'],
                "site_name": self.body['site_name']
            }
            self.code = http_codes.HTTP_OK

    def delete(self):
        '''
        Handle a DELETE request to the /sites endpoint

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

        # Connect to the database and delete the site record
        with SqlServer(
            server=config.SQLSERVER,
            db=config.DATABASE,
            table=SITE_TABLE
        ) as site_sql:
            output = site_sql.delete(
                field='id',
                value=self.body['site_id'],
            )

        # If there was an error, return it
        if not output:
            self.response = {
                "status": "error",
                "error": "SQL error"
            }
            self.code = http_codes.HTTP_BADREQUEST

        else:
            self.response = ''
            self.code = http_codes.HTTP_NOCONTENT


class SiteDevices(api.ApiCall):
    '''
    Create an object to represent the Sites endpoint

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    request : flask.request
        The request object from Flask

    Methods
    -------
    get()
        Handle a GET request to the /sites/:site_id endpoint
    post()
        Handle a POST request to the /sites/:site_id endpoint
    patch()
        Handle a PATCH request to the /sites/:site_id endpoint
    delete()
        Handle a DELETE request to the /sites/:site_id endpoint
    '''

    def __init__(self, request, site_id):
        '''
        Class constructor

        Parameters:
            request : flask.request
                The request object from Flask

        Raises:
            None

        Returns:
            None
        '''

        # Call the superclass constructor
        super().__init__(request)

        # Set the site_id
        self.site_id = site_id

        # Extract parameters from the request
        self.vendor = False
        self.dev_type = False

        # Check for the 'vendor' parameter
        if 'vendor' in self.args:
            vendor = self.args.getlist('vendor')

            # There can only be one vendor
            if len(vendor) != 1:
                response = {
                    "status": "error",
                    "error": "Bad JSON"
                }
                code = http_codes.HTTP_BADREQUEST
                return response, code

        # Check for the 'type' parameter
        if 'type' in self.args:
            self.dev_type = self.args.getlist('type')

    def get(self):
        '''
        Handle a GET request to the /sites/:site_id endpoint

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        '''

        # Check if the site exists
        if not self.site_exists(self.site_id):
            self.response = {
                "status": "error",
                "error": "Site ID is incorrect"
            }
            self.code = http_codes.HTTP_BADREQUEST

            return

        # Check if we're filtering by vendor or device type
        if self.vendor:
            pass

        if self.dev_type:
            pass

        # Connect to the database and get a list devices in a site
        with SqlServer(
            server=config.SQLSERVER,
            db=config.DATABASE,
            table=DEVICE_TABLE
        ) as site_sql:
            output = site_sql.read(
                field='site',
                value=self.site_id
            )

        # If there was an error, return it
        if not output:
            self.response = {
                "status": "error",
                "error": ("Site ID is incorrect, "
                          "or there are no devices in the site")
            }
            self.code = http_codes.HTTP_BADREQUEST

        # Otherwise, build the response
        else:
            self.response = []
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
                self.response.append(entry)
            self.code = http_codes.HTTP_OK

    def post(self):
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
        if ('hostname' not in self.body or
                'vendor' not in self.body or
                'auth_type' not in self.body or
                'type' not in self.body):
            self.response = {
                "status": "error",
                "error": "Bad parameters"
            }
            self.code = http_codes.HTTP_BADREQUEST

            return

        # Confirm the site exists
        if not self.site_exists(self.site_id):
            self.response = {
                "status": "error",
                "error": "Site ID is incorrect"
            }
            self.code = http_codes.HTTP_BADREQUEST

            return

        # Generate a UUID
        device_id = uuid.uuid4()

        # Build a dictionary of fields
        fields = {
            'id': device_id,
            'name': self.body['hostname'],
            'site': self.site_id,
            'vendor': self.body['vendor'],
            'type': self.body['type'],
            'auth_type': self.body['auth_type'],
        }

        # Handle auth_type
        if self.body['auth_type'] == 'secret':
            fields['secret'] = self.body['secret']
            fields['username'] = self.body['username']
            fields['salt'] = self.body['salt']
        elif self.body['auth_type'] == 'token':
            fields['token'] = self.body['token']
        else:
            self.response = {
                "status": "error",
                "error": "Wrong auth_type"
            }
            self.code = http_codes.HTTP_BADREQUEST
            return

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
            self.response = {
                "status": "error",
                "error": "SQL error"
            }
            self.code = http_codes.HTTP_BADREQUEST

        # Otherwise, return the new device
        else:
            self.response = {
                "device_id": str(device_id),
                "hostname": self.body['hostname'],
                "site": self.site_id,
                "vendor": self.body['vendor'],
                "type": self.body['type'],
                "auth_type": self.body['auth_type'],
                "username": self.body['username'],
                "secret": self.body['secret'],
                "salt": self.body['salt'],
                "token": self.body['token']
            }
            self.code = http_codes.HTTP_CREATED

    def patch(self):
        '''
        Handle a PATCH request to the /sites/:site_id endpoint

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
        if 'device_id' not in self.body:
            self.response = {
                "status": "error",
                "error": "Bad parameters"
            }
            self.code = http_codes.HTTP_BADREQUEST

            return

        # Check if the site exists
        if not self.site_exists(self.site_id):
            self.response = {
                "status": "error",
                "error": "Site ID is incorrect"
            }
            self.code = http_codes.HTTP_BADREQUEST

            return

        # Build a dictionary of fields
        #   Only include fields that are in the body
        fields = {
            'id': self.body['device_id'],
            'site': self.site_id,
        }

        if 'hostname' in self.body:
            fields['name'] = self.body['hostname']

        if 'vendor' in self.body:
            fields['vendor'] = self.body['vendor']

        if 'type' in self.body:
            fields['type'] = self.body['type']

        if 'auth_type' in self.body:
            fields['auth_type'] = self.body['auth_type']

        if 'username' in self.body:
            fields['username'] = self.body['username']

        if 'secret' in self.body:
            fields['secret'] = self.body['secret']

        if 'salt' in self.body:
            fields['salt'] = self.body['salt']

        if 'token' in self.body:
            fields['token'] = self.body['token']

        # Send the fields to the database
        with SqlServer(
            server=config.SQLSERVER,
            db=config.DATABASE,
            table=DEVICE_TABLE
        ) as site_sql:
            output = site_sql.update(
                field='id',
                value=self.body['device_id'],
                body=fields
            )

        # If there was an error, return it
        if not output:
            self.response = {
                "status": "error",
                "error": "SQL error"
            }
            self.code = http_codes.HTTP_BADREQUEST

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
                    value=self.body['device_id']
                )

            self.response = {
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
            self.code = http_codes.HTTP_CREATED

    def delete(self):
        '''
        Handle a DELETE request to the /sites/:site_id endpoint

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
        if 'device_id' not in self.body:
            self.response = {
                "status": "error",
                "error": "Bad parameters"
            }
            self.code = http_codes.HTTP_BADREQUEST

            return

        # Check if the site exists
        if not self.site_exists(self.site_id):
            self.response = {
                "status": "error",
                "error": "Site ID is incorrect"
            }
            self.code = http_codes.HTTP_BADREQUEST

            return

        # Delete the device in the site
        # Send the fields to the database
        with SqlServer(
            server=config.SQLSERVER,
            db=config.DATABASE,
            table=DEVICE_TABLE
        ) as site_sql:
            output = site_sql.delete(
                field='id',
                value=self.body['device_id']
            )

        # If there was an error, return it
        if not output:
            self.response = {
                "status": "error",
                "error": "SQL error"
            }
            self.code = http_codes.HTTP_BADREQUEST

        # Otherwise, return an empty string
        else:
            self.response = ''
            self.code = http_codes.HTTP_NOCONTENT

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
