# Import
from blueprints import db
from flask_restful import fields
import datetime
from blueprints.products.model import Products
from blueprints.promo.model import Promos

# Create Model
class DetailPromo(db.Model):
    __tablename__ = "detail_promo"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_product = db.Column(db.Integer, db.ForeignKey("products.id", ondelete = 'CASCADE'), nullable = False)
    id_promo = db.Column(db.Integer, db.ForeignKey("promos.id", ondelete = 'CASCADE'), nullable = False)
    discount = db.Column(db.Integer, nullable = False, default = 0)

    response_fields = {
        'id' : fields.Integer,
        'id_product' : fields.Integer,
        'id_promo' : fields.Integer,
        'discount' : fields.Integer
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'id_product' : fields.Integer,
        'id_promo' : fields.Integer
    }

    def __init__(self, id_product, id_promo, discount):
        self.id_product = id_product
        self.id_promo = id_promo
        self.discount = discount

    def __repr__(self):
        return '<DetailPromo %r>' %self.id