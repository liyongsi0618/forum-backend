from common.pre_jsonify import pre_jsonify
from flask import jsonify
from sqlalchemy import Column, DateTime, Integer, MetaData, SmallInteger, String, Table, Text
from blog_app import db


class Comment(db.Model):

    __table__ = Table(
        'comment',
        MetaData(),
        Column("commentid", Integer, primary_key=True, autoincrement='auto'),
        Column("userid", Integer, nullable=True),
        Column("articleid", Integer, nullable=True),
        Column("content", Text, nullable=True),
        Column("ipaddr", String(20), nullable=True),
        Column("replyid", Integer, nullable=True, default=0),
        Column("agreement", Integer, nullable=True, default=0),
        Column("opposement", Integer, nullable=True, default=0),
        Column("hidden", SmallInteger, nullable=True, default=0),
        Column("createtime", DateTime, nullable=True),
        Column("updatetime", DateTime, nullable=True),
    )