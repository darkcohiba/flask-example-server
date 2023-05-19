from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property


class Users(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    _password_hash = db.Column(db.String)

    # serialize_rules = ()

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        if password is not None:
            password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
            self._password_hash = password_hash.decode('utf-8')
        else:
            raise ValueError("Password cannot be None")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))