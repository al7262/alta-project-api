# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from .model import Users
from blueprints import db, app, user_required
from datetime import datetime, timedelta
from password_strength import PasswordPolicy
import json,hashlib
from mailjet_rest import Client
import os

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
Bp_user = Blueprint('user',__name__)
api = Api(Bp_user)

class RegisterUserResource(Resource):
    #Enable CORS
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
            
            # Send email
            # API configuration
            api_key = '2d98ebcc594d78589595e138f7f9d9c5'
            api_secret = 'fae993d3128a94fa5eb119c90afb5ece'
            
            if 'FLASK_ENV' not in os.environ: os.environ['FLASK_ENV'] = 'development'
            if os.environ['FLASK_ENV'] == 'development': mailjet = Client(auth=(api_key, api_secret), version='v3.1')

            # Preparing the body of the email
            first_greeting = "<h3>Selamat! Akunmu sudah terdaftar di EasyKachin.</h3>"
            greeting_content = "Terimakasih telah memilih kami untuk menjadi bagian dalam perjalanan menuju kesuksesanmu."

            # Prepare the email to be sent
            data = {
            'Messages': [
                {
                "From": {
                    "Email": "easykachin2020@gmail.com",
                    "Name": "EasyKachin"
                },
                "To": [
                    {
                    "Email": args['email'],
                    "Name": ""
                    }
                ],
                "Subject": "Selamat Datang",
                "HTMLPart": first_greeting + greeting_content,
                "CustomID": "AppGettingStartedTest"
                }
            ]
            }
            
            # Send the email
            if 'FLASK_ENV' not in os.environ: os.environ['FLASK_ENV'] = 'development'
            if os.environ['FLASK_ENV'] == 'development': mailjet.send.create(data=data)

        encrypted = hashlib.md5(args['password'].encode()).hexdigest()
        qry_user = Users.query.filter_by(email = args['email']).filter_by(password = encrypted)
        userData = qry_user.first()

        if userData is not None:
            userData = marshal(userData,Users.jwt_claims_fields)
            token = create_access_token(identity = userData['email'], user_claims = userData)

            return {'token' : token, 'message': 'Registrasi Berhasil'}, 200,{'Content-Type': 'application/json'}
        return {'message' : "Registrasi Gagal"}, 401

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
        if args['fullname'] == '' or args['password'] == '' or args['phone_number'] == '' or args['business_name'] == '' or args['image'] == '' or args['fullname'] is None or args['phone_number'] is None or args['business_name'] is None or args['image'] is None:
            return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 400

        # This is the case when post register
        if args['password'] is None: pass

        # Normal case
        elif args['password'] is not None or args['password'] != '':
            validation = self.policy.test(args['password'])
            if validation:
                errorList = []
                for item in validation:
                    split = str(item).split('(')
                    error, num = split[0], split[1][0]
                    errorList.append("{err}(minimum {num})".format(err=error, num=num))
                message = "Tolong periksa kembali password Anda: " + ', '.join(x for x in errorList)
                return {'message': message}, 422, {'Content-Type': 'application/json'}
            encrypted = hashlib.md5(args['password'].encode()).hexdigest()
            qry.password = encrypted

        qry.phone_number = args['phone_number']
        qry.fullname = args['fullname']
        qry.business_name = args['business_name']
        qry.image = args['image']

        db.session.commit()
        return marshal(qry, Users.response_fields), 200

class ChangePassword(Resource):
    # Enable CORS    
    def options(self,id=None):
        return {'status':'ok'} , 200
        
    # To keep the password secret
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    @jwt_required
    @user_required
    def put(self):
        # Take input from user
        claims = get_jwt_claims()
        
        parser = reqparse.RequestParser()
        parser.add_argument('old_password', location = 'json')
        parser.add_argument('new_password', location = 'json')
        parser.add_argument('confirm_new_password', location = 'json')
        args = parser.parse_args()

        # Check emptyness
        if args['old_password'] == None or args['old_password'] == '' or args['new_password'] == None or args['new_password'] == '' or args['confirm_new_password'] == None or args['confirm_new_password'] == '':
            return {'message': 'Tidak boleh ada kolom yang dikosongkan'}, 400
        
        # Check the old password
        encrypted = hashlib.md5(args['old_password'].encode()).hexdigest()
        owner = Users.query.filter_by(id = claims['id']).filter_by(password = encrypted).first()
        if owner is None:
            return {'message': 'Mohon maaf password lama yang Anda masukkan salah'}, 400
        
        # Check new password and confirmation
        if args['new_password'] != args['confirm_new_password']:
            return {'message': 'Tolong periksa kembali password Anda'}, 400
        
        # Validate the new password
        validation = self.policy.test(args['new_password'])
        if validation:
            errorList = []
            for item in validation:
                split = str(item).split('(')
                error, num = split[0], split[1][0]
                errorList.append("{err}(minimum {num})".format(err=error, num=num))
            message = "Tolong periksa kembali password Anda: " + ', '.join(x for x in errorList)
            return {'message': message}, 422, {'Content-Type': 'application/json'}
        encrypted = hashlib.md5(args['new_password'].encode()).hexdigest()
        owner.password = encrypted
        db.session.commit()
        return {'message': 'Sukses mengubah password'}, 200

api.add_resource(RegisterUserResource,'/user/register')
api.add_resource(UserResource,'/user/profile')
api.add_resource(ChangePassword,'/user/change-password')