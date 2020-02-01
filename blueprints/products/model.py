from blueprints import db
from flask_restful import fields
import datetime

class Products (db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(150), nullable = False, default = "")
    category = db.Column(db.String(150), nullable = False, default = "")
    selling_price = db.Column(db.Integer, nullable = False, default = 0)
    show = db.Column(db.Boolean, nullable = False, default = True)
    stock = db.Column(db.Integer, nullable = False, default = 0)
    image = db.Column(db.String(150), nullable = False, default = "")
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())

    response_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'category' : fields.String,
        'selling_price' : fields.Integer,
        'show' : fields.Boolean,
        'stock' : fields.Integer,
        'image' : fields.String,
        'deleted': fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer
    }

    def __init__(self, name, category, selling_price, show, image):
        self.name = name
        self.category = category
        self.selling_price = selling_price
        self.show = show
        self.image = image

    def __repr__(self):
        return '<Product %r>' %self.id