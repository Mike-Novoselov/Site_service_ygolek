from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ghbdtnsql@127.0.0.1/ygolek'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    name = db.Column(db.String(50), nullable=False)  # Имя пользователя
    email = db.Column(db.String(50), unique=True, nullable=False)  # Адрес электронной почты пользователя
    password = db.Column(db.String(100), nullable=False)  # Хэш пароля пользователя
    last_address = db.Column(db.String(100))  # Последний адрес пользователя


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор поставщика
    name = db.Column(db.String(50), nullable=False)  # Название поставщика


class CoalBrand(db.Model):
    __tablename__ = 'coal_brands'
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор марки угля
    name = db.Column(db.String(50), nullable=False)  # Название марки угля
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)  # Идентификатор поставщика, который предоставляет эту марку угля
    price_per_ton = db.Column(db.Numeric(10, 2), nullable=False)  # Цена за тонну угля данной марки


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор заказа
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Идентификатор пользователя, который сделал заказ
    coal_brand_id = db.Column(db.Integer, db.ForeignKey('coal_brand.id'), nullable=False)  # Идентификатор марки угля, которую заказал пользователь
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)  # Идентификатор поставщика, у которого заказан уголь
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Дата оформления заказа
    total_price = db.Column(db.Numeric(10, 2), nullable=False)  # Общая стоимость заказа
    address = db.Column(db.String(100), nullable=False)  # Адрес, на который должен быть доставлен уголь

    user = db.relationship('User', backref=db.backref('orders', lazy=True))  # Связь с таблицей пользователей
    coal_brand = db.relationship('CoalBrand', backref=db.backref('orders', lazy=True))  # Связь с таблицей марок угля
    supplier = db.relationship('Supplier', backref=db.backref('orders', lazy=True))  # Связь с таблицей поставщиков


with app.app_context():
    db.create_all()
