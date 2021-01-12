# Warehouse Management API

## Motivation

As part of Udacity's 'Full Stack Web Developer Nanodegree Program' capstone project, the motivation was to create a that demonstrates many of the skills that were learnt throughout this course. This project depicts a warehouse app with a database that includes tables of customers, items and orders. There are also different user roles within this project that are commonly found in many warehouse environments. The goal was to create an API with self-explanatory endpoints and pre-understood relationships between the database tables, so anyone trying to get info can easily understand how to utilize this API.

# Getting Started

Please note: All commands must be run from the folders root directory

### Installing Dependencies

#### Python 3.9.0

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

It is recommended to work within a virtual environment in order to keep the dependencies organized.

#### PIP Dependencies

Once the virtual environment is up and running, dependencies can be installed by running:

```bash
pip install -r requirements.txt
```

The requirements.txt file includes all dependencies used to run this file.

## Database Setup

The app utilizes a postgres database: 'capstone_test'. After creating a postgres database the data can be populated with the included 'capstone_test.pgsql' file. The command is:

```bash
psql {$CREATED DATABASE} < capstone_test.pgsql
```

## Environment Variables

This app includes an 'setup.sh' file with environment variables. The variables must be exported to the terminal for the app to operate correctly. The command is:

```bash
source setup.sh
```

## Auth0

This app utilizes Auth0 to authenticate and provide endpoint authorization to users. There are 3 sample users setup with preassigned roles. The JWT tokens provided might will eventually expire and new JWT's can be generated with the following info:

User #1: Warehouse Manager

email: manager@warehouse.com
password: Password123

The warehouse manager has access to all the endpoints in the API.

User #2: Inventory Manager

email: inventory@warehouse.com
password: Password123

The inventory manager role has the following permissions: [get:items, get:orders, post:item, patch:item, delete:item]

User #3: Salesperson

email: sales@warehouse.com
password: Password123

A salesperson has the following permissions: [get:customers, get:items, get:orders, post:customer, post:order]

New JWT's can be generated at 'https://mapfdev.us.auth0.com/authorize?audience=warehouse-api&response_type=token&client_id=e4IYUqpnwQ16cg2YUxnj87L6rZqzlrEz&redirect_uri=https://127.0.0.1:8080/login-results'

It is recommended to login with an incognito browser, since a standard browser may automatically redirect to the first user that signed in.

## Unittest

This app includes a unittest file 'test_app.py'. The unittest utilizes a test postgres database 'test_capstone_test'. The .pgsql file can be used in the same manner as described above to populate the 'test_capstone_test' database.

PLEASE NOTE: Do not run the unittest suite without verifying that the jwt's are updated. Running the test suite with expired tokens will require manually deleting the entries entered into the database. If the unittest was run with invalid jwt's the database must be dropped and recreated. Once the JWT's are updated the 'source setup.sh' command must be rerun in the bash terminal.

The commands to run the unittest tests are:

```bash
source setup.sh
dropdb test_capstone_test
createdb test_capstone_test
psql test_capstone_test < capstone_test.pgsql
python test_app.py
```

## Running the server

First ensure that the virtual environment is activated and that the environment variables have been exported with:

```bash
source setup.sh
```

To run the server, execute:

```bash
export FLASK_APP=app.py

flask run

```

#### API Reference

This app can be run on localhost. The app is hosted at `http://127.0.0.1:5000`

This app is also deployed to Heroku. The heroku address is `https://my-capstone-starter.herokuapp.com`

## Endpoints

-All Objects are returned in JSON.

-All endpoints include success keys of either True or False with status codes.

-All data included in the request body, must be in JSON.

-All endpoints require permissions. Permissions are included in the user JWT's. All tokens must start with 'Bearer'.

### GET '/customers'

-Fetches a list of 'customers'
-Returns a customers list array with individual customer dictionaries that contain values of id, name, email

-Sample: Postman GET `http://127.0.0.1:5000/customers`
-Response:

{
"customers": [
{
"email": null,
"id": 1,
"name": "Walmart"
},
{
"email": null,
"id": 2,
"name": "Costco"
},
{
"email": "zara@zara.com",
"id": 3,
"name": "Zara"
},
{
"email": "info@pizza.com",
"id": 9,
"name": "Pizza"
},
{
"email": "info@pcworld.com",
"id": 10,
"name": "PC World"
},
{
"email": "",
"id": 11,
"name": "H & M"
},
{
"email": "None",
"id": 12,
"name": "Macy's"
},
{
"email": "email@JCPenny.com",
"id": 13,
"name": "JC Penny"
},
{
"email": "info@amazingsavings.com",
"id": 14,
"name": "Amazing Savings"
},
{
"email": "info@yamaha.com",
"id": 15,
"name": "Yamaha"
},
{
"email": "info@casio.com",
"id": 16,
"name": "Casio"
},
{
"email": "info@casio.com",
"id": 17,
"name": "Casio"
},
{
"email": "info@target.com",
"id": 18,
"name": "Target"
},
{
"email": "Email",
"id": 20,
"name": "name"
},
{
"email": "info@khols.com",
"id": 21,
"name": "Kohl's"
}
],
"status_code": 200,
"success": true
}

### POST '/new_customer'

-Posts a new customer to the database. Requires 'name' and 'email' keys containing values in the JSON request body.
-Returns a dictionary in key:value format containing keys of 'customer' and 'id'

-Sample: Postman 'POST' `http://127.0.0.1:5000/new_customer`

-Sample request JSON body:

{
"name": "Kohl's",
"email": "info@khols.com"
}

-Response:

{
"customer": "Kohl's",
"id": 21,
"status_code": 200,
"success": true
}

### PATCH '/update_customer/<int:id>'

-Updates a customers name and/or email. Requires either 'name' and/or 'email' keys containing values in the JSON request body.
-Returns an object with keys of 'name' and 'email'

-Sample: Postman 'PATCH' `http://127.0.0.1:5000/update_customer`

-Sample request JSON body:
{
"name": "Macy's",
"email":"macys@macys.com"
}

-Response:
{
"customer_email": "macys@macys.com",
"customer_name": "Macy's",
"status_code": 200,
"success": true
}

### DELETE '/delete_customer/<int:id>'

-Deletes a customer.
-Returns an object with keys for 'deleted_customer', 'deleted_id' and 'num_of_remaining_customers'

-Sample: Postman 'DELETE' `http://127.0.0.1:5000/delete_customer/8`

-Response:
{
"deleted_customer": "Macy's",
"deleted_id": 8,
"num_of_remaining_customers": 15,
"status_code": 200,
"success": true
}

### GET '/items'

-Fetches a list of 'items'
-Returns a 'items' list array with individual item dictionaries containing keys of id, name, brand and price

-Sample: Postman GET `http://127.0.0.1:5000/items`
-Response:
{
"items": [
{
"brand": "Fuji",
"id": 1,
"name": "keyboard",
"price": 23
},
{
"brand": "test brand",
"id": 7,
"name": "test item",
"price": 50
},
{
"brand": "Sony",
"id": 2,
"name": "camera",
"price": 85
}
],
"status_code": 200,
"success": true
}

### POST '/new_item'

-Posts a new item to the database. Requires 'name', 'email' and 'price' keys containing values in the JSON request body.
-Returns a dictionary in key:value format containing keys of 'id' and 'item'.

-Sample: Postman 'POST' `http://127.0.0.1:5000/new_item`

-Sample request JSON body:

{
"name": "charger",
"brand": "Panasonic",
"price": 8
}

-Response:

{
"id": 8,
"item": "charger",
"status_code": 200,
"success": true
}

### PATCH '/update_item/<int:id>'

-Updates an items name and/or brand and/or price. Requires either 'name' and/or 'brand' and/or 'price' keys containing values in the JSON request body.
-Returns an object with keys of 'item_name', 'item_brand' and 'item_price'.

-Sample request JSON body:
{
"name": "camera"
}

-Response:

{
"item_brand": "Sony",
"item_name": "camera",
"item_price": 85,
"status_code": 200,
"success": true
}

### DELETE '/delete_customer/<int:id>'

-Deletes an item.
-Returns an object with keys of 'deleted_item', 'deleted_id' and 'num_of_remaining_items'

-Sample: Postman 'DELETE' `http://127.0.0.1:5000/delete_customer/8`

-Response:
{
"deleted_id": 8,
"deleted_item": "charger",
"num_of_remaining_items": 3,
"status_code": 200,
"success": true
}

### GET '/items'

-Fetches a list of 'orders'
-Returns the 'orders' list array with individual order dictionaries containing keys of 'customer_name', 'id', 'item_name', 'order_date' and 'quantity'. Also returns a key 'num_of_orders' containing the number of total orders.

-Sample: Postman 'GET' `http://127.0.0.1:5000/orders`

-Returns:
{
"num_of_orders": 3,
"orders_list": [
{
"customer_name": "Costco",
"id": 2,
"item_name": "camera",
"order_date": "Wed, 06 Jan 2021 00:00:00 GMT",
"quantity": 10
},
{
"customer_name": "Zara",
"id": 3,
"item_name": "camera",
"order_date": "Wed, 06 Jan 2021 00:00:00 GMT",
"quantity": 8
},
{
"customer_name": "Zara",
"id": 4,
"item_name": "keyboard",
"order_date": "Wed, 06 Jan 2021 00:00:00 GMT",
"quantity": 8
}
],
"status_code": 200,
"success": true
}

### POST '/submit_order'

-Posts a new order to the database. Requires 'customer_id', 'item_id' and 'quantity' keys containing values in the JSON request body.
-Returns a dictionary with an 'order_id' key.

-Sample: Postman 'POST' `http://127.0.0.1:5000/submit_order`

-Sample request JSON body:

{
"customer_id": 1,
"item_id": 1,
"quantity": 2
}

-Response:

{
"order_id": 5,
"status_code": 200,
"success": true
}

### DELETE '/delete_order/<int:id>'

-Deletes an order.
-Returns an object with keys of 'current_orders', 'deleted_order_id', 'message', and 'previous_orders'

-Sample: Postman 'DELETE' `http://127.0.0.1:5000/delete_order/5`

-Response:
{
"current_orders": 3,
"deleted_order_id": 5,
"message": "order was deleted",
"previous_orders": 4,
"status_code": 200,
"success": true
}

## Author

Mendy Apfelbaum
