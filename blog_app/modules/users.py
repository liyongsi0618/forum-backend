from common.pre_jsonify import pre_jsonify
from flask import jsonify
from sqlalchemy import Column, DateTime, Integer, MetaData, SmallInteger, String, Table, Text
from blog_app import db


class Users(db.Model):

    __table__ = Table(
        'users',
        MetaData(),
        Column("userid", Integer, primary_key=True, autoincrement='auto'),
        Column("username", String(50), nullable=False),
        Column("password", String(32), nullable=False),
        Column("nickname", String(30), nullable=True),
        Column("avatar", String(20), nullable=True),
        Column("qq", String(15), nullable=True),
        Column("role", String(10), nullable=False, default='user'),
        Column("credit", Integer, nullable=False, default=50),
        Column("createtime", DateTime, nullable=True),
        Column("updatetime", DateTime, nullable=True),
    )

