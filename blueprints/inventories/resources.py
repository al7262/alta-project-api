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
from blueprints import dashboard_required, user_required, apps_required

# Creating blueprint
bp_inventories = Blueprint('inventories', __name__)
api = Api(bp_inventories)

class InventoryResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get all inventories for specified owner
    @jwt_required
    def get(self):
        # Take input from users
        claims = get_jwt_claims()
        id_user = claims['id']
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        args = parser.parse_args()

        # Get all inventories
        inventories = Inventories.query.filter_by(id_users = id_user).filter_by(deleted = 0)

        # Filter by inventory name
        if args['name'] != '':
            inventories = inventories.filter(Inventories.name.like("%" + args['name'] + "%"))
        
        # Show the result
        result = []
        for inventory in inventories:
            inventory = marshal(inventory, Inventories.inventories_fields)
            inventory['stock'] = inventory['total_stock']
            inventory['status'] = "Available"

            # Get the stock outlet
            id_inventory = inventory['id']
            stock_outlet_list = StockOutlet.query.filter_by(id_inventory = id_inventory)
            for stock_outlet in stock_outlet_list:
                stock_outlet = marshal(stock_outlet, StockOutlet.response_fields)
                if stock_outlet['stock'] <= stock_outlet['reminder']:
                    inventory['status'] = "Warning"

            result.append(inventory)
        return result, 200

class InventoryPerOutlet(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get all inventories in an outlet
    @jwt_required
    @dashboard_required
    def get(self, id_outlet):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        args = parser.parse_args()

        # Get all inventories in specified outlet
        stock_outlet_list = StockOutlet.query.filter_by(id_outlet = id_outlet)
        data_list = []
        below_reminder = 0
        for stock_outlet in stock_outlet_list:
            stock_outlet = marshal(stock_outlet, StockOutlet.response_fields)
            id_inventory = stock_outlet['id_inventory']

            # Get related row in inventories table
            inventory = Inventories.query.filter_by(id = id_inventory).filter_by(deleted = False).first()
            inventory = marshal(inventory, Inventories.inventories_fields)
            
            # Check reminder status
            if int(stock_outlet['stock']) <= int(stock_outlet['reminder']):
                reminder = 'Warning'
                below_reminder = below_reminder + 1
            else:
                reminder = 'Available' 

            # Prepare the data to be shown
            data = {
                'name': inventory['name'],
                'unit': inventory['unit'],
                'unit_price': inventory['unit_price'],
                'stock': stock_outlet['stock'],
                'status': reminder
            }
            data_list.append(data)
        
        # Prepare the result
        result = {
            'below_reminder': below_reminder,
            'inventories': data_list
        }
        return result, 200
    
    # Add new inventory to specified outlet
    @jwt_required
    @dashboard_required
    def post(self, id_outlet):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('total_stock', location = 'json', required = True)
        parser.add_argument('unit', location = 'json', required = True)
        parser.add_argument('unit_price', location = 'json', required = True)
        parser.add_argument('reminder', location = 'json', required = True)
        args = parser.parse_args()

        # Get ID users
        claims = get_jwt_claims()
        id_user = claims['id']        

        # Check for duplicate
        inventories = Inventories.query.filter_by(deleted = False)

        # Store to the database

class InventoryLogResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

api.add_resource(InventoryResource, '')
api.add_resource(InventoryPerOutlet, '/<id_outlet>')
api.add_resource(InventoryLogResource, '/log')