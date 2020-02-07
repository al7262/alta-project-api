from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.users.model import Users
from blueprints.outlets.model import Outlets
from blueprints.employees.model import Employees
import json , hashlib

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

class LoginApps(Resource):
        
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
        userData = qry_user.first()
        employeeData = qry_employee.first()
        tes_employee = Employees.query

        if userData is not None:
            userData = marshal(userData,Users.jwt_claims_fields)
            token = create_access_token(identity = userData['email'], user_claims = userData)
            return {'token' : token}, 200

        if employeeData is not None:
            employeeData = marshal(employeeData,Employees.jwt_claim_fields)
            
            if employeeData['deleted']==False:
            # Get ID users
                if employeeData['position'] == 'Kasir':
                    qry_employee = qry_employee.first()
                    outlet = Outlets.query.filter_by(deleted = False).filter_by(id = qry_employee.id_outlet).first()
                    id_user = outlet.id_user
                    employeeData['id_employee'] = employeeData['id']
                    employeeData['id'] = id_user

                    token = create_access_token(identity = employeeData['username'], user_claims = employeeData)
                    return {'token' : token}, 200
            
        return{'status' : 'UNATUTHORIZED' , 'message' : 'Username atau Password Tidak Valid'}, 401
    
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims' : claims}, 200

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
        userData = qry_user.first()
        employeeData = qry_employee.first()

        if userData is not None:
            userData = marshal(userData,Users.jwt_claims_fields)
            token = create_access_token(identity = userData['email'], user_claims = userData)
            return {'token' : token}, 200

        if employeeData is not None:
            employeeData = marshal(employeeData,Employees.jwt_claim_fields)
            
            if employeeData['deleted']==False:
                if employeeData['position']=='Admin':
                    qry_employee = qry_employee.first()
                    outlet = Outlets.query.filter_by(deleted = False).filter_by(id = qry_employee.id_outlet).first()
                    id_user = outlet.id_user
                    employeeData['id_employee'] = employeeData['id']
                    employeeData['id'] = id_user

                    token = create_access_token(identity = employeeData['username'], user_claims = employeeData)
                    return {'token' : token}, 200
            
        return{'status' : 'UNATUTHORIZED' , 'message' : 'Username atau Password Tidak Valid'}, 401
    
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims' : claims}, 200
        
api.add_resource(LoginApps,'/login/apps')
api.add_resource(LoginDashboard,'/login/dashboard')