from blueprints import db
from flask_restful import fields
import datetime

class Users(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fullname = db.Column(db.String(255), nullable = False, default = "")
    email = db.Column(db.String(255), nullable = False, default = "")
    password = db.Column(db.String(255), nullable = False, default = "")
    number_phone = db.Column(db.Integer, nullable = False, default = "")
    business_name = db.Column(db.String(255), nullable = False, default = "")
    image = db.Column(db.String(255), nullable = False, default = "")
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())

    
    response_fields = {
        'id' : fields.Integer,
        'fullname' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'number_phone' : fields.Integer,
        'business_name' : fields.String,
        'image' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'email' : fields.String
    }

    def __init__(self, fullname, username, password, email, number_phone):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.email = email
        self.number_phone = number_phone

    def __repr__(self):
        return '<User %r>' %self.id