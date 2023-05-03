"""
General configuration for the API

Modules:
    None

Classes:

    None

Functions

    None

Exceptions:

    None

Misc Variables:

    SQLSERVER : str
        The SQL server
    DATABASE : str
        The SQL database name

    WEB_PORT : int
        The port to run the API on
    DEBUG : bool
        Whether to run in debug mode
    HOST_IP : str
        The IP to run the API on

    LDAP_SERVER : str
        The LDAP server
    LDAP_PORT : int
        The LDAP port
    LDAP_USER : str
        The LDAP user

    VERSION : str
        The version of the API
    STATUS : str
        The status of the API

Author:
    Luke Robertson - May 2023
"""

# SQL configuration
SQLSERVER = 'servername'
DATABASE = 'database name'

# Flask Configuration
WEB_PORT = 5000
DEBUG = True
HOST_IP = '0.0.0.0'

# LDAP Configuration
LDAP_SERVER = '10.10.10.1'
LDAP_PORT = 389
LDAP_USER = 'username@domain.com'

# API Information
VERSION = 'beta'
STATUS = 'up'
