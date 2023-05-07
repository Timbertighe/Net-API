"""
General configuration for the API
Loads configuration from a YAML file into a dictionary

Modules:
    3rd party: yaml, sys
    internal: None

Classes:

    None

Functions

    None

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""

import yaml
import sys


# Open the YAML file, and store in the 'config' variable
with open('config.yaml') as config:
    try:
        config = yaml.load(config, Loader=yaml.FullLoader)
    except yaml.YAMLError as err:
        print('Error parsing config file, exiting')
        print('Check the YAML formatting at \
            https://yaml-online-parser.appspot.com/')
        print(err)
        sys.exit()

# Update our dictionaries with the config
WEB_SERVER = config['web_server']
SQL_SERVER = config['sql_server']
LDAP_SERVER = config['ldap_server']
API = config['api']
