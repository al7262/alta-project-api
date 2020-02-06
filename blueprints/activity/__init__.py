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
        
        # Get all cart detail
        item_list = []
        for cart in carts:
            item_detail = {

            }

api.add_resource(ActivityResource, '/<id_outlet>')