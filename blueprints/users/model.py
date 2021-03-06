from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fullname = db.Column(db.String(150), nullable = False, default = "")
    email = db.Column(db.String(150), nullable = False, default = "")
    password = db.Column(db.String(150), nullable = False, default = "")
    phone_number = db.Column(db.String(20), nullable = False, default = "")
    business_name = db.Column(db.String(150), nullable = False, default = "")
    image = db.Column(db.String(150), nullable = False, default = "")
    created_at = db.Column(db.DateTime, default = (datetime.now() + timedelta(hours = 7)))
    update_at = db.Column(db.DateTime, onupdate = (datetime.now() + timedelta(hours = 7)))
    
    response_fields = {
        'id' : fields.Integer,
        'fullname' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'phone_number' : fields.String,
        'business_name' : fields.String,
        'image' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'email' : fields.String
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Users %r>' %self.id