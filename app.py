"""
The Web front end of the API system

Modules:
    3rd Party: Flask, json, traceback, flask_apscheduler, xmlrpc.client
    Internal: endpoints, config, basic_auth, sql

Classes:

    None

Functions

    about_endpoint
        Returns information about the API
    sites_endpoint
        Get a list of sites
        Add a device to a site
    site_devices_endpoint
        Get a list of devices in a site
        Add a device to a site
    dev_list_endpoint
        Collect a list of devices in the environment
    devices_endpoint
        GET information about a device
        PATCH to update a device's configuration
        POST to /op to perform operational tasks
    dev_hardware_endpoint
        Gets hardware information for a device
    interfaces_endpoint
        GET information about interfaces on a device
        POST to /op to perform operational tasks
    lldp_endpoint
        GET information about connected devices (via LLDP)
    vlans_endpoint
        GET information about VLANs on a device
        PATCH to update VLAN configuration
    mac_table_endpoint
        GET information about MAC addresses
    routing_table_endpoint
        GET information about routes
    ospf_endpoint
        GET information about OSPF
        POST to perform OSPF operations

Exceptions:

    None

Misc Variables:

    WEB_PORT : int
        The port the web server runs on
    DEBUG : bool
        Whether to enable debug mode
    HOST_IP : str
        The IP to bind the webserver to
    VERSION : str
        The API's version number
    STATUS : str
        The status of the API; Set to 'up' for now

Author:
    Luke Robertson - May 2023
"""

from flask import Flask, request
import json
from flask_apscheduler import APScheduler
import endpoints.http_codes as http_codes
import endpoints.sites as sites
import endpoints.devices as devices
import endpoints.interfaces as interfaces
import endpoints.switching as switching
import endpoints.routing as routing
import endpoints.api as api

import security.basic_auth as basic_auth

import plugins.plugin as plugin

import config


def load_plugins():
    """
    Load plugins from the config file
    Add them to the config.PLUGINS['loaded'] list

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

    loaded = []
    for entry in config.PLUGINS:
        new_plugin = plugin.Plugin(
            vendor=config.PLUGINS[entry]['vendor'],
            rpc_host=config.PLUGINS[entry]['host'],
            port=config.PLUGINS[entry]['port'],
            description=config.PLUGINS[entry]['description']
        )
        loaded.append(new_plugin)
    config.PLUGINS['loaded'] = loaded


# The Flask class is used to create the web server
# The APScheduler class is used to schedule tasks
# The scheduler object is stored in config, for access later
app = Flask(__name__)
sched_obj = APScheduler()
sched_obj.init_app(app)
config.API['scheduler'] = sched_obj

# Load plugins
load_plugins()


# /about
@app.route('/about', methods=['GET'])
def about_endpoint():
    '''
    Returns information about the API

    Parameters:
        methods : list
            A list of methods this route will accept

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
        code : int
            The HTTP response code
    '''

    with api.ApiCall(request) as about:
        if about.code == 0:
            about.response = {
                "version": config.API['version'],
                "status": config.API['status']
            }
            about.code = http_codes.HTTP_OK
        code = about.code
        response = about.response

    # Return the response as JSON, as well as the error code
    return json.dumps(response), code


# /sites
@app.route('/sites', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def sites_endpoint():
    '''
    Site management

    GET information about sites
    POST information to add sites

    Parameters:
        methods : list
            A list of methods this route will accept

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with sites.Sites(request) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()
            elif request.method == 'POST':
                endpoint.post()
            elif request.method == 'PATCH':
                endpoint.patch()
            elif request.method == 'DELETE':
                endpoint.delete()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code

    # Check if the Authorization header is present
    if request.headers.get('Authorization') is None:
        # If not, return a 401
        code = http_codes.HTTP_UNAUTHORIZED
        response = {
            "status": "error",
            "error": "Failed Authentication"
        }
        return json.dumps(response), code

    # Check if this request is authenticated
    if not basic_auth.api_auth(request.headers.get('authorization')):
        # If not, return a 401
        code = http_codes.HTTP_UNAUTHORIZED
        response = {
            "status": "error",
            "error": "Failed Authentication"
        }
        return json.dumps(response), code

    # Handle a GET request
    if request.method == 'GET':
        response = endpoint.get_sites()

    # Handle a POST (create a new site)
    if request.method == 'POST':
        response = endpoint.post_sites(
            body=request.json
        )

    # Handle a PATCH (update a site)
    if request.method == 'PATCH':
        response = endpoint.patch_sites(
            body=request.json
        )

    # Handle a DELETE (remove a site)
    if request.method == 'DELETE':
        response = endpoint.delete_sites(
            body=request.json
        )

    # Return the response as JSON, as well as the error code
    return response


# /sites/:site_id
@app.route(
    '/sites/<string:site_id>',
    methods=['GET', 'POST', 'PATCH', 'DELETE']
)
def site_devices_endpoint(site_id):
    '''
    Manage devices within a site

    GET information about devices within a site
    POST information to add devices to a site

    Parameters:
        methods : list
            A list of methods this route will accept
        site_id : str
            The ID of a site

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with sites.SiteDevices(request, site_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()
            elif request.method == 'POST':
                endpoint.post()
            elif request.method == 'PATCH':
                endpoint.patch()
            elif request.method == 'DELETE':
                endpoint.delete()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# /devices/:device_id
# /devices/:device_id/op
@app.route(
    '/devices/<string:device_id>',
    methods=['GET', 'PATCH']
)
@app.route(
    '/devices/<string:device_id>/op',
    methods=['POST']
)
def devices_endpoint(device_id, **kwargs):
    '''
    Access devices

    GET information about a device
    PATCH to update a device's configuration
    POST to /op to perform operational tasks

    Parameters:
        methods : list
            A list of methods this route will accept
        device_id : string
            The ID of a device

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with devices.Devices(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()
            elif request.method == 'POST':
                endpoint.post()
            elif request.method == 'PATCH':
                endpoint.patch()

        code = endpoint.code
        response = endpoint.response

    # Return the response (already JSON), as well as the status code
    return response, code
    return json.dumps(response), code


# /devices/:device_id/hardware
@app.route('/devices/<string:device_id>/hardware', methods=['GET'])
def dev_hardware_endpoint(device_id):
    '''
    Gets hardware information for a device

    Parameters:
        methods : list
            A list of methods this route will accept

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with devices.Hardware(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# /devices/:device_id/interfaces
# /devices/:device_id/interfaces/op
@app.route(
    '/devices/<string:device_id>/interfaces',
    methods=['GET', 'PATCH']
)
@app.route(
    '/devices/<string:device_id>/interfaces/op',
    methods=['POST']
)
def interfaces_endpoint(device_id):
    '''
    Device interfaces

    GET information about interfaces on a device
    POST to /op to perform operational tasks

    Parameters:
        methods : list
            A list of methods this route will accept
        device_id : string
            The ID of a device

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with interfaces.Interfaces(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()
            if request.method == 'PATCH':
                endpoint.patch()
            if request.method == 'POST':
                endpoint.post()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# /devices/:device_id/lldp
@app.route('/devices/<string:device_id>/lldp', methods=['GET'])
def lldp_endpoint(device_id):
    '''
    Manage LLDP

    GET information about connected devices

    Parameters:
        methods : list
            A list of methods this route will accept
        site_id : str
            The ID of a site

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with switching.Lldp(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# /devices/:device_id/vlans
@app.route('/devices/<string:device_id>/vlans', methods=['GET', 'PATCH'])
def vlans_endpoint(device_id):
    '''
    Manage VLANs on a device

    GET information about VLANs on a device
    PATCH to update VLAN configuration

    Parameters:
        methods : list
            A list of methods this route will accept
        site_id : str
            The ID of a site

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with switching.Vlans(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()
            if request.method == 'PATCH':
                endpoint.patch()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# /devices/:device_id/mac_table
@app.route('/devices/<string:device_id>/mac_table', methods=['GET'])
def mac_table_endpoint(device_id):
    '''
    Collect MAC table information

    GET information about MAC addresses

    Parameters:
        methods : list
            A list of methods this route will accept
        device_id : str
            The ID of a device

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with switching.Mac(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# /devices/:device_id/routing_table
@app.route('/devices/<string:device_id>/routing_table', methods=['GET'])
def routing_table_endpoint(device_id):
    '''
    Collect routing table information

    GET information about routes

    Parameters:
        methods : list
            A list of methods this route will accept
        device_id : str
            The ID of a device

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with routing.Routing_Table(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# /devices/:device_id/routing_table
@app.route('/devices/<string:device_id>/ospf', methods=['GET'])
@app.route('/devices/<string:device_id>/ospf/op', methods=['POST'])
def ospf_endpoint(device_id):
    '''
    Manage OSPF

    GET information about OSPF
    POST to send operational commands

    Parameters:
        methods : list
            A list of methods this route will accept
        device_id : str
            The ID of a device

    Raises:
        None

    Returns:
        response : JSON
            The JSON response with the requested information or error
            For a POST, this echoes back the request body
        code : int
            The HTTP response code
    '''

    with routing.Ospf(request, device_id) as endpoint:
        if endpoint.code == 0:
            if request.method == 'GET':
                endpoint.get()
            if request.method == 'POST':
                endpoint.post()

        code = endpoint.code
        response = endpoint.response

    return json.dumps(response), code


# Start the Flask app
if __name__ == '__main__':
    app.run(
        debug=config.WEB_SERVER['flask_debug'],
        host=config.WEB_SERVER['host_ip'],
        port=config.WEB_SERVER['web_port']
    )
