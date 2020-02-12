# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Promos
from blueprints.detail_promo.model import DetailPromo
from blueprints.products.model import Products
from blueprints import db, app, user_required
from datetime import datetime
import json

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_promo = Blueprint('promo', __name__)
api = Api(bp_promo)

class PromoResource(Resource):

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
            qry = Promos.query.filter_by(id_users = claims['id']).filter_by(deleted = False).filter(Promos.name.like("%"+args["keyword"]+"%") | Promos.day.like("%"+args["keyword"]+"%"))
        if args['keyword'] is None:
            qry = Promos.query.filter_by(id_users = claims['id']).filter_by(deleted = False)
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if not row.deleted:
                rows.append(marshal(row, Promos.response_fields))
        return rows, 200

    @jwt_required
    @user_required
    # delete promos
    def delete(self,id=None):
        claims = get_jwt_claims()
        qry = Promos.query.filter_by(id_users = claims['id']).filter_by(id = id).first()
        if qry.deleted:
            return {'message':'Data Tidak Ditemukan'}, 404

        qry.deleted = True
        db.session.commit()
        return {"message": "Data Telah Dihapus"},200

    @jwt_required
    @user_required
    # edit promo
    def put(self,id=None):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('status', type = bool, location = 'json', required = True)
        parser.add_argument('day', type = list, location = 'json', required = True)
        parser.add_argument('product', type = list, location = 'json')
        parser.add_argument('discount', type = list, location = 'json')
        args = parser.parse_args()

        changes = []
        data = []
        data_product = []
        dict_product ={}
        days = ""

        for day in args['day']:
            days = days +" "+str(day)
        qry = Promos.query.filter_by(id_users = claims['id']).filter_by(id = id).first()

        if qry.deleted:
            return{'message' : 'NOT_FOUND'}, 404
        if args['name'] is not None:
            qry.name = args['name']
        if args['status'] is not None:
            qry.status = args['status']
        if args['day'] is not None:
            qry.day = days
        db.session.commit()

        qry_detail_promo = DetailPromo.query.filter_by(id_promo = qry.id).all()
        for detail in qry_detail_promo:
            data.append(detail.id_product)
        for product in args['product'] :
            qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(name = product).filter_by(deleted = False).first()
            if qry_product is not None:
                changes.append(qry_product.id)
        # print(changes)
        count = 0
        for change in changes:
            if change in data:
                detail_promo = DetailPromo.query.filter_by(id_product = change).filter_by(id_promo = qry.id).first()
                detail_promo.id_product = change
                detail_promo.id_promo = qry.id
                detail_promo.discount = args['discount'][count]
                db.session.commit()
                app.logger.debug('DEBUG : %s', detail_promo)
                count+=1
                continue
            if change not in data:
                promodetail = DetailPromo(change, qry.id, args['discount'][count])
                db.session.add(promodetail)
                db.session.commit()
                app.logger.debug('DEBUG : %s', promodetail)
                count+=1
                continue
        
        for datum in data:
            if datum not in changes:
                qry_detail_promo = DetailPromo.query.filter_by(id_product = datum).filter_by(id_promo = qry.id).first()
                db.session.delete(qry_detail_promo)
                continue

        qry_detail_promo = DetailPromo.query.filter_by(id_promo = qry.id).all()
        for detail in qry_detail_promo:
            qry_product = Products.query.filter_by(id = detail.id_product).first()
            dict_product = {
                "name_product" : qry_product.name,
                "discount" : detail.discount
            }
            data_product.append(dict_product)
        marshal_qry = marshal(qry, Promos.response_fields)
        result = {
            "promo" : marshal_qry,
            "product" :  data_product
        }
        return result, 200

#CRUD outlet POST (accessed by owner)
class CreatePromoResource(Resource):

    def options(self,id=None):
        return{'status':'ok'} , 200

    # create outlet
    @jwt_required
    @user_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location = 'json', required = True)
        parser.add_argument('day', type = list, location = 'json', required = True)
        parser.add_argument('discount', type = list, location = 'json', required = True)
        parser.add_argument('product', type = list, location = 'json', required = True)
        
        args = parser.parse_args()
        days = ""
        for day in args['day']:
            days = days +""+str(day)

        qry = Promos.query.filter_by(id_users = claims['id']).filter_by(name = args['name']).filter_by(deleted = False).first()
        if qry is None:
            promo = Promos(claims['id'], args['name'], True, days)
            db.session.add(promo)
            db.session.commit()
            app.logger.debug('DEBUG : %s', promo)

            qry = Promos.query.filter_by(id_users = claims['id']).filter_by(name = args['name']).filter_by(deleted = False).first()
            
            for product in range(len(args['product'])) :
                qry_product = Products.query.filter_by(id_users = claims['id']).filter_by(name = args['product'][product]).filter_by(deleted = False).first()
                if qry_product is not None:
                    promodetail = DetailPromo(qry_product.id, qry.id, args['discount'][product])
                    db.session.add(promodetail)
                    db.session.commit()
                    app.logger.debug('DEBUG : %s', promodetail)
    
            return {'message' : "Masukkan Promo Berhasil"}, 200, {'Content-Type': 'application/json'}
        return {'message' : "Promo Sudah Ada"}, 409,

class PromoGetByOne(Resource):
    
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @user_required
    # showing product
    def get(self,id=None):
        claims = get_jwt_claims()
        qry = Promos.query.get(id)
        data_product = []

        if qry is not None:
            if not qry.deleted:
                qry_detail_promo = DetailPromo.query.filter_by(id_promo = qry.id).all()
                for detail in qry_detail_promo:
                    # print("detail = ", detail)
                    qry_product = Products.query.filter_by(id = detail.id_product).first()
                    dict_product = {
                        "name_product" : qry_product.name,
                        "discount" : detail.discount
                    }
                    data_product.append(dict_product)
                marshal_qry = marshal(qry, Promos.response_fields)
                result = {
                    "promo" : marshal_qry,
                    "product" :  data_product
                }
                return result, 200
        return {'message' : 'Data Tidak Ditemukan'}, 404

api.add_resource(PromoGetByOne,'/promo/get/<int:id>')
api.add_resource(PromoResource, '/promo','/promo/<int:id>')
api.add_resource(CreatePromoResource,'/promo/create')