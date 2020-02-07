import pytest, logging, hashlib
from app import app #cache
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
def reset_db():
    db.drop_all()
    db.create_all()

    # ---------- Create Users ----------
    # User 1
    user_1 = Users(email = 'hedy@alterra.id', password = 'Hedygading1')
    db.session.add(user_1)
    db.session.commit()

    # User 2
    user_2 = Users(email = 'garry@alterra.id', password = 'Garryac1')
    db.session.add(user_2)
    db.session.commit()

    # ---------- Create Outlets ----------
    outlet_1 = Outlets(id_user = 1, name = 'Surabaya', phone_number = '089145672345', address = 'Jl. Tidar No. 25', tax = 10, city = 'Surabaya')
    db.session.add(outlet_1)
    db.session.commit()

    outlet_2 = Outlets(id_user = 1, name = 'Malang', phone_number = '089245572345', address = 'Jl. Semeru No. 31', tax = 10, city = 'Malang')
    db.session.add(outlet_1)
    db.session.commit()

    outlet_3 = Outlets(id_user = 1, name = 'Jakarta', phone_number = '089245571758', address = 'Jl. Merbabu No. 42', tax = 15, city = 'Jakarta')
    db.session.add(outlet_1)
    db.session.commit()

    # ---------- Create Cashier ----------
    cashier_1 = Employees(id_outlet = 1, full_name = 'Budi Setiawan', username = 'budisetiawan', password = 'Budisetiawan1', position = 'Kasir')
    db.session.add(cashier_1)
    db.session.commit()

    # ---------- Create Admin ----------
    admin_1 = Employees(id_outlet = 1, full_name = 'Steve Jobs', username = 'stevejobs', password = 'Stevejobs1', position = 'Admin')
    db.session.add(admin_1)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)