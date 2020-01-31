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

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['admin']:
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        return fn(*args, **kwargs)
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
    if env is not 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0/Final_Project_Backend'
    else:
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
# ROUTE
##############################

@app.route('/')
def index():
    return {'message': 'Hello! This is the main route'}, 200, {'Content-Type': 'application/json'}

##############################
# MIDDLEWARES
##############################

# Put blueprints here

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
