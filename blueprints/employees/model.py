# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta
from blueprints.outlets.model import Outlets

# Model fields
class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_outlet = db.Column(db.Integer, db.ForeignKey('outlets.id'), nullable = False)
    username = db.Column(db.String(100), nullable = False, unique = True)
    full_name = db.Column(db.String(150), nullable = False, default = '')
    position = db.Column(db.String(20), nullable = False, default = '')
    password = db.Column(db.String(190), nullable = False, default = '')
    created_at = db.Column(db.DateTime, nullable = False, default = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, nullable = False, default = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S"))
    deleted = db.Column(db.Boolean, default = False)

    # JWT required claims
    jwt_claim_fields = {
        'id': fields.Integer,
        'id_outlet': fields.Integer,
        'username': fields.String,
        'position': fields.String,
        'deleted': fields.Boolean
    }

    # Responsive employee fields
    response_fields = {
        'id': fields.Integer,
        'id_outlet': fields.Integer,
        'username': fields.String,
        'full_name': fields.String,
        'position': fields.String,
        'password': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'deleted': fields.Boolean
    }

    # required fields when create new data
    def __init__(self, id_outlet, full_name, username, password, position):
        self.id_outlet = id_outlet
        self.full_name = full_name
        self.username = username
        self.password = password
        self.position = position

    # for display log this table
    def __repr__(self):
        return '<Employees %r>' %self.username