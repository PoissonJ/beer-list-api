from app import models


def clear_db():
    models.User.objects.all().delete()
    models.Beer.objects.all().delete()
