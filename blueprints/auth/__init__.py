from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.user.model import Users
from blueprints.seller.model import Sellers
import json , hashlib

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
        
    def options(self,id=None):
        return{'status':'ok'} , 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'args', required = True)
        parser.add_argument('password', location = 'args', required = True)

        args = parser.parse_args()

        if args['username'] == 'admin' and args['password'] == 'admin':
            token = create_access_token(identity = args['username'], user_claims = ({"id": 0, "username": "admin", "isinternal" : True}))
            return {'token' : token}, 200
        
        encrypted = hashlib.md5(args['password'].encode()).hexdigest()
        qry_user = Users.query.filter_by(username = args['username']).filter_by(password = encrypted)
        qry_seller = Sellers.query.filter_by(username = args['username']).filter_by(password = encrypted)
        userData = qry_user.first()
        sellerData = qry_seller.first()

        if userData is not None:
            userData = marshal(userData,Users.jwt_claims_fields)
            if userData['deleted']==False:
                userData['isinternal'] = False
                token = create_access_token(identity = userData['username'], user_claims = userData)
            return {'token' : token}, 200

        if sellerData is not None:
            sellerData = marshal(sellerData,Users.jwt_claims_fields)
            if sellerData['deleted']==False:
                sellerData['isinternal'] = False
                token = create_access_token(identity = sellerData['username'], user_claims = sellerData)
            return {'token' : token}, 200
        return{'status' : 'UNATUTHORIZED' , 'message' : 'invalid username or password'}, 401
    
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        return {'claims' : claims}, 200

class RefressTokenResources(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200
    
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token' : token}, 200
        
api.add_resource(CreateTokenResource,'/login')
api.add_resource(RefressTokenResources,'/refresh')