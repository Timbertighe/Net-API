"""
Manage plugins for the Net-API

NOTE: This only returns dummy data at the moment

Modules:
    External: xmlrpc.client, base64
    Internal: sql.sql, config, security.encryption

Classes:

    None

Functions

    TBA

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""

# Imports
import xmlrpc.client
import base64

from sql.sql import SqlServer
from security.encryption import CryptoSecret
import config


class Plugin:
    """
    Create an object to represent plugins

    Attributes
    ----------
    vendor : str
        The vendor of the plugin
    host : str
        The hostname for the RPC connection
    port : int
        The port for the RPC connection
    description : str
        The description of the plugin

    Methods
    -------
    device
        Manage device information, such as hostname, IP address, etc.
    hardware
        Manage hardware information, such as CPU, RAM, etc.
    interfaces
        Manage interface information, such as MAC address, IP address, etc.
    lldp
        Manage lldp information, such as neighbors, etc.
    mac
        Manage MAC table information, such as MAC address, VLAN, etc.
    ospf
        Manage OSPF information, such as neighbors, etc.
    routing
        Manage routing table information, such as routes, etc.
    vlans
        Manage VLAN information, such as VLAN ID, name, etc.
    """

    def __init__(self, vendor, rpc_host, port, description):
        """
        Class constructor

        Parameters
        ----------
        vendor : str
            The vendor of the plugin
        host : str
            The host of the plugin
        port : int
            The port of the plugin
        description : str
            The description of the plugin

        Raises
        ------
        None

        Returns
        -------
        None
        """

        # Set attributes
        self.vendor = vendor
        self.host = rpc_host
        self.port = port
        self.description = description

        # Connection to the RPC server
        self.server = xmlrpc.client.ServerProxy(
            f'http://{self.host}:{self.port}'
        )

    def device(self, device_id):
        """
        Manages device information, such as hostname, IP address, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        device_json : dict
            A dictionary containing device information
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        # Get the device information
        try:
            device_json = self.server.device_info(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                device_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                device_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

            print(f"Problem connecting to the {self.vendor} plugin")
            print(e)

        return device_json

    def hardware(self, device_id):
        """
        Manages hardware information, such as CPU, RAM, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        hardware_json : dict
            A dictionary containing hardware information
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        try:
            hardware_json = self.server.hardware(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                hardware_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                hardware_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

            print(f"Problem connecting to the {self.vendor} plugin")
            print(e)

        return hardware_json

    def interfaces(self, device_id):
        """
        Manages interface information, such as MAC address, IP address, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        interface_json : dict
            A dictionary containing interface information
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        try:
            interface_json = self.server.interfaces(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                interface_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                interface_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

            print(f"Problem connecting to the {self.vendor} plugin")
            print(e)

        return interface_json

    def lldp(self, device_id):
        """
        Manages lldp information, such as neighbors, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        lldp_json : dict
            A dictionary containing lldp information
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        try:
            lldp_json = self.server.lldp(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                lldp_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                lldp_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

        return lldp_json

    def mac(self, device_id):
        """
        Manages MAC table information, such as MAC address, VLAN, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        mac_json : dict
            A dictionary containing MAC table information
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        try:
            mac_json = self.server.mac(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                mac_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                mac_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

        return mac_json

    def ospf(self, device_id):
        """
        Manages OSPF information, such as neighbors, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        ospf_json : dict
            A dictionary containing OSPF information
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        try:
            ospf_json = self.server.ospf(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                ospf_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                ospf_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

        return ospf_json

    def routing(self, device_id):
        """
        Manages routing table information, such as routes, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        routing_json : dict
            A dictionary containing routing table information
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        try:
            routing_json = self.server.routing(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                routing_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                routing_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

        return routing_json

    def vlans(self, device_id):
        """
        Manages VLAN information, such as VLAN ID, name, etc.

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        TBA
        """

        # Get the username and password for the device
        host, username, password = self.authenticate(device_id=device_id)

        try:
            vlan_json = self.server.vlans(
                host,
                username,
                password
            )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                vlan_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                vlan_json = {
                    "status": "error",
                    "error": "Unknown Error"
                }

        return vlan_json

    def authenticate(self, device_id):
        """
        Get the username and password for a device

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        TBA
        """

        # Connect to the database and get a list devices in a site
        with SqlServer(
            server=config.SQL_SERVER['db_server'],
            db=config.SQL_SERVER['db_name'],
            table=config.SQL_SERVER['device_table']
        ) as site_sql:
            output = site_sql.read(
                field='id',
                value=device_id
            )[0]

        host = output[1]
        user = output[6]
        secret = output[7]
        salt = output[8]

        with CryptoSecret() as decryptor:
            # Decrypt the password
            password = decryptor.decrypt(
                secret=secret,
                salt=base64.urlsafe_b64decode(salt.encode())
            )

        return host, user, password
