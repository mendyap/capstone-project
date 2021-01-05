import os
database_path = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_TRACK_MODIFICATIONS=False
DEBUG=True