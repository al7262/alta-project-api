# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime
from blueprints.employee.model import employee
from blueprints.customers.model import customers

# Create Model
class Carts(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable = False)
    id_customers = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable = True)
    order_code = db.Column(db.String(50), unique = True, nullable = False)
    name = db.Column(db.String(150), nullable = False, default = '')
    email = db.Column(db.String(150), nullable = False, default = '')
    total_transaction = db.Column(db.Integer, nullable = False, default = 0)
    total_payment = db.Column(db.Integer, nullable = False, default = 0)
    total_discount = db.Column(db.Integer, nullable = False, default = 0)
    total_tax = db.Column(db.Integer, nullable = False, default = 0)
    paid_price = db.Column(db.Integer, nullable = False, default = 0)
    status = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deleted = db.Column(db.Boolean, default = False)

    carts_fields = {
        'id': fields.Integer,
        'id_employee': fields.Integer,
        'id_customers': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'total_transaction': fields.Integer,
        'total_payment': fields.Integer,
        'total_discount': fields.Integer,
        'total_tax': fields.Integer,
        'paid_price': fields.Integer,
        'status': fields.Boolean
        'created_at': fields.DateTime,
        'deleted': fields.Boolean
    }

    jwt_claim_fields = {
        'id': fields.Integer,
        'id_employee': fields.Integer,
        'deleted': fields.Boolean
    }

    def __init__(self, id_employee, id_customers, name, email, total_transaction, total_payment, total_discount, total_tax, paid_price):
        self.id_employee = id_employee
        self.id_customers = id_customers
        self.name = name
        self.email = email
        self.total_transaction = total_transaction
        self.total_payment = total_payment
        self.total_discount = total_discount
        self.total_tax = total_tax
        self.paid_price = paid_price
        self. status = True
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.deleted = False
    
    def __repr__(self):
        return '<Carts %r>' %self.id