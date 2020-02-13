from flask import Flask, request
import json, os
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, get_raw_jwt
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

##############################
# JWT
##############################

app.config['JWT_SECRET_KEY'] = 'c2n!$st0pDo1ngt#!s$tuff'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'email' in claims:
            return fn(*args, **kwargs)
        else:
            return {'status': 'FORBIDDEN', 'message': 'Hanya untuk owner'}, 403
    return wrapper

def dashboard_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'position' in claims:
            if claims['position'] == "Admin":
                return fn(*args, **kwargs)
            else:
                return {'status': 'FORBIDDEN', 'message': 'Hanya dapat diakses oleh Admin'}, 403
        else:
            if 'email' in claims:
                return fn(*args, **kwargs)
            else:
                return {'status': 'FORBIDDEN', 'message': 'Hanya dapat diakses oleh Admin'}, 403
    return wrapper

def apps_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'position' in claims:
            if claims['position'] == "Kasir":
                return fn(*args, **kwargs)
            else:
                return {'status': 'FORBIDDEN', 'message': 'Hanya dapat diakses oleh kasir'}, 403
        else:
            if 'email' in claims:
                return fn(*args, **kwargs)
            else:
                return {'status': 'FORBIDDEN', 'message': 'Hanya dapat diakses oleh kasir'}, 403
    return wrapper

##############################
# DATABASE
##############################

db_user=os.getenv('DB_USER')
db_pass=os.getenv('DB_PASS')
db_url=os.getenv('DB_URL')
db_selected=os.getenv('DB_SELECTED')

##############################
# TESTING
##############################
try:
    env = os.environ.get('FLASK_ENV', 'development')
    username_laptop = os.environ['HOME']
    if username_laptop == '/home/alta8' and env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/final_project_backend_testing'
    elif username_laptop == '/home/alta10'and env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0/Final_Project_Backend_test'
    elif username_laptop == '/home/alta10'and env != 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0/Final_Project_Backend'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:agungajin19@portofolio.ce1fym8eoinv.ap-southeast-1.rds.amazonaws.com:3306/pos_api'

except Exception as e:
    raise e
#############################

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

##############################
# MIDDLEWARES
##############################

# Put blueprints here
from blueprints.customers.resources import bp_customers
app.register_blueprint(bp_customers, url_prefix='')

from blueprints.employees.resources import bp_employees
app.register_blueprint(bp_employees, url_prefix='')

from blueprints.inventories.resources import bp_inventories
app.register_blueprint(bp_inventories, url_prefix='/inventory')

from blueprints.outlets.resources import bp_outlets
app.register_blueprint(bp_outlets, url_prefix='')

from blueprints.products.resources import bp_products
app.register_blueprint(bp_products, url_prefix='/product')

# from blueprints.promo.resources import bp_promo
# app.register_blueprint(bp_promo, url_prefix='')

# from blueprints.recipes.resources import bp_recipe
# app.register_blueprint(bp_recipe, url_prefix='/recipe')

from blueprints.auth import bp_auth
app.register_blueprint(bp_auth,url_prefix = '')

from blueprints.users.resources import Bp_user
app.register_blueprint(Bp_user,url_prefix = '')

from blueprints.dashboard import bp_dashboard
app.register_blueprint(bp_dashboard,url_prefix = '')

from blueprints.activity import bp_activity
app.register_blueprint(bp_activity,url_prefix = '/activity')

from blueprints.report import bp_report
app.register_blueprint(bp_report,url_prefix = '/report')

db.create_all()

@app.after_request
def after_request(response):
    try:
        requestData = response.get_json()
    except Exception as e:
        requestData = response.args.to_dict()
    logData = json.dumps({
        'status_code': response.status_code,
        'method': request.method,
        'code': response.status,
        'uri': request.full_path,
        'requedatetimest': requestData,
        'response': json.loads(response.data.decode('utf-8'))
    })
    log = app.logger.info("REQUEST_LOG\t%s", logData) if response.status_code==200 else app.logger.warning("REQUEST_LOG\t%s", logData)
    return response