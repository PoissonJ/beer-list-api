import bson
from werkzeug.local import LocalProxy
from flask import current_app, _request_ctx_stack, request
from itsdangerous import (
    SignatureExpired,
    BadSignature
)


def is_a_valid_object_id(object_id):
    """Verify if the value is valid as an object id.
    :object_id: a string object
    :returns: True or False

    """
    return bson.objectid.ObjectId.is_valid(object_id)

def manual_verify_jwt(auth):
    """Does the actual work of verifying the JWT data in the current request.
    This is done automatically for you by `jwt_required()` but you could call it manually.
    Doing so would be useful in the context of optional JWT access in your APIs.

    :param realm: an optional realm
    """
    _jwt = LocalProxy(lambda: current_app.extensions['jwt'])
    if auth is None:
        return False

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        return False
    elif len(parts) == 1:
        return False
    elif len(parts) > 2:
        return False



    try:
        handler = _jwt.decode_callback
        payload = handler(parts[1])
    except SignatureExpired:
        return False
    except BadSignature:
        return False

    _request_ctx_stack.top.current_user = user = _jwt.user_callback(payload)

    if user is None:
        return False

    return True

def logged_in():
    auth_cookie = None
    if request.cookies.get('auth'):
        auth_cookie = 'bearer ' + request.cookies.get('auth')
        if manual_verify_jwt(auth_cookie):
            return True
        return False
