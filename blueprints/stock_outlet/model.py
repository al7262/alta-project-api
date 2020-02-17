# Import
from blueprints import db
from flask_restful import fields
import datetime
from blueprints.outlets.model import Outlets

# Create Model
class StockOutlet(db.Model):
    __tablename__ = "stock_outlet"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_outlet = db.Column(db.Integer, db.ForeignKey("outlets.id", ondelete = 'CASCADE'), nullable = False)
    id_inventory = db.Column(db.Integer, db.ForeignKey("inventories.id", ondelete = 'CASCADE'), nullable = False)
    reminder = db.Column(db.Integer, nullable = False, default = 0)
    stock = db.Column(db.Integer, nullable = False, default = 0)

    response_fields = {
        'id' : fields.Integer,
        'id_outlet' : fields.Integer,
        'id_inventory' : fields.Integer,
        'reminder' : fields.Integer,
        'stock' : fields.Integer
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'id_outlet' : fields.Integer,
        'id_inventory' : fields.Integer
    }

    def __init__(self, id_outlet, id_inventory, reminder, stock):
        self.id_outlet = id_outlet
        self.id_inventory = id_inventory
        self.reminder = reminder
        self.stock = stock

    def __repr__(self):
        return '<StockOutlet %r>' %self.id