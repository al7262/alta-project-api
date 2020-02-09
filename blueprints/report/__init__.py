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
from datetime import datetime
import json
import random

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
            products = products.filter_by(name = args['name'])
        
        # By category
        if args['category'] != '' and args['category'] is not None:
            products = products.filter_by(category = args['category'])

        # Search all transactions related to the products in specified outlet
        if args['id_outlet'] != '' and args['id_outlet'] is not None:
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

api.add_resource(ProductReport, '/product-sales')