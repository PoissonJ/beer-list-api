from flask import request
from utils import logged_in

from flask_mongoengine import MongoEngine
db = MongoEngine()


from flask_jwt import JWT, verify_jwt
jwt = JWT()

def create_admin(app):
    from flask import redirect, url_for
    import flask_admin as admin
    from flask_admin import expose, AdminIndexView
    from flask_admin.contrib.mongoengine import ModelView
    from models import User, Beer, BeerImage

    class MyAdminIndexView(AdminIndexView):

        @expose('/', methods=('GET', 'POST'))
        def index(self):
            if not logged_in():
                return redirect(url_for('login.login'))
            return super(MyAdminIndexView, self).index()


    # Customized admin views
    class UserView(ModelView):
        def is_accessible(self):
            if not logged_in(): return False
            return True
        def inaccessible_callback(self, name, **kwargs):
            # redirect to login page if user doesn't have access
            return redirect(url_for('login.login'))

        can_create = False
        column_filters = ['username']
        column_exclude_list = ['password',]
        form_excluded_columns = ['password']

        # column_searchable_list = ('username')
    class BeerView(ModelView):
        def is_accessible(self):
            return True
        column_filters = ['name']

    admin = admin.Admin(app, 'Beer List Api', index_view=MyAdminIndexView())

    admin.add_view(UserView(User))
    admin.add_view(BeerView(Beer))
    admin.add_view(ModelView(BeerImage))

    return app
