from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints.employees.model import Employees
from blueprints.outlets.model import Outlets
from blueprints.carts.model import Carts
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
        number_transaction = 0
        sales_amount = 0
        row = []
        if args['name_outlet'] is None or args['name_outlet'] == "":
            qry_outlet = Outlets.query.filter_by(id_user = claims['id']).all()
            for outlet in qry_outlet:
                qry_employee = Employees.query.filter_by(id_outlet = outlet.id).all()
                for employee in qry_employee:
                    qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_employee = employee.id).all()
                    if qry_cart is not None:
                        for cart in qry_cart:
                            create_at = cart.created_at
                            if start <= create_at and create_at <= end:
                                row.append(marshal(cart, Carts.carts_fields))
                                sales_amount = sales_amount + cart.total_payment
                                number_transaction = number_transaction + 1

        elif args['name_outlet'] is not None:
            qry_outlet = Outlets.query.filter_by(id_user = claims['id']).filter_by(name = args['name_outlet']).first()
            qry_employee = Employees.query.filter_by(id_outlet = qry_outlet.id).all()
            for employee in qry_employee:
                qry_cart = Carts.query.filter_by(id_users = claims['id']).filter_by(id_employee = employee.id).all()
                if qry_cart is not None:
                    for cart in qry_cart:
                        create_at = cart.created_at
                        if start <= create_at and create_at <= end:
                            row.append(marshal(cart, Carts.carts_fields))
                            sales_amount = sales_amount + cart.total_payment
                            number_transaction = number_transaction + 1
        
        result = {
            "sales_amount" : sales_amount,
            "number_transaction" : number_transaction,
            "start" : str(start),
            "end" : str(end)
        }
        return result, 200
api.add_resource(Dashboard,'/dashboard')