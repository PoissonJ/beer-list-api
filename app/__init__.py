import flask
from flask import render_template, redirect
from . import extensions, config, users, beers, login
from .auth import jwt


def create_app(config_name='default'):
    """Flask app factory

    :config_name: a string object.
    :returns: flask.Flask object

    """

    app = flask.Flask(__name__)

    # set the config vars using the config name and current_app
    config.config[config_name](app)

    register_extensions(app)
    register_blueprints(app)
    jwt.set_jwt_handlers(extensions.jwt)

    return app


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.

    :app: flask.Flask object
    :returns: None

    """

    app = extensions.create_admin(app)
    extensions.db.init_app(app)
    extensions.jwt.init_app(app)


def register_blueprints(app):
    """Register all blueprints.

    :app: flask.Flask object
    :returns: None

    """
    app.register_blueprint(users.blueprint)
    app.register_blueprint(beers.blueprint)
    app.register_blueprint(login.blueprint)

    # Redirect to admin
    @app.route('/')
    def index():
        return redirect('/admin')

    @app.before_first_request
    def create_admin_user():
        if not users.models.User.objects():
            users.controllers.create_or_update_user('admin', 'password', 'admin')
