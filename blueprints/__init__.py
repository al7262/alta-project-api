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


app.config['JWT_SECRET_KEY'] = 'JWjs924bG9epW02LsqwZaM309QL1tW31'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def owner_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['email'] is None:
            return {'status': 'FORBIDDEN', 'message' : 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['position'] == "user":
            return fn(*args, **kwargs)
        else:
            return {'status': 'FORBIDDEN', 'message' : 'user doesn\'t get access!'}, 403
    return wrapper

def kasir_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] == "agent":
            return fn(*args, **kwargs)
        else:
            return {'status': 'FORBIDDEN', 'message' : 'agent doesn\'t get access!'}, 403
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
    if username_laptop == '/home/alta8' and env is not 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/final_project_backend'
    elif username_laptop == '/home/alta10' and env is not 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0/Final_Project_Backend'
    elif username_laptop == '/home/alta8':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/final_project_backend_testing'
    elif username_laptop == '/home/alta10':
       app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0/Final_Project_Backend_test'

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
app.register_blueprint(bp_customers, url_prefix='/customer')

from blueprints.employees.resources import bp_employees
app.register_blueprint(bp_employees, url_prefix='/employee')

from blueprints.inventories.resources import bp_inventories
app.register_blueprint(bp_inventories, url_prefix='/inventory')

from blueprints.outlets.resources import bp_outlets
app.register_blueprint(bp_outlets, url_prefix='/outlet')

from blueprints.products.resources import bp_products
app.register_blueprint(bp_products, url_prefix='/product')

from blueprints.promo.resources import bp_promo
app.register_blueprint(bp_promo, url_prefix='/promo')

from blueprints.recipes.resources import bp_recipe
app.register_blueprint(bp_recipe, url_prefix='/recipe')

from blueprints.users.resources import bp_users
app.register_blueprint(bp_users, url_prefix='/users')

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
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps(log))
    elif response.status_code >= 400:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps(log))
    
    return response

