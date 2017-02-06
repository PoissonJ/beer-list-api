from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app import helpers, utils
from . import controllers


def post_put_parser():
    """Request parser for HTTP POST or PUT.
    :returns: flask_restful.reqparse.RequestParser object

    """
    parse = reqparse.RequestParser()
    parse.add_argument(
        'name', type=str, location='json', required=True)
    parse.add_argument(
        'description', type=str, location='json', required=True)
    parse.add_argument(
        'abv', type=float, location='json', required=True)
    parse.add_argument(
        'floor', type=int, location='json', required=True)
    parse.add_argument(
        'image', type=str, location='json', required=True)
    parse.add_argument(
        'active', type=bool, location='json', required=True)

    return parse


class BeersAPI(Resource):

    """An API to get or create Beers."""

    @jwt_required()
    @helpers.standardize_api_response
    def get(self, name=None):
        """HTTP GET. Get one or all beers.

        :name: a string valid as object id.
        :returns: One or all available users.

        """

        return controllers.get_beers(name)

    # @jwt_required()
    @helpers.standardize_api_response
    def post(self):
        """HTTP POST. Create a beer.

        :name: The beer name
        :description: The beer description
        :abv: The beer abv percent
        :floor: The beer floor number
        :image: The beer image name on the server
        :active: Boolean whethe the beer is being used currently
        :returns: The user id

        """

        parse = post_put_parser()
        args = parse.parse_args()

        name, description = args['name'], args['description']
        abv, floor = args['abv'], args['floor']
        image, active = args['image'], args['active']

        print image

        return controllers.create_or_update_beer(
            name, description, abv, floor, image, active)


class BeerAPI(Resource):

    """An API to update or delete a beer. """

    # @jwt_required()
    @helpers.standardize_api_response
    def put(self):
        """HTTP PUT. Update a beer.
        :returns:

        """

        parse = post_put_parser()
        parse.add_argument('beer_id', type=str, location='json', required=True)
        args = parse.parse_args()

        name, description = args['name'], args['description']
        abv, floor = args['abv'], args['floor']
        image, active = args['image'], args['active']
        beer_id = args['beer_id']
        print abv
        print args['abv']

        return controllers.create_or_update_beer(
            name, description, abv, floor, image, active, beer_id)

    # @jwt_required()
    @helpers.standardize_api_response
    def delete(self, beer_id):
        """HTTP DELETE. Delete a beer.
        :returns:

        """

        if not utils.is_a_valid_object_id(beer_id):
            return {'error': 'Invalid beer id.'}
        return controllers.delete_beer(beer_id)
