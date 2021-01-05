from flask import Flask, jsonify, request
from models import app, db, Customer
from datetime import date

@app.route('/<int:id>')
def index(id):

    customer = Customer.query.filter_by(id=id).one_or_none()

    return jsonify({
        'success': True,
        'customer': customer.name
    })

@app.route('/customers')
def get_customers():
    customers = Customer.query.all()

    customer_list = []

    for customer in customers:
        customer_list.append(customer.name)

    return jsonify({
        'success': True,
        'customers': customer_list
    })


@app.route('/new_customer', methods=['POST'])
def create_customer():

    data = request.get_json()
    today = date.today()

    if not data['name'] or not data['email']:
        abort(404)

    customer = Customer(name=data['name'],
                        email=data['email'], join_date=today)

    db.session.add(customer)
    db.session.commit()

    new_customer = Customer.query.filter_by(name=data['name']).one_or_none()
    print('Customer:', new_customer)

    return jsonify({
        'success': True,
        'Customer': new_customer.name
    })


@app.route('/update_customer/<int:id>', methods=['PATCH'])
def update_customer(id):
    data = request.get_json()

    customer = Customer.query.filter_by(id=id).one_or_none()

    if not data['name'] and not data['email']:
        abort(404)

    if data['name']:
        customer.name = data['name']

    if data['email']:
        customer.email = data['email']

        db.session.commit()

        updated_customer = Customer.query.filter_by(id=id).one_or_none()

    return jsonify({
        'success': True,
        'customer_name': updated_customer.name,
        'customer_email': updated_customer.email
    })


@app.route('/delete_customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.filter_by(id=id).one_or_none()
    deleted_name = customer.name

    db.session.delete(customer)
    db.session.commit()

    customers = customer.query.all()

    return jsonify({
        'success': True,
        'deleted_customer': deleted_name,
        'num_of_remaining_customers': len(customers)
    })



