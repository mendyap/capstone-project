import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# get database path from environment variable
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)
    # orders assists the relationship between orders and table with a<br>
    # backref of 'customer' allowing Orders objects to include data<br>
    # from the 'Item' table. Cascade 'all,delete' enables deletion<br>
    # without violating foreign key constraints
    orders = db.relationship('Orders', cascade='all, delete',
                             backref='customer')

    # insert, update and delete functions for Customer class
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # __repr__ returns customer name
    def __repr__(self):
        return '<Customer {}>'.format(self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    brand = db.Column(db.String(30))
    price = db.Column(db.Integer)
    # product availability has a default of true
    available = db.Column(db.Boolean, default=True)
    # orders assists the relationship between orders and table with a<br>
    # backref of 'item' allowing Orders objects to include data from<br>
    # the 'Item' table. Cascade 'all,delete' enables<br>
    # deletion without violating foreign key constraints
    orders = db.relationship('Orders', cascade='all, delete', backref='item')

    # insert, update and delete functions for Item class
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # __repr__ returns Item name and availability
    def __repr__(self):
        return '<Item: {}, Available: {}>'.format(self.name, self.available)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime)
    # declare customer_id as a foreign key for customer.id
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    # declare item_id as a foreign key for item.id
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)
    amount_due = db.Column(db.Integer)
    amount_paid = db.Column(db.Integer)

    # insert, update and delete functions for Orders class
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    # __repr__ returns order info including customer name,<br>
    # item name, and quantity.

    # (customer and item name are retreived by<br>
    # utilizing the relationship backref)
    def __repr__(self):
        return '<Customer: {}, Item: {}, Quantity: {}>'.format(
            self.customer.name, self.item.name, self.quantity)
