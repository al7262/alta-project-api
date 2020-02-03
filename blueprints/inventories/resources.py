# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Inventories, InventoryLog
from blueprints.stock_outlet.model import StockOutlet
from blueprints import db, app
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_inventories = Blueprint('inventories', __name__)
api = Api(bp_inventories)

class InventoryResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get all inventories for specified owner

class InventoryLogResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

api.add_resource(InventoryResource, '')
api.add_resource(InventoryLogResource, '/log')