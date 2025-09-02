from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt 
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt() 


# User and landlord Models
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_only = ('id', 'username', 'created_at', 'updated_at', 'landlord_id')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())
        
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'))

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

class Landlord(db.Model, SerializerMixin):
    __tablename__ = "landlords"
    serialize_only = ('id', 'name', 'created_at', 'updated_at', 'users.id')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    users = db.relationship('User', backref="landlords")

class Property(db.Model, SerializerMixin):
    __tablename__ = "properties"
    serialize_only = ('id', 'name', 'description', 'price', 'location_id', 'landlord_id')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(2000))
    price = db.Column(db.Float, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'))

    location = db.relationship('Location', backref='properties')
    landlord = db.relationship('Landlord', backref='properties')

class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"
    serialize_only = ('id', 'address', 'city', 'town', 'zip_code', 'properties.id')

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    town = db.Column(db.String(80), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    properties = db.relationship('Property', backref='locations')
