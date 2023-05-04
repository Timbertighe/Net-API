"""
Template class for handling API requests
Each endpoint has a class that inherits this class, and adds specific methods
These methods correspond to the HTTP methods that the endpoint supports
    (eg. GET, POST, PUT, DELETE)

Modules:
    3rd Party: traceback, flask
    Internal: http_codes, sql, security

Classes:

    ApiCall
        Create an object to represent an API call
        Inherited by endpoint classes to provide common functionality

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - May 2023
"""


from flask import request
import traceback as tb
import endpoints.http_codes as http_codes
import sql.logging as logging
import security.basic_auth as basic_auth


class ApiCall:
    """
    Create an object to represent an API call

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    request : flask.request
        The request object from Flask

    Methods
    -------
    __init__(request)
        Class constructor
    __enter__()
        Called when the 'with' statement is used
    __exit__(exc_type, exc_value, traceback)
        Called when the 'with' statement is finished
    check_auth_header()
        Checks the request for an Authorization header
    check_auth()
        Checks the Authorization header for valid credentials
    log()
        Logs the API call to the SQL Server database
    """

    def __init__(self, request):
        """
        Class constructor

        Gets the request object from Flask and sets the attributes

        Parameters
        ----------
        request : flask.request
            The request object from Flask

        Raises
        ------
        None

        Returns
        -------
        None
        """

        self.headers = request.headers
        self.code = 0
        self.response = None
        self.error = None
        self.src = request.remote_addr
        self.url = request.url
        self.method = request.method
        self.args = request.args

        # Get the request body, if one exists
        if request.headers.get('Content-Length') is not None:
            self.body = request.get_json(force=True)
        else:
            self.body = None

    def __enter__(self):
        """
        Called when the 'with' statement is used

        Calls the 'connect' method to connect to the server

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            The instantiated object
        """

        # Check for an Authorization header
        if self.check_auth_header():
            # Check the Authorization header for valid credentials
            self.check_auth()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when the 'with' statement is finished

        Calls the 'disconnect' method to gracefully close the connection
            to the server

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            None
        """

        # Log the API call
        self.log()

        # handle errors that were raised
        if exc_type:
            print(
                f"Exception of type {exc_type.__name__} occurred: {exc_value}"
            )
            if traceback:
                print("Traceback:")
                print(tb.format_tb(traceback))

        # Return the response and code
        return self.response, self.code

    def check_auth_header(self):
        """
        Checks the request for an Authorization header

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        True : boolean
            If the write was successful
        False : boolean
            If the write failed
        """

        # Check for an Authorization header
        if request.headers.get('Authorization') is None:
            self.error = 'Failed Authentication'
            self.response = {
                "status": "error",
                "error": self.error
            }
            self.code = http_codes.HTTP_UNAUTHORIZED
            return False

        # If the header is present, return True
        else:
            return True

    def check_auth(self):
        """
        Checks the Authorization header for valid credentials

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        True : boolean
            If the write was successful
        False : boolean
            If the write failed
        """

        # Check the Authorization header for valid credentials
        if not basic_auth.api_auth(self.headers.get('authorization')):
            self.error = 'Failed Authentication'
            self.response = {
                "status": "error",
                "error": self.error
            }
            self.code = http_codes.HTTP_UNAUTHORIZED
            return False

        # If the credentials are valid, return True
        else:
            return True

    def log(self):
        """
        Logs the API call to the SQL Server database

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        None
        """

        # Convert the body to a string
        body_string = str(self.body)
        body_string = body_string.replace("\'", "\"")

        # Convert the URL to and API endpoint
        endpoint = self.url.split('/')
        endpoint = endpoint[-1]

        # Log the API call
        with logging.LogEntries() as log:
            log.log_request(
                source=self.src,
                endpoint=f"/{endpoint}",
                headers=self.headers,
                req_body=body_string,
                return_code=self.code,
                error=self.error,
                method=self.method,
            )
