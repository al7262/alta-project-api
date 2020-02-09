# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Outlets
from blueprints import db, app, user_required
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_outlets = Blueprint('outlets', __name__)
api = Api(bp_outlets)

class OutletResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @user_required
    # show outlet
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('keyword', location = 'args')

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        if args['keyword'] is not None:
            qry = Outlets.query.filter_by(id_user = claims['id']).filter(Outlets.name.like("%"+args["keyword"]+"%") | Outlets.city.like("%"+args["keyword"]+"%"))
        elif args['keyword'] is None:
            qry = Outlets.query.filter_by(id_user = claims['id'])
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Outlets.response_fields))
        return rows, 200

    @jwt_required
    @user_required
    # delete outlet
    def delete(self,id=None):
        claims = get_jwt_claims()
        qry = Outlets.query.filter_by(id_user = claims['id']).filter_by(id = id).first()
        if qry.deleted:
            return {'message':'Data Tidak Ditemukan'}, 404

        qry.deleted = True
        db.session.commit()
        return {"message": "Data Telah Dihapus"},200

    @jwt_required
    @user_required
    # edit outlet
    def put(self,id=None):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json')
        parser.add_argument('phone_number', location = 'json')
        parser.add_argument('address', location = 'json')
        parser.add_argument('city', location = 'json')
        parser.add_argument('tax', location = 'json')
        args = parser.parse_args()

        qry = Outlets.query.filter_by(id_user = claims['id']).filter_by(id = id).first()

        if qry.deleted:
            return{'message' : 'NOT_FOUND'}, 404
        if args['name'] is not None:
            qry.name = args['name']
        if args['phone_number'] is not None:
            qry.phone_number = args['phone_number']
        if args['address'] is not None:
            qry.address = args['address']
        if args['city'] is not None:
            qry.city = args['city']
        if args['tax'] is not None:
            qry.tax = args['tax']

        db.session.commit()
        return marshal(qry, Outlets.response_fields), 200

#CRUD outlet POST (accessed by owner)
class CreateOutletResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    # create outlet
    @jwt_required
    @user_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('phone_number', location = 'json', required = True)
        parser.add_argument('address', location = 'json', required = True)
        parser.add_argument('city', location = 'json', required = True)
        parser.add_argument('tax', location = 'json', required = True)
        
        args = parser.parse_args()

        qry = Outlets.query.filter_by(id_user = claims['id']).filter_by(name = args['name']).filter_by(deleted = False).first()
        if qry is None:
            outlet = Outlets(claims['id'], args['name'], args['phone_number'], args['address'], args['city'], args['tax'])
            db.session.add(outlet)
            db.session.commit()
            app.logger.debug('DEBUG : %s', outlet)
    
            return {'message' : "Masukkan Outlet Berhasil"}, 200, {'Content-Type': 'application/json'}
        return {'message' : "Outlet Sudah Ada"}, 409,

class OutletGetByOne(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @user_required
    # showing product
    def get(self,id=None):
        claims = get_jwt_claims()
        qry = Outlets.query.get(id)
        marshal_qry = (marshal(qry, Outlets.response_fields))

        if qry is not None:
            if not qry.deleted:
                return marshal_qry, 200
        return {'message' : 'Data Tidak Ditemukan'}, 404

api.add_resource(OutletResource,'/outlet','/outlet/<int:id>')
api.add_resource(CreateOutletResource,'/outlet/create')
api.add_resource(OutletGetByOne,'/outlet/get/<int:id>')