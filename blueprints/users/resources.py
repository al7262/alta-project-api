# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Users
from blueprints import db, app, user_required
from datetime import datetime
from password_strength import PasswordPolicy
import json,hashlib

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
Bp_user = Blueprint('user',__name__)
api = Api(Bp_user)

class RegisterUserResource(Resource):
    #enalble CORS
    def options(self,id=None):
        return{'status':'ok'} , 200

    # to keep the password secret
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    # create user account
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()
        
        qry = Users.query.filter_by(email = args['email']).first()
        if qry is None:
            validation = self.policy.test(args['password'])
            if validation:
                errorList = []
                for item in validation:
                    split = str(item).split('(')
                    error, num = split[0], split[1][0]
                    errorList.append("{err}(minimum {num})".format(err=error, num=num))
                message = "Please check your passwword: " + ', '.join(x for x in errorList)
                return {'message': message}, 422, {'Content-Type': 'application/json'}
            encrypted = hashlib.md5(args['password'].encode()).hexdigest()

            user = Users(args['email'], encrypted)
            db.session.add(user)
            db.session.commit()
            app.logger.debug('DEBUG : %s', user)
            
            return {'message' : "Registrasi Berhasil"},200,{'Content-Type': 'application/json'}
        return {'message' : "Registrasi Gagal"},401

class UserResource(Resource):
    # Enable CORS    
    def options(self,id=None):
        return {'status':'ok'} , 200
        
    # To keep the password secret
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    # Showing user profile (himself)
    @jwt_required
    @user_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        return marshal(qry, Users.response_fields), 200

    @jwt_required
    @user_required
    def put(self):
        # Take input from user
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        parser = reqparse.RequestParser()

        parser.add_argument('fullname', location = 'json')
        parser.add_argument('password', location = 'json')
        parser.add_argument('phone_number', location = 'json')
        parser.add_argument('business_name', location = 'json')
        parser.add_argument('image', location = 'json')

        args = parser.parse_args()

        # Check emptyness
        if args['fullname'] == '' or args['password'] == '' or args['phone_number'] == '' or args['business_name'] == '' or args['image'] == '' or 'fullname' not in args or 'password' not in args or 'phone_number' not in args or 'business_name' not in args or 'image' not in args:
            return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 400

        if args['password'] is not None or args['password'] != '':
            validation = self.policy.test(args['password'])
            if validation:
                errorList = []
                for item in validation:
                    split = str(item).split('(')
                    error, num = split[0], split[1][0]
                    errorList.append("{err}(minimum {num})".format(err=error, num=num))
                message = "Please check your password: " + ', '.join(x for x in errorList)
                return {'message': message}, 422, {'Content-Type': 'application/json'}
            encrypted = hashlib.md5(args['password'].encode()).hexdigest()
            qry.password = encrypted

            qry.fullname = args['fullname']
            qry.phone_number = args['phone_number']
            qry.business_name = args['business_name']
            qry.image = args['image']

        db.session.commit()
        return marshal(qry, Users.response_fields), 200

api.add_resource(RegisterUserResource,'/user/register')
api.add_resource(UserResource,'/user/profile')