import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Customer, Item, Orders

manager_jwt = {
    'Content-Type': 'application/json',
    'Authorization': os.environ['MANAGER_TOKEN']
}

inventory_manager_jwt = {
    'Content-Type': 'application/json',
    'Authorization': os.environ['INVENTORY_MANAGER_TOKEN']
}

salesperson_jwt = {
    'Content-Type': 'application/json',
    'Authorization': os.environ['SALESPERSON_TOKEN']
}


class WarehouseAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'test_capstone_test'
        self.database_path = 'postgres://{}/{}'.format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_customer = {
            'name': 'test_customer_name',
            'email': 'test_email'
        }

        self.new_item = {
            "name": "test item",
            "brand": "test brand",
            "price": 50
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after reach test
        pass

    def test_get_customers(self):
        res = self.client().get('/customers', headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['customers']))

    def test_post_customer(self):
        res = self.client().post('/new_customer', headers=manager_jwt, json=self.new_customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['customer'], self.new_customer['name'])

        customer = Customer.query.filter_by(id=data['id']).one_or_none()
        customer.delete()

    def test_update_customer(self):
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        res = self.client().patch('/update_customer/{}'.format(customer.id),
                                  headers=manager_jwt, json={'name': 'updated name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['customer_name'], 'updated name')

        customer.delete()

    def test_delete_customer(self):
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        num_of_current_customers = len(Customer.query.all())

        res = self.client().delete(
            '/delete_customer/{}'.format(customer.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], customer.id)
        self.assertEqual(data['num_of_remaining_customers'],
                         (num_of_current_customers - 1))

    def test_get_items(self):
        res = self.client().get('/items', headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['items']))

    def test_post_item(self):
        res = self.client().post('/new_item', headers=manager_jwt, json=self.new_item)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['item'], self.new_item['name'])

        item = Item.query.filter_by(id=data['id']).one_or_none()
        item.delete()

    def test_update_item(self):
        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        res = self.client().patch('/update_item/{}'.format(item.id),
                                  headers=manager_jwt, json={'name': 'updated item'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['item_name'], 'updated item')

        item.delete()

    def test_delete_item(self):
        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        num_of_current_items = len(Item.query.all())

        res = self.client().delete('/delete_item/{}'.format(item.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], item.id)
        self.assertEqual(data['num_of_remaining_items'],
                         (num_of_current_items - 1))

    def test_get_orders(self):
        res = self.client().get('/orders', headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['orders_list']))

    def test_submit_order(self):
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        res = self.client().post('/submit_order', headers=manager_jwt,
                                 json={'customer_id': customer.id, 'item_id': item.id, 'quantity': 10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['order_id'])

        order = Orders.query.filter_by(id=data['order_id']).one_or_none()

        order.delete()
        customer.delete()
        item.delete()

    def test_delete_order(self):
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        order = Orders(customer_id=customer.id, item_id=item.id, quantity=10)
        order.insert()

        order_id = order.id

        res = self.client().delete('/delete_order/{}'.format(order.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_order_id'], order_id)
        self.assertEqual(data['current_orders'], (data['previous_orders'] - 1))

        customer.delete()
        item.delete()

    # TEST error handlers

    def test_400_post_customer_without_sufficient_data(self):
        res = self.client().post('/new_customer', headers=manager_jwt,
                                 json={"name": "test_post"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_update_404_non_existent_customer(self):
        mock_customer = Customer(name='test_name', email='test_email')
        mock_customer.insert()
        nonexistent_customer_id = mock_customer.id
        mock_customer.delete()

        res = self.client().patch('/update_customer/{}'.format(nonexistent_customer_id),
                                  headers=manager_jwt, json={'name': 'updated name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_delete_non_existent_customer(self):
        mock_customer = Customer(name='test_name', email='test_email')
        mock_customer.insert()
        nonexistent_customer_id = mock_customer.id
        mock_customer.delete()

        res = self.client().delete(
            '/delete_customer/{}'.format(nonexistent_customer_id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_400_post_item_without_sufficient_data(self):
        res = self.client().post('/new_item', headers=manager_jwt,
                                 json={"name": "test_post"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_404_update_non_existent_item(self):
        mock_item = Item(name='test_name', brand='test_brand', price=10)
        mock_item.insert()
        nonexistent_item_id = mock_item.id
        mock_item.delete()

        res = self.client().patch('/update_item/{}'.format(nonexistent_item_id),
                                  headers=manager_jwt, json={'name': 'updated name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_delete_non_existent_item(self):
        mock_item = Item(name='test_name', brand='test_brand', price=10)
        mock_item.insert()
        nonexistent_item_id = mock_item.id
        mock_item.delete()

        res = self.client().delete(
            '/delete_item/{}'.format(nonexistent_item_id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_submit_order_without_sufficient_data(self):
        res = self.client().post('/submit_order', headers=manager_jwt,
                                 json={"customer_id": "test_customer_id", "item_id": "test_item_id"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_422_submit_order_with_unavailable_item(self):
        customer = Customer(name='test_name', email='test_email')
        unavailable_item = Item(
            name='unavailable item', brand='unavailable brand', price=100, available=False)
        customer.insert()
        unavailable_item.insert()

        res = self.client().post('/submit_order', headers=manager_jwt,
                                 json={"customer_id": customer.id, "item_id": unavailable_item.id, 'quantity': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

        customer.delete()
        unavailable_item.delete()

    def test_404_delete_nonexistent_order(self):
        customer = Customer(name='test_name', email='test_email')
        item = Item(name='test_name', brand='test_brand', price=1)
        customer.insert()
        item.insert()
        mock_order = Orders(customer_id=customer.id,
                            item_id=item.id, quantity=1)
        mock_order.insert()
        nonexistent_order_id = mock_order.id
        mock_order.delete()
        customer.delete()
        item.delete()

        res = self.client().delete(
            '/delete_order/{}'.format(nonexistent_order_id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    #test authentication and authorization(RBAC)

    ''' Warehouse Manager has access to all endpoints. The warehouse manager jwt has been utilized for all tested endpoints up to this point'''

    # test access endpoint without authorization

    def test_401_access_endpoint_without_authentication(self):
        res = self.client().get('/customers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization header missing')


    ## Test inventory manager successfull endpoint access
 
    def test_inventory_manager_get_items(self):
        res = self.client().get('/items', headers=inventory_manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(['success'])
        self.assertTrue(len(data['items']))
    
    ## Test inventory manager fail to access endpoint due to lack of authorization
    def test_401_inventory_manager_accessing_post_customer_endpoint(self):
        res = self.client().post('/new_customer', headers=inventory_manager_jwt, json=self.new_customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'user lacks appropriate permission')

    ## Test salesperson successfull endpoint access
    def test_salesperson_get_customers(self):
        res = self.client().get('/items', headers=salesperson_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(['success'])
        self.assertTrue(len(data['items']))

    ## Test salesperson failure to access endpoint due to lack of authorization
    def test_401_salesperson_accessing_post_item_endpoint(self):
        res = self.client().post('/new_item', headers=salesperson_jwt, json=self.new_item)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'user lacks appropriate permission')    


if __name__ == "__main__":
    unittest.main()
