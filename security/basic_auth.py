"""
A module for API basic authentication.
Accounts are retrieved from LDAP.

Modules:
    3rd Party: base64
    Custom: ldap_ad, config

Classes:

    ApiAuth
        Checks API authentication

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - May 2023
"""


import base64

import security.ldap_ad as ldap_ad
import config


def api_auth(authorization):
    """
    Checks API authentication

    Parameters
    ----------
    authorization : str
        The contents of the 'authorization' header

    Raises
    ------
    None

    Returns
    -------
    bool
        Whether the user is authenticated
    """

    # Strip the 'Basic ' from the authorization header
    authorization = authorization.replace('Basic ', '')

    # Decode the authorization header from base64
    #   Use try/except in case the encoding is invalid
    try:
        authorization = base64.b64decode(authorization.encode()).decode()
    except Exception as err:
        print(f"Basic Auth error: Base64 {err}")
        return False

    # Split the authorization header into username and password
    username, password = authorization.split(':')

    # Get LDAP details
    ldap_user, ldap_domain = config.LDAP_USER.split('@')

    # Check that the user is the one specified in the config
    if username != ldap_user:
        return False

    # Authenticate the user against LDAP
    with ldap_ad.LdapUser(
        server=config.LDAP_SERVER,
        port=config.LDAP_PORT,
        domain=ldap_domain
    ) as ldap_account:
        return ldap_account.authenticate(username, password)
