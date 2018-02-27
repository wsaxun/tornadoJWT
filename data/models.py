# -*- coding: utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
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
