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

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)

#  consider changing location to properties 