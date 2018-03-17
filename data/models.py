# -*- coding: utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, ForeignKey, Enum, DateTime,
                        Text)
from sqlalchemy.orm import relationship

Model = declarative_base()


class User(Model):
    __tablename__ = 't_user'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_user = Column(String(20), nullable=False, unique=True)
    f_passwd = Column(String(200), nullable=False)
    f_description = Column(String(200), nullable=True, default="default")
    user_user_group = relationship('UserRelationGroup', backref='t_user')


class UserGroup(Model):
    __tablename__ = 't_user_group'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_user_group = Column(String(20), nullable=False, unique=True)
    f_description = Column(String(200), nullable=True, default="default")
    user_user_group = relationship('UserRelationGroup',
                                   backref='t_user_group')
    user_group_permission = relationship('Permission',
                                         backref='t_user_group')


class UserRelationGroup(Model):
    __tablename__ = 't_user_relation_group'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_user_id = Column(Integer, ForeignKey('t_user.f_id'))
    f_user_group_id = Column(Integer, ForeignKey('t_user_group.f_id'))


class Menu(Model):
    __tablename__ = 't_menu'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_uri = Column(String(100), nullable=False, unique=True)
    f_description = Column(String(200), nullable=True)
    menu_permission = relationship('Permission', backref='t_menu')


class Permission(Model):
    __tablename__ = 't_permission'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_menu_id = Column(Integer, ForeignKey('t_menu.f_id'))
    f_user_group_id = Column(Integer, ForeignKey('t_user_group.f_id'))


class Product(Model):
    __tablename__ = 't_product'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(String(50), unique=True, nullable=False)
    f_description = Column(String(200), nullable=True)
    product_product_schema = relationship('ProductSchema',
                                          backref='t_product')
    product_history = relationship('ConfigHistory',
                                          backref='t_product')


class ProductSchema(Model):
    __tablename__ = 't_product_schema'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_product_id = Column(Integer, ForeignKey('t_product.f_id'))
    f_hardware_type = Column(Integer, ForeignKey('t_hardware_type.f_id'))
    f_option_config = Column(Enum('0', '1'), default='1', nullable=False)
    f_min_num = Column(Integer, nullable=False)
    f_description = Column(String(200), nullable=True)


class Hardware(Model):
    __tablename__ = 't_hardware'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(String(50), nullable=False)
    f_type = Column(Integer, ForeignKey('t_hardware_type.f_id'))
    f_description = Column(String(200), nullable=True)
    hardware_price = relationship('Price', backref='t_price.f_id')


class HardwareType(Model):
    __tablename__ = 't_hardware_type'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(String(100), nullable=False, unique=True)
    f_description = Column(String(200), nullable=True)
    hardware_type_product_schema = relationship('ProductSchema',
                                                backref='t_hardware_type')
    hardware_type_hardware = relationship('Hardware',
                                          backref='t_hardware_type')


class Price(Model):
    __tablename__ = 't_price'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_hardware_id = Column(Integer, ForeignKey('t_hardware.f_id'),
                           nullable=False, unique=True)
    f_cost_price = Column(Integer, nullable=True)
    f_business_price = Column(Integer, nullable=True)
    f_description = Column(String(100), nullable=True)


class ConfigHistory(Model):
    __tablename__ = 't_config_history'
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    f_create_time = Column(DateTime, nullable=False)
    f_product_id = Column(Integer, ForeignKey('t_product.f_id'),
                          nullable=False)
    f_config = Column(Text, nullable=False)
    f_description = Column(String(100), nullable=True)
