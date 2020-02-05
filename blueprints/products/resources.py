# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Products
from blueprints.carts.model import Carts, CartDetail
from blueprints.employees.model import Employees
from blueprints.inventories.model import Inventories, InventoryLog
from blueprints.stock_outlet.model import StockOutlet
from blueprints.users.model import Users
from blueprints.outlets.model import Outlets
from blueprints import db, app
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import user_required, dashboard_required, apps_required

# Creating blueprint
bp_products = Blueprint('products', __name__)
api = Api(bp_products)

class ProductResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get all products from specified owner (can be filtered by: category, show / not, product name)
    @jwt_required
    def get(self):
        # Take input from users
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('category', location = 'args', required = False)
        parser.add_argument('show', location = 'args', required = False)
        parser.add_argument('name', location = 'args', required = False)
        args = parser.parse_args()

        # Get id user
        id_user = claims['id']

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
    @jwt_required
    @dashboard_required
    def post(self):
        # Get claims
        claims = get_jwt_claims()
        id_users = claims['id']

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

        # Check for duplicate
        products = Products.query.filter_by(deleted = False)
        for product in products:
            product = marshal(product, Products.response_fields)
            if product['id_users'] == id_users and product['name'] == args['name'] and product['category'] == args['category']:
                return {'message': 'Maaf, produk yang ingin kamu tambahkan sudah ada'}, 200

        # Store the new product into database
        new_product = Products(
            id_users = id_users,
            name = args['name'],
            category = args['category'],
            price = args['price'],
            show = show,
            image = args['image'],
            update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Sukses menambahkan produk"}, 200

class SpecificProductResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200

    # Get product specified by its ID
    @jwt_required
    def get(self, id_product):
        # Get the product and show the result
        product = Products.query.filter_by(id = id_product).filter_by(deleted = False).first()
        if product is None:
            return {}, 200
        product = marshal(product, Products.response_fields)
        return product, 200
    
    # Edit specified product
    @jwt_required
    @dashboard_required
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
    @jwt_required
    @dashboard_required
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
    @jwt_required
    def get(self):
        # Get id user
        claims = get_jwt_claims()
        id_user = claims['id']

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

    # Get all items in a category from specified owner
    @jwt_required
    def get(self):
        # Take input from users
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('category', location = 'args', required = True)
        args = parser.parse_args()

        # Get id user and category
        id_user = claims['id']
        category = args['category']

        # Get all products of the specified user and filter by category
        products = Products.query.filter_by(id_users = id_user).filter_by(deleted = False).filter_by(category = category)

        # Show the result
        result = []
        for product in products:
            product = marshal(product, Products.response_fields)
            result.append(product)
        return result, 200

class CheckoutResource(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Get all data needed to be shown in receipt
    @jwt_required
    @apps_required
    def get(self, id_cart):
        # Get user id
        claims = get_jwt_claims()
        id_users = claims['id']
        
        # Searching for specified cart
        specified_cart = Carts.query.filter_by(id = id_cart).filter_by(deleted = False).first()

        # Empty active cart
        if specified_cart is None:
            return {'message': 'Tidak ada transaksi aktif saat ini'}, 200
        
        # ---------- Prepare the receipt ----------
        # Get business logo
        owner = Users.query.filter_by(id = id_users).first()
        logo = owner.image

        # Get outlet information
        employee = Employees.query.filter_by(deleted = False).filter_by(id = id_employee).first()
        cashier_name = employee.full_name
        id_outlet = employee.id_outlet
        outlet = Outlets.query.filter_by(deleted = False).filter_by(id = id_outlet).first()
        
        # Serach for all items in cart
        cart_detail = CartDetail.query.filter_by(id_cart = specified_cart.id)
        items_list = []
        transaction_total_price = 0
        for detail in cart_detail:
            # Get related product information
            product = Products.query.filter_by(deleted = False).filter_by(id = detail.id_product).first()
            product_name = product.name
            item_data = {
                'product_name': product_name,
                'quantity': detail.quantity,
                'unit_price': detail.total_price_product / detail.quantity,
                'total_price': detail.total_price_product
            }
            transaction_total_price = transaction_total_price + detail.total_price_product
            items_list.append(item_data)

        # Create receipt
        receipt = {
            'logo': logo,
            'outlet_name': outlet.name,
            'address': outlet.address,
            'city': outlet.city,
            'phone_number': outlet.phone_number,
            'order': specified_cart.order_code,
            'customer_name': specified_cart.name,
            'time': specified_cart.created_at,
            'cashier_name': employee.full_name,
            'items_list': items_list,
            'transaction_total_price': transaction_total_price,
            'discount': specified_cart.total_discount,
            'tax': specified_cart.total_tax,
            'to_paid': transaction_total_price - specified_cart.total_discount + specified_cart.total_tax,
            'paid': specified_cart.paid_price,
            'payment_method': '',
            'return': specified_cart.paid_price - (transaction_total_price - specified_cart.total_discount + specified_cart.total_tax)
        }
        return receipt, 200

api.add_resource(ProductResource, '')
api.add_resource(SpecificProductResource, '/<id_product>')
api.add_resource(CategoryResource, '/category')
api.add_resource(ItemsPerCategory, '/category/items')
api.add_resource(CheckoutResource, '/checkout/<id_cart>')