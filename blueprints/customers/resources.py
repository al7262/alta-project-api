# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Customers
from blueprints import db, app, dashboard_required, apps_required
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_customers = Blueprint('customers', __name__)
api = Api(bp_customers)

class CustomerResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @dashboard_required
    # show outlet
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Customers.query.filter_by(id_users = claims['id'])      
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Customers.response_fields))
        return rows, 200

    @jwt_required
    @apps_required
    # edit outlet
    def put(self,id=None):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', location = 'json', required = True)
        parser.add_argument('phone_number', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)

        args = parser.parse_args()

        qry = Customers.query.filter_by(id_users = claims['id']).filter_by(id = id).first()

        if qry is None:
            return {'message' : "Not Found !!!"},404
        if args['fullname'] is not None:
            qry.fullname = args['fullname']
        if args['phone_number'] is not None:
            qry.phone_number = args['phone_number']
        if args['email'] is not None:
            qry.email = args['email']
            
        db.session.commit()
        return marshal(qry, Customers.response_fields), 200

#CRUD outlet POST (accessed by owner)
class CreateCustomerResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    # create product
    @jwt_required
    @apps_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', location = 'json', required = True)
        parser.add_argument('phone_number', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        
        args = parser.parse_args()
        
        customer = Customers(claims['id'], args['fullname'], args['phone_number'], args['email'])
        db.session.add(customer)
        db.session.commit()
        app.logger.debug('DEBUG : %s', customer)
        
        return {'message' : "add customer success !!!"},200,{'Content-Type': 'application/json'}

class SearchCustomer(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @apps_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('keyword', location = 'args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Customers.query.filter(Customers.fullname.like("%"+args["keyword"]+"%") | Customers.phone_number.like("%"+args["keyword"]+"%") | Customers.email.like("%"+args["keyword"]+"%"))
        
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Customers.response_fields))
        return rows, 200

class CustomerGetByOne(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @apps_required
    # showing product
    def get(self,id=None):
        claims = get_jwt_claims()
        qry = Customers.query.get(id)
        marshal_qry = (marshal(qry, Customers.response_fields))

        if qry is not None:
            return marshal_qry, 200
        return {'message' : 'NOT_FOUND'}, 404

api.add_resource(CustomerResource,'/customer','/customer/<int:id>')
api.add_resource(SearchCustomer,'/customer/search')
api.add_resource(CreateCustomerResource,'/customer/create')
api.add_resource(CustomerGetByOne,'/customer/get/<int:id>')