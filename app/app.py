#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Landlord
from flask_restful import Api, Resource



app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///multi_tenant.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SESSION_TYPE'] = 'SQLAlchemy'
app.json.compact = True 

migrate = Migrate(app, db)
db.init_app(app)

jwt = JWTManager(app)


@app.route("/")
def home():
    return {"Message": "Welcome to the multi-tenant SaaS API"}

# Registration and Login Endpoints
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'], landlord_id=data['landlord_id'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity={'username': user.username, 'landlord_id': user.landlord_id})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

if __name__ == '__main__':
    app.run(port=5555, debug=True)