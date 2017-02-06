from app import helpers
from . import models


def is_an_available_beer(name):
    """Verify if a beer is available.

    :username: a string object
    :returns: True or False

    """
    return models.Beer.objects(name=name).first() is None


def get_beers(name=None):
    """Get all beers info.

    :returns: a dict with the operation result

    """

    query = {} if not name else {'name': name}
    beers = models.Beer.objects(**query).all()

    if not beers:
        return {'no-data': ''}

    return {'success': [b.to_json2() for b in beers]}


def create_or_update_beer(name, description, abv,
    floor, image, active, beer_id=None):
    """Creates or updates a beer.

    :name: a string object
    :description: a string object
    :abv: an int object
    :floor: an int object
    :image: a string object. Name of the image file on the server
    :active: a bool object.
    :beer_id: a str object. Indicates an update.

    :returns: a dict with the operation result

    """

    # Need to enforce uniqueness on the name of a beer.
    # Can either do that in another function or here

    # if is_an_available_beer(name) is False:
    #     return {'error': 'The beer {!r} already exists.'.format(username)}

    try:
        query = {'id': beer_id} if beer_id else {'name': name}
        result = models.Beer.objects(**query).update(
            set__name=name,
            set__description=description,
            set__abv=abv,
            set__floor=floor,
            set__image=image,
            set__active=active,
            upsert=True,
            full_result=True
        )
    except Exception as e:
        return {'error': 'Error during the operation: {}'.format(e)}

    if result.get('updatedExisting') is False:
        return {'created': 'Created the beer {!r}.'.format(name)}

    return {'updated': 'Updated the beer {!r}.'.format(name)}


def delete_beer(beer_id):
    """Delete a beer by beer id.

    :beere_id: a str object
    :returns: a dict with the operation result

    """

    beer = models.Beer.objects(id=beer_id).first()

    if not beer:
        return {'error': 'Invalid beer id.'}

    beer.delete()
    return {'deleted': 'Beer deleted'}
