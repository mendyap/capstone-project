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

class WarehouseAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'test_capstone_test'
        self.database_path = 'postgres://{}/{}'.format('localhost:5432', self.database_name)
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
        #Executed after reach test
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
        customer = Customer(name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        res = self.client().patch('/update_customer/{}'.format(customer.id), headers=manager_jwt, json={'name': 'updated name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['customer_name'], 'updated name')

        customer.delete()

    def test_delete_customer(self):
        customer = Customer(name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        num_of_current_customers = len(Customer.query.all())

        res = self.client().delete('/delete_customer/{}'.format(customer.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], customer.id)
        self.assertEqual(data['num_of_remaining_customers'], (num_of_current_customers -1))

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
        item = Item(name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        res = self.client().patch('/update_item/{}'.format(item.id), headers=manager_jwt, json={'name': 'updated item'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['item_name'], 'updated item')

        item.delete()

    def test_delete_item(self):
        item = Item(name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        num_of_current_items = len(Item.query.all())

        res = self.client().delete('/delete_item/{}'.format(item.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], item.id)
        self.assertEqual(data['num_of_remaining_items'], (num_of_current_items -1))

    def test_get_orders(self):
        res = self.client().get('/orders', headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['orders_list']))

    def test_submit_order(self):
        customer = Customer(name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        item = Item(name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        res = self.client().post('/submit_order', headers=manager_jwt, json={'customer_id': customer.id, 'item_id': item.id, 'quantity': 10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['order_id'])

        order = Orders.query.filter_by(id=data['order_id']).one_or_none()

        order.delete()
        customer.delete()
        item.delete()
    
    def test_delete_order(self):
        customer = Customer(name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        item = Item(name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        order = Orders(customer_id=customer.id, item_id=item.id, quantity=10)
        order.insert()
        
        order_id=order.id

        res = self.client().delete('/delete_order/{}'.format(order.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_order_id'], order_id)
        self.assertEqual(data['current_orders'], (data['previous_orders'] -1))

        customer.delete()
        item.delete()


if __name__ == "__main__":
    unittest.main()