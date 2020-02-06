# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app
from blueprints.recipes.model import Recipe
from blueprints.inventories.model import Inventories
from blueprints.outlets.model import Outlets
from blueprints.stock_outlet.model import StockOutlet
from blueprints.carts.model import CartDetail, Carts
from blueprints.products.model import Products
from datetime import datetime, timedelta
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import dashboard_required, apps_required

# Creating blueprint
bp_activity = Blueprint('activity', __name__)
api = Api(bp_activity)

class ActivityResource(Resource):
    # Enable CORS
    def options(self, id_outlet=None):
        return {'status': 'ok'}, 200
    
    # Get transactions history in an outlet
    @jwt_required
    def get(self, id_outlet):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('order_code', location = 'args', required = False)
        parser.add_argument('date', location = 'args', required = True)
        args = parser.parse_args()
        
        # Get all carts in an outlet
        carts = Carts.query.filter_by(id_outlet = id_outlet)
        
        # Filter by order code
        if args['order_code'] != '':
            carts = carts.filter_by(order_code = args['order_code'])

        # Filter by date
        if args['date'] == 'Hari Ini':
            carts = carts.filter(Carts.created_at >= datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)).filter(Carts.created_at <= datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0) + timedelta(days = 1))
        elif args['date'] == 'Kemarin':
            carts = carts.filter(Carts.created_at >= datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0) - timedelta(days = 1)).filter(Carts.created_at <= datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0))

        # Loop through all carts
        transaction_detail = []
        total_sales = 0
        total_transactions = 0
        for cart in carts:
            # Prepare transaction data
            transaction_data = {
                'order_code': cart.order_code,
                'name': cart.name,
                'time': cart.created_at.strftime('%H:%M'),
                'total_payment': cart.total_payment,
                'total_item': cart.total_item,
                'total_discount': cart.total_discount,
                'total_tax': cart.total_tax,
                'item_detail': []
            }

            # Get detail of the cart
            cart_detail = CartDetail.query.filter_by(id_cart = cart.id)
            for detail in cart_detail:
                product = Products.query.filter_by(id = detail.id_product).filter_by(deleted = False).first()
                item_detail = {
                    'name': product.name,
                    'quantity': detail.quantity,
                    'total_price': detail.total_price_product
                }
                transaction_data['item_detail'].append(item_detail)
            transaction_detail.append(transaction_data)

            # Calculate some values
            total_transactions = total_transactions + 1
            total_sales = total_sales + cart.total_payment

        # Show the result
        result = {
            'total_transactions': total_transactions,
            'total_sales': total_sales,
            'transaction_detail': transaction_detail
        }
        return result, 200

api.add_resource(ActivityResource, '/<id_outlet>')