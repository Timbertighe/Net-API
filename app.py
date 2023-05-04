"""
The Web front end of the API system

Modules:
    3rd Party: Flask, json, traceback
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

import endpoints.http_codes as http_codes
import endpoints.sites as sites
import endpoints.devices as devices
import endpoints.hardware as hardware
import endpoints.interfaces as interfaces
import endpoints.lldp as lldp
import endpoints.vlans as vlans
import endpoints.mac as mac
import endpoints.routing as routing
import endpoints.ospf as ospf
import endpoints.api as api

import security.basic_auth as basic_auth

import config


# Initialise the Flask class
app = Flask(__name__)


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
                "version": config.VERSION,
                "status": config.STATUS
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

    # Get parameters from the request
    args = request.args

    # Check for the 'filter' parameter
    filter = False
    if 'filter' in args:
        filter = args.getlist('filter')

    # Handle a GET request
    response = hardware.get_hardware(
        device_id=device_id,
        query=filter
    )

    # Return the response as JSON, as well as the error code
    return response


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

    # Get parameters from the request
    args = request.args
    interface = False
    summary = False

    # Check for the 'interface' parameter
    if 'interface' in args:
        interface = args.getlist('interface')

    # Check for the 'summary' parameter
    if 'interface' in args:
        summary = args.getlist('summary')

    # Handle a GET request
    if request.method == 'GET':
        response = interfaces.get_interfaces(
            device_id=device_id,
            interface=interface,
            summary=summary
        )

    # Handle a PATCH request
    if request.method == 'PATCH':
        if not request.data:
            body = False
        else:
            body = request.json

        response = interfaces.post_interfaces_op(
            device_id=device_id,
            body=body
        )

    # Handle a POST request
    if request.method == 'POST':
        if not request.data:
            body = False
        else:
            body = request.json

        response = interfaces.post_interfaces_op(
            device_id=device_id,
            body=body
        )

    # Return the response as JSON, as well as the error code
    return response


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

    # Get parameters from the request
    args = request.args
    interface = False

    # Check for the 'type' parameter
    if 'interface' in args:
        interface = args.getlist('interface')

    # Handle a GET request
    if request.method == 'GET':
        response = lldp.get_lldp(
            device_id=device_id,
            interface=interface
        )

    # Return the response as JSON, as well as the error code
    return response


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

    # Get parameters from the request
    args = request.args
    vlan = False

    # Check for the 'type' parameter
    if 'vlan' in args:
        vlan = args.getlist('vlan')

    # Handle a GET request
    if request.method == 'GET':
        response = vlans.get_vlans(
            device_id=device_id,
            vlan=vlan
        )

    # Handle a PATCH
    if request.method == 'PATCH':
        response = vlans.patch_vlans(
            device_id=device_id,
            body=request.json
        )

    # Return the response as JSON, as well as the error code
    return response


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

    # Get parameters from the request
    args = request.args
    interface = False
    mac_addr = False

    # Check for the 'interface' parameter
    if 'interface' in args:
        interface = args.getlist('interface')

    # Check for the 'mac' parameter
    if 'mac' in args:
        mac_addr = args.getlist('mac')

    # Handle a GET request
    if request.method == 'GET':
        response = mac.get_mac(
            device_id=device_id,
            interface=interface,
            mac=mac_addr
        )

    # Return the response as JSON, as well as the error code
    return response


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

    # Get parameters from the request
    args = request.args
    route = False

    # Check for the 'interface' parameter
    if 'route' in args:
        route = args.getlist('route')

    # Handle a GET request
    if request.method == 'GET':
        response = routing.get_routes(
            device_id=device_id,
            route=route,
        )

    # Return the response as JSON, as well as the error code
    return response


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
        response = ospf.get_ospf(
            device_id=device_id,
        )

    # Handle a POST request
    if request.method == 'POST':
        if not request.data:
            body = False
        else:
            body = request.json

        response = ospf.post_ospf_op(
            device_id=device_id,
            body=body
        )

    # Return the response as JSON, as well as the error code
    return response


# Start the Flask app
if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        host=config.HOST_IP,
        port=config.WEB_PORT
    )
