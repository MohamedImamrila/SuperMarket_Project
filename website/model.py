from . import db
from flask_login import UserMixin
from datetime import datetime

class UserDetails(db.Model,UserMixin):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    purchases = db.relationship('Purchase', backref='user', lazy=True)


class StoreUser(db.Model,UserMixin):
    __tablename__ = 'store_user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.String(30), nullable=False)

class Product(db.Model,UserMixin):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    purchases = db.relationship('Purchase', backref='product', lazy=True)

class Purchase(db.Model,UserMixin):
    __tablename__ = 'purchase'
    purchase_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    itemName = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    date_of_purchase = db.Column(db.DateTime, nullable=False, default=datetime.now())