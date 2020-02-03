# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Users
from blueprints import db, app
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_users = Blueprint('users', __name__)
api = Api(bp_users)

class RegisterUserResource(Resource):

    #
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
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('fullname', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('address', location = 'json', required = True)
        parser.add_argument('number_phone', location = 'json', required = True)
        args = parser.parse_args()
        
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

        role = "user"
        
        user = Users(args['username'], encrypted, args['fullname'], args['email'], args['address'], args['number_phone'], "user")
        db.session.add(user)
        db.session.commit()
        app.logger.debug('DEBUG : %s', user)
        
        return {'message' : "registration success !!!"},200,{'Content-Type': 'application/json'}

class UserResource(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200
        
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    @jwt_required
    @user_required
    # showing user profile (himself)
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        if qry.deleted == False:
            return marshal(qry, Users.response_fields), 200
        return {'message' : 'NOT_FOUND'}, 404

    def put(self):
            claims =api.add_resource(LoginCashier, '/login-cashier') get_jwt_claims()
            qry = Users.query.filter_by(id = claims['id']).first()
            parser = reqparse.RequestParser()
            parser.add_argument('username', location = 'json')
            parser.add_argument('password', location = 'json')
            parser.add_argument('fullname', location = 'json')
            parser.add_argument('number_phone', location = 'json')
            parser.add_argument('address', location = 'json')
            parser.add_argument('email', location = 'json')
            parser.add_argument('gender', location = 'json', help = "Invalid input", choices=('Male', 'Female'))
            parser.add_argument('city', location = 'json')
            parser.add_argument('image', location = 'json')

            args = parser.parse_args()

            if qry.deleted:
                return{'message' : 'NOT_FOUND'}, 404
            if args ['username'] is not None:
                qry.username = args['username']
            if args['password'] is not None:
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
            if args['fullname'] is not None:
                qry.fullname = args['fullname']
            if args['number_phone'] is not None:
                qry.number_phone = args['number_phone']
            if args['address'] is not None:
                qry.address = args['address']
            if args['email'] is not None:
                qry.email = args['email']
            if args['gender'] is not None:
                qry.gender = args['gender']
            if args['city'] is not None:
                qry.city = args['city']
            if args['image'] is not None:
                qry.image = args['image']

            db.session.commit()
            return marshal(qry, Users.response_fields), 200