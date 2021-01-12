from flask import Flask, jsonify, request, abort
from models import setup_db, db, Customer, Item, Orders
from datetime import date
from auth import AuthError, requires_auth
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CUSTOMER ENDPOINTS

    # get list of customers

    @app.route('/customers')
    # add permission decorator
    @requires_auth('get:customers')
    def get_customers():
        # get all customers in database
        customers = Customer.query.all()
        # confirm that there are customers
        if customers is None:
            abort(404)
        # create a list to append customers to
        customer_list = []
        # loop through queried customers and append info to customer_list
        for customer in customers:
            customer_list.append(
                {'id': customer.id, 'name': customer.name,
                 'email': customer.email})

        return jsonify({
            'success': True,
            'status_code': 200,
            'customers': customer_list
        })

    @app.route('/new_customer', methods=['POST'])
    @requires_auth('post:customer')
    def create_customer():
        # parse the JSON data included in request
        data = request.get_json()
        # assign todays date to 'today' variable
        today = date.today()
        # verify that data includes the correct info
        if (data.get('name') is None) or (data.get('email') is None):
            abort(400)
        # create customer object to insert into database
        customer = Customer(name=data['name'],
                            email=data['email'], join_date=today)
        # attempt to insert new customer into database using .insert()<br>
        # defined in customer class model(see models.py)
        try:
            customer.insert()
        # if insert fails rollback data entry
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)

        return jsonify({
            'success': True,
            'status_code': 200,
            'id': customer.id,
            'customer': customer.name
        })

    # include customer to be updated id in http request
    @app.route('/update_customer/<int:id>', methods=['PATCH'])
    @requires_auth('patch:customer')
    # pass id to be updated into function
    def update_customer(id):
        data = request.get_json()
        # query customer from database by 'id'
        customer = Customer.query.filter_by(id=id).one_or_none()
        # verify that customer exists
        if customer is None:
            abort(404)
        # check which field is being updated
        if data.get('name') is None and data.get('email') is None:
            abort(400)

        if data.get('name'):
            customer.name = data['name']

        if data.get('email'):
            customer.email = data['email']
        # attempt to update customer
        try:
            customer.update()
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)
        # query updated customer data to insert into json
        updated_customer = Customer.query.filter_by(id=id).one_or_none()
        if updated_customer is None:
            abort(422)

        return jsonify({
            'success': True,
            'status_code': 200,
            'customer_name': updated_customer.name,
            'customer_email': updated_customer.email
        })

    @app.route('/delete_customer/<int:id>', methods=['DELETE'])
    @requires_auth('delete:customer')
    def delete_customer(id):
        # get customer object pending deletion by 'id'
        customer = Customer.query.filter_by(id=id).one_or_none()
        # verify that customer exists
        if customer is None:
            abort(404)

        # attempt to delete customer with .delete()(see models.py)
        try:
            customer.delete()
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)
        # select remaining customers
        customers = customer.query.all()

        return jsonify({
            'success': True,
            'status_code': 200,
            'deleted_id': customer.id,
            'deleted_customer': customer.name,
            'num_of_remaining_customers': len(customers)
        })

    # ITEM ENDPOINTS

    @app.route('/items')
    @requires_auth('get:items')
    def get_items():
        # select all items
        items = Item.query.all()
        # verify that items exist
        if items is None:
            abort(404)
        # empty list to append items to
        item_list = []
        # loop through selected items and append info to item_list
        for item in items:
            item_list.append({'id': item.id, 'name': item.name,
                              'brand': item.brand, 'price': item.price})

        return jsonify({
            'success': True,
            'status_code': 200,
            'items': item_list
        })

    @app.route('/new_item', methods=['POST'])
    @requires_auth('post:item')
    def create_item():
        # get JSON data
        data = request.get_json()
        # verify that data includes correct fields
        if (data.get('name') is None or data.get('brand') is None
                or data.get('price') is None):
            abort(400)
        # create item to be inserted
        item = Item(name=data['name'],
                    brand=data['brand'], price=data['price'])
        # attempt to insert item
        try:
            item.insert()
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)

        return jsonify({
            'success': True,
            'status_code': 200,
            'id': item.id,
            'item': item.name
        })

    @app.route('/update_item/<int:id>', methods=['PATCH'])
    @requires_auth('patch:item')
    # include item to be updated 'id' in http request and pass into function
    def update_item(id):
        data = request.get_json()
        # assign object to be updated to 'item' variable
        item = Item.query.filter_by(id=id).one_or_none()
        # veify that item exists
        if item is None:
            abort(404)
        # verify that update data includes correct data
        if (data.get('name') is None and data.get('brand') is None
                and data.get('price') is None):
            abort(400)
        # check what fields are to be updated and assign updated fields<br>
        # to item object
        if data.get('name'):
            item.name = data['name']

        if data.get('brand'):
            item.brand = data['brand']

        if data.get('price'):
            item.price = data['price']
        # attempt to update item with .update() (see models.py)
        try:
            item.update()
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)

        return jsonify({
            'success': True,
            'status_code': 200,
            'item_name': item.name,
            'item_brand': item.brand,
            'item_price': item.price
        })

    @app.route('/delete_item/<int:id>', methods=['DELETE'])
    @requires_auth('delete:item')
    def delete_Item(id):
        # retrieve id of item to be deleted and query database for item object
        item = Item.query.filter_by(id=id).one_or_none()
        # verify that item exists
        if item is None:
            abort(404)
        # assign item's name to deleted_name variable
        deleted_name = item.name
        # attempt to delete item with .delete()(see models.py)
        try:
            item.delete()
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)
        # query remaining items
        items = Item.query.all()

        return jsonify({
            'success': True,
            'status_code': 200,
            'deleted_id': id,
            'deleted_item': deleted_name,
            'num_of_remaining_items': len(items)
        })

    # ORDER endpoints

    @app.route('/orders')
    @requires_auth('get:orders')
    def get_orders():
        # select all orders from database
        orders = Orders.query.all()
        # verify that orders exist
        if orders is None:
            abort(404)
        # create empty list to append orders to
        orders_list = []
        '''loop through orders and append them to orders_list (appended
        data includes data from the Customer and Item tables which was made
        possible by declaring a relationship between the Orders and Customer
        and Item tables (see models.py from implementation))'''
        for order in orders:
            orders_list.append({'id': order.id,
                                'order_date': order.order_date,
                                'customer_name': order.customer.name,
                                'item_name': order.item.name,
                                'quantity': order.quantity})

        return jsonify({
            'success': True,
            'status_code': 200,
            'orders_list': orders_list,
            'num_of_orders': len(orders)
        })

    @app.route('/submit_order', methods=['POST'])
    @requires_auth('post:order')
    def submit_order():
        # get request JSON data
        data = request.get_json()
        # verify that data contains the correct info
        if (data.get('customer_id') is None or data.get('item_id') is None
                or data.get('quantity') is None):
            abort(404)
        # select item to be added to order
        item = Item.query.filter_by(id=data['item_id']).one_or_none()
        if item is None:
            abort(404)
        # verify that item is available
        if item.available is False:
            abort(422, 'item not available')
        # get todays date
        today = date.today()
        # calculate total price of order based upon item price<br>
        # and quantity of order
        total_price = item.price * data['quantity']
        # create orders object
        order = Orders(order_date=today, customer_id=data['customer_id'],
                       item_id=data['item_id'], quantity=data['quantity'],
                       amount_due=total_price)
        # attempt to insert order into database with .insert() (see models.py)
        try:
            order.insert()
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)

        return ({
            'success': True,
            'status_code': 200,
            'order_id': order.id
        })

    @app.route('/delete_order/<int:id>', methods=['DELETE'])
    @requires_auth('delete:order')
    def delete_order(id):
        # select rder to be deleted from database
        order = Orders.query.filter_by(id=id).one_or_none()
        # verify that order exists
        if order is None:
            abort(404)
        # get previous number of orders
        previous_num_of_orders = len(Orders.query.all())
        # attempt to delete order with .delete() (see models.py)
        try:
            order.delete()
        except Exception as exc:
            db.session.rollback()
            print('Exception:', exc)
            abort(422)
        # get number of current orders
        current_num_of_orders = len(Orders.query.all())

        # check that order has been deleted before returning
        if (current_num_of_orders) == (previous_num_of_orders - 1):
            return jsonify({
                'success': True,
                'status_code': 200,
                'deleted_order_id': id,
                'message': 'order was deleted',
                'previous_orders': previous_num_of_orders,
                'current_orders': current_num_of_orders
            })

        else:
            abort(500, 'Order was not deleted')

    # ERROR HANDLERS

    # error handler for auth0

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
