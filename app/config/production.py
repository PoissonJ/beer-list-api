import os
import datetime

# database connection data
DB_CONNECTION = {
    "MONGODB_DB": "beer-development",
    "MONGODB_USERNAME": "",
    "MONGODB_PASSWORD": "",
    "MONGODB_HOST": os.environ["DB_PORT_27017_TCP_ADDR"],
    "MONGODB_PORT": 27017
}

# database uri
DATABASE_URI = ''

# flask vars
FLASK_VARS = {
    'DEBUG': False,
    'SECRET_KEY': os.environ['SECRET_KEY'],
}

# flask-jwt vars
FLASK_JWT_VARS = {
    'JWT_AUTH_URL_RULE': '/api/auth',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1)
}

# another third party libs...
PASSLIB = {
    'HASH_ALGORITHM': 'SHA512',
    'HASH_SALT': os.environ['HASH_SALT'],
}
