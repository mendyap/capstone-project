from flask import Flask, jsonify, request
from models import app, db, Customer, Item, Orders
from datetime import date
from auth import AuthError, requires_auth

@app.route('/<int:id>')
def index(id):

    customer = Customer.query.filter_by(id=id).one_or_none()

    return jsonify({
        'success': True,
        'customer': customer.name
    })


@app.route('/customers')
@requires_auth('get:customers')
def get_customers():
    customers = Customer.query.all()

    customer_list = []

    for customer in customers:
        customer_list.append([customer.name, customer.email])

    return jsonify({
        'success': True,
        'customers': customer_list
    })


@app.route('/new_customer', methods=['POST'])
@requires_auth('post:customer')
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
@requires_auth('patch:customer')
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
@requires_auth('delete:customer')
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


# ITEM ENDPOINTS

@app.route('/items')
@requires_auth('get:items')
def get_items():
    items = Item.query.all()

    item_list = []

    for item in items:
        item_list.append([item.name, item.brand, item.price])

    return jsonify({
        'success': True,
        'items': item_list
    })


@app.route('/new_item', methods=['POST'])
@requires_auth('post:item')
def create_item():

    data = request.get_json()

    if not data['name'] or not data['brand'] or not data['price']:
        abort(404)

    item = Item(name=data['name'],
                brand=data['brand'], price=data['price'])

    db.session.add(item)
    db.session.commit()

    new_item = Item.query.filter_by(name=data['name']).one_or_none()

    return jsonify({
        'success': True,
        'Item': new_item.name
    })


@app.route('/update_item/<int:id>', methods=['PATCH'])
@requires_auth('patch:item')
def update_item(id):
    data = request.get_json()

    item = Item.query.filter_by(id=id).one_or_none()

    if not data['name'] and not data['brand'] and not data['price']:
        abort(404)

    if data['name']:
        item.name = data['name']

    if data['brand']:
        item.brand = data['brand']

    if data['brand']:
        item.price = data['price']

        db.session.commit()

        updated_item = Item.query.filter_by(id=id).one_or_none()

    return jsonify({
        'success': True,
        'item_name': updated_item.name,
        'item_brand': updated_item.brand,
        'item_price': updated_item.price
    })


@app.route('/delete_Item/<int:id>', methods=['DELETE'])
@requires_auth('delete:item')
def delete_Item(id):
    item = Item.query.filter_by(id=id).one_or_none()
    deleted_name = Item.name

    db.session.delete(item)
    db.session.commit()

    items = Item.query.all()

    return jsonify({
        'success': True,
        'deleted_item': deleted_name,
        'num_of_remaining_items': len(items)
    })

# ORDER endpoints


@app.route('/orders')
@requires_auth('get:orders')
def get_orders():
    orders = Orders.query.all()

    orders_list = []

    for order in orders:
        orders_list.append([order.id, order.order_date,
                            order.customer.name, order.item.name, order.quantity])

    return jsonify({
        'success': True,
        'orders_list': orders_list,
        'num_of_orders': len(orders)
    })


@app.route('/submit_order', methods=['POST'])
@requires_auth('post:order')
def submit_order():
    data = request.get_json()

    item = Item.query.filter_by(id=data['item_id']).one_or_none()

    if item.available == False:
        abort(422, 'Item not available')

    today = date.today()
    total_price = item.price * data['quantity']
    print('TOTAL:', total_price)

    order = Orders(order_date=today, customer_id=data['customer_id'],
                   item_id=data['item_id'], quantity=data['quantity'], amount_due=total_price)

    db.session.add(order)
    db.session.commit()

    return ({
        'success': True
    })


@app.route('/delete_order/<int:id>', methods=['DELETE'])
@requires_auth('delete:order')
def delete_order(id):
    order = Orders.query.filter_by(id=id).one_or_none()

    orders = Orders.query.all()

    previous_num_of_orders = len(orders)

    db.session.delete(order)
    db.session.commit()

    current_orders = Orders.query.all()

    current_num_of_orders = len(current_orders)

    if (current_num_of_orders) == (previous_num_of_orders - 1):
        return jsonify({
            'success': True,
            'message': 'order was deleted',
            'previous_orders': previous_num_of_orders,
            'current_orders': current_num_of_orders
        })

    else:
        abort(422, 'Order was not deleted')
