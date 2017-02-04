from app.extensions import db


class Beer(db.Document):

    """Beer model """

    name = db.StringField(required=true, unique=true)
    description = db.StringField()
    abv = db.IntField()
    floor = db.IntField()
    image = db.StringField()
    active = db.BooleanField(required=true)

    def to_json2(self):
        """Returns a json representantion of the beer.
        :returns: a json object.

        """

        return {
            'id': str(self.id),
            'beer': self.name,
            'abv': self.abv,
            'floor': self.floor,
            'image': self.floor
        }
