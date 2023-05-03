"""
An LDAP module for the security package.
Connects to Active Directory and checks authentication.

Modules:
    3rd Party: ldap3, traceback
    Custom: None

Classes:

    LdapUser
        Tests authentication against Active Directory

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - May 2023
"""


import ldap3
import traceback as tb


class LdapUser:
    """
    Provides LDAP authentication for users

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    TBA

    Methods
    -------
    authenticate(username, password)
        Authenticate a user against Active Directory
    """

    def __init__(self, server, port, domain):
        """
        Class constructor

        Gets the master password from an environment variable

        Parameters
        ----------
        server : str
            The server to connect to
        port : int
            The port to connect to
        domain : str
            The domain to connect to

        Raises
        ------
        None

        Returns
        -------
        None
        """

        self.server = server
        self.port = port
        self.domain = domain

    def __enter__(self):
        """
        Called when the 'with' statement is used

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

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Called when the 'with' statement is finished
        Ignore invalidCredentials errors

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

        # Handle errors that were raised
        #   NOTE: invalidCredentials is raised when authentication fails
        if exc_type and 'invalidCredentials' not in str(exc_value):
            print(
                f"Exception of type {exc_type.__name__} occurred: {exc_value}"
            )
            if exc_traceback:
                print("Traceback:")
                print(tb.format_tb(exc_traceback))

    def authenticate(self, username, password):
        """
        Authenticate a user against Active Directory

        Parameters
        ----------
        username : str
            The username to authenticate
        password : str
            The password to authenticate

        Raises
        ------
        None

        Returns
        -------
        bool
            True if the user is authenticated, False otherwise
        """

        # Create a connection to Active Directory
        try:
            with ldap3.Connection(
                server=f'ldap://{self.server}:{self.port}',
                user=f'{username}@{self.domain}',
                password=password,
                auto_bind=True
            ) as conn:

                # Check if the user is authenticated
                if conn.bind():
                    return True
                else:
                    return False

        except Exception as e:
            if 'invalidCredentials' in str(e):
                return False
            else:
                print(e)
                return False
