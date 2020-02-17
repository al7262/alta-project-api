# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta
from blueprints.users.model import Users

# Create Model
class Products (db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    name = db.Column(db.String(150), nullable = False, default = "")
    category = db.Column(db.String(150), nullable = False, default = "")
    price = db.Column(db.Integer, nullable = False, default = 0)
    show = db.Column(db.Boolean, nullable = False, default = True)
    stock = db.Column(db.Integer, nullable = False, default = 0)
    image = db.Column(db.String(255), nullable = False, default = "")
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, default = (datetime.now() + timedelta(hours = 7)))
    updated_at = db.Column(db.DateTime, onupdate = (datetime.now() + timedelta(hours = 7)))

    response_fields = {
        'id' : fields.Integer,
        'id_users': fields.Integer,
        'name' : fields.String,
        'category' : fields.String,
        'price' : fields.Integer,
        'show' : fields.Boolean,
        'stock' : fields.Integer,
        'image' : fields.String,
        'deleted': fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }


    def __init__(self, id_users, name, category, price, show, image):
        self.id_users = id_users
        self.name = name
        self.category = category
        self.price = price
        self.show = show
        self.image = image

    def __repr__(self):
        return '<Products %r>' %self.name
    