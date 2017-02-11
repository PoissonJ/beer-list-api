from bson.objectid import ObjectId
from app.beers import controllers
from tests import clear_db


def test_beer_exists(app, mock_beer):
    clear_db()
    beer = mock_beer()
    assert controllers.beer_exists(id=beer.id) is True


def test_beer_does_not_exist(app):
    clear_db()

    assert controllers.beer_exists(id=str(ObjectId())) is False


def test_get_beers_no_data(app):
    clear_db()
    assert controllers.get_beers() == {'no-data': ''}


def test_get_beers_with_data(app, mock_beer):
    clear_db()
    beer = mock_beer()
    expected = {
        'success': [{
            'id': str(beer.id),
            'name': beer.name,
            'description': None,
            'abv': None,
            'floor': None,
            'image_name': None,
            'active': beer.active
        }]
    }

    assert controllers.get_beers() == expected


def test_get_beer_with_data_and_specific_name(app, mock_beer):
    clear_db()
    beer = mock_beer()
    expected = {
        'success': [{
            'id': str(beer.id),
            'name': beer.name,
            'description': None,
            'abv': None,
            'floor': None,
            'image_name': None,
            'active': beer.active
        }]
    }

    assert controllers.get_beers(name=beer.name) == expected


def test_create_beer(app):
    clear_db()

    assert 'created' in controllers.create_or_update_beer(
        'Samuel Adams', 'Yummy Beer', 5.0, 4, None, True)


def test_update_beer(app, mock_beer):
    clear_db()
    beer = mock_beer()

    assert 'updated' in controllers.create_or_update_beer(
        'Samuel Adams', 'Yummy Beer', 5.0, 4, None, True, beer.id)


def test_delete_beer_with_invalid_id(app):
    clear_db()
    expected = {'error': 'Invalid beer id.'}

    assert controllers.delete_beer(str(ObjectId())) == expected


def test_delete_beer_with_valid_id(app, mock_beer):
    clear_db()
    beer = mock_beer()

    expected = {'deleted': 'Beer deleted'}

    assert controllers.delete_beer(str(beer.id)) == expected
