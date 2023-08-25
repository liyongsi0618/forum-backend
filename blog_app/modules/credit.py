from common.pre_jsonify import pre_jsonify
from flask import jsonify
from sqlalchemy import Column, DateTime, Integer, MetaData, SmallInteger, String, Table, Text
from blog_app import db


class Credit(db.Model):

    __table__ = Table(
        'credit',
        MetaData(),
        Column("creditid", Integer, primary_key=True, autoincrement='auto'),
        Column("userid", Integer, nullable=False),
        Column("category", String(10), default='', nullable=True),
        Column("target", Integer, default=0, nullable=True),
        Column("credit", Integer, nullable=True),
        Column("createtime", DateTime, nullable=True),
        Column("updatetime", DateTime, nullable=True),
    )