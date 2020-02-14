# Import
from flask import Blueprint, request
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Products
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
from twilio.rest import Client as twilio_client
from io import BytesIO
from PIL import Image, ImageDraw
from mailjet_rest import Client

import json
import random
import os

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
        parser.add_argument('id_outlet', location = 'args', required = False)
        args = parser.parse_args()

        # Get id user
        if 'email' in claims:
            id_user = claims['id']
        else:
            id_user = claims['id']

        # Get all products of the specified user
        products = Products.query.filter_by(id_users = id_user).filter_by(deleted = False)

        # ----- Filter -----
        # Category
        if args['category'] != '' and args['category'] is not None:
            products = products.filter_by(category = args['category'])

        # Show
        if args['show'] == 'Ya':
            products = products.filter_by(show = True)
        elif args['show'] == 'Tidak':
            products = products.filter_by(show = False)
        
        # Product Name
        if args['name'] != '' and args['name'] is not None:
            if products.all() != []:
                products = products.filter(Products.name.like("%" + args['name'] + "%"))

        # Showing the result
        result = []
        for product in products:
            product = marshal(product, Products.response_fields)
            
            # ----- Counting the stock -----
            if args['id_outlet'] != '' and args['id_outlet'] is not None:
                # Find all its recipe
                max_stock = []
                recipes = Recipe.query.filter_by(id_product = product['id'])
                if recipes.all() != []:
                    for recipe in recipes:
                        # Find related stock outlet
                        inventory_id = recipe.id_inventory
                        related_stock_outlet = StockOutlet.query.filter_by(id_outlet = args['id_outlet']).filter_by(id_inventory = inventory_id).first()
                        max_portion = 0
                        if related_stock_outlet is not None:
                            max_portion = int(related_stock_outlet.stock // recipe.amount)
                        max_stock.append(max_portion)
                    product['stock'] = min(max_stock)
            
            result.append(product)
        return result[::-1], 200
    
    # Add new product to database
    @jwt_required
    @dashboard_required
    def post(self):
        # Get claims
        claims = get_jwt_claims()
        
        # Get id user
        if 'email' in claims:
            id_users = claims['id']
        else:
            id_users = claims['id']

        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('category', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        parser.add_argument('show', location = 'json', required = True)
        parser.add_argument('image', location = 'json', required = True)
        parser.add_argument('recipe', location = 'json', required = True, type = list)
        args = parser.parse_args()

        # Check emptyness
        if args['name'] == '' or args['price'] == '' or args['image'] == '' or args['category'] == '' or args['name'] is None or args['price'] is None or args['image'] is None or args['category'] is None:
            return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 400

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
                return {'message': 'Maaf, produk yang ingin kamu tambahkan sudah ada'}, 409

        # Store the new product into database
        new_product = Products(
            id_users = id_users,
            name = args['name'],
            category = args['category'],
            price = args['price'],
            show = show,
            image = args['image'],
        )
        db.session.add(new_product)
        db.session.commit()

        # Loop through recipe list
        for recipe in args['recipe']:
            # Check whether this inventory has already added or not
            inventory = Inventories.query.filter_by(name = recipe['name']).filter_by(deleted = False).first()
            if inventory is None:
                # Create new inventory and stock outlet in all outlets
                new_inventory = Inventories(id_users = id_users, name = recipe['name'], total_stock = 0, unit = recipe['unit'], unit_price = 0, times_edited = 0)
                db.session.add(new_inventory)
                db.session.commit()
                id_inventory = new_inventory.id
                outlets = Outlets.query.filter_by(deleted = False).filter_by(id_user = id_users)
                for outlet in outlets:
                    new_stock_outlet = StockOutlet(id_outlet = outlet.id, id_inventory = new_inventory.id, reminder = 0, stock = 0)
                    db.session.add(new_stock_outlet)
                    db.session.commit()
            else:
                # Checking whether the unit is correct or not
                id_inventory = inventory.id
            
            # Add the new recipe
            new_recipe = Recipe(id_inventory = id_inventory, id_product = new_product.id, amount = recipe['quantity'])
            db.session.add(new_recipe)
            db.session.commit()

        return {"message": "Sukses menambahkan produk"}, 200

class SpecificProductResource(Resource):
    # Enable CORS
    def options(self, id_product=None):
        return {'status': 'ok'}, 200

    # Get product specified by its ID
    @jwt_required
    def get(self, id_product):
        # Get the product
        product = Products.query.filter_by(id = id_product).filter_by(deleted = False).first()
        if product is None:
            return {}, 200
        product = marshal(product, Products.response_fields)

        # Get its recipe
        recipes = Recipe.query.filter_by(id_product = product['id'])
        recipe_list = []
        for recipe in recipes:
            # Get inventory name
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id = recipe.id_inventory).first()
            data = {
                'name': inventory.name,
                'quantity': recipe.amount,
                'unit': inventory.unit
            }
            recipe_list.append(data)
        
        # Check show field
        if product['show'] == True:
            show = 'Ya'
        elif product['show'] == False:
            show = 'Tidak'

        # Show the result
        result = {
            'id': product['id'],
            'name': product['name'],
            'category': product['category'],
            'price': product['price'],
            'image': product['image'],
            'show': show,
            'recipe': recipe_list
        }
        return result, 200
    
    # Edit specified product
    @jwt_required
    @dashboard_required
    def put(self, id_product):
        # Take input from users
        claims = get_jwt_claims()
        if 'email' in claims:
            id_users = claims['id']
        else:
            id_users = claims['id']
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('category', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        parser.add_argument('show', location = 'json', required = True)
        parser.add_argument('image', location = 'json', required = True)
        parser.add_argument('recipe', location = 'json', required = True, type = list)
        args = parser.parse_args()

        # Check emptyness
        if args['name'] == '' or args['price'] == '' or args['image'] == '' or args['category'] == '' or args['name'] is None or args['price'] is None or args['image'] is None or args['category'] is None:
            return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 400

        # Get the specified product
        product = Products.query.filter_by(deleted = False).filter_by(id = id_product).first()

        # Turn the show field into boolean
        if args['show'] == 'Ya':
            show = True
        elif args['show'] == 'Tidak':
            show = False

        # Edit the product and commit it
        product.name = args['name']
        product.category = args['category']
        product.price = args['price']
        product.show = show
        product.image = args['image']
        product.updated_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()

        # Come in recipe
        come_in_recipe = []
        for recipe in args['recipe']:
            come_in_recipe.append(recipe['name'])

        # Before edit recipe
        recipes = Recipe.query.filter_by(id_product = product.id)
        for recipe in recipes:
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id = recipe.id_inventory).first()
            inventory_name = inventory.name
            
            # Delete the recipe if the inventory is not in come in recipe list
            if inventory_name not in come_in_recipe:
                db.session.delete(recipe)
                db.session.commit()

        # Add new recipe or modify existing one
        for come_in_recipe in args['recipe']:
            inventory = Inventories.query.filter_by(deleted = False).filter_by(id_users = id_users).filter_by(name = come_in_recipe['name']).first()
            if inventory is None:
                # Add new inventory and its stock outlet
                new_inventory = Inventories(id_users = id_users, name = come_in_recipe['name'], total_stock = 0, unit = come_in_recipe['unit'], unit_price = 0, times_edited = 0)
                db.session.add(new_inventory)
                db.session.commit()
                id_inventory = new_inventory.id
                outlets = Outlets.query.filter_by(deleted = False).filter_by(id_user = id_users)
                for outlet in outlets:
                    new_stock_outlet = StockOutlet(id_outlet = outlet.id, id_inventory = new_inventory.id, reminder = 0, stock = 0)
                    db.session.add(new_stock_outlet)
                    db.session.commit()
                
                # Add new recipe
                new_recipe = Recipe(id_inventory = new_inventory.id, id_product = id_product, amount = come_in_recipe['quantity'])
                db.session.add(new_recipe)
                db.session.commit()

            else:
                existing_recipe = Recipe.query.filter_by(id_inventory = inventory.id).filter_by(id_product = id_product).first()
                # Add new recipe
                if existing_recipe is None:
                    new_recipe = Recipe(id_inventory = inventory.id, id_product = id_product, amount = come_in_recipe['quantity'])
                    db.session.add(new_recipe)
                    db.session.commit()

                # Edit existing recipe    
                else:
                    existing_recipe.amount = come_in_recipe['quantity']
                    db.session.commit()

        return {'message': 'Sukses mengubah produk'}, 200

    # Soft delete specified product
    @jwt_required
    @dashboard_required
    def delete(self, id_product):
        # Soft delete the product
        product = Products.query.filter_by(id = id_product).filter_by(deleted = False).first()
        product.deleted = True
        product.updated_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()

        # Delete related recipe
        recipes = Recipe.query.filter_by(id_product = id_product).all()
        for recipe in recipes:
            db.session.delete(recipe)
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
        if 'email' in claims:
            id_user = claims['id']
        else:
            id_user = claims['id']

        # Get all products of the specified user
        products = Products.query.filter_by(id_users = id_user).filter_by(deleted = False)

        # Get the category and show the result
        result = []
        for product in products:
            if product.category not in result:
                result.append(product.category)
        return result[::-1], 200

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
        parser.add_argument('id_outlet', location = 'args', required = False)
        args = parser.parse_args()

        # Check emptyness
        if args['category'] == '' or args['category'] is None:
            return [], 200

        # Get id user and category
        if 'email' in claims:
            id_user = claims['id']
        else:
            id_user = claims['id']
        category = args['category']

        # Get all products of the specified user and filter by category
        products = Products.query.filter_by(id_users = id_user).filter_by(deleted = False).filter_by(category = category)

        # Check emptyness
        if products.all() == []:
            return [], 200

        # Show the result
        result = []
        for product in products:
            product = marshal(product, Products.response_fields)
            
            # ----- Counting the stock -----
            if args['id_outlet'] != '' and args['id_outlet'] is not None:
                # Find all its recipe
                max_stock = []
                recipes = Recipe.query.filter_by(id_product = product['id'])
                if recipes.all() != []:
                    for recipe in recipes:
                        # Find related stock outlet
                        inventory_id = recipe.id_inventory
                        related_stock_outlet = StockOutlet.query.filter_by(id_outlet = args['id_outlet']).filter_by(id_inventory = inventory_id).first()
                        max_portion = 0
                        if related_stock_outlet is not None:
                            max_portion = int(related_stock_outlet.stock // recipe.amount)
                        max_stock.append(max_portion)
                    product['stock'] = min(max_stock)

            result.append(product)
        return result[::-1], 200

class CheckoutResource(Resource):
    # Enable CORS
    def options(self, id_cart=None):
        return {'status': 'ok'}, 200
    
    # Get all data needed to be shown in receipt
    @jwt_required
    @apps_required
    def get(self, id_cart):
        # Get user id
        claims = get_jwt_claims()
        if 'email' in claims:
            id_users = claims['id']
        else:
            id_users = claims['id']
        
        # Searching for specified cart
        specified_cart = Carts.query.filter_by(id = id_cart).filter_by(deleted = True).first()

        # Empty active cart
        if specified_cart is None:
            return {'message': 'Tidak ada transaksi aktif saat ini'}, 404
        
        # ---------- Prepare the receipt ----------
        # Get business logo
        owner = Users.query.filter_by(id = id_users).first()
        logo = owner.image
        business_name = owner.business_name

        # Get cashier name
        if specified_cart.id_employee == None:
            # Get owner name
            cashier_name = owner.fullname
        else:
            employee = Employees.query.filter_by(id = specified_cart.id_employee).first()
            cashier_name = employee.full_name
        
        # Get outlet information
        outlet = Outlets.query.filter_by(id = specified_cart.id_outlet).first()
        
        # Serach for all items in cart
        cart_detail = CartDetail.query.filter_by(id_cart = specified_cart.id)
        items_list = []
        transaction_total_price = 0
        for detail in cart_detail:
            # Get related product information
            product = Products.query.filter_by(id = detail.id_product).first()
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
            'business_name': business_name,
            'outlet_name': outlet.name,
            'address': outlet.address,
            'city': outlet.city,
            'phone_number': outlet.phone_number,
            'order': specified_cart.order_code,
            'customer_name': specified_cart.name,
            'time': specified_cart.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'cashier_name': cashier_name,
            'items_list': items_list,
            'transaction_total_price': transaction_total_price,
            'discount': specified_cart.total_discount,
            'tax': specified_cart.total_tax,
            'to_paid': transaction_total_price - specified_cart.total_discount + specified_cart.total_tax,
            'paid': specified_cart.paid_price,
            'payment_method': specified_cart.payment_method,
            'return': specified_cart.paid_price - (transaction_total_price - specified_cart.total_discount + specified_cart.total_tax)
        }
        return receipt, 200

class SendOrder(Resource):
    # Enable CORS
    def options(self, id=None):
        return {'status': 'ok'}, 200
    
    # Finalize order
    @jwt_required
    @apps_required
    def post(self):
        # Get owner ID
        claims = get_jwt_claims()
        if 'email' in claims:
            id_users = claims['id']
        else:
            id_users = claims['id']
        owner = Users.query.filter_by(id = id_users).first()

        # Check who is login (owner or cashier) and get related information
        id_employee = None
        if 'id_employee' in claims:
            id_employee = claims['id_employee']
            employee = Employees.query.filter_by(deleted = False).filter_by(id = id_employee).first()
        
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('id_outlet', location = 'json', required = True)
        parser.add_argument('id_customers', location = 'json', required = False)
        parser.add_argument('item_list', location = 'json', required = True, type = list)
        parser.add_argument('promo', location = 'json', required = False)
        parser.add_argument('payment_method', location = 'json', required = True)
        parser.add_argument('paid_price', location = 'json', required = True)
        parser.add_argument('name', location = 'json', required = False)
        parser.add_argument('phone', location = 'json', required = False)
        parser.add_argument('email', location = 'json', required = False)
        args = parser.parse_args()

        # Check emptyness
        if args['id_outlet'] == '' or args['id_outlet'] is None or args['payment_method'] == '' or args['payment_method'] is None or args['paid_price'] == '' or args['paid_price'] is None:
            return {'message': 'Tidak boleh ada field yang dikosongkan'}, 400

        # ---------- Create cart instance ----------
        # Seraching the outlet
        outlet = Outlets.query.filter_by(deleted = False).filter_by(id = args['id_outlet']).first()
        
        # Calculate some values
        total_item = 0
        total_payment = 0
        total_tax = 0
        for item in args['item_list']:
            total_item = total_item + int(item['unit'])
            total_item_price = int(item['unit']) * int(item['price'])
            total_payment = total_payment + total_item_price
            item_tax = (outlet.tax * total_item_price) // 100
            total_tax = total_tax + item_tax

        # Customer related
        if args['id_customers'] == '' or args['id_customers'] is None:
            id_customers = None
        else:
            id_customers = args['id_customers']
            # Edit customers
            customer = Customers.query.filter_by(id = id_customers).first()
            customer.total_transaction = customer.total_transaction + 1
            db.session.commit()
            
        # Validate some input
        if int(args['paid_price']) < total_payment or int(args['paid_price']) <= 0:
            return {'message': 'Ada kesalahan input'}, 422

        # Generate order code
        all_carts = Carts.query.filter_by(deleted = True).filter_by(id_users = id_users)
        unique_code = True
        while unique_code:
            # Generate code
            unique_code = False
            code_symbol = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890123456789'
            order_code = ''
            for index in range(6):
                random_number = random.randint(0, 36)
                order_code = order_code + code_symbol[random_number]

            # Uniqueness check
            for cart in all_carts:
                if cart.order_code == unique_code:
                    unique_code = True

        # Create the instance
        new_cart = Carts(
            id_users = id_users,
            id_outlet = args['id_outlet'],
            id_employee = id_employee,
            id_customers = id_customers,
            order_code = order_code,
            name = args['name'],
            payment_method = args['payment_method'],
            total_item = total_item,
            total_payment = total_payment,
            total_discount = 0,
            total_tax = total_tax,
            paid_price = args['paid_price']
        )
        db.session.add(new_cart)
        db.session.commit()

        # ---------- Create cart detail instance ----------
        cart_id = new_cart.id

        # Looping through items and create the instances
        for item in args['item_list']:
            new_cart_detail = CartDetail(
                id_cart = cart_id,
                id_product = item['id'],
                quantity = item['unit'],
                total_price_product = int(item['unit']) * int(item['price'])
            )
            db.session.add(new_cart_detail)
            db.session.commit()
            item['total_price_product'] = new_cart_detail.total_price_product
        
        # ---------- Edit inventory and stock outlet, and add inventory log ----------
        for item in args['item_list']:
            # Get inventory and stock outlet
            recipes = Recipe.query.filter_by(id_product = item['id'])
            for recipe in recipes:
                id_inventory = recipe.id_inventory
                inventory = Inventories.query.filter_by(id = id_inventory).filter_by(deleted = False).first()
                stock_outlet = StockOutlet.query.filter_by(id_outlet = args['id_outlet']).filter_by(id_inventory = id_inventory).first()
                stock_outlet.stock = stock_outlet.stock - (recipe.amount * int(item['unit']))
                inventory.total_stock = inventory.total_stock - (recipe.amount * int(item['unit']))
                inventory.updated_at = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d %H:%M:%S")
                new_log = InventoryLog(
                    id_stock_outlet = stock_outlet.id,
                    amount = recipe.amount * int(item['unit']),
                    status = 'Keluar',
                    last_stock = stock_outlet.stock
                )
                db.session.add(new_log)
                db.session.commit()
        
        # Prepare the data to be shown
        new_cart = marshal(new_cart, Carts.carts_fields)
        new_cart['item_list'] = args['item_list']
        result = {
            'id_order': new_cart['id'],
            'message': 'Transaksi berhasil'
        }
        return result, 200

class SendWhatsapp(Resource):
    # Enable CORS
    def options(self, id_product=None):
        return {'status': 'ok'}, 200
    
    # Send receipt to whatsapp
    @jwt_required
    @apps_required
    def post(self):
        # Take input from user
        parser = reqparse.RequestParser()
        parser.add_argument('image', location = 'json', required = True)
        parser.add_argument('id_cart', location = 'json', required = True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        id_users = claims['id']

        # Search user, transaction and related customer
        owner = Users.query.filter_by(id = id_users).first()
        transaction = Carts.query.filter_by(deleted = True).filter_by(id = args['id_cart']).first()
        customer = Customers.query.filter_by(id = transaction.id_customers).first()

        # Check customer
        if customer is None: return {'message': 'Data pelanggan tidak ditemukan'}, 404

        # Formatting phone
        customer_phone = customer.phone_number
        customer_phone = '+62' + customer_phone[1:]

        # Send the receipt
        account_sid = 'AC74c51f7d88218337455c1aba6fb8e45c'
        auth_token = '1612839a4c29ad63b826eb534be2ad0a'
        client = twilio_client(account_sid, auth_token)
        message = client.messages \
            .create(
                media_url = [args['image']],
                from_ = 'whatsapp:+14155238886',
                body = "Terima kasih atas kunjungannya. Berikut ini kami kirimkan struk transaksimu. Kami tunggu kedatanganmu kembali.",
                to = 'whatsapp:' + customer_phone
            )
        
        return {'message': 'Sukses mengirim struk transaksi'}, 200

class SendEmail(Resource):
    # Enable CORS
    def options(self, id_product=None):
        return {'status': 'ok'}, 200

    # Send receipt to email
    @jwt_required
    @apps_required
    def post(self):
        # Take input from user
        parser = reqparse.RequestParser()
        parser.add_argument('image', location = 'json', required = True)
        parser.add_argument('id_cart', location = 'json', required = True)
        args = parser.parse_args()
        claims = get_jwt_claims()
        id_users = claims['id']

        # Search user, transaction and related customer
        owner = Users.query.filter_by(id = id_users).first()
        transaction = Carts.query.filter_by(deleted = True).filter_by(id = args['id_cart']).first()
        customer = Customers.query.filter_by(id = transaction.id_customers).first()

        # Check email
        if customer is None: return {'message': 'Email tidak ditemukan'}, 404

        # ---------- Prepare the data needed ----------
        required_data = {
            'customer_email': customer.email,
            'customer_name': transaction.name,
            'owner_email': owner.email,
            'business_name': owner.business_name
        }

        # API configuration
        api_key = '2d98ebcc594d78589595e138f7f9d9c5'
        api_secret = 'fae993d3128a94fa5eb119c90afb5ece'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # Preparing the body of the email
        first_greeting = "<h3>Terima kasih atas kunjungannya. Berikut ini kami kirimkan struk transaksimu. Kami tunggu kedatanganmu kembali di " + required_data["business_name"] + "</h3>"
        receipt_image = '<br /><br /><img src="' + args['image'] + '" />'

        # Prepare the email to be sent
        data = {
        'Messages': [
            {
            "From": {
                "Email": "easykachin2020@gmail.com",
                "Name": required_data["business_name"]
            },
            "To": [
                {
                "Email": required_data["customer_email"],
                "Name": required_data["customer_name"]
                }
            ],
            "Subject": "Transaksi",
            "HTMLPart": first_greeting + receipt_image,
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        
        # Send the email
        if 'FLASK_ENV' not in os.environ: os.environ['FLASK_ENV'] = 'development'
        if os.environ['FLASK_ENV'] == 'development': mailjet.send.create(data=data)
        return {'message': 'Sukses mengirim struk transaksi'}, 200

api.add_resource(ProductResource, '')
api.add_resource(SpecificProductResource, '/<id_product>')
api.add_resource(CategoryResource, '/category')
api.add_resource(ItemsPerCategory, '/category/items')
api.add_resource(SendOrder, '/checkout')
api.add_resource(CheckoutResource, '/checkout/<id_cart>')
api.add_resource(SendWhatsapp, '/checkout/send-whatsapp')
api.add_resource(SendEmail, '/checkout/send-email')