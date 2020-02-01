# Import
from blueprints import db
from flask_restful import fields
from datetime import datetime
from blueprints.outlets.model import Outlets

# Create Model
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_outlet = db.Column(db.Integer, db.ForeignKey('outlets.id'), nullable = False)
    username = db.Column(db.String(20), nullable = False, unique = True)
    full_name = db.Column(db.String(150), nullable = False, default = '')
    position = db.Column(db.String(20), nullable = False, default = '')
    password = db.Column(db.String(30), nullable = False, default = '')
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = db.Column(db.DateTime, nullable = False, default = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deleted = db.Column(db.Boolean, default = False)

    employee_fields = {
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

    jwt_claim_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'deleted': fields.Boolean
    }

    def __init__(self, id_outlet, username, full_name, position, password, deleted):
        self.id_outlet = id_outlet
        self.username = username
        self.full_name = full_name
        self.position = position
        self.password = password
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.deleted = False
    
    def __repr__(self):
        return '<Employee %r>' %self.username