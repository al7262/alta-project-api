# Import
from blueprints import db
from flask_restful import fields
import datetime
from blueprints.inventories.model import Inventories
from blueprints.products.model import Products

# Create Model
class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_inventory = db.Column(db.Integer, db.ForeignKey("inventories.id", ondelete = 'CASCADE'), nullable = False)
    id_product = db.Column(db.Integer, db.ForeignKey("products.id", ondelete = 'CASCADE'), nullable = False)
    amount = db.Column(db.Integer, nullable = False, default = 0)

    response_fields = {
        'id' : fields.Integer,
        'id_inventory' : fields.Integer,
        'id_product' : fields.Integer,
        'amount' : fields.Integer
    }

    def __init__(self, id_inventory, id_product, amount):
        self.id_inventory = id_inventory
        self.id_product = id_product
        self.amount = amount

    def __repr__(self):
        return '<Recipe %r>' %self.id