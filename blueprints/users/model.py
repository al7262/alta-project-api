from blueprints import db
from flask_restful import fields
import datetime

class Users(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(30), unique = True, nullable = False, default = "")
    password = db.Column(db.String(255), nullable = False, default = "")
    fullname = db.Column(db.String(255), nullable = False, default = "")
    number_phone = db.Column(db.Integer, nullable = False, default = "")
    address = db.Column(db.String(255), nullable = False, default = "")
    email = db.Column(db.String(255), nullable = False, default = "")
    gender = db.Column(db.String(12), nullable = False, default = "")
    city = db.Column(db.String(255), nullable = False, default = "")
    role = db.Column(db.String(12), nullable = False, default = "")
    image = db.Column(db.String(255), nullable = False, default = "")
    rating = db.Column(db.Integer, nullable = False, default = 0)
    review = db.Column(db.String(255), nullable = False, default = "")
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())

    
    response_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'fullname' : fields.String,
        'number_phone' : fields.Integer,
        'address' : fields.String,
        'email' : fields.String,
        'gender' : fields.String,
        'city' : fields.String,
        'role' : fields.String,
        'image' : fields.String,
        'rating' : fields.Integer,
        'review' : fields.String,
        'deleted': fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'role' : fields.String,
        'deleted' : fields.Boolean
    }

    def __init__(self, username, password, fullname, email, address, number_phone, role):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email
        self.address = address
        self.number_phone = number_phone
        self.role = role

    def __repr__(self):
        return '<User %r>' %self.id