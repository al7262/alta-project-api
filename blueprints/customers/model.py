# Import
from blueprints import db
from flask_restful import fields
import datetime
from blueprints.users.model import Users

# Create Model
class Customers(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    fullname = db.Column(db.String(150), nullable = False, default = "")
    phone_number = db.Column(db.String(20), nullable = False, default = "")
    email = db.Column(db.String(150), nullable = False, default = "")
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())

    response_fields = {
        'id' : fields.Integer,
        'id_users' : fields.Integer,
        'fullname' : fields.String,
        'phone_number' : fields.String,
        'email' : fields.String,
        'created_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer
    }

    def __init__(self, id_users, fullname, phone_number, email):
        self.id_users = id_users
        self.fullname = fullname
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        return '<Customers %r>' %self.fullname