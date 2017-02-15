import flask_jwt
from flask import Blueprint, request, render_template, redirect, url_for, current_app, make_response
from app import helpers, users
from wtforms import Form, TextField, PasswordField, validators
from pprint import pprint


blueprint = Blueprint('login', __name__, template_folder='../templates')

class AdminLoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        print 'in post'
        url = request.url_root + 'api/auth'
        payload = {'username': form.username.data, 'password': form.password.data}

        # Check for User
        _jwt = current_app.extensions['jwt']
        user = _jwt.authentication_callback(username=username, password=password)

        # Build JWT token
        if user:

            payload = _jwt.payload_callback(user)
            token = _jwt.encode_callback(payload)

            # Redirect user to admin while setting cookie
            resp = make_response(redirect('/admin'))
            resp.set_cookie('auth', token)
            return resp

        error = 'Invalid username or password'
    return render_template('login.html', form=form, error=error)
