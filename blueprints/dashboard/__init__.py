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

class Dashboard(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @dashboard_required
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name_outlet', location = 'args')
        parser.add_argument('start_time', location = 'args')
        parser.add_argument('end_time', location = 'args')
        parser.add_argument('date_interval', location = 'args')
        parser.add_argument('month', location = 'args')

        args = parser.parse_args()
        time = datetime.now().strftime("%Y-%m-%d")
        today = datetime(int(time[0:4]),int(time[5:7]),int(time[8::]))
        start = today
        end = today + relativedelta(days = +1)
        if args['date_interval'] is not None:
            if args['date_interval'] == "Hari ini":
                start = today
                end = today + relativedelta(days = +1)
            elif args['date_interval'] == "Kemarin":
                start = today + relativedelta(days = -1)
                end = today
            elif args['date_interval'] == "Minggu ini":
                start = today + relativedelta(days = -7)
                end = today + relativedelta(days = +1)
            elif args['date_interval'] == "Bulan ini":
                start = today + relativedelta(days = -(int(time[8::]))+1)
                end = today + relativedelta(days = +1)
            elif args['date_interval'] == "Bulan lalu":
                start = today + relativedelta(months= -1, days = -(int(time[8::]))+1)
                end = today + relativedelta(days = -(int(time[8::]))+1)
        elif args['start_time'] is not None and args['end_time'] is not None:
            start_time = args['start_time']
            start = datetime(int(start_time[0:4]),int(start_time[5:7]),int(start_time[8::]))
            end_time = args['end_time']
            end = datetime(int(end_time[0:4]),int(end_time[5:7]),int(end_time[8::]))
            end = end + relativedelta(days = +1)
            if end <= start :
                return {"massage" : "inputan anda salah"}, 401

        # variabel untuk jumlah pemasukan
        number_transaction = 0

        # variabel untuk jumlah pemasukan
        sales_amount = 0

        # variabel untuk produk terlaris
        total_quantity = 0
        list_product = []
        info_product = {}
        info_products = []

        # variabel untuk kategori terlaris
        categories = []
        list_category = []
        info_category = {}
        info_categories = []
        info_another = {}

        # variable untuk produk terlaris dan kategori terlaris
        tops = []
        top_product = []
        top_category = []
        
        # ini untuk jumlah penjualan dan jumlah pemasukkan
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
            
            # ini untuk produk terlaris
            qry_product = Products.query.filter_by(id_users = claims['id']).all()
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
                    info_product = {
                        "id" : product.id,
                        "name" : product.name,
                        "total" : total_quantity
                    }
                    info_products.append(info_product)
            list_product.sort(reverse = True)
            if len(list_product) < 5:
                tops = list_product[0::].copy()
            else:
                tops = list_product[0:5].copy()
            for top in tops:
                for info in info_products:
                    if info['total'] == top:
                        if info not in top_product:
                            top_product.append(info)
                            break
    
            # ini untuk kategori terlaris
            total_quantity = 0
            for product in qry_product:
                if qry_cart is not None:
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                            if qry_cartdetail is not None:
                                total_quantity = total_quantity + qry_cartdetail.quantity
            info_another = {
                "category_product" : "another",
                "total" : total_quantity
            }               
            for category in categories:
                qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(category = category).all()
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
                info_category = {
                    "category_product" : category,
                    "total" : total_quantity
                }
                info_categories.append(info_category)
            list_category.sort(reverse = True)
            if len(list_category) < 5 :
                tops = list_category[0::].copy()
            else:
                tops = list_category[0:5].copy()
            for top in tops:
                for info in info_categories:
                    if info['total'] == top:
                        if info not in top_category:
                            top_category.append(info)
                            break
            top_category = top_category + info_another

            # ini untuk pengingat stock
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
                        outlet = Outlets.query.filter_by(deleted = False).filter_by(id = stock_outlet['id_outlet']).first()
                        if outlet is not None:
                            outlet_name = outlet.name

                            data = {
                            'name': inventory_name,
                            'stock': stock_outlet['stock'],
                            'outlet': outlet_name
                            }
                            inventories_data.append(data)
             
        elif args['name_outlet'] is not None:
            qry_outlet = Outlets.query.filter_by(id_user = claims['id']).filter_by(name = args['name_outlet']).first()
            qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_outlet = qry_outlet.id).all()
            if qry_cart is not None:
                for cart in qry_cart:
                    create_at = cart.created_at
                    if start <= create_at and create_at <= end:
                        sales_amount = sales_amount + cart.total_payment
                        number_transaction = number_transaction + 1
                
            # ini untuk produk terlaris
            qry_product = Products.query.filter_by(id_users = claims['id']).all()
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
                    info_product = {
                        "id" : product.id,
                        "nama_product" : product.name, 
                        "total" : total_quantity
                    }
                    info_products.append(info_product)
            list_product.sort(reverse = True)
            if len(list_product) < 5 :
                tops = list_product[0::].copy()
            else:
                tops = list_product[0:5].copy()
            for top in tops:
                for info in info_products:
                    if info['total'] == top:
                        if info not in top_product:
                            top_product.append(info)
                            break
            
            # ini untuk kategori terlaris
            total_quantity = 0
            for product in qry_product:
                if qry_cart is not None:
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            qry_cartdetail = CartDetail.query.filter_by(id_cart = cart.id).filter_by(id_product = product.id).first()
                            if qry_cartdetail is not None:
                                total_quantity = total_quantity + qry_cartdetail.quantity
            info_another = {
                "category_product" : "another",
                "total" : total_quantity
            }
            for category in categories: 
                qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(category = category).all()
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
                info_category = {
                    "category_product" : category,
                    "total" : total_quantity
                }
                info_categories.append(info_category)
            list_category.sort(reverse = True)
            if len(list_category) < 5 :
                tops = list_category[0::].copy()
            else:
                tops = list_category[0:5].copy()
            for top in tops:
                for info in info_categories:
                    if info['total'] == top:
                        if info not in top_category:
                            top_category.append(info)
                            break
            top_category = top_category + info_another
            
            #ini untuk pengingat stock
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

                        data = {
                            'name': inventory_name,
                            'stock': stock_outlet['stock'],
                            'outlet': outlet_name
                        }
                        inventories_data.append(data)


        # Ini untuk grafik
        chart = []
        if args['month'] is not None:
            month = int(args['month'])
        if args['month'] is None:
            month = 0
        now_month = int(time[5:7])
        end = today + relativedelta(months = (month)+1, days = -(int(time[8::]))+1)
        qry_outlet = Outlets.query.filter_by(id_user = claims['id']).all()
        start = today + relativedelta(months = (month), days = -(int(time[8::]))+1)
        while start < end: 
            amount_sales = 0
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
            chart.append(amount_sales)
            start = start + relativedelta(days = +1)

        #ini untuk member loyal
        min = 0
        new_customer = 0
        total_costumer = 0
        qry = Customers.query.filter_by(id_users = claims['id']) 
        time = datetime.now().strftime("%Y-%m-%d")
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

api.add_resource(Dashboard,'/dashboard')