from common.pre_jsonify import pre_jsonify
from flask import current_app, jsonify
from sqlalchemy import Column, DateTime, Integer, MetaData, SmallInteger, String, Table, Text
from blog_app import db
from modules.users import Users


class Article(db.Model):

    __table__ = Table(
        'article',
        MetaData(),
        Column("articleid", Integer, primary_key=True, autoincrement='auto'),
        Column("userid", Integer, nullable=True),
        Column("category", SmallInteger, nullable=True),
        Column("headline", String(255), nullable=False),
        Column("content", Text, nullable=False),
        Column("thumbnail", String(20), nullable=True),
        Column("credit", Integer, nullable=True, default=0),
        Column("readcount", Integer, nullable=True, default=0),
        Column("replycount", Integer, nullable=True, default=0),
        Column("recommended", SmallInteger, nullable=True, default=0),
        Column("hidden", SmallInteger, nullable=True, default=0),
        Column("drafted", SmallInteger, nullable=True, default=0),
        Column("checked", SmallInteger, nullable=True, default=1),
        Column("createtime", DateTime, nullable=True),
        Column("updatetime", DateTime, nullable=True),
        Column("type", Integer, nullable=True),
    )

    def query_article_id(self, articleid):
        '''根据articleid查询文章信息'''
        result = db.session.query(Article).filter_by(articleid=articleid).first()
        return result

    def query_limits_join_users(self, start, count):
        '''
        用于分页，根据articleid顺序获取多条article信息及与之相关的Users.nickname信息。返回数据格式为[(Article, Users.nickname), ...]
        传入参数start为起始id，count为获取条数。
        '''
        result = db.session.query(Article, Users.nickname).join(Users, Article.userid == Users.userid)\
                .where(Article.drafted==0, Article.hidden==0).order_by(Article.articleid.desc())\
                .limit(count).offset(start).all()
        return result


if __name__ == '__main__':
    from app import app
    with app.app_context():
        data = (Article().query_article_id(2))
        print(data)
