from flask import Flask, jsonify
from models import app, db, Customer

@app.route('/<int:id>')
def index(id):

    customer = Customer.query.filter_by(id=id).one_or_none()

    return jsonify({
        'success': True,
        'customer': customer.name
    })



