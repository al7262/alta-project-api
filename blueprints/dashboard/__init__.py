# import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints.employees.model import Employees
from blueprints.outlets.model import Outlets
from blueprints.carts.model import Carts, CartDetail
from blueprints.products.model import Products
from blueprints.stock_outlet.model import StockOutlet
from blueprints.inventories.model import Inventories
from blueprints.customers.model import Customers 
from blueprints import db, app, user_required, dashboard_required
from datetime import datetime, timedelta, date
from dateutil.relativedelta import *
import json, hashlib

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_dashboard = Blueprint('dashboard', __name__)
api = Api(bp_dashboard)

# CRUD dashboard options (CORS), get
class Dashboard(Resource):

    # Enable CORS
    def options(self,id=None):
        return{'status':'ok'} , 200

    # Get all information needed to be shown in the dashboard
    @jwt_required
    @dashboard_required
    def get(self):
        # Tak input from users
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name_outlet', location = 'args')
        parser.add_argument('start_time', location = 'args')
        parser.add_argument('end_time', location = 'args')
        args = parser.parse_args()

        # Datetime related
        time = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d")
        if args['start_time'] == "" and args['end_time'] == "":
            today = datetime(int(time[0:4]),int(time[5:7]),int(time[8::]))
            start = today
            end = today + relativedelta(days = +1)
        if args['start_time'] is not None and args['end_time'] is not None and  args['start_time'] != "" and args['end_time'] != "":
            start_time = args['start_time']
            start = datetime(int(start_time[6::]),int(start_time[3:5]),int(start_time[0:2]))
            end_time = args['end_time']
            end = datetime(int(end_time[6::]),int(end_time[3:5]),int(end_time[0:2]))
            end = end + relativedelta(days = +1)
            if end <= start :
                return {"message" : "Inputan Anda salah"}, 400
        
        # ---------- Setting some variables needed ----------
        number_transaction = 0
        sales_amount = 0
        total_quantity = 0
        list_product = []
        info_products = []

        # Popular Category and Products
        categories = []
        list_category = []
        info_categories = []
        another = []
        total = []
        tops = []
        top_product = []
        top_category = []
        count_category = 0
        
        #-------------------------------- without args name outlet --------------------------------

        # Calculate total items and total sales
        if args['name_outlet'] is None or args['name_outlet'] == "":
            qry_outlet = Outlets.query.filter_by(id_user = claims['id']).all()
            for outlet in qry_outlet:
                qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = outlet.id).all()
                if qry_cart is not None:
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            sales_amount = sales_amount + cart.total_payment
                            number_transaction = number_transaction + 1
            
            # For popular products
            qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(deleted = False).all()
            for product in qry_product:
                if product.category not in categories:
                    categories.append(product.category)

            qry_cart = Carts.query.filter_by(id_users = claims['id']).all()
            for product in qry_product:
                total_quantity = 0
                if qry_cart is not None:
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                            if qry_cartdetail is not None:
                                total_quantity = total_quantity + qry_cartdetail.quantity
                    list_product.append(total_quantity)
                    info_products.append([product.name,total_quantity])
            list_product.sort(reverse = True)
            if len(list_product) < 5:
                tops = list_product[0::].copy()
            else:
                tops = list_product[0:5].copy()
            for top in tops:
                for info in info_products:
                    if info[1] == top:
                        if info not in top_product:
                            top_product.append(info)
                            break
    
            # For popular categories
            total_quantity = 0
            for product in qry_product:
                if qry_cart is not None:
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                            if qry_cartdetail is not None:
                                total_quantity = total_quantity + qry_cartdetail.quantity
            total = ["total",total_quantity]
            for category in categories:
                qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(category = category).filter_by(deleted = False).all()
                total_quantity = 0
                for product in qry_product:
                    if qry_cart is not None:
                        for cart in qry_cart:
                            create_at = cart.created_at
                            if start <= create_at and create_at <= end:
                                qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                                if qry_cartdetail is not None:
                                    total_quantity = total_quantity + qry_cartdetail.quantity
                list_category.append(total_quantity)
                info_categories.append([category,total_quantity])
            list_category.sort(reverse = True)
            if len(list_category) < 5 :
                tops = list_category[0::].copy()
            else:
                tops = list_category[0:5].copy()
            for top in tops:
                for info in info_categories:
                    if info[1] == top:
                        if info not in top_category:
                            top_category.append(info)
                            break
            for datum in range(len(top_category)):
                count_category = count_category + top_category[datum][1]
            count_category = total[1] - count_category 
            another = ["Lainnya", count_category]
            top_category.append(another)

            # for stock reminders
            inventories = Inventories.query.filter_by(id_users = claims['id']).filter_by(deleted = False).all()
            stock_outlet_list = []
            if inventories is not None:
                for inventory in inventories:
                    inventory_id = inventory.id
                    related_stock_outlet = StockOutlet.query.filter_by(id_inventory = inventory_id).all()
                    for stock_outlet in related_stock_outlet:
                        stock_outlet_list.append(stock_outlet)
            stock_outlet_filtered = filter(lambda stock_outlet: stock_outlet.stock <= stock_outlet.reminder, stock_outlet_list)
            if stock_outlet_filtered is not None:
                inventories_data = []
                for stock_outlet in stock_outlet_filtered:
                    stock_outlet = marshal(stock_outlet, StockOutlet.response_fields)
                    id_inventory = stock_outlet['id_inventory']
                    inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()
                    if inventory is not None:
                        inventory_name = inventory.name
                        inventory_unit = inventory.unit
                        outlet = Outlets.query.filter_by(deleted = False).filter_by(id = stock_outlet['id_outlet']).first()
                        if outlet is not None:
                            outlet_name = outlet.name
                            
                            data = {
                            'name': inventory_name,
                            'stock': stock_outlet['stock'],
                            'outlet': outlet_name,
                            'unit' : inventory_unit
                            }
                            inventories_data.append(data)
             
        
        #-------------------------------- with args name outlet --------------------------------
        # Calculate total items and total sales
        elif args['name_outlet'] is not None:
            qry_outlet = Outlets.query.filter_by(id_user = claims['id']).filter_by(name = args['name_outlet']).first()
            qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = qry_outlet.id).all()
            if qry_cart is not None:
                for cart in qry_cart:
                    create_at = cart.created_at
                    if start <= create_at and create_at <= end:
                        sales_amount = sales_amount + cart.total_payment
                        number_transaction = number_transaction + 1
                
            # For popular products
            qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(deleted = False).all()
            for product in qry_product:
                if product.category not in categories:
                    categories.append(product.category)
            qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = qry_outlet.id).all()
            if qry_cart is not None:
                for product in qry_product:
                    total_quantity = 0
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                            if qry_cartdetail is not None:
                                total_quantity = total_quantity + qry_cartdetail.total_price_product
                    list_product.append(total_quantity)
                    info_products.append([product.name,total_quantity])
            list_product.sort(reverse = True)
            if len(list_product) < 5 :
                tops = list_product[0::].copy()
            else:
                tops = list_product[0:5].copy()
            for top in tops:
                for info in info_products:
                    if info[1] == top:
                        if info not in top_product:
                            top_product.append(info)
                            break
            
            # For popular categories
            total_quantity = 0
            for product in qry_product:
                if qry_cart is not None:
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                            if qry_cartdetail is not None:
                                total_quantity = total_quantity + qry_cartdetail.quantity
            total = ["total",total_quantity]
            for category in categories: 
                qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(category = category).filter_by(deleted = False).all()
                total_quantity = 0
                for product in qry_product:
                    if qry_cart is not None:
                        for cart in qry_cart:
                            create_at = cart.created_at
                            if start <= create_at and create_at <= end:
                                qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                                if qry_cartdetail is not None:
                                    total_quantity = total_quantity + qry_cartdetail.quantity
                list_category.append(total_quantity)
                info_categories.append([category,total_quantity])
            list_category.sort(reverse = True)
            if len(list_category) < 5 :
                tops = list_category[0::].copy()
            else:
                tops = list_category[0:5].copy()
            for top in tops:
                for info in info_categories:
                    if info[1] == top:
                        if info not in top_category:
                            top_category.append(info)
                            break
            for datum in range(len(top_category)):
                count_category = count_category + top_category[datum][1]
            count_category = total[1] - count_category 
            another = ["Lainnya", count_category]
            top_category.append(another)
            
            # for stock reminders
            stock_outlet_list = StockOutlet.query.filter_by(id_outlet = qry_outlet.id)
            stock_outlet_filtered = filter(lambda stock_outlet: stock_outlet.stock <= stock_outlet.reminder, stock_outlet_list)
            if stock_outlet_filtered is not None:
                outlet_name = qry_outlet.name
                   
                inventories_data = []
                for stock_outlet in stock_outlet_filtered:
                    stock_outlet = marshal(stock_outlet, StockOutlet.response_fields)

                    id_inventory = stock_outlet['id_inventory']
                    inventory = Inventories.query.filter_by(deleted = False).filter_by(id = id_inventory).first()
                    if inventory is not None:
                        inventory_name = inventory.name
                        inventory_unit = inventory.unit

                        data = {
                            'name': inventory_name,
                            'stock': stock_outlet['stock'],
                            'outlet': outlet_name,
                            'unit' : inventory_unit
                        }
                        inventories_data.append(data)

        # for create chart
        chart = {}
        if args['name_outlet'] is not None and args['name_outlet'] != "":
            qry_outlet = Outlets.query.filter_by(id_user = claims['id']).filter_by(name = args['name_outlet']).filter_by(deleted = False).first()
        if qry_outlet is None or args['name_outlet'] == "":
            qry_outlet = Outlets.query.filter_by(id_user = claims['id']).filter_by(deleted = False).all()
        count = 0
        limit = start + relativedelta(days = +1)
        if limit == end:
            while start < end: 
                amount_sales = 0
                if args['name_outlet'] is not None and args['name_outlet'] != "":
                    qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = qry_outlet.id).all()
                    if qry_cart is not None:
                        for carts in qry_cart:
                            create_at = carts.created_at
                            interval = start + relativedelta(hours = +1)
                            if start <= create_at and create_at <= interval:
                                amount_sales = amount_sales + carts.total_payment
                    if qry_cart is None:
                        amount_sales = amount_sales + 0
                    chart[str(count)] = amount_sales
                    start = start + relativedelta(hours = +1)
                    count+=1
                if args['name_outlet'] is None or args['name_outlet'] == "":
                    for outlet in qry_outlet:
                        qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = outlet.id).all()
                        if qry_cart is not None:
                            for carts in qry_cart:
                                create_at = carts.created_at
                                interval = start + relativedelta(hours = +1)
                                if start <= create_at and create_at <= interval:
                                    amount_sales = amount_sales + carts.total_payment
                        if qry_cart is None:
                            amount_sales = amount_sales + 0
                    chart[str(count)] = amount_sales
                    start = start + relativedelta(hours = +1)
                    count+=1

        if limit != end:
            while start < end: 
                amount_sales = 0
                if args['name_outlet'] is not None and args['name_outlet'] != "":
                    qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = qry_outlet.id).all()
                    if qry_cart is not None:
                        for carts in qry_cart:
                            create_at = carts.created_at
                            interval = start + relativedelta(days = +1)
                            if start <= create_at and create_at <= interval:
                                amount_sales = amount_sales + carts.total_payment
                    if qry_cart is None:
                        amount_sales = amount_sales + 0
                    the_time = str(start)
                    my_time = the_time[0:10]
                    chart[str(my_time)] = amount_sales
                    start = start + relativedelta(days = +1)
                    count+=1
                if args['name_outlet'] is None or args['name_outlet'] == "":
                    for outlet in qry_outlet:
                        qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = outlet.id).all()
                        if qry_cart is not None:
                            for carts in qry_cart:
                                create_at = carts.created_at
                                interval = start + relativedelta(days = +1)
                                if start <= create_at and create_at <= interval:
                                    amount_sales = amount_sales + carts.total_payment
                        if qry_cart is None:
                            amount_sales = amount_sales + 0
                    the_time = str(start)
                    my_time = the_time[0:10]
                    chart[str(my_time)] = amount_sales
                    start = start + relativedelta(days = +1)
                    count+=1
            
        # for loyal members
        min = 0
        new_customer = 0
        total_costumer = 0
        qry = Customers.query.filter_by(id_users = claims['id']) 
        time = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d")
        today = datetime(int(time[0:4]),int(time[5:7]),int(time[8::]))
        start = today + relativedelta(days = -(int(time[8::]))+1)
        end = today + relativedelta(days = +1)
        for costumer in qry:
            total_costumer = total_costumer + 1
        for costumer in qry:
            create_at = costumer.created_at
            if start <= create_at and create_at <= end:
                new_customer = new_customer + 1

        result = {
            "sales_amount" : sales_amount,
            "number_transaction" : number_transaction,
            "chart" : chart,
            "top_product" : top_product,
            "top_category" : top_category,
            "new_customer" : new_customer,
            "total_costumer" : total_costumer,
            'below_reminder': len(inventories_data),
            'reminder': inventories_data
        }
        return result, 200

# endpoint in Dashboard
api.add_resource(Dashboard,'/dashboard')