from common.pre_jsonify import pre_jsonify
from flask import jsonify
from sqlalchemy import Column, DateTime, Integer, MetaData, SmallInteger, String, Table, Text
from blog_app import db


class Opinion(db.Model):

    __table__ = Table(
        'opinion',
        MetaData(),
        Column("opinionid", Integer, primary_key=True, autoincrement='auto'),
        Column("commentid", Integer, nullable=True),
        Column("userid", Integer, default=0, nullable=True),
        Column("type", SmallInteger, nullable=False),
        Column("ipaddr", String(30), nullable=True),
        Column("createtime", DateTime, nullable=True),
        Column("updatetime", DateTime, nullable=True),
    )