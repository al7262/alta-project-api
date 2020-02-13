# # Import
# from flask import Blueprint
# from flask_restful import Api, reqparse, Resource, marshal, inputs
# from sqlalchemy import desc
# from .model import Recipe
# from blueprints import db, app
# from blueprints.inventories.model import Inventories
# from blueprints.outlets.model import Outlets
# from blueprints.stock_outlet.model import StockOutlet
# from datetime import datetime
# import json

# # Import Authentication
# from flask_jwt_extended import jwt_required, get_jwt_claims
# from blueprints import dashboard_required, apps_required

# # Creating blueprint
# bp_recipe = Blueprint('recipe', __name__)
# api = Api(bp_recipe)

# class RecipeResource(Resource):
#     # Enable CORS
#     def options(self, id_product=None):
#         return {'status': 'ok'}, 200
    
# #     # Get recipe of a product
# #     @jwt_required
# #     @dashboard_required
# #     def get(self, id_product):
# #         # Get all recipes list
# #         recipes = Recipe.query.filter_by(id_product = id_product)

# #         # Get inventory name and unit
# #         result = []
# #         for recipe in recipes:
# #             inventory = Inventories.query.filter_by(deleted = False).filter_by(id = recipe.id_inventory).first()
# #             name = inventory.name
# #             unit = inventory.unit

# #             # Prepare the data
# #             data = {
# #                 'name': name,
# #                 'unit': unit,
# #                 'amount': recipe.amount
# #             }
# #             result.append(data)
        
# #         return result, 200
    
# #     # Add recipe of a product
# #     @jwt_required
# #     @dashboard_required
# #     def post(self, id_product):
# #         # Take input from user
# #         claims = get_jwt_claims()
# #         id_users = claims['id']
# #         parser = reqparse.RequestParser()
# #         parser.add_argument('name', location = 'json', required = True)
# #         parser.add_argument('amount', location = 'json', required = True)
# #         parser.add_argument('unit', location = 'json', required = True)
# #         args = parser.parse_args()

# #         # Check emptyness
# #         if args['name'] == '' or args['amount'] == '' or args['unit'] == '' or args['amount'] is None:
# #             return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 400

# #         # Positivity check
# #         if int(args['amount']) <= 0:
# #             return {'message': 'Kuantitas harus bernilai positif'}, 400

# #         # Check whether this inventory has already added or not
# #         inventory = Inventories.query.filter_by(name = args['name']).filter_by(deleted = False).first()
# #         if inventory is None:
# #             # Create new inventory and stock outlet in all outlets
# #             new_inventory = Inventories(id_users = id_users, name = args['name'], total_stock = 0, unit = args['unit'], unit_price = 0, times_edited = 0)
# #             db.session.add(new_inventory)
# #             db.session.commit()
# #             id_inventory = new_inventory.id
# #             outlets = Outlets.query.filter_by(deleted = False).filter_by(id_user = id_users)
# #             for outlet in outlets:
# #                 new_stock_outlet = StockOutlet(id_outlet = outlet.id, id_inventory = new_inventory.id, reminder = 0, stock = 0)
# #                 db.session.add(new_stock_outlet)
# #                 db.session.commit()
# #         else:
# #             # Checking whether the unit is correct or not
# #             if inventory.unit != args['unit']:
# #                 return {'message': 'Maaf, unit untuk bahan baku ' + inventory.name + ' tidak tepat'}, 400
# #             id_inventory = inventory.id

# #         # Check whether the recipe exist or not
# #         recipe = Recipe.query.filter_by(id_inventory = id_inventory).filter_by(id_product = id_product).first()
# #         if recipe is None:
# #             # Add the new recipe
# #             new_recipe = Recipe(id_inventory = id_inventory, id_product = id_product, amount = args['amount'])
# #             db.session.add(new_recipe)
# #             db.session.commit()
# #         else:
# #             # Edit existing recipe
# #             recipe.amount = args['amount']
# #             db.session.commit()

# #         return {'message': 'Sukses menambahkan resep'}, 200
    
# # class EditRecipe(Resource):
# #     # Enable CORS
# #     def options(self, id_recipe=None):
# #         return {'status': 'ok'}, 200

# #     # Edit recipe of a product
# #     @jwt_required
# #     @dashboard_required
# #     def put(self, id_recipe):
# #         # Take input from user
# #         claims = get_jwt_claims()
# #         id_users = claims['id']
# #         parser = reqparse.RequestParser()
# #         parser.add_argument('name', location = 'json', required = True)
# #         parser.add_argument('amount', location = 'json', required = True)
# #         parser.add_argument('unit', location = 'json', required = True)
# #         args = parser.parse_args()

# #         # Check emptyness
# #         if args['name'] == '' or args['amount'] == '' or args['unit'] == '' or args['amount'] is None:
# #             return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 400

# #         # Positivity check
# #         if int(args['amount']) <= 0:
# #             return {'message': 'Kuantitas harus bernilai positif'}, 400

# #         # Get specified recipe and its inventory name
# #         recipe = Recipe.query.filter_by(id = id_recipe).first()
# #         id_inventory = recipe.id_inventory
# #         its_inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()
# #         recipe_name = its_inventory.name

# #         # Check whether the name of inventory has already added in database or not
# #         inventories = Inventories.query.filter_by(deleted = False).filter_by(id_users = id_users)
# #         for inventory in inventories:
# #             if inventory.name == args['name'] and inventory.name != recipe_name:
# #                 return {'message': 'Maaf, nama tersebut sudah digunakan untuk bahan baku yang lain'}, 409

# #         # Edit inventory
# #         its_inventory.name = args['name']
# #         its_inventory.unit = args['unit']
# #         its_inventory.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         db.session.commit()

# #         # Edit recipe
# #         recipe.amount = args['amount']
# #         db.session.commit()

# #         return {'message': 'Sukses mengubah resep'}, 200

# # class DeleteRecipe(Resource):
# #     # Enable CORS
# #     def options(self, id_recipe=None):
# #         return {'status': 'ok'}, 200

# #     # Edit recipe of a product
# #     @jwt_required
# #     @dashboard_required
# #     def delete(self, id_recipe):
# #         # Get specified recipe and delete it
# #         recipe = Recipe.query.filter_by(id = id_recipe).first()
# #         db.session.delete(recipe)
# #         db.session.commit()

# #         return {'message': 'Sukses menghapus bahan dari resep'}, 200

# # class DetailRecipe(Resource):
# #     # Enable CORS
# #     def options(self, id_recipe=None):
# #         return {'status': 'ok'}, 200

# #     # Get the detail of recipe item
# #     @jwt_required
# #     @dashboard_required
# #     def get(self, id_recipe):
# #         # Get specified recipe and its inventory
# #         recipe = Recipe.query.filter_by(id = id_recipe).first()
# #         inventory = Inventories.query.filter_by(deleted = False).filter_by(id = recipe.id_inventory).first()
# #         result = {
# #             'name': inventory.name,
# #             'amount': recipe.amount,
# #             'unit': inventory.unit
# #         }
# #         return result, 200

# api.add_resource(RecipeResource, '/<id_product>')
# # api.add_resource(EditRecipe, '/edit/<id_recipe>')
# # api.add_resource(DeleteRecipe, '/delete/<id_recipe>')
# # api.add_resource(DetailRecipe, '/detail/<id_recipe>')