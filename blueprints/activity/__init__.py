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
from datetime import datetime
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
        # Get all carts in an outlet
        carts = Carts.query.filter_by(id_outlet = id_outlet)
        
        # Loop through all carts
        result = []
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
            result.append(transaction_data)
        
        return result, 200

api.add_resource(ActivityResource, '/<id_outlet>')