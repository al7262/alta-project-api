from blueprints import db
from flask_restful import fields
import datetime

class Custumers(db.Model):
    __tablename__ = "custumers"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fullname = db.Column(db.String(150), nullable = False, default = "")
    phone_number = db.Column(db.String(20), nullable = False, default = "")
    email = db.Column(db.String(150), nullable = False, default = "")
    image = db.Column(db.String(150), nullable = False, default = "")
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())

    
    response_fields = {
        'id' : fields.Integer,
        'fullname' : fields.String,
        'phone_number' : fields.String,
        'email' : fields.String,
        'image' : fields.String,
        'created_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer
    }

    def __init__(self, fullname, phone_number, email, image):
        self.fullname = fullname
        self.phone_number = phone_number
        self.email = email
        self.image = image

    def __repr__(self):
        return '<Custumers %r>' %self.id