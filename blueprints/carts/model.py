# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta
from blueprints.users.model import Users
from blueprints.employees.model import Employees
from blueprints.customers.model import Customers
from blueprints.products.model import Products
from blueprints.outlets.model import Outlets

# Model fields
class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    id_outlet = db.Column(db.Integer, db.ForeignKey('outlets.id'), nullable = False, default = None)
    id_employee = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable = True, default = None)
    id_customers = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable = True, default = None)
    order_code = db.Column(db.String(50), unique = True, nullable = False)
    name = db.Column(db.String(150), nullable = False, default = '')
    total_item = db.Column(db.Integer, nullable = False, default = 0)
    payment_method = db.Column(db.String(150), nullable = False, default = '')
    total_payment = db.Column(db.Integer, nullable = False, default = 0)
    total_discount = db.Column(db.Integer, nullable = False, default = 0)
    total_tax = db.Column(db.Integer, nullable = False, default = 0)
    paid_price = db.Column(db.Integer, nullable = False, default = 0)
    created_at = db.Column(db.DateTime, nullable = False, default = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"))
    deleted = db.Column(db.Boolean, default = False)

    # responsive carts fields
    carts_fields = {
        'id': fields.Integer,
        'id_users': fields.Integer,
        'id_outlet': fields.Integer,
        'id_employee': fields.Integer,
        'id_customers': fields.Integer,
        'order_code': fields.String,
        'name': fields.String,
        'total_item': fields.Integer,
        'payment_method': fields.String,
        'total_payment': fields.Integer,
        'total_discount': fields.Integer,
        'total_tax': fields.Integer,
        'paid_price': fields.Integer,
        'created_at': fields.DateTime,
        'deleted': fields.Boolean
    }

    # required fields when create new data
    def __init__(self, id_users, id_outlet, order_code, name, total_item, payment_method, total_payment, total_discount, total_tax, paid_price, id_employee = None, id_customers = None):
        self.id_users = id_users
        self.id_outlet = id_outlet
        self.id_employee = id_employee
        self.id_customers = id_customers
        self.order_code = order_code
        self.name = name
        self.total_item = total_item
        self.payment_method = payment_method
        self.total_payment = total_payment
        self.total_discount = total_discount
        self.total_tax = total_tax
        self.paid_price = paid_price
        self.created_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
        self.deleted = True
    
    # for display log this table 
    def __repr__(self):
        return '<Carts %r>' %self.id

# Model fields
class CartDetail(db.Model):
    __tablename__ = 'cart_detail'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_cart = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable = False)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False, default = 0)
    total_price_product = db.Column(db.Integer, nullable = False, default = 0)
    updated_at = db.Column(db.DateTime, nullable = False, default = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"))

    # responsive cart detail fields
    cart_detail_fields = {
        'id': fields.Integer,
        'id_cart': fields.Integer,
        'id_product': fields.Integer,
        'quantity': fields.Integer,
        'total_price_product': fields.Integer,
        'updated_at': fields.DateTime
    }

    # required fields when create new data
    def __init__(self, id_cart, id_product, quantity, total_price_product):
        self.id_cart = id_cart
        self.id_product = id_product
        self.quantity = quantity
        self.total_price_product = total_price_product
        self.updated_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
    
    # for display log this table
    def __repr__(self):
        return '<CartDetail %r>' %self.id