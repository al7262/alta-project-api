#import
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.users.model import Users
from blueprints.outlets.model import Outlets
from blueprints.employees.model import Employees
import json , hashlib

# Creating blueprint
bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

# CRUD options (CORS), post, get
class LoginApps(Resource):
    
    # Enable CORS
    def options(self,id=None):
        return{'status':'ok'} , 200

    # Login to apps
    def post(self):
        # Take input from users
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()

        # Encrypt password
        encrypted = hashlib.md5(args['password'].encode()).hexdigest()
        
        # Find who is login
        qry_user = Users.query.filter_by(email = args['username']).filter_by(password = encrypted)
        qry_employee = Employees.query.filter_by(username = args['username']).filter_by(password = encrypted)
        user_data = qry_user.first()
        employee_data = qry_employee.first()

        # Handle case when owner login
        if user_data is not None:
            user_data = marshal(user_data,Users.jwt_claims_fields)
            token = create_access_token(identity = user_data['email'], user_claims = user_data)
            return {'token' : token}, 200

        # Handle case when employee login
        if employee_data is not None:
            employee_data = marshal(employee_data,Employees.jwt_claim_fields)
            
            if employee_data['deleted'] == False:
            # Get ID users
                if employee_data['position'] == 'Kasir':
                    qry_employee = qry_employee.first()
                    outlet = Outlets.query.filter_by(deleted = False).filter_by(id = qry_employee.id_outlet).first()
                    id_user = outlet.id_user
                    employee_data['id_employee'] = employee_data['id']
                    employee_data['id'] = id_user

                    token = create_access_token(identity = employee_data['username'], user_claims = employee_data)
                    return {'token' : token}, 200
            
        return{'status' : 'UNATUTHORIZED' , 'message' : 'Username atau Password Tidak Valid'}, 401
    
    # display the contents
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims' : claims}, 200

# CRUD options (CORS), post, get
class LoginDashboard(Resource):
    def options(self,id=None):
        return{'status':'ok'} , 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)

        args = parser.parse_args()
        
        encrypted = hashlib.md5(args['password'].encode()).hexdigest()
        qry_user = Users.query.filter_by(email = args['username']).filter_by(password = encrypted)
        qry_employee = Employees.query.filter_by(username = args['username']).filter_by(password = encrypted)
        user_data = qry_user.first()
        employee_data = qry_employee.first()

        if user_data is not None:
            user_data = marshal(user_data,Users.jwt_claims_fields)
            post_register = False
            if 'fulname' not in user_data: post_register = True
            token = create_access_token(identity = user_data['email'], user_claims = user_data)
            return {'token' : token, 'post_register': post_register}, 200

        if employee_data is not None:
            employee_data = marshal(employee_data,Employees.jwt_claim_fields)
            
            if employee_data['deleted']==False:
                if employee_data['position']=='Admin':
                    qry_employee = qry_employee.first()
                    outlet = Outlets.query.filter_by(deleted = False).filter_by(id = qry_employee.id_outlet).first()
                    id_user = outlet.id_user
                    employee_data['id_employee'] = employee_data['id']
                    employee_data['id'] = id_user

                    token = create_access_token(identity = employee_data['username'], user_claims = employee_data)
                    return {'token' : token, 'post_register': False}, 200
            
        return{'status' : 'UNATUTHORIZED' , 'message' : 'Username atau Password Tidak Valid'}, 401
    
    # display the contents
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims' : claims}, 200

# endpoint in Auth
api.add_resource(LoginApps,'/login/apps')
api.add_resource(LoginDashboard,'/login/dashboard')