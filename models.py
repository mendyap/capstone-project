import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)
    orders = db.relationship('Orders', cascade='all, delete', backref='customer')

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Customer {}>'.format(self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    brand = db.Column(db.String(30))
    price = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=True)
    orders = db.relationship('Orders', cascade='all, delete', backref='item')

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Item: {}, Available: {}>'.format(self.name, self.available)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)
    amount_due = db.Column(db.Integer)
    amount_paid = db.Column(db.Integer)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Customer: {}, Item: {}, Quantity: {}>'.format(self.customer.name, self.item.name, self.quantity)