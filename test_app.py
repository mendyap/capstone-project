import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Customer, Item, Orders

## User JWT's. See README for each users permissions


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

        # sample customer for testing purposes

        self.new_customer = {
            'name': 'test_customer_name',
            'email': 'test_email'
        }

        # sample item for testing purposes

        self.new_item = {
            "name": "test item",
            "brand": "test brand",
            "price": 50
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass
    
    ''' NOTE: All data that is added to the database during testing is deleted by the end of each test unit in order to not interfere with future tests'''
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

        # select new customer from database
        customer = Customer.query.filter_by(id=data['id']).one_or_none()
        # delete new customer
        customer.delete()

    def test_update_customer(self):
        # create customer to updated
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        # insert customer to database
        customer.insert()
        # send request to update customer that has been just entered into database
        res = self.client().patch('/update_customer/{}'.format(customer.id),
                                  headers=manager_jwt, json={'name': 'updated name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['customer_name'], 'updated name')
        # delete customer after test
        customer.delete()

    def test_delete_customer(self):
        # create and enter into database customer to be deleted
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        # get number of customers prior to deletion
        num_of_current_customers = len(Customer.query.all())

        res = self.client().delete(
            '/delete_customer/{}'.format(customer.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], customer.id)
        # verify that number of customer is one customer less than what it was prior to deletion
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
        # verify that new item matches the name that was entered
        self.assertEqual(data['item'], self.new_item['name'])
        # assign new item to item variable
        item = Item.query.filter_by(id=data['id']).one_or_none()
        # delete new item once test has completed
        item.delete()

    def test_update_item(self):
        # create and insert item to be updated
        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()
        # send request to update item
        res = self.client().patch('/update_item/{}'.format(item.id),
                                  headers=manager_jwt, json={'name': 'updated item'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # verify that item_name matched updated name entered
        self.assertEqual(data['item_name'], 'updated item')
        # delete item once tests have been passed
        item.delete()

    def test_delete_item(self):
        # create and enter item to be deleted
        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()
        # get total of items prior to deletion
        num_of_current_items = len(Item.query.all())
        # send request to delete item
        res = self.client().delete('/delete_item/{}'.format(item.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        # verify that deleted id matches id in request
        self.assertEqual(data['deleted_id'], item.id)
        # verify that 1 item has been deleted from that database
        self.assertEqual(data['num_of_remaining_items'],
                         (num_of_current_items - 1))

    def test_get_orders(self):
        res = self.client().get('/orders', headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['orders_list']))

    def test_submit_order(self):
        # create a customer to be inserted into database
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()
        # create an item to be inserted into database
        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()
        '''
        assign the created customer and item id's to the created order. The created customer and order were implemented to esure that the tests are self sufficient in order to provide a predictable outcome and confirm that the units being tested do exist.
        '''
        res = self.client().post('/submit_order', headers=manager_jwt,
                                 json={'customer_id': customer.id, 'item_id': item.id, 'quantity': 10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['order_id'])
    
        order = Orders.query.filter_by(id=data['order_id']).one_or_none()
        # after tests are passed delete all mock data(order, customer, item)
        order.delete()
        customer.delete()
        item.delete()

    def test_delete_order(self):
        # create customer, item and order and insert into database pending deletion request
        customer = Customer(
            name=self.new_customer['name'], email=self.new_customer['email'])
        customer.insert()

        item = Item(
            name=self.new_item['name'], brand=self.new_item['brand'], price=self.new_item['price'])
        item.insert()

        order = Orders(customer_id=customer.id, item_id=item.id, quantity=10)
        order.insert()
        # assign order id to variable prior to deletion for testing purposes
        order_id = order.id
        # delete order that was currently created
        res = self.client().delete('/delete_order/{}'.format(order.id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        # verify that deleted order id matched id included in request
        self.assertEqual(data['deleted_order_id'], order_id)
        self.assertEqual(data['current_orders'], (data['previous_orders'] - 1))

        # delete customer and item
        customer.delete()
        item.delete()

    # TEST error handlers

    # test failure of post('/new_customer') endpoint if sufficient data is not provided
    def test_400_post_customer_without_sufficient_data(self):
        res = self.client().post('/new_customer', headers=manager_jwt,
                                 json={"name": "test_post"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


    def test_404_update_non_existent_customer(self):
        '''
        insert mock customer, assign mock customer's id to variable and then delete mock customer prior to the test to ensure that customer pending update does not exist
        '''
        mock_customer = Customer(name='test_name', email='test_email')
        mock_customer.insert()
        nonexistent_customer_id = mock_customer.id
        mock_customer.delete()
        # send request to update nonexistent customer
        res = self.client().patch('/update_customer/{}'.format(nonexistent_customer_id),
                                  headers=manager_jwt, json={'name': 'updated name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_delete_non_existent_customer(self):
        '''
        insert mock customer, assign mock customer's id to variable and then delete mock customer prior to the test to ensure that customer pending delete does not exist
        '''
        mock_customer = Customer(name='test_name', email='test_email')
        mock_customer.insert()
        nonexistent_customer_id = mock_customer.id
        mock_customer.delete()
        # send request to delete nonexistent customer
        res = self.client().delete(
            '/delete_customer/{}'.format(nonexistent_customer_id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # test failure of post('/new_item') endpoint if sufficient data is not provided
    def test_400_post_item_without_sufficient_data(self):
        res = self.client().post('/new_item', headers=manager_jwt,
                                 json={"name": "test_post"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_404_update_non_existent_item(self):
        '''
        insert mock item, assign mock item's id to variable and then delete mock item prior to the test to ensure that item pending update does not exist
        '''
        mock_item = Item(name='test_name', brand='test_brand', price=10)
        mock_item.insert()
        nonexistent_item_id = mock_item.id
        mock_item.delete()
        # send request to update non existent item
        res = self.client().patch('/update_item/{}'.format(nonexistent_item_id),
                                  headers=manager_jwt, json={'name': 'updated name'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_404_delete_non_existent_item(self):
        '''
        insert mock item, assign mock item's id to variable and then delete mock item prior to the test to ensure that item pending delete does not exist
        '''
        mock_item = Item(name='test_name', brand='test_brand', price=10)
        mock_item.insert()
        nonexistent_item_id = mock_item.id
        mock_item.delete()
        # send delete request for nonexistent item
        res = self.client().delete(
            '/delete_item/{}'.format(nonexistent_item_id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # test failure of post('/submit_order') endpoint if sufficient data is not provided
    def test_404_submit_order_without_sufficient_data(self):
        res = self.client().post('/submit_order', headers=manager_jwt,
                                 json={"customer_id": "test_customer_id", "item_id": "test_item_id"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_422_submit_order_with_unavailable_item(self):
        # create and insert customer to be included in order
        customer = Customer(name='test_name', email='test_email')
        # create and insert item that is unavailable to be included in order
        unavailable_item = Item(
            name='unavailable item', brand='unavailable brand', price=100, available=False)
        customer.insert()
        unavailable_item.insert()
        # attempt to submit order with unavailable item
        res = self.client().post('/submit_order', headers=manager_jwt,
                                 json={"customer_id": customer.id, "item_id": unavailable_item.id, 'quantity': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

        # delete customer and item after test is completed
        customer.delete()
        unavailable_item.delete()

    def test_404_delete_nonexistent_order(self):
        '''
        create and insert customer and item to be included in mock order.
        insert mock order, assign mock order's id to variable and then delete mock order prior to the test to ensure that order pending delete does not exist
        '''
        customer = Customer(name='test_name', email='test_email')
        item = Item(name='test_name', brand='test_brand', price=1)
        customer.insert()
        item.insert()
        mock_order = Orders(customer_id=customer.id,
                            item_id=item.id, quantity=1)
        mock_order.insert()
        nonexistent_order_id = mock_order.id
        mock_order.delete()
        # after mock order is deleted delete customer and item too
        customer.delete()
        item.delete()
        # attempt to delete nonexistent order
        res = self.client().delete(
            '/delete_order/{}'.format(nonexistent_order_id), headers=manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    #test authentication and authorization(RBAC)

    ''' NOTE: Warehouse Manager has access to all endpoints. The warehouse manager jwt has been utilized for all tested endpoints up to this point'''

    # test access endpoint without authorization header
    def test_401_access_endpoint_without_authentication(self):
        res = self.client().get('/customers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization header missing')


    ## Test Inventory Manager role permissions

    # Test inventory manager role's successfull endpoint access
    def test_inventory_manager_get_items(self):
        res = self.client().get('/items', headers=inventory_manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(['success'])
        self.assertTrue(len(data['items']))
    
    # Test inventory manager role's failure to access endpoint due to lack of appropriate authorization
    def test_401_inventory_manager_accessing_post_customer_endpoint(self):
        res = self.client().post('/new_customer', headers=inventory_manager_jwt, json=self.new_customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'user lacks appropriate permission')

    ## Test Salesperson role permissions

    # Test salesperson role's successfull endpoint access
    def test_salesperson_get_customers(self):
        res = self.client().get('/items', headers=salesperson_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(['success'])
        self.assertTrue(len(data['items']))

    # Test inventory manager role's failure to access endpoint due to lack of appropriate authorization
    def test_401_salesperson_accessing_post_item_endpoint(self):
        res = self.client().post('/new_item', headers=salesperson_jwt, json=self.new_item)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'user lacks appropriate permission')    


if __name__ == "__main__":
    unittest.main()
