# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Products
from blueprints.carts.model import Carts, CartDetail
from blueprints import db, app
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_products = Blueprint('products', __name__)
api = Api(bp_products)

class ProductResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get all products from specified owner (can be filtered by: category, show / not, product name)
    def get(self):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('id_users', location = 'json', required = True)
        parser.add_argument('category', location = 'json', required = False)
        parser.add_argument('show', location = 'json', required = False)
        parser.add_argument('name', location = 'json', required = False)
        args = parser.parse_args()

        # Get id user
        id_user = args['id_users']

        # Get all products of the specified user
        products = Products.query.filter_by(id_users = id_user).filter_by(deleted = False)

        # ----- Filter -----
        # Category
        if args['category'] != '':
            products = products.filter_by(category = args['category'])

        # Show
        if args['show'] != '':
            if args['show'] == 'Ya':
                products = products.filter_by(show = True)
            elif args['show'] == 'Tidak':
                products = products.filter_by(show = False)
        
        # Product Name
        if args['name'] != '':
            products = products.filter(Products.name.like("%" + args['name'] + "%"))

        # Showing the result
        result = []
        for product in products:
            product = marshal(product, Products.response_fields)
            result.append(product)
        return result, 200
    
    # Add new product to database
    def post(self):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('id_users', location = 'json', required = True)
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('category', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        parser.add_argument('show', location = 'json', required = True)
        parser.add_argument('image', location = 'json', required = True)
        args = parser.parse_args()

        # Turn the show field into boolean
        if args['show'] == 'Ya':
            show = True
        elif args['show'] == 'Tidak':
            show = False

        # Check for duplicate
        products = Products.query.filter_by(deleted = False)
        for product in products:
            product = marshal(product, Products.response_fields)
            if product['id_users'] == args['id_users'] and product['name'] == args['name'] and product['category'] == args['category']:
                return {'Maaf, produk yang ingin kamu tambahkan sudah ada'}, 200

        # Store the new product into database
        new_product = Products(
            id_users = args['id_users'],
            name = args['name'],
            category = args['category'],
            price = args['price'],
            show = show,
            image = args['image']
        )
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Sukses menambahkan produk"}, 200

class SpecificProductResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get product specified by its ID
    def get(self, id_product):
        # Get the product and show the result
        product = Products.query.filter_by(id = id_product).filter_by(deleted = False).first()
        if product is None:
            return {}, 200
        product = marshal(product, Products.response_fields)
        return product, 200
    
    # Edit specified product
    def put(self, id_product):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('category', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        parser.add_argument('show', location = 'json', required = True)
        parser.add_argument('image', location = 'json', required = True)
        args = parser.parse_args()

        # Turn the show field into boolean
        if args['show'] == 'Ya':
            show = True
        elif args['show'] == 'Tidak':
            show = False

        # Get the product and edit it
        product = Products.query.filter_by(id = id_product).filter_by(deleted = False).first()
        product.name = args['name']
        product.category = args['category']
        product.price = args['price']
        product.show = show
        product.image = args['image']
        product.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Commit and show the result
        db.session.commit()
        return {'message': 'Sukses mengubah produk'}, 200

    # Soft delete specified product
    def delete(self, id_product):
        # Soft delete the product
        product = Products.query.filter_by(id = id_product).filter_by(deleted = False).first()
        product.deleted = True
        product.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Commit and show the result
        db.session.commit()
        return {'message': 'Sukses menghapus produk'}, 200

class CategoryResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get all categories from specified owner
    def get(self):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('id_users', location = 'json', required = True)
        args = parser.parse_args()

        # Get id user
        id_user = args['id_users']

        # Get all products of the specified user
        products = Products.query.filter_by(id_users = id_user).filter_by(deleted = False)

        # Get the category and show the result
        result = []
        for product in products:
            if product.category not in result:
                result.append(product.category)
        return result, 200

class ItemsPerCategory(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get all categories from specified owner
    def get(self):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('id_users', location = 'json', required = True)
        parser.add_argument('category', location = 'json', required = True)
        args = parser.parse_args()

        # Get id user and category
        id_user = args['id_users']
        category = args['category']

        # Get all products of the specified user and filter by category
        products = Products.query.filter_by(id_users = id_user).filter_by(deleted = False).filter_by(category = category)

        # Show the result
        result = []
        for product in products:
            product = marshal(product, Products.response_fields)
            result.append(product)
        return result, 200

api.add_resource(ProductResource, '')
api.add_resource(SpecificProductResource, '/<id_product>')
api.add_resource(CategoryResource, '/category')
api.add_resource(ItemsPerCategory, '/category/items')