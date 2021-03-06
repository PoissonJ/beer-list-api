import json

import pytest
from bson.objectid import ObjectId

from tests import clear_db
from . import jrequest, get_jwt_auth_header

unauthorized_scenarios = [
    ['GET', '/api/users', 'Authorization Required', 401],
]


@pytest.mark.parametrize(
    'method, url, error, status_code ', unauthorized_scenarios)
def test_unauthorized_request(method, url, error, status_code, client):

    response = jrequest(method, url, client)

    assert response.status_code == status_code
    assert json.loads(response.data.decode('utf-8'))['error'] == error


def test_get_users_without_username(client, mock_user):
    clear_db()
    user = mock_user('user', 'password')
    jwt_header = get_jwt_auth_header('user', 'password', client)

    response = json.loads(jrequest(
        'GET', '/api/users', client, jwt_header).data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': [{
            'id': str(user.id),
            'username': user.username,
            'role': user.role
        }],
        'description': 'Successful Operation',
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_get_users_specifing_username(client, mock_user):
    clear_db()
    user = mock_user('user', 'password')
    jwt_header = get_jwt_auth_header('user', 'password', client)

    response = json.loads(jrequest(
        'GET', '/api/users', client, jwt_header).data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': [{
            'id': str(user.id),
            'username': user.username,
            'role': user.role
        }],
        'description': 'Successful Operation',
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_create_a_user_invalid_username(client, mock_user):

    clear_db()
    user = mock_user('user', 'password')
    jwt_header = get_jwt_auth_header('user', 'password', client)

    payload = json.dumps({'username': user.username, 'password': 'foo'})
    response = jrequest('POST', '/api/users', client, jwt_header, data=payload)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        u'status_code': 400,
        u'data': u"The user 'user' already exists.",
        u'error': u'Bad Request'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_create_a_user_with_valid_username(client, mock_user):

    clear_db()
    mock_user('auth', 'auth')
    jwt_header = get_jwt_auth_header('auth', 'auth', client)

    payload = json.dumps({'username': 'valid', 'password': 'valid'})
    response = jrequest('POST', '/api/users', client, jwt_header, data=payload)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 201,
        'data': "Created the user 'valid'.",
        'description': 'Successfully created'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_update_a_user_invalid_username(client, mock_user):

    clear_db()
    # user to auth
    user_to_auth = mock_user('auth', 'auth')

    # to test if an username is really unique
    user_to_test = mock_user('user', 'password')

    jwt_header = get_jwt_auth_header('auth', 'auth', client)
    payload = json.dumps({
        'user_id': str(user_to_auth.id),
        'username': user_to_test.username,
        'password': 'password'
    })

    response = jrequest('PUT', '/api/user', client, jwt_header, data=payload)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 400,
        'data': "The user 'user' already exists.",
        'error': 'Bad Request'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_update_a_user_with_valid_username(client, mock_user):

    clear_db()

    user = mock_user('user', 'password')
    jwt_header = get_jwt_auth_header('user', 'password', client)
    response = json.loads(jrequest(
        'GET', '/api/users', client, jwt_header).data.decode('utf-8'))
    print 'response'
    print response
    payload = json.dumps({
        'user_id': str(user.id),
        'username': 'it works',
        'password': 'password'
    })

    response = jrequest('PUT', '/api/user', client, jwt_header, data=payload)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': "Updated the user 'it works'.",
        'description': 'Successfully updated'
    }
    response2 = json.loads(jrequest(
        'GET', '/api/users', client, jwt_header).data.decode('utf-8'))
    print 'response2'
    print response2

    assert sorted(response.items()) == sorted(expected.items())


def test_delete_a_user_with_invalid_user_id(client, mock_user):

    clear_db()

    mock_user('user', 'password')
    jwt_header = get_jwt_auth_header('user', 'password', client)

    response = jrequest(
        'DELETE', '/api/user/{}'.format(ObjectId()), client, jwt_header)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 400,
        'data': 'Invalid user id.',
        'error': 'Bad Request'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_delete_a_user_with_valid_user_id(client, mock_user):

    clear_db()
    user_to_delete = mock_user('delete', 'delete')
    # user_to_auth
    mock_user('user', 'password')

    jwt_header = get_jwt_auth_header('user', 'password', client)

    response = jrequest(
        'DELETE', '/api/user/{}'.format(user_to_delete.id), client, jwt_header)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': 'User deleted',
        'description': 'Successfully deleted'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_non_admin_user_cannot_access_admin_routes(client, mock_user):

    clear_db()
    # user_to_auth
    mock_user('user', 'password', 'non_admin')

    jwt_header = get_jwt_auth_header('user', 'password', client)

    response = json.loads(jrequest(
        'GET', '/api/users', client, jwt_header).data.decode('utf-8'))

    expected = {
        u'status_code': 401,
        u'error': u'Authorization Required',
        u'description': u'User does not have sufficent rights'
    }

    assert sorted(response.items()) == sorted(expected.items())
