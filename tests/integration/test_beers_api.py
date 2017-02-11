import json

import pytest
from bson.objectid import ObjectId

from tests import clear_db
from . import jrequest, get_jwt_auth_header

unauthorized_scenarios = [
    ['POST', '/api/beers', 'Authorization Required', 401],
]


@pytest.mark.parametrize(
    'method, url, error, status_code ', unauthorized_scenarios)
def test_unauthorized_request(method, url, error, status_code, client):

    response = jrequest(method, url, client)

    assert response.status_code == status_code
    assert json.loads(response.data.decode('utf-8'))['error'] == error


def test_get_all_beers(client, mock_beer):
    clear_db()
    beer_1 = mock_beer()
    beer_2 = mock_beer('Rolling Rock')

    response = json.loads(jrequest(
        'GET', '/api/beers', client).data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': [{
            'id': str(beer_1.id),
            'name': beer_1.name,
            'description': beer_1.description,
            'abv': beer_1.abv,
            'floor': beer_1.floor,
            'image_name': beer_1.image,
            'active': beer_1.active
        }, {
            'id': str(beer_2.id),
            'name': beer_2.name,
            'description': beer_2.description,
            'abv': beer_2.abv,
            'floor': beer_2.floor,
            'image_name': beer_2.image,
            'active': beer_2.active
        }],
        'description': 'Successful Operation',
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_get_beer_specifing_beer_name(client, mock_user, mock_beer):
    clear_db()
    beer = mock_beer()

    payload = json.dumps({'name': 'Samule Adams'})
    response = json.loads(jrequest(
        'GET', '/api/beers', client, data=payload).data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': [{
            'id': str(beer.id),
            'name': beer.name,
            'description': beer.description,
            'abv': beer.abv,
            'floor': beer.floor,
            'image_name': beer.image,
            'active': beer.active
        }],
        'description': 'Successful Operation',
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_create_a_beer(client, mock_user, mock_beer):

    clear_db()
    mock_user('auth', 'auth')
    jwt_header = get_jwt_auth_header('auth', 'auth', client)

    payload = json.dumps({
        'name': 'Rolling Rock',
        'description': None,
        'abv': None,
        'floor': None,
        'image': None,
        'active': True,
    })
    response = jrequest('POST', '/api/beers', client, jwt_header, data=payload)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 201,
        'data': "Created the beer 'Rolling Rock'.",
        'description': 'Successfully created'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_update_a_beer_invalid_id(client, mock_user, mock_beer):

    clear_db()
    # user to auth
    mock_user('auth', 'auth')

    beer = mock_beer()

    jwt_header = get_jwt_auth_header('auth', 'auth', client)
    payload = json.dumps({
        'beer_id': str(ObjectId()),  # invalid id
        'name': 'test',
        'description': beer.description,
        'abv': beer.abv,
        'floor': beer.floor,
        'image': beer.image,
        'active': beer.active,
    })

    response = jrequest('PUT', '/api/beer', client, jwt_header, data=payload)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 400,
        'data': "Beer not found",
        'error': 'Bad Request'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_update_a_beer(client, mock_user, mock_beer):

    clear_db()
    # user to auth
    mock_user('auth', 'auth')

    beer = mock_beer()

    jwt_header = get_jwt_auth_header('auth', 'auth', client)
    payload = json.dumps({
        'beer_id': str(beer.id),  # valid id
        'name': beer.name,
        'description': beer.description,
        'abv': beer.abv,
        'floor': beer.floor,
        'image': beer.image,
        'active': beer.active,
    })

    response = jrequest('PUT', '/api/beer', client, jwt_header, data=payload)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': "Updated the beer 'Samuel Adams'.",
        'description': 'Successfully updated'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_delete_a_beer_with_invalid_beer_id(client, mock_user, mock_beer):

    clear_db()

    mock_user('user', 'password')
    mock_beer()
    jwt_header = get_jwt_auth_header('user', 'password', client)

    response = jrequest(
        'DELETE', '/api/beer/{}'.format(ObjectId()), client, jwt_header)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 400,
        'data': 'Invalid beer id.',
        'error': 'Bad Request'
    }

    assert sorted(response.items()) == sorted(expected.items())


def test_delete_a_beer_with_valid_beer_id(client, mock_user, mock_beer):

    clear_db()
    # user_to_auth
    mock_user('user', 'password')
    beer = mock_beer()

    jwt_header = get_jwt_auth_header('user', 'password', client)

    response = jrequest(
        'DELETE', '/api/beer/{}'.format(beer.id), client, jwt_header)
    response = json.loads(response.data.decode('utf-8'))

    expected = {
        'status_code': 200,
        'data': 'Beer deleted',
        'description': 'Successfully deleted'
    }

    assert sorted(response.items()) == sorted(expected.items())
