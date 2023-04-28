"""
A definition of HTTP error codes, to be used by Flask

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

Functions

    None

Exceptions:

    None

Misc Variables:

    HTTP_OK : int
        The '200 - OK' return code
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200
    HTTP_CREATED : int
        The '201 - Created' code
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201
    HTTP_ACCEPTED : int
        The '202 - Accepted' code
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/202
    HTTP_NOCONTENT : int
        The '204 - No content' code
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204
    HTTP_BADREQUEST : int
        The '400 - Bad Request' return code
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
    HTTP_NOTFOUND : int
        The '404 - Not found' code
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
    HTTP_CONFLICT : int
        The '409 - Conflict' code
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409


Author:
    Luke Robertson - April 2023
"""

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_ACCEPTED = 202
HTTP_NOCONTENT = 204
HTTP_BADREQUEST = 400
HTTP_NOTFOUND = 404
HTTP_CONFLICT = 409
