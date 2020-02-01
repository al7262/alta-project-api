# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime

# Create Model
class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(150), nullable = False, default = '')
    total_stock = db.Column(db.Integer, nullable = False, default = 0)
    unit = db.Column(db.String(20), nullable = False, default = '')
    unit_price = db.Column(db.Integer, nullale = False, default = 0)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, nullable = False, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deleted = db.Column(db.Boolean, default = False)

    employee_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'total_stock': fields.Integer,
        'unit': fields.String,
        'unit_price': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'deleted': fields.Boolean
    }

    jwt_claim_fields = {
        'id': fields.Integer,
        'deleted': fields.Boolean
    }

    def __init__(self, name, total_stock, unit, unit_price):
        self.name = name
        self.total_stock = total_stock
        self.unit = unit
        self.unit_price = unit_price
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.deleted = False
    
    def __repr__(self):
        return '<Inventory %r>' %self.name