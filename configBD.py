"""
создаем таблицы со связями в бд ygolek
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        name = Column(String(50), nullable=False)
        email = Column(String(50), unique=True, nullable=False)
        password = Column(String(100), nullable=False)
        last_address = Column(String(100))


class Supplier(Base):
        __tablename__ = 'suppliers'

        id = Column(Integer, primary_key=True)
        name = Column(String(50), nullable=False)


class CoalBrand(Base):
        __tablename__ = 'coal_brands'

        id = Column(Integer, primary_key=True)
        name = Column(String(50), nullable=False)
        supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
        price_per_ton = Column(Numeric(10, 2), nullable=False)
        supplier = relationship('Supplier', backref='coal_brands')


class Order(Base):
        __tablename__ = 'orders'

        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        coal_brand_id = Column(Integer, ForeignKey('coal_brands.id'), nullable=False)
        supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
        order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
        total_price = Column(Numeric(10, 2), nullable=False)
        address = Column(String(100), nullable=False)

        user = relationship('User', backref='orders')
        coal_brand = relationship('CoalBrand', backref='orders')
        supplier = relationship('Supplier', backref='orders')


# Создание базы данных и таблиц
engine = create_engine('postgresql://postgres:ghbdtnsql@localhost:5432/ygolek')
Base.metadata.create_all(engine)
