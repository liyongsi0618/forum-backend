import time
from common.pre_jsonify import pre_jsonify
from flask import current_app, jsonify, session
from sqlalchemy import Column, DateTime, Integer, MetaData, SmallInteger, String, Table, Text, func
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
    
    def get_total_page(self):
        ''' 计算文章数量，用于分页 '''
        count = db.session.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .count()
        return count

    # 根据文章类型获取文章
    def query_by_type(self, type, start, count):
        '''
        根据type参数查询对应type的多条article信息及与之相关的Users.nickname信息。返回数据格式为[(Article, Users.nickname), ...]
        传入参数start为起始id，count为获取条数。
        '''
        result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.type == type) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 根据文章类型获取数量，便于分页
    def get_count_by_type(self, type):
        ''' 计算指定type文章数量，用于分页 '''
        count = db.session.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                                Article.type == type).count()
        return count
    
    # 搜索文章标题获得文章信息
    def query_by_search(self, search_word):
        '''
        根据搜索词查询匹配的全部article信息及与之相关的Users.nickname信息。返回数据格式为[(Article, Users.nickname), ...]
        '''
        result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, \
                    Article.headline.like('%'+ search_word + '%')).order_by(Article.articleid.desc()).all()
        return result

    # 最新文章
    def query_latest_9(self):
        ''' 查询最新发布的9篇文章 '''
        query = db.session.query(Article.articleid, Article.headline) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.articleid.desc()).limit(9).all()
        return query

    # 最多阅读
    def query_most_read_9(self):
        ''' 查询最多阅读的9篇文章 '''
        query = db.session.query(Article.articleid, Article.headline) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.readcount.desc()).limit(9).all()
        return query

    # 特别推荐，超过9篇则随机推荐9篇
    def query_recommended_9(self):
        ''' 查询编辑推荐的9篇文章 '''
        query = db.session.query(Article.articleid, Article.headline) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(func.rand()).limit(9).all()
        return query


if __name__ == '__main__':
    from app import app
    with app.app_context():
        data = (Article().query_article_id(2))
        print(data)
