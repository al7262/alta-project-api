# Import
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Employees
from blueprints.outlets.model import Outlets
from blueprints import db, app, user_required, dashboard_required, apps_required
from datetime import datetime
from password_strength import PasswordPolicy
import json, hashlib

# Import Authentication
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_employees = Blueprint('employees', __name__)
api = Api(bp_employees)

class CreateEmployeeResource(Resource):
    # Enable CORS
    def options(self,id=None):
        return{'status':'ok'} , 200

    # To keep the password secret
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    # Create user account
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_outlet', location = 'json', required = True)
        parser.add_argument('full_name', location = 'json', required = True)
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('position', location = 'json', required = True)
        args = parser.parse_args()
        
        # Check emptyness
        if args['full_name'] == '' or args['username'] == '' or args['password'] == '':
            return {'message': 'tidak boleh ada kolom yang dikosongkan'}, 400

        qry = Employees.query.filter_by(username = args['username']).first()
        if qry is None:
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
            
            employee = Employees(args['id_outlet'], args['full_name'], args['username'], encrypted, args['position'])
            db.session.add(employee)
            db.session.commit()
            app.logger.debug('DEBUG : %s', employee)
            
            return {'message' : "Input Pegawai Berhasil"}, 200, {'Content-Type': 'application/json'}
        return {'message' : "Input Pegawai Gagal"}, 401

class EmployeeResource(Resource):
    def options(self,id=None):
        return{'status':'ok'} , 200
        
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    # Showing user profile (himself)
    @jwt_required
    @user_required
    def get(self):
        parser = reqparse.RequestParser()
        claims = get_jwt_claims()
        parser.add_argument('name_outlet', location = 'args')
        parser.add_argument('position', location = 'args')
        parser.add_argument('keyword', location = 'args')

        args = parser.parse_args()

        if args['name_outlet'] is None or args['name_outlet'] == "":
            qry = Outlets.query.filter_by(id_user = claims['id']).all()
            if qry is not None:
                rows = []
                for outlet in qry:
                    if not outlet.deleted:
                        if args['position'] is None or args['position'] == "":
                            if args['keyword'] is not None:
                                qry_employee = Employees.query.filter_by(id_outlet = outlet.id).filter(Employees.full_name.like("%"+args["keyword"]+"%") | Employees.username.like("%"+args["keyword"]+"%")).all()
                            elif args['keyword'] is None:
                                qry_employee = Employees.query.filter_by(id_outlet = outlet.id).all()
                        elif args['position'] is not None:
                            if args['keyword'] is not None:
                                qry_employee = Employees.query.filter_by(id_outlet = outlet.id).filter_by(position = args['position']).filter(Employees.full_name.like("%"+args["keyword"]+"%") | Employees.username.like("%"+args["keyword"]+"%")).all()
                            elif args['keyword'] is None:
                                qry_employee = Employees.query.filter_by(id_outlet = outlet.id).filter_by(position = args['position']).all()
                        if qry_employee is not None:
                            for employee in qry_employee:
                                if not employee.deleted:
                                    rows.append(marshal(employee, Employees.response_fields))        
                return rows, 200

        rows = []
        qry = Outlets.query.filter_by(id_user = claims['id']).filter_by(name = args['name_outlet']).first()
        if qry is not None:
            if not qry.deleted:
                if args['position'] is None or args['position'] == "":
                    if args['keyword'] is not None:
                        qry_employee = Employees.query.filter_by(id_outlet = qry.id).filter(Employees.full_name.like("%"+args["keyword"]+"%") | Employees.username.like("%"+args["keyword"]+"%")).all()
                    elif args['keyword'] is None:
                        qry_employee = Employees.query.filter_by(id_outlet = qry.id).all()
                elif args['position'] is not None:
                    if args['keyword'] is not None:
                        qry_employee = Employees.query.filter_by(id_outlet = qry.id).filter_by(position = args['position']).filter(Employees.full_name.like("%"+args["keyword"]+"%") | Employees.username.like("%"+args["keyword"]+"%")).all()
                    elif args['keyword'] is None:
                        qry_employee = Employees.query.filter_by(id_outlet = qry.id).filter_by(position = args['position']).all()
                if qry_employee is not None:
                    for employee in qry_employee:
                        if not employee.deleted:
                            rows.append(marshal(employee, Employees.response_fields))
                    return rows, 200
        return {'message' : "Data Tidak Ditemukan"},404
    
    @jwt_required
    @user_required
    def put(self,id=None):
        claims = get_jwt_claims()
        qry = Employees.query.get(id)
        parser = reqparse.RequestParser()

        parser.add_argument('id_outlet', location = 'json', required = True)
        parser.add_argument('fullname', location = 'json', required = True)
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('position', location = 'json', required = True)

        args = parser.parse_args()

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
        if args['id_outlet'] is not None:
            qry.id_outlet = args['id_outlet']
        if args['username'] is not None:
            qry.username = args['username']
        if args['position'] is not None:
            qry.position = args['position']
        qry.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        return marshal(qry, Employees.response_fields), 200

    @jwt_required
    @user_required
    # delete product (himself)
    def delete(self,id=None):
        claims = get_jwt_claims()
        qry = Employees.query.get(id)
        if qry.deleted:
            return {'message':'Data Tidak Ditemukan'}, 404

        qry.deleted = True
        db.session.commit()
        return {"message": "Data Telah Dihapus"},200

class EmployeeGetByOne(Resource):
    def options(self,id=None):
        return{'status':'ok'} , 200

    @jwt_required
    @user_required
    def get(self,id=None):
        claims = get_jwt_claims()
        qry = Employees.query.get(id)
        marshal_qry = (marshal(qry, Employees.response_fields))

        if qry is not None:
            if not qry.deleted:
                return marshal_qry, 200
        return {'message' : 'Data Tidak Ditemukan'}, 404

api.add_resource(CreateEmployeeResource,'/employee/create')
api.add_resource(EmployeeResource,'/employee','/employee/<int:id>')
api.add_resource(EmployeeGetByOne,'/employee/get/<int:id>')