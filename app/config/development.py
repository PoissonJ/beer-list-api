import datetime
import os


# database connection data
DB_CONNECTION = {
    "MONGODB_DB": "beer-development",
    "MONGODB_USERNAME": "",
    "MONGODB_PASSWORD": "",
    "MONGODB_HOST": os.environ["DB_PORT_27017_TCP_ADDR"],
    "MONGODB_PORT": 27017
}

print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
print os.environ["DB_PORT_27017_TCP_ADDR"]
print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

# database uri
DATABASE_URI = ''

# flask vars
FLASK_VARS = {
    'DEBUG': True,
    'SECRET_KEY': 'aReallySecretKey',
}

# flask-jwt vars
FLASK_JWT_VARS = {
    'JWT_AUTH_URL_RULE': '/api/auth',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1)
}

# another third party libs...
PASSLIB = {
    'HASH_ALGORITHM': 'SHA512',
    'HASH_SALT': 'HiMyNameIsGoku',
}
