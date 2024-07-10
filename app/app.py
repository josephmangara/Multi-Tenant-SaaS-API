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

# Properties Endpoint
@app.route('/properties', methods=['POST'])
@jwt_required()
def create_property():
    data = request.get_json()
    current_user = get_jwt_identity()
    landlord_id = current_user['landlord_id']
    
    new_property = Property(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        location_id=data['location_id'],
        landlord_id=landlord_id
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify(message="Property created"), 201

@app.route('/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    properties_list = [{"id": prop.id, "name": prop.name, "description": prop.description, "price": prop.price, "location_id": prop.location_id, "landlord_id": prop.landlord_id} for prop in properties]
    return jsonify(properties=properties_list), 200

# Locations Endpoint
@app.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    new_location = Location(
        address=data['address'],
        city=data['city'],
        state=data['state'],
        zip_code=data['zip_code']
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify(message="Location created"), 201


@app.route('/locations', methods=['POST'])
def locations():
    pass

@app.route('/landlords', methods=['POST'])
def landlords():
    pass


if __name__ == '__main__':
    app.run(port=5555, debug=True)