# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints.products.model import Products
from blueprints.carts.model import Carts, CartDetail
from blueprints.employees.model import Employees
from blueprints.customers.model import Customers
from blueprints.inventories.model import Inventories, InventoryLog
from blueprints.stock_outlet.model import StockOutlet
from blueprints.recipes.model import Recipe
from blueprints.users.model import Users
from blueprints.outlets.model import Outlets
from blueprints import db, app
from datetime import datetime, timedelta
import json
import random
import re

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import user_required, dashboard_required, apps_required

# Creating blueprint
bp_report = Blueprint('report', __name__)
api = Api(bp_report)

class ProductReport(Resource):
    # Enable CORS
    def options(self, id_product=None):
        return {'status': 'ok'}, 200
    
    # Get product report
    @jwt_required
    @dashboard_required
    def get(self):
        # Get ID users and
        claims = get_jwt_claims()
        id_users = claims['id']

        # Prepare variable needed
        product_list = []
        total_sold = 0
        total_sales = 0

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'args', required = False)
        parser.add_argument('category', location = 'args', required = False)
        parser.add_argument('id_outlet', location = 'args', required = False)
        parser.add_argument('date_start', location = 'args', required = False)
        parser.add_argument('date_end', location = 'args', required = False)
        args = parser.parse_args()

        # Get all products from specific owner
        products = Products.query.filter_by(deleted = False).filter_by(id_users = id_users)

        # ----- First Filter -----
        # By name
        if args['name'] != '' and args['name'] is not None:
            products = products.filter(Products.name.like('%' + args['name'] + '%'))
        
        # By category
        if args['category'] != '' and args['category'] is not None:
            products = products.filter_by(category = args['category'])

        # Search all transactions related to the products in specified outlet
        for product in products:
            # Prepare variable needed
            add_status = True
            total_sales_of_product = 0
            total_sold_of_product = 0
            detail_transaction = CartDetail.query.filter_by(id_product = product.id)

            # ----- Second Filter -----
            # By date interval
            if args['date_start'] is not None and args['date_end'] is not None and args['date_start'] != '' and args['date_end'] != '':
                start_year = int(args['date_start'][0:4])
                start_month = int(args['date_start'][5:7])
                start_day = int(args['date_start'][8:10])
                end_year = int(args['date_end'][0:4])
                end_month = int(args['date_end'][5:7])
                end_day = int(args['date_end'][8:10])
                detail_transaction = detail_transaction.filter(CartDetail.updated_at >= datetime(start_year, start_month, start_day).replace(hour = 0, minute = 0, second = 0, microsecond = 0)).filter(CartDetail.updated_at <= datetime(end_year, end_month, end_day).replace(hour = 0, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1))

            for detail in detail_transaction:
                # ----- Third Filter -----
                # By outlet id
                if args['id_outlet'] != '' and args['id_outlet'] is not None:
                    transaction = Carts.query.filter_by(deleted = True).filter_by(id = detail.id_cart).first()
                    if transaction.id_outlet != int(args['id_outlet']):
                        add_status = False
                
                # Calculate some values
                if add_status == True:
                    total_sold_of_product = total_sold_of_product + detail.quantity
                    total_sales_of_product = total_sales_of_product + detail.total_price_product

            total_sales = total_sales + total_sales_of_product
            total_sold = total_sold + total_sold_of_product
            data = {
                'name': product.name,
                'category': product.category,
                'total_sold': total_sold_of_product,
                'total_sales': total_sales_of_product   
            }
            product_list.append(data)
            
        result = {
            'total_sales': total_sales,
            'total_sold': total_sold,
            'detail': product_list
        }
        return result, 200

class HistoryReport(Resource):
    # Enable CORS
    def options(self, id_product=None):
        return {'status': 'ok'}, 200
    
    # Get history report
    @jwt_required
    @dashboard_required
    def get(self):
        # Get the owner
        claims = get_jwt_claims()
        id_users = claims['id']
        owner = Users.query.filter_by(id = id_users).first()

        # Prepare variable needed
        product_list = []
        total_items_sold = 0
        total_sales = 0
        tax_summary = 0

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'args', required = False)
        parser.add_argument('id_outlet', location = 'args', required = False)
        parser.add_argument('date_start', location = 'args', required = False)
        parser.add_argument('date_end', location = 'args', required = False)
        args = parser.parse_args()

        # Get all transactions history from specific owner
        transactions = Carts.query.filter_by(deleted = True).filter_by(id_users = id_users)
        
        # ----- Filter by Date Interval -----
        if args['date_start'] is not None and args['date_end'] is not None and args['date_start'] != '' and args['date_end'] != '':
            start_year = int(args['date_start'][0:4])
            start_month = int(args['date_start'][5:7])
            start_day = int(args['date_start'][8:10])
            end_year = int(args['date_end'][0:4])
            end_month = int(args['date_end'][5:7])
            end_day = int(args['date_end'][8:10])
            transactions = transactions.filter(Carts.created_at >= datetime(start_year, start_month, start_day).replace(hour = 0, minute = 0, second = 0, microsecond = 0)).filter(Carts.created_at <= datetime(end_year, end_month, end_day).replace(hour = 0, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1))

        # ----- Filter by Outlet -----
        if args['id_outlet'] is not None and args['id_outlet'] != '':
            transactions = transactions.filter_by(id_outlet = args['id_outlet'])
        
        # Looping through all transactions
        for transaction in transactions:
            detail_transaction = CartDetail.query.filter_by(id_cart = transaction.id)
            outlet = Outlets.query.filter_by(id = transaction.id_outlet).first()
            
            # Search for cashier name
            if transaction.id_employee == None or transaction.id_employee == '':
                cashier_name = owner.fullname
            else:
                # Search for the employee
                cashier = Employees.query.filter_by(id = transaction.id_employee).first()
                cashier_name = cashier.full_name

            for detail in detail_transaction:
                # Prepare the variable needed
                add_stock = True
                
                # ----- Filter by Product Name -----
                product = Products.query.filter_by(id = detail.id_product).first()
                if args['name'] is not None and args['name'] != '':
                    if not re.search(args['name'].lower(), product.name.lower()):
                        add_stock = False

                if add_stock == True:
                    total_items_sold = total_items_sold + detail.quantity
                    total_sales = total_sales + detail.total_price_product
                    tax_summary = int(tax_summary + ((outlet.tax * detail.total_price_product) / 100))
                    data = {
                        'date_time': transaction.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'date': transaction.created_at.strftime("%Y-%m-%d"),
                        'time': transaction.created_at.strftime('%H:%M:%S'),
                        'outlet': outlet.name,
                        'cashier_name': cashier_name,
                        'product_name': product.name,
                        'total_items': detail.quantity,
                        'total_sales': detail.total_price_product
                    }
                    product_list.append(data)

        result = {
            'total_items_sold': total_items_sold,
            'total_sales': total_sales,
            'tax_summary': tax_summary,
            'detail': product_list
        }

        return result, 200

class InventoryLogReport(Resource):
    # Enable CORS
    def options(self, id_product=None):
        return {'status': 'ok'}, 200
    
    # Get inventory log report
    @jwt_required
    @dashboard_required
    def get(self):
        # Get the owner
        claims = get_jwt_claims()
        id_users = claims['id']
        owner = Users.query.filter_by(id = id_users).first()

        # Prepare variable needed
        log_list = []

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'args', required = False)
        parser.add_argument('id_outlet', location = 'args', required = False)
        parser.add_argument('type', location = 'args', required = False)
        parser.add_argument('date_start', location = 'args', required = False)
        parser.add_argument('date_end', location = 'args', required = False)
        args = parser.parse_args()

        # Get all products
        logs = InventoryLog.query.filter_by()

api.add_resource(ProductReport, '/product-sales')
api.add_resource(HistoryReport, '/history')
api.add_resource(InventoryLogReport, '/inventory-log')