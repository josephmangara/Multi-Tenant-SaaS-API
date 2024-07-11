from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt 
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()
bcrypt = Bcrypt() 


# User and Tenant Models
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())
        
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'))

class Landlord(db.Model):
    __tablename__ = "landlords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    users = db.relationship('User', backref="landlords")

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'))

    location = db.relationship('Location', backref='properties')
    landlord = db.relationship('Landlord', backref='properties')

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    town = db.Column(db.String(80), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    properties = db.relationship('Property', backref='locations')
