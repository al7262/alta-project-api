# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Inventories, InventoryLog
from blueprints.stock_outlet.model import StockOutlet
from blueprints.outlets.model import Outlets
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
        parser.add_argument('name', location = 'json', required = False)
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
        parser.add_argument('name', location = 'json', required = False)
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
        parser.add_argument('stock', location = 'json', required = True)
        parser.add_argument('unit', location = 'json', required = True)
        parser.add_argument('unit_price', location = 'json', required = True)
        parser.add_argument('reminder', location = 'json', required = True)
        args = parser.parse_args()

        # Get ID users
        claims = get_jwt_claims()
        id_user = claims['id']        

        # Check for duplicate
        stock_outlet_list = StockOutlet.query.filter_by(id_outlet = id_outlet)
        for stock_outlet in stock_outlet_list:
            id_inventory = stock_outlet.id_inventory
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()
            if inventory.name == args['name']:
                return {"message": "Bahan baku yang ingin kamu tambahkan sudah ada"}

        # Validate unit if the item has already added in other outlet
        inventories = Inventories.query.filter_by(id_users = id_user)
        for inventory in inventories:
            # Unit is different
            if inventory.name == args['name'] and inventory.unit != args['unit']:
                return {"message": "Unit untuk bahan baku " + inventory.name + " tidak tepat"}
            
            # The unit is correct
            elif inventory.name == args['name']:
                id_inventory = inventory.id
                
                # Add new stock outlet instance
                new_stock_outlet = StockOutlet(id_outlet = id_outlet, id_inventory = id_inventory, reminder = args['reminder'], stock = args['stock'])
                db.session.add(new_stock_outlet)
                db.session.commit()

                # Edit related inventory instance
                inventory.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                inventory.total_stock = inventory.total_stock + int(args['stock'])
                inventory.unit_price = int(((inventory.unit_price * inventory.times_edited) + int(args['unit_price']))/(inventory.times_edited + 1))
                inventory.times_edited = inventory.times_edited + 1
                db.session.commit()

                # Add inventory log instance
                new_inventory_log = InventoryLog(id_stock_outlet = new_stock_outlet.id, status = "Masuk", amount = args['stock'], last_stock = new_stock_outlet.stock)
                db.session.add(new_inventory_log)
                db.session.commit()

                return {'message': 'Sukses menambahkan bahan baku'}, 200
            
        # Create new one
        # Add new inventory instance
        new_inventory = Inventories(id_users = id_user, name = args['name'], total_stock = args['stock'], unit = args['unit'], unit_price = args['unit_price'], times_edited = 1)
        db.session.add(new_inventory)
        db.session.commit()
        id_inventory = new_inventory.id

        # Add new stock outlet instance
        new_stock_outlet = StockOutlet(id_outlet = id_outlet, id_inventory = id_inventory, reminder = args['reminder'], stock = args['stock'])
        db.session.add(new_stock_outlet)
        db.session.commit()

        # Add inventory log instance
        new_inventory_log = InventoryLog(id_stock_outlet = new_stock_outlet.id, status = "Masuk", amount = args['stock'], last_stock = new_stock_outlet.stock)
        db.session.add(new_inventory_log)
        db.session.commit()

        return {'message': 'Sukses menambahkan bahan baku'}, 200

class InventoryDetail(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get inventory information from specified stock outlet id
    def get(self, id_stock_outlet):
        # Find targeted stock outlet
        stock_outlet = StockOutlet.query.filter_by(id = id_stock_outlet).first()
        inventory = Inventories.query.filter_by(deleted = False).filter_by(id = stock_outlet.id_inventory).first()

        # Prepare the result
        result = {
            'name': inventory.name,
            'stock': stock_outlet.stock,
            'unit': inventory.unit,
            'reminder': stock_outlet.reminder
        }

        return result, 200

    # Edit existing stock outlet
    @jwt_required
    @dashboard_required
    def put(self, id_stock_outlet):
        # Find targeted stock outlet
        target_stock_outlet = StockOutlet.query.filter_by(id = id_stock_outlet).first()
        inventory = Inventories.query.filter_by(deleted = False).filter_by(id = target_stock_outlet.id_inventory).first()

        # Find related stock outlet in other outlet
        id_inventory = inventory.id
        related_stock_outlet_list = StockOutlet.query.filter_by(id_inventory = id_inventory)

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('stock', location = 'json', required = True)
        parser.add_argument('unit', location = 'json', required = True)
        parser.add_argument('reminder', location = 'json', required = True)
        args = parser.parse_args()

        # Validate emptyness
        if args['name'] == '' or args['stock'] == '' or args['unit'] == '' or args['reminder'] == '':
            return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 200

        # Edit stock outlet
        target_stock_outlet.reminder = args['reminder']
        target_stock_outlet.stock = args['stock']
        db.session.commit()

        # Edit inventory
        total_stock = 0
        for stock_outlet in related_stock_outlet_list:
            total_stock = total_stock + stock_outlet.stock
        inventory.name = args['name']
        inventory.unit = args['unit']
        inventory.total_stock = total_stock
        inventory.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()

        return {'message': 'Sukses mengubah bahan baku'}

    # Delete existing stock outlet
    @jwt_required
    @dashboard_required
    def delete(self, id_stock_outlet):
        # Searching for specified stock outlet and inventory
        stock_outlet = StockOutlet.query.filter_by(id = id_stock_outlet).first()
        id_inventory = stock_outlet.id_inventory
        inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()

        # Edit the inventory
        inventory.total_stock = inventory.total_stock - stock_outlet.stock
        inventory.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()

        # Delete inventory log related to this stock outlet
        logs = InventoryLog.query.filter_by(id_stock_outlet = id_stock_outlet)
        for log in logs:
            db.session.delete(log)
            db.session.commit()

        # Delete the stock outlet
        db.session.delete(stock_outlet)
        db.session.commit()

        # Get other related stock outlet
        related_stock_outlet = StockOutlet.query.filter_by(id_inventory = id_inventory).all()

        # Delete the inventory if there is nothing left in other outlet
        if len(related_stock_outlet) == 0:
            # Delete related recipe first

            # Delete the inventory
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()
            db.session.delete(inventory)
            db.session.commit()
        
        return {'message': 'Sukses menghapus bahan baku'}, 200

class AddStock(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Add stock to an inventory
    @jwt_required
    @dashboard_required
    def put(self, id_stock_outlet):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('stock', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        args = parser.parse_args()

        # Search for specified stock outlet and inventory related
        stock_outlet = StockOutlet.query.filter_by(id = id_stock_outlet).first()
        id_inventory = stock_outlet.id_inventory
        inventory = Inventories.query.filter_by(id = id_inventory).filter_by(deleted = False).first()

        # Edit stock outlet
        stock_outlet.stock = stock_outlet.stock + int(args['stock'])

        # Edit inventory
        inventory.total_stock = inventory.total_stock + int(args['stock'])
        inventory.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        inventory.unit_price = int(((inventory.unit_price * inventory.times_edited) + int(args['price']))/(inventory.times_edited + 1))
        inventory.times_edited = inventory.times_edited + 1

        # Add inventory log instance
        new_inventory_log = InventoryLog(id_stock_outlet = id_stock_outlet, status = "Masuk", amount = args['stock'], last_stock = stock_outlet.stock)
        db.session.add(new_inventory_log)
        db.session.commit()

        return {'message': 'Sukses menambahkan stok bahan baku'}, 200

class InventoryLogOutlet(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get all logs related to specified inventory in an outlet
    @jwt_required
    @dashboard_required
    def get(self, id_stock_outlet):
        # Get all inventory log of that inventory
        logs = InventoryLog.query.filter_by(id_stock_outlet = id_stock_outlet)

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('type', location = 'json', required = False)
        parser.add_argument('date', location = 'json', required = True)
        args = parser.parse_args()

        # Filter by type
        if args['type'] != '' or args['type'] != 'Semua':
            logs = logs.filter_by(status = args['type'])

        # Filter by date
        filtered_logs = []
        for log in logs:
            created_at = log.created_at
            if created_at.strftime("%Y-%m-%d") == args['date']:
                filtered_logs.append(log)
        
        # Get outlet name
        stock_outlet = StockOutlet.query.filter_by(id = id_stock_outlet).first()
        id_outlet = stock_outlet.id_outlet
        outlet = Outlets.query.filter_by(deleted = False).filter_by(id = id_outlet).first()
        outlet_name = outlet.name

        # Show the result
        logs_list = []
        for log in filtered_logs:
            log_data = {
                'date': log.created_at.strftime("%Y-%m-%d"),
                'time': log.created_at.strftime("%H:%M:%S"),
                'type': log.status,
                'amount': log.amount,
                'last_stock': log.last_stock
            }
            logs_list.append(log_data)
        result = {
            'outlet_name': outlet_name,
            'logs': logs_list
        }
        return result, 200

class InventoryLogAll(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get logs of an inventory in all outlets
    @jwt_required
    @dashboard_required
    def get(self, id_inventory):
        # Get all inventory log of that inventory
        stock_outlet_list = StockOutlet.query.filter_by(id_inventory = id_inventory)
        log_list = []
        for stock_outlet in stock_outlet_list:
            stock_outlet_id = stock_outlet.id
            logs = InventoryLog.query.filter_by(id_stock_outlet = stock_outlet_id)
            for log in logs:
                log_list.append(log)

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('type', location = 'json', required = False)
        parser.add_argument('date', location = 'json', required = True)
        args = parser.parse_args()

        # Filter by type
        if args['type'] != '' or args['type'] != 'Semua':
            log_list = filter(lambda log: log.status == args['type'], log_list)

        # Filter by date
        filtered_logs = []
        for log in log_list:
            created_at = log.created_at
            if created_at.strftime("%Y-%m-%d") == args['date']:
                filtered_logs.append(log)
        
        # Prepare the result
        result = []
        for log in filtered_logs:
            log_data = {
                'date': log.created_at.strftime("%Y-%m-%d"),
                'time': log.created_at.strftime("%H:%M:%S"),
                'type': log.status,
                'amount': log.amount,
                'last_stock': log.last_stock
            }
            result.append(log_data)
        return result, 200

class InventoryReminder(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get all inventories which almost run-out-of stock in an outlet
    @jwt_required
    @dashboard_required
    def get(self, id_outlet):
        # Get all stock outlet and filter those which stock less than or equal to reminder
        stock_outlet_list = StockOutlet.query.filter_by(id_outlet = id_outlet)
        stock_outlet_filtered = filter(lambda stock_outlet: stock_outlet.stock <= stock_outlet.reminder, stock_outlet_list)

        # Get outlet name
        outlet = Outlets.query.filter_by(deleted = False).filter_by(id = id_outlet).first()
        outlet_name = outlet.name

        # Prepare the result
        inventories_data = []
        for stock_outlet in stock_outlet_filtered:
            stock_outlet = marshal(stock_outlet, StockOutlet.response_fields)
            
            # Search for inventory name
            id_inventory = stock_outlet['id_inventory']
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()
            inventory_name = inventory.name

            # Prepare the data
            data = {
                'name': inventory_name,
                'stock': stock_outlet['stock'],
                'outlet': outlet_name
            }
            inventories_data.append(data)
        result = {
            'below_reminder': len(inventories_data),
            'reminder': inventories_data
        }
        return result, 200

class InventoryReminderAll(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get all inventories which stock almost run-out of stock in all outlets
    @jwt_required
    @dashboard_required
    def get(self):
        # Get ID users
        claims = get_jwt_claims()
        id_user = claims['id']

        # Get all stock outlet which belong to that user
        inventories = Inventories.query.filter_by(id_users = id_user).filter_by(deleted = False)
        stock_outlet_list = []
        for inventory in inventories:
            inventory_id = inventory.id
            related_stock_outlet = StockOutlet.query.filter_by(id_inventory = inventory_id)
            for stock_outlet in related_stock_outlet:
                stock_outlet_list.append(stock_outlet)

        # Get all stock outlet and filter those which stock less than or equal to reminder
        stock_outlet_filtered = filter(lambda stock_outlet: stock_outlet.stock <= stock_outlet.reminder, stock_outlet_list)

        # Prepare the result
        inventories_data = []
        for stock_outlet in stock_outlet_filtered:
            stock_outlet = marshal(stock_outlet, StockOutlet.response_fields)
            
            # Search for inventory name
            id_inventory = stock_outlet['id_inventory']
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()
            inventory_name = inventory.name

            # Get outlet name
            outlet = Outlets.query.filter_by(deleted = False).filter_by(id = stock_outlet['id_outlet']).first()
            outlet_name = outlet.name

            # Prepare the data
            data = {
                'name': inventory_name,
                'stock': stock_outlet['stock'],
                'outlet': outlet_name
            }
            inventories_data.append(data)
        result = {
            'below_reminder': len(inventories_data),
            'reminder': inventories_data
        }
        return result, 200

api.add_resource(InventoryResource, '')
api.add_resource(InventoryPerOutlet, '/<id_outlet>')
api.add_resource(InventoryDetail, '/detail/<id_stock_outlet>')
api.add_resource(AddStock, '/add-stock/<id_stock_outlet>')
api.add_resource(InventoryLogOutlet, '/log/<id_stock_outlet>')
api.add_resource(InventoryLogAll, '/log/all/<id_inventory>')
api.add_resource(InventoryReminder, '/reminder/<id_outlet>')
api.add_resource(InventoryReminderAll, '/reminder')