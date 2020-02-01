from blueprints import db
from flask_restful import fields
import datetime

class Promos (db.Model):
    __tablename__ = "promos"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(150), nullable = False, default = "")
    status = db.Column(db.Boolean, nullable = False, default = False)
    day = db.Column(db.String(150), nullable = False, default = "")
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())

    response_fields = {
        'id' : fields.Integer,
        'name' : fields.String,
        'status' : fields.Boolean,
        'day' : fields.String,
        'deleted': fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    jwt_claims_fields = {
        'id' : fields.Integer
    }

    def __init__(self, name, status, day):
        self.name = name
        self.status = status
        self.day = day

    def __repr__(self):
        return '<Promos %r>' %self.id