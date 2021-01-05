from flask import Flask, jsonify
from models import app, db, Customer

@app.route('/<int:id>')
def index(id):

    customer = Customer.query.filter_by(id=id).one_or_none()

    return jsonify({
        'success': True,
        'customer': customer.name
    })

@app.route('/create', methods=['POST'])
def create_customer():
    data = request.get_json()

    customer = Customer(name=data['name'])

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        'success': True,
        'Customer': customer.name
    })



