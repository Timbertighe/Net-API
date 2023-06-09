"""
Manage plugins for the Net-API

NOTE: This only returns dummy data at the moment

Modules:
    External: xmlrpc.client, base64, json
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
    Luke Robertson - June 2023
"""

if __name__ == '__main__':
    print('This is a library of functions and cannot be executed directly')
    print('Please import this library into another Python script')

else:
    # Imports
    import xmlrpc.client
    import base64
    import json

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                device_json = self.server.device_info(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                device_json = self.server.device_info(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                device_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                device_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }

            print(f"Problem connecting to the {self.vendor} plugin")
            print(e)
            device_json = json.dumps(device_json)

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                hardware_json = self.server.hardware(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                hardware_json = self.server.hardware(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                hardware_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                hardware_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }

            print(f"Problem connecting to the {self.vendor} plugin")
            print(e)
            hardware_json = json.dumps(hardware_json)

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                interface_json = self.server.interfaces(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                interface_json = self.server.interfaces(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                interface_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                interface_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }

            print(f"Problem connecting to the {self.vendor} plugin")
            print(e)
            interface_json = json.dumps(interface_json)

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                lldp_json = self.server.lldp(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                lldp_json = self.server.lldp(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                lldp_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                lldp_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }
            lldp_json = json.dumps(lldp_json)

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                mac_json = self.server.mac(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                mac_json = self.server.mac(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                mac_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                mac_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }
            mac_json = json.dumps(mac_json)

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                ospf_json = self.server.ospf(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                ospf_json = self.server.ospf(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                ospf_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                ospf_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }
            ospf_json = json.dumps(ospf_json)

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                routing_json = self.server.routing(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                routing_json = self.server.routing(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                routing_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                routing_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }
            routing_json = json.dumps(routing_json)

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
        host, auth_type, username, password, token = self.authenticate(
            device_id=device_id
        )

        # Get the device information
        try:
            if auth_type == 'secret':
                vlan_json = self.server.vlans(
                    host,
                    username,
                    password
                )
            elif auth_type == 'token':
                vlan_json = self.server.vlans(
                    host,
                    token
                )

        except Exception as e:
            if 'target machine actively refused it' in str(e):
                vlan_json = {
                    "status": "error",
                    "error": "Connection Refused"
                }

            else:
                vlan_json = {
                    "status": f"{self.vendor} plugin error",
                    "error": str(e)
                }
            vlan_json = json.dumps(vlan_json)

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
        tuple, depending on the authentication type
        host : str
            The IP address or hostname of the device
        auth_type : str
            The type of authentication to use
        user : str
            The username to authenticate with
        password : str
            The password to authenticate with
        token : str
            The token to authenticate with
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

        auth_type = output[5]
        host = output[1]

        # For devices wuth a username and password
        if auth_type == 'secret':
            user = output[6]
            secret = output[7]
            salt = output[8]

            # Decrypt the password
            with CryptoSecret() as decryptor:
                password = decryptor.decrypt(
                    secret=secret,
                    salt=base64.urlsafe_b64decode(salt.encode())
                )

            return host, auth_type, user, password, None

        # For devices with a token
        elif auth_type == 'token':
            token = output[9]

            return host, auth_type, None, None, token
