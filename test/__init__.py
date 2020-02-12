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
from blueprints.recipes.model import Recipe
from blueprints.promo.model import Promos
from blueprints.detail_promo.model import DetailPromo
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

    encrypted = hashlib.md5('Cashierpass'.encode()).hexdigest()
    cashier_2 = Employees(id_outlet = 1, full_name = 'Cashier02', username = 'cashier02', password = encrypted, position = 'Kasir')
    db.session.add(cashier_2)
    db.session.commit()

    encrypted = hashlib.md5('Cashierpass'.encode()).hexdigest()
    cashier_3 = Employees(id_outlet = 1, full_name = 'Cashier03', username = 'cashier03', password = encrypted, position = 'Kasir')
    db.session.add(cashier_3)
    db.session.commit()

    encrypted = hashlib.md5('Cashierpass'.encode()).hexdigest()
    cashier_4 = Employees(id_outlet = 1, full_name = 'Cashier04', username = 'cashier04', password = encrypted, position = 'Kasir')
    db.session.add(cashier_4)
    db.session.commit()

    encrypted = hashlib.md5('Cashierpass'.encode()).hexdigest()
    cashier_5 = Employees(id_outlet = 1, full_name = 'Cashier05', username = 'cashier05', password = encrypted, position = 'Kasir')
    db.session.add(cashier_5)
    db.session.commit()

    # ---------- Create Admin ----------
    encrypted_5 = hashlib.md5('Stevejobs1'.encode()).hexdigest()
    admin_1 = Employees(id_outlet = 1, full_name = 'Steve Jobs', username = 'stevejobs', password = encrypted_5, position = 'Admin')
    db.session.add(admin_1)
    db.session.commit()

    encrypted_admin = hashlib.md5('Adminpass'.encode()).hexdigest()
    admin_2 = Employees(id_outlet = 1, full_name = 'AdminPass02', username = 'administrator02', password = encrypted_admin, position = 'Admin')
    db.session.add(admin_2)
    db.session.commit()

    encrypted_admin = hashlib.md5('Adminpass'.encode()).hexdigest()
    admin_3 = Employees(id_outlet = 1, full_name = 'AdminPass03', username = 'administrator03', password = encrypted_admin, position = 'Admin')
    db.session.add(admin_3)
    db.session.commit()

    encrypted_admin = hashlib.md5('Adminpass'.encode()).hexdigest()
    admin_4 = Employees(id_outlet = 1, full_name = 'AdminPass04', username = 'administrator04', password = encrypted_admin, position = 'Admin')
    db.session.add(admin_4)
    db.session.commit()

    encrypted_admin = hashlib.md5('Adminpass'.encode()).hexdigest()
    admin_5 = Employees(id_outlet = 1, full_name = 'AdminPass05', username = 'administrator05', password = encrypted_admin, position = 'Admin')
    db.session.add(admin_5)
    db.session.commit()

    # ---------- Create Customer ----------
    customer_1 = Customers(id_users = 1, fullname = 'Buzz Lightyear', phone_number = '089514145654', email = 'buzz@lightyear.com')
    db.session.add(customer_1)
    db.session.commit()

    customer_2 = Customers(id_users = 1, fullname = 'Tsubasa Ozora', phone_number = '089514145657', email = '')
    db.session.add(customer_2)
    db.session.commit()

    # ---------- Create Product ----------
    product_1 = Products(id_users = 1, name = 'Indomie Goreng', category = 'Indomie', price = 12000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_1)
    db.session.commit()

    product_2 = Products(id_users = 1, name = 'Indomie Kaldu Ayam', category = 'Indomie', price = 15000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_2)
    db.session.commit()

    product_3 = Products(id_users = 1, name = 'Indomie Ayam Geprek', category = 'Indomie', price = 12000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_3)
    db.session.commit()

    product_4 = Products(id_users = 1, name = 'Indomie Cabe Hijau', category = 'Indomie', price = 12000, image = 'http://dummy.jpg', show = False)
    db.session.add(product_4)
    db.session.commit()

    product_5 = Products(id_users = 1, name = 'Mie Ayam Biasa', category = 'Mie Ayam', price = 10000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_5)
    db.session.commit()

    product_6 = Products(id_users = 1, name = 'Mie Ayam Bawang', category = 'Mie Ayam', price = 15000, image = 'http://dummy.jpg', show = True)
    db.session.add(product_6)
    db.session.commit()

    product_7 = Products(id_users = 1, name = 'Mie Ayam Bakso', category = 'Mie Ayam', price = 18000, image = 'http://dummy.jpg', show = False)
    db.session.add(product_7)
    db.session.commit()

    # ---------- Create Inventory ----------
    inventory_1 = Inventories(id_users = 1, name = 'Mie', total_stock = 10000, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_1)
    db.session.commit()

    inventory_2 = Inventories(id_users = 1, name = 'Garam', total_stock = 800, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_2)
    db.session.commit()

    inventory_3 = Inventories(id_users = 1, name = 'Daun Bawang', total_stock = 285, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_3)
    db.session.commit()

    inventory_4 = Inventories(id_users = 1, name = 'Cabe Hijau', total_stock = 700, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_4)
    db.session.commit()

    inventory_5 = Inventories(id_users = 1, name = 'Ayam', total_stock = 2000, unit = 'gram', unit_price = 0, times_edited = 0)
    db.session.add(inventory_5)
    db.session.commit()

    inventory_6 = Inventories(id_users = 1, name = 'Indomie Goreng', total_stock = 30, unit = 'pcs', unit_price = 0, times_edited = 0)
    db.session.add(inventory_6)
    db.session.commit()

    inventory_7 = Inventories(id_users = 1, name = 'Indomie Kaldu Ayam', total_stock = 30, unit = 'pcs', unit_price = 0, times_edited = 0)
    db.session.add(inventory_7)
    db.session.commit()

    # ---------- Create Recipe ----------
    recipe_1 = Recipe(id_inventory = 6, id_product = 1, amount = 1)
    db.session.add(recipe_1)
    db.session.commit()

    recipe_2 = Recipe(id_inventory = 3, id_product = 1, amount = 50)
    db.session.add(recipe_2)
    db.session.commit()

    recipe_3 = Recipe(id_inventory = 7, id_product = 2, amount = 1)
    db.session.add(recipe_3)
    db.session.commit()

    recipe_4 = Recipe(id_inventory = 3, id_product = 2, amount = 50)
    db.session.add(recipe_4)
    db.session.commit()

    recipe_5 = Recipe(id_inventory = 1, id_product = 5, amount = 120)
    db.session.add(recipe_5)
    db.session.commit()

    recipe_6 = Recipe(id_inventory = 2, id_product = 5, amount = 20)
    db.session.add(recipe_6)
    db.session.commit()

    recipe_7 = Recipe(id_inventory = 3, id_product = 5, amount = 50)
    db.session.add(recipe_7)
    db.session.commit()

    recipe_8 = Recipe(id_inventory = 4, id_product = 5, amount = 50)
    db.session.add(recipe_8)
    db.session.commit()

    recipe_9 = Recipe(id_inventory = 5, id_product = 5, amount = 50)
    db.session.add(recipe_9)
    db.session.commit()

    # ---------- Create Stock Outlet ----------
    stock_outlet_1 = StockOutlet(id_outlet = 1, id_inventory = 1, reminder = 500, stock = 3000)
    db.session.add(stock_outlet_1)
    db.session.commit()

    stock_outlet_2 = StockOutlet(id_outlet = 2, id_inventory = 1, reminder = 1000, stock = 4000)
    db.session.add(stock_outlet_2)
    db.session.commit()

    stock_outlet_3 = StockOutlet(id_outlet = 3, id_inventory = 1, reminder = 700, stock = 3000)
    db.session.add(stock_outlet_3)
    db.session.commit()

    stock_outlet_4 = StockOutlet(id_outlet = 1, id_inventory = 2, reminder = 50, stock = 300)
    db.session.add(stock_outlet_4)
    db.session.commit()

    stock_outlet_5 = StockOutlet(id_outlet = 2, id_inventory = 2, reminder = 100, stock = 500)
    db.session.add(stock_outlet_5)
    db.session.commit()

    stock_outlet_6 = StockOutlet(id_outlet = 1, id_inventory = 3, reminder = 300, stock = 285)
    db.session.add(stock_outlet_6)
    db.session.commit()

    stock_outlet_7 = StockOutlet(id_outlet = 1, id_inventory = 4, reminder = 1000, stock = 700)
    db.session.add(stock_outlet_7)
    db.session.commit()

    stock_outlet_8 = StockOutlet(id_outlet = 1, id_inventory = 5, reminder = 500, stock = 3000)
    db.session.add(stock_outlet_8)
    db.session.commit()

    stock_outlet_9 = StockOutlet(id_outlet = 1, id_inventory = 6, reminder = 10, stock = 30)
    db.session.add(stock_outlet_9)
    db.session.commit()

    stock_outlet_10 = StockOutlet(id_outlet = 1, id_inventory = 7, reminder = 10, stock = 30)
    db.session.add(stock_outlet_10)
    db.session.commit()

    # ---------- Create Cart ----------
    cart_1 = Carts(id_users = 1, id_outlet = 1, id_employee = 1, order_code = 'A32BC1', name = 'Lelianto Eko Pradana', total_item = 1, payment_method = 'Tunai', total_payment = 12000, total_discount = 0, total_tax = 1200, paid_price = 15000)
    db.session.add(cart_1)
    db.session.commit()

    cart_2 = Carts(id_users = 1, id_outlet = 1, order_code = 'A32BC2', name = 'Willy Sumarno', total_item = 1, payment_method = 'Tunai', total_payment = 12000, total_discount = 0, total_tax = 1200, paid_price = 15000)
    db.session.add(cart_2)
    db.session.commit()

    cart_3 = Carts(id_users = 1, id_outlet = 1, id_customers = 1, order_code = 'A52BCX', name = 'Buzz Lightyear', total_item = 2, payment_method = 'Kartu', total_payment = 12000, total_discount = 0, total_tax = 1200, paid_price = 27000)
    db.session.add(cart_3)
    db.session.commit()

    cart_4 = Carts(id_users = 1, id_outlet = 1, id_customers = 1, order_code = 'A52BCY', name = 'Buzz Lightyear', total_item = 3, payment_method = 'Tunai', total_payment = 37000, total_discount = 0, total_tax = 3700, paid_price = 45000)
    db.session.add(cart_4)
    db.session.commit()

    cart_5 = Carts(id_users = 1, id_outlet = 1, id_customers = 1, order_code = 'A62BCY', name = 'Buzz Lightyear', total_item = 1, payment_method = 'Tunai', total_payment = 12000, total_discount = 0, total_tax = 1200, paid_price = 50000)
    db.session.add(cart_5)
    db.session.commit()

    # ---------- Create Cart Detail ----------
    cart_detail_1 = CartDetail(id_cart = 1, id_product = 1, quantity = 1, total_price_product = 10000)
    db.session.add(cart_detail_1)
    db.session.commit()

    cart_detail_2 = CartDetail(id_cart = 2, id_product = 1, quantity = 1, total_price_product = 10000)
    db.session.add(cart_detail_1)
    db.session.commit()

    cart_detail_3 = CartDetail(id_cart = 3, id_product = 1, quantity = 1, total_price_product = 12000)
    db.session.add(cart_detail_3)
    db.session.commit()

    cart_detail_4 = CartDetail(id_cart = 3, id_product = 6, quantity = 1, total_price_product = 15000)
    db.session.add(cart_detail_4)
    db.session.commit()

    cart_detail_5 = CartDetail(id_cart = 4, id_product = 1, quantity = 1, total_price_product = 12000)
    db.session.add(cart_detail_5)
    db.session.commit()

    cart_detail_6 = CartDetail(id_cart = 4, id_product = 2, quantity = 1, total_price_product = 15000)
    db.session.add(cart_detail_6)
    db.session.commit()

    cart_detail_7 = CartDetail(id_cart = 4, id_product = 5, quantity = 1, total_price_product = 10000)
    db.session.add(cart_detail_7)
    db.session.commit()

    cart_detail_8 = CartDetail(id_cart = 5, id_product = 1, quantity = 1, total_price_product = 12000)
    db.session.add(cart_detail_8)
    db.session.commit()

    # ------------- Create Promo -------------
    promo_1 = Promos(id_users = 1, name = "Merdeka", day = "Senin, Selasa", status = False)
    db.session.add(promo_1)
    db.session.commit()

    promo_2 = Promos(id_users = 1, name = "Valentine", day = "Minggu", status = False)
    db.session.add(promo_2)
    db.session.commit()

    # ---------- Create Promo Detail ---------
    detail_promo_1 = DetailPromo(id_promo = 1, id_product = 1, discount = 10)
    db.session.add(detail_promo_1)
    db.session.commit()

    detail_promo_2 = DetailPromo(id_promo = 1, id_product = 2, discount = 20)
    db.session.add(detail_promo_2)
    db.session.commit()

    detail_promo_3 = DetailPromo(id_promo = 2, id_product = 3, discount = 5)
    db.session.add(detail_promo_3)
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
    else:
        for index in [2,3,4,5]:
            if username == 'cashier0' + str(index):
                cachename = "test-cashier-" + str(index)
                data = {
                    'username': 'cashier0' + str(index),
                    'password': 'Cashierpass',
                    'position': 'Kasir'
                }
            elif username == 'administrator0' + str(index):
                cachename = "test-admin-" + str(index)
                data = {
                    'username': 'administrator0' + str(index),
                    'password': 'Adminpass',
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