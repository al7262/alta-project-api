# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta
from blueprints.users.model import Users
from blueprints.stock_outlet.model import StockOutlet

# Create Model
class Inventories(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'), nullable = False)
    name = db.Column(db.String(150), nullable = False, default = '')
    total_stock = db.Column(db.Integer, nullable = False, default = 0)
    unit = db.Column(db.String(20), nullable = False, default = '')
    unit_price = db.Column(db.Integer, nullable = False, default = 0)
    times_edited = db.Column(db.Integer, nullable = False, default = 0)
    created_at = db.Column(db.DateTime, nullable = False, default = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, nullable = False, default = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"))
    deleted = db.Column(db.Boolean, default = False)

    inventories_fields = {
        'id': fields.Integer,
        'id_users': fields.Integer,
        'name': fields.String,
        'total_stock': fields.Integer,
        'unit': fields.String,
        'unit_price': fields.Integer,
        'times_edited': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'deleted': fields.Boolean
    }

    jwt_claim_fields = {
        'id': fields.Integer,
        'deleted': fields.Boolean
    }

    def __init__(self, id_users, name, total_stock, unit, unit_price, times_edited):
        self.id_users = id_users
        self.name = name
        self.total_stock = total_stock
        self.unit = unit
        self.unit_price = unit_price
        self.times_edited = times_edited
        self.created_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
        self.deleted = False
    
    def __repr__(self):
        return '<Inventories %r>' %self.name

class InventoryLog(db.Model):
    __tablename__ = 'inventory_log'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_stock_outlet = db.Column(db.Integer, db.ForeignKey('stock_outlet.id', ondelete = 'CASCADE'), nullable = False)
    status = db.Column(db.String(10), nullable = False, default ='')
    amount = db.Column(db.Integer, nullable = False, default = 0)
    last_stock = db.Column(db.Integer, nullable = False, default = 0)
    created_at = db.Column(db.DateTime, nullable = False, default = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"))

    inventory_log_fields = {
        'id': fields.Integer,
        'id_stock_outlet': fields.Integer,
        'status': fields.String,
        'amount': fields.Integer,
        'last_stock': fields.Integer,
        'created_at': fields.DateTime,
    }

    jwt_claim_fields = {
        'id': fields.Integer,
        'id_stock_outlet': fields.Integer,
    }

    def __init__(self, id_stock_outlet, status, amount, last_stock):
        self.id_stock_outlet = id_stock_outlet
        self.status = status
        self.amount = amount
        self.last_stock = last_stock
        self.created_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
    
    def __repr__(self):
        return '<InventoryLog %r>' %self.id