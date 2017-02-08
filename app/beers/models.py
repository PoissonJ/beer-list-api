from app.extensions import db

class BeerImage(db.Document):
    name = db.StringField(required=True, unique=True)
    image = db.ImageField(thumbnail_size=(100, 100, True))

class Beer(db.Document):

    """Beer model """

    name = db.StringField(required=True, unique=True)
    description = db.StringField()
    abv = db.FloatField()
    floor = db.IntField()
    image = db.ReferenceField(BeerImage)
    active = db.BooleanField(required=True)

    def to_json2(self):
        """Returns a json representantion of the beer.
        :returns: a json object.

        """

        return {
            'id': str(self.id),
            'beer': self.name,
            'description': self.description,
            'abv': self.abv,
            'floor': self.floor,
            'image_name': None if not self.image else self.image.name
        }
