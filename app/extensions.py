from flask_mongoengine import MongoEngine
db = MongoEngine()


from flask_jwt import JWT
jwt = JWT()

def create_admin(app):
    from flask import redirect, url_for
    import flask_admin as admin
    from flask_admin.contrib.mongoengine import ModelView
    from models import User, Beer, BeerImage

    admin = admin.Admin(app, 'Beer List Api')

    # Customized admin views
    class UserView(ModelView):
        def is_accessible(self):
            return True
        def inaccessible_callback(self, name, **kwargs):
            # redirect to login page if user doesn't have access
            return redirect(url_for('admin'))
        can_create = False
        column_filters = ['username']
        column_exclude_list = ['password',]
        form_excluded_columns = ['password']

        # column_searchable_list = ('username')
    class BeerView(ModelView):
        def is_accessible(self):
            return True
        column_filters = ['name']
        form_ajax_refs = {
            'image': {
                'fields': ['name']
            }
        }

    admin.add_view(UserView(User))
    admin.add_view(BeerView(Beer))
    admin.add_view(ModelView(BeerImage))

    return app
