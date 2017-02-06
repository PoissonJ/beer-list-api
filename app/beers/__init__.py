from flask import Blueprint
from app import helpers
from . import resources


blueprint = Blueprint('beers', __name__)
api = helpers.MyApi(blueprint, prefix='/api')

api.add_resource(resources.BeersAPI, '/beers')
api.add_resource(resources.BeerAPI, '/beer', '/beer/<beer_id>')
