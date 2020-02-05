# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Recipe
from blueprints import db, app
from blueprints.inventories.model import Inventories
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import dashboard_required, apps_required

# Creating blueprint
bp_recipe = Blueprint('recipe', __name__)
api = Api(bp_recipe)

class RecipeResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get recipe of a product
    @jwt_required
    @dashboard_required
    def get(self, id_product):
        # Get all recipes list
        recipes = Recipe.query.filter_by(id_product = id_product)

        # Get inventory name and unit
        result = []
        for recipe in recipes:
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id = recipe.id_inventory).first()
            name = inventory.name
            unit = inventory.unit

            # Prepare the data
            data = {
                'name': name,
                'unit': unit,
                'amount': recipe.amount
            }
            result.append(data)
        
        return result, 200

api.add_resource(RecipeResource, '/<id_product>')