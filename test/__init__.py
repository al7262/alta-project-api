import pytest, logging, hashlib
from app import app, cache
from blueprints import db
from flask import Flask, request, json
from datetime import datetime
from blueprints.users.model import Users
from blueprints.employees.model import Employees
from blueprints.outlets.model import Outlets
from blueprints.customers.model import Customers
from blueprints.products.model import Products
from blueprints.inventories.model import Inventories, InventoryLog
from blueprints.stock_outlet.model import StockOutlet
from blueprints.carts.model import Carts, CartDetail

# Creating dummy DB for testing purpose
def db_reset():
    db.drop_all()
    db.create_all()

    # ---------- Create Users ----------
    # User 1
    encrypted_1 = hashlib.md5('Hedygading1'.encode()).hexdigest()
    user_1 = Users(email = 'hedy@alterra.id', password = encrypted_1)
    db.session.add(user_1)
    db.session.commit()

    # User 2
    encrypted_2 = hashlib.md5('Garryac1'.encode()).hexdigest()
    user_2 = Users(email = 'garry@alterra.id', password = encrypted_2)
    db.session.add(user_2)
    db.session.commit()

    # ---------- Create Outlets ----------
    outlet_1 = Outlets(id_user = 1, name = 'Surabaya', phone_number = '089145672345', address = 'Jl. Tidar No. 25', tax = 10, city = 'Surabaya')
    db.session.add(outlet_1)
    db.session.commit()

    outlet_2 = Outlets(id_user = 1, name = 'Malang', phone_number = '089245572345', address = 'Jl. Semeru No. 31', tax = 10, city = 'Malang')
    db.session.add(outlet_2)
    db.session.commit()

    outlet_3 = Outlets(id_user = 1, name = 'Jakarta', phone_number = '089245571758', address = 'Jl. Merbabu No. 42', tax = 15, city = 'Jakarta')
    db.session.add(outlet_3)
    db.session.commit()

    # ---------- Create Cashier ----------
    encrypted_4 = hashlib.md5('Budisetiawan1'.encode()).hexdigest()
    cashier_1 = Employees(id_outlet = 1, full_name = 'Budi Setiawan', username = 'budisetiawan', password = encrypted_4, position = 'Kasir')
    db.session.add(cashier_1)
    db.session.commit()

    # ---------- Create Admin ----------
    encrypted_5 = hashlib.md5('Stevejobs1'.encode()).hexdigest()
    admin_1 = Employees(id_outlet = 1, full_name = 'Steve Jobs', username = 'stevejobs', password = encrypted_5, position = 'Admin')
    db.session.add(admin_1)
    db.session.commit()

    # ---------- Create Customer ----------
    customer_1 = Customers(id_users = 1, fullname = 'Buzz Lightyear', phone_number = '089514145654', email = 'buzz@lightyear.com')
    db.session.add(customer_1)
    db.session.commit()

    # ---------- Create Product ----------
    product_1 = Products(id_users = 1, name = 'Indomie Yogyakarta', category = 'Indomie', price = 12000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_1)
    db.session.commit()

    product_2 = Products(id_users = 1, name = 'Indomie Makassar', category = 'Indomie', price = 15000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_2)
    db.session.commit()

    product_3 = Products(id_users = 1, name = 'Indomie Ayam Geprek', category = 'Indomie', price = 12000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_3)
    db.session.commit()

    product_4 = Products(id_users = 1, name = 'Indomie Cabe Hijau', category = 'Indomie', price = 12000, image = 'http://dummy.jpg', show = False)
    db.session.add(product_4)
    db.session.commit()

    # ---------- Create Inventory ----------
    inventory_1 = Inventories(id_users = 1, name = 'Mie', total_stock = 0, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_1)

    inventory_2 = Inventories(id_users = 1, name = 'Merica', total_stock = 0, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_2)

    inventory_3 = Inventories(id_users = 1, name = 'Daun Bawang', total_stock = 0, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_3)

    # ---------- Create Cart ----------
    cart_1 = Carts(id_users = 1, id_outlet = 1, id_employee = 1, order_code = 'A32BC1', name = 'Lelianto Eko Pradana', total_item = 1, payment_method = 'Tunai', total_payment = 12000, total_discount = 0, total_tax = 1200, paid_price = 15000)
    db.session.add(cart_1)
    db.session.commit()

    cart_2 = Carts(id_users = 1, id_outlet = 1, order_code = 'A32BC2', name = 'Willy Sumarno', total_item = 1, payment_method = 'Tunai', total_payment = 12000, total_discount = 0, total_tax = 1200, paid_price = 15000)
    db.session.add(cart_2)
    db.session.commit()

    # ---------- Create Cart Detail ----------
    cart_detail_1 = CartDetail(id_cart = 1, id_product = 1, quantity = 1, total_price_product = 10000)
    db.session.add(cart_detail_1)
    db.session.commit()

    cart_detail_2 = CartDetail(id_cart = 2, id_product = 1, quantity = 1, total_price_product = 10000)
    db.session.add(cart_detail_1)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(username):
    # Checking whether admin or user and prepare the data
    if username == 'budisetiawan':
        cachename = "test-kasir-1-token"
        data = {
            'username': 'budisetiawan',
            'password': 'Budisetiawan1',
            'position': 'Kasir'
        }
    elif username == 'hedy@alterra.id':
        cachename = "test-user-1-token"
        data = {
            'username': 'hedy@alterra.id',
            'password': 'Hedygading1',
            'position': 'Owner'
        }
    elif username == 'stevejobs':
        cachename = "test-admin-1-token"
        data = {
            'username': 'stevejobs',
            'password': 'Stevejobs1',
            'position': 'Admin'
        }

    token = cache.get(cachename)
    if token is None:
        # Do Request
        req = call_client(request)
        if data['position'] == 'Owner' or data['position'] == 'Kasir':
            res = req.post('/login/apps', json = data, content_type='application/json')
        elif data['position'] == 'Owner' or data['position'] == 'Admin':
            res = req.post('/login/dashboard', json = data, content_type='application/json')        

        # Store Response
        res_json = json.loads(res.data)
        logging.warning('RESULT : %s', res_json)

        # Assertion
        assert res.status_code == 200

        # Save token into cache
        cache.set(cachename, res_json['token'], timeout = 60)

        # Return, because it is useful for other test
        return res_json['token']
    else:
        return token