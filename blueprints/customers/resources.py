# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Customers
from blueprints import db, app, dashboard_required, apps_required
from datetime import datetime, timedelta, date
from dateutil.relativedelta import *
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_customers = Blueprint('customers', __name__)
api = Api(bp_customers)

# CRUD customer options (CORS), get, put, delete
class CustomerResource(Resource):
    
    # Enable CORS
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    # Get all customers
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 125)
        parser.add_argument('keyword', location = 'args')

        # Pagination
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
            
        # Get all customers and sort it from the newest
        qry = Customers.query.filter_by(id_users = claims['id'])
        qry = qry.order_by(desc(Customers.created_at))

        if args['keyword'] is not None and args['keyword'] != '':
            qry = qry.filter_by(id_users = claims['id']).filter(Customers.fullname.like("%"+args["keyword"]+"%") | Customers.phone_number.like("%"+args["keyword"]+"%") | Customers.email.like("%"+args["keyword"]+"%"))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Customers.response_fields))
        
        # variable
        min = 0
        new_customer = 0
        total_costumer = 0
        custumer_id = ''

        # setting time
        time = (datetime.now() + timedelta(hours = 7)).strftime("%Y-%m-%d")
        today = datetime(int(time[0:4]),int(time[5:7]),int(time[8::]))
        start = today + relativedelta(days = -(int(time[8::]))+1)
        end = today + relativedelta(days = +1)
        qry_grand_customers = Customers.query.all()
        for costumer in qry_grand_customers:
            total_costumer = total_costumer + 1
            if costumer.total_transaction > min:
                min = costumer.total_transaction
                custumer_id = costumer.id
        for costumer in qry_grand_customers:
            create_at = costumer.created_at
            if start <= create_at and create_at <= end:
                new_customer = new_customer + 1

        # Case when loyal customer exists
        if custumer_id != '':   
            qry_costumer_loyal = Customers.query.get(custumer_id)
            custumer_loyal = marshal(qry_costumer_loyal, Customers.response_fields)
            result = {
                "list_all_customer" : rows,
                "total_costumer" : total_costumer,
                "costumer_loyal" : custumer_loyal,
                "new_customer" : new_customer
            }

        # Case when there are no customer have made transaction        
        else:
            result = {
                "list_all_customer" : rows,
                "total_costumer" : total_costumer,
                "costumer_loyal" : "Belum ada pelanggan yang melakukan transaksi",
                "new_customer" : new_customer
            }
        return result, 200

    @jwt_required
    # Delete a customer
    def delete(self, id=None):
        # Get customer and delete it
        customer = Customers.query.filter_by(id = id).first()
        db.session.delete(customer)
        db.session.commit()

        return {'message': 'Sukses menghapus pelanggan'}, 200

    @jwt_required
    @apps_required
    # Edit customers
    def put(self,id=None):
        # Take input from users
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', location = 'json', required = True)
        parser.add_argument('phone_number', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        args = parser.parse_args()

        qry = Customers.query.get(id)

        if qry is None:
            return {'message' : "Data pelanggan yang Anda cari tidak ditemukan"}, 404
        if args['fullname'] is None or args['fullname'] == '':
            return {'message': 'Data pada kolom nama lengkap harus isi'}, 400

        # Filter
        qry.fullname = args['fullname']
        if args['phone_number'] is not None:
            qry.phone_number = args['phone_number']
        if args['email'] is not None:
            qry.email = args['email']
            
        db.session.commit()
        return marshal(qry, Customers.response_fields), 200

#CRUD customer POST (accessed by owner)
class CreateCustomerResource(Resource):
    
    # Enable CORS
    def options(self,id=None):
        return{'status':'ok'} , 200

    # Add new customer
    @jwt_required
    @apps_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', location = 'json', required = True)
        parser.add_argument('phone_number', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        
        args = parser.parse_args()
        
        if args['fullname'] == '' or args['fullname'] is None:
            return {'message': 'Kolom nama tidak boleh dikosongkan'}, 400
        
        # Check for duplicate
        qry = Customers.query.filter_by(id_users = claims['id']).filter_by(fullname = args['fullname'])
        if args['phone_number'] is not None:
            qry = qry.filter_by(phone_number = args['phone_number'])
        if args['email'] is not None:
            qry = qry.filter_by(email = args['email'])
        
        if qry.all() == []:
            customer = Customers(claims['id'], args['fullname'], args['phone_number'], args['email'])
            db.session.add(customer)
            db.session.commit()
            app.logger.debug('DEBUG : %s', customer)
            
            return {'message' : "Masukkan pelanggan berhasil", "id" : customer.id}, 200, {'Content-Type': 'application/json'}
        return {'message' : "Masukkan pelanggan gagal"}, 409

# CRUD customer options (CORS), get
class CustomerGetByOne(Resource):
        
    # Enable CORS
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @apps_required
    # Get customer by ID
    def get(self,id=None):
        qry = Customers.query.get(id)
        marshal_qry = (marshal(qry, Customers.response_fields))

        if qry is not None:
            return marshal_qry, 200
        return {'message' : 'Data Tidak Ditemukan'}, 404

# endpoint in Customer
api.add_resource(CustomerResource,'/customer','/customer/<int:id>')
api.add_resource(CreateCustomerResource,'/customer/create')
api.add_resource(CustomerGetByOne,'/customer/get/<int:id>')