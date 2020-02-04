# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime
from blueprints.users.model import Users

# Create Model
class Outlets(db.Model):
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    name = db.Column(db.String(150), nullable = False, default = '')
    phone_number = db.Column(db.String(20), nullable = False, default = '')
    address = db.Column(db.String(150), nullable = False, default = '')
    city = db.Column(db.String(150), nullable = False, default = '')
    tax = db.Column(db.Integer, nullable = False, default = 0)
    created_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deleted = db.Column(db.Boolean, default = False)

    response_fields = {
        'id': fields.Integer,
        'id_user': fields.Integer,
        'name': fields.String,
        'phone_number': fields.String,
        'address': fields.String,
        'city': fields.String,
        'tax': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'deleted': fields.Boolean
    }

    jwt_claim_fields = {
        'id': fields.Integer,
        'deleted': fields.Boolean
    }

    def __init__(self, id_user, name, phone_number, address, city, tax):
        self.id_user = id_user
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.city = city
        self.tax = tax
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.deleted = False
    
    def __repr__(self):
        return '<Outlets %r>' %self.name