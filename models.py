import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))

