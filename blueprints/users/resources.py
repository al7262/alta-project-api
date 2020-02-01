from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app, admin_required, user_required, agent_required
from blueprints.user.model import Users
from blueprints.cart.model import Carts, Cartdetails
from blueprints.transaction.model import Trasactions,Transactiondetails
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy

Bp_user = Blueprint('user',__name__)
api = Api(Bp_user)

# CRUD user GET, DELETE, PUT (accessed by users)
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

    @jwt_required
    @user_required
    # delete user account (himself)
    def delete(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        if qry.deleted:
            return {'message':'NOT_FOUND'}, 404

        qry.deleted = True
        db.session.commit()
        
        # cart = Carts.query.filter_by(id_user = claims['id']).all()
        # if cart[0] is not None:
        #     for each_cart in cart:
        #         db.session.delete(each_cart)
        #         db.session.commit()

        # cart_cartdetails = Cartdetails.query.filter(id_cart = cart.id).all()
        # if cart_cartdetails[0] is not None:
        #     for each_cart_cartdetails in cart_cartdetails:
        #         db.session.delete(each_cart_cartdetails)
        #         db.session.commit()
        
        # cart_transaction_detail = Transactiondetails.query.filter_by(id_cart = cart.id).all()
        # if cart_transaction_detail[0] is not None:
        #     for each_cart_transaction_detail in cart_transaction_detail:
        #         db.session.delete(each_cart_transaction_detail)
        #         db.session.commit()

        # transaction = Trasactions.query.filter_by(id_user = claims['id']).all()
        # if transaction is not None:
        #     for each_transaction in transaction:
        #         db.session.delete(each_transaction)
        #         db.session.commit()

        # transaction_transaction_detail = Transactiondetails.query.filter_by(id_transaction = transaction.id).all()
        # if transaction_transaction_detail[0] is not None:
        #     for each_transaction_transaction_detail in transaction_transaction_detail:
        #         db.session.delete(each_transaction)
        #         db.session.commit()
        
                
        return {"message": "Deleted"},200

    @jwt_required
    @user_required
    # edit user account (himself)
    def put(self):
        claims = get_jwt_claims()
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

class AgentResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )
    @jwt_required
    @agent_required
    # showing agent profile (himself)
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        if qry.deleted == False:
            return marshal(qry, Users.response_fields), 200
        return {'message' : 'NOT_FOUND'}, 404

    @jwt_required
    @agent_required
    # delete agent account (himself)
    def delete(self):

        def options(self,id=None):
            return{'status':'ok'} , 200

        claims = get_jwt_claims()
        qry = Users.query.filter_by(id = claims['id']).first()
        if qry.deleted:
            return {'message':'NOT_FOUND'}, 404

        qry.deleted = True
        db.session.commit()
        
        # cart = Carts.query.filter_by(id_user = claims['id']).all()
        # if cart is not None:
        #     for each_cart in cart:
        #         db.session.delete(each_cart)
        #         db.session.commit()

        # cartdetails_cart = Cartdetails.query.filter(id_cart = cart.id)
        # if cartdetails_cart is not None:
        #     for each_cartdetails_cart in cartdetails_cart:
        #         db.session.delete(each_cartdetails_cart)
        #         db.session.commit()

        # transaction = Trasactions.query.filter_by(id_user = claims['id']).all()
        # if transaction is not None:
        #     for each_transaction in transaction:
        #         db.session.delete(each_transaction)
        #         db.session.commit()

        # cartdetails_transaction = Cartdetails.query.filter(id_transaction = transaction.id)
        # if cartdetails_transaction is not None:
        #     for each_cartdetails_transaction in cartdetails_transaction:
        #         db.session.delete(each_cartdetails_transaction)
        #         db.session.commit()
                
        return {"message": "Deleted"},200

    @jwt_required
    @agent_required
    # edit agent account (himself)
    def put(self):

        def options(self,id=None):
            return{'status':'ok'} , 200

        claims = get_jwt_claims()
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

#CRUD user POST (accessed by user)
class RegisterUserResource(Resource):

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


#CRUD agent POST (accessed by agent)
class RegisterAgentResource(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200
    # to keep the password secret
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    # create agent account
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('fullname', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('address', location = 'json', required = True)
        parser.add_argument('number_phone', location = 'json', required = True)
        # parser.add_argument('role', location = 'json', required = True)
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


        
        user = Users(args['username'], encrypted, args['fullname'], args['email'], args['address'], args['number_phone'], "agent")
        db.session.add(user)
        db.session.commit()
        app.logger.debug('DEBUG : %s', user)
        
        return {'message' : "registration success !!!"},200,{'Content-Type': 'application/json'}


#CRUD user and agent GET (accessed by admin)
class GetUsersAgentsAdmin(Resource):
    @jwt_required
    @admin_required
    # showing all user and agent account
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('id', location = 'args')
        parser.add_argument('role', location = 'args', help = "Invalid input", choices = ('user', 'agent'))
        parser.add_argument('username', location = 'args')
        parser.add_argument('city', location = 'args')
        parser.add_argument('gender', location = 'args', help = "Invalid input", choices = ('Male', 'Female'))

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Users.query

        if args['id'] is not None:
            qry = qry.filter_by(id = args['id'])

        if args['username'] is not None:
            qry = qry.filter_by(username = args['username'])
        
        if args['city'] is not None:
            qry = qry.filter_by(city = args['city'])
        
        if args['gender'] is not None:
            qry = qry.filter_by(gender = args['gender'])
        
        if args['role'] is not None:
            qry = qry.filter_by(role = args['role'])
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Users.response_fields))
        return rows, 200

#CRUD user agent DELETE (accessed by admin)
class DeleteUsersAgentsAdmin(Resource):
    @jwt_required
    @admin_required
    # delete user and agent account with filter by id or username
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args')
        parser.add_argument('username', location = 'args')

        args = parser.parse_args()

        if (args['id'] is not None) and (args['username'] is not None):
            return {'message':'Please, just enter one'}, 404
        
        elif args['id'] is not None:
            qry = Users.query.filter_by(id = args['id']).first()

        elif args['username'] is not None:
            qry = Users.query.filter_by(username = args['username']).first()

        if qry.deleted:
            return {'message':'NOT_FOUND'}, 404

        qry.deleted = True
        db.session.commit()
        
        # cart = Carts.query.filter_by(user_id=args['id']).all()
        # if cart is not None:
        #     for each_cart in cart:
        #         db.session.delete(each_cart)
        #         db.session.commit()

        # transaction = Trasactions.query.filter_by(user_id = args['id']).all()
        # if transaction is not None:
        #     for each_transaction in transaction:
        #         db.session.delete(each_transaction)
        #         db.session.commit()

        return {"message": "Deleted"},200

#CRUD user and agent PUT (accessed by admin)
class ActivatedUsersAgentsAdmin(Resource):
    @jwt_required
    @admin_required
    # Activate user and agent account with filter by id or username
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args')
        parser.add_argument('username', location = 'args')

        args = parser.parse_args()

        if (args['id'] is not None) and (args['username'] is not None):
            return {'message':'Please, just enter one'}, 404
        
        elif args['id'] is not None:
            qry = Users.query.filter_by(id = args['id']).first()

        elif args['username'] is not None:
            qry = Users.query.filter_by(username = args['username']).first()

        if qry.deleted == False:
            return {'message':'This account is still active!'}, 404

        qry.deleted = False
        db.session.commit()
        return {"message": "Activated"},200

api.add_resource(UserResource,'/user')
api.add_resource(RegisterUserResource,'/user/registration')
api.add_resource(AgentResource,'/agent')
api.add_resource(RegisterAgentResource,'/agent/registration')
api.add_resource(GetUsersAgentsAdmin,'/admin/get/costumer')
api.add_resource(DeleteUsersAgentsAdmin,'/admin/delete/costumer')
api.add_resource(ActivatedUsersAgentsAdmin,'/admin/activate/costumer')