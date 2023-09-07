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
    def find_by_type(self, type, start, count):
        result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.type == type) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 根据文章类型获取数量
    def get_count_by_type(self, type):
        count = db.session.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                                Article.type == type).count()
        return count

    # 根据文章标题进行模糊搜索
    def find_by_headline(self, headline, start, count):
        result = db.session.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, \
                    Article.headline.like('%' + headline + '%')).order_by(Article.articleid.desc()) \
            .limit(count).offset(start).all()
        return result

    # 统计搜索数
    def get_count_by_headline(self, headline):
        count = db.session.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                                Article.headline.like('%' + headline + '%')).count()
        return count

    # 最新文章
    def find_last_9(self):
        result = db.session.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.articleid.desc()).limit(9).all()
        return result

    # 最多阅读
    def find_most_9(self):
        result = db.session.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.readcount.desc()).limit(9).all()
        return result

    # 特别推荐，超过9篇则随机推荐9篇
    def find_recommended_9(self):
        result = db.session.query(Article.articleid, Article.headline). \
            filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(func.rand()).limit(9).all()
        return result

    # 一次返回上述3个数据
    def find_last_most_recommended(self):
        last = self.find_last_9()
        most = self.find_most_9()
        recommended = self.find_recommended_9()
        # 上述三个对象均为列表属性，但其内部元素类型为'sqlalchemy.engine.row.Row'
        # 无法直接进行jsonify操作
        return last, most, recommended

    # 每阅读一次，更新阅读次数
    def update_read_count(self, articleid):
        article = db.session.query(Article).filter_by(articleid=articleid).first()
        article.readcount += 1
        db.session.commit()

    # 根据文章ID查询标题
    def find_headline_by_id(self, articleid):
        row = db.session.query(Article.headline).filter_by(articleid=articleid).first()
        return row.headline

    # 获取当前文章的上一篇和下一篇
    def find_prev_next_by_id(self, articleid):
        dict = {}

        # 查询比当前文章编号小的文章中编号最大的一个为上一篇文章
        row = db.session.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                              Article.articleid < articleid).order_by(Article.articleid.desc())\
                                              .limit(1).first()

        # 如果未查询到相关文章，说明本文是第一篇，上一篇仍为当前文章
        if not row:
            prev_id = articleid
        else:
            prev_id = row.articleid

        dict['prev_id'] = prev_id
        dict['prev_headline'] = self.find_headline_by_id(prev_id)

        # 同理下一篇文章
        row = db.session.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
                                              Article.articleid > articleid).order_by(Article.articleid) \
                                              .limit(1).first()

        # 如果未查询到相关文章，说明本文是第一篇，上一篇仍为当前文章
        if not row:
            next_id = articleid
        else:
            next_id = row.articleid

        dict['next_id'] = next_id
        dict['next_headline'] = self.find_headline_by_id(next_id)

        return dict

    # 计算评论数
    def update_replycount(self, articleid):
        row = db.session.query(Article).filter_by(articleid=articleid).first()
        row.replycount += 1
        db.session.commit()

    # 插入文章
    def insert_article(self, type, headline, content, thumbnail, credit, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        userid = session.get('userid')
        article = Article(userid=userid, type=type, headline=headline, content=content, thumbnail=thumbnail,
                          credit=credit, drafted=drafted, checked=checked, createtime=now, updatetime=now)
        db.session.add(article)
        db.session.commit()
        return article.articleid    # 返回id方便跳转

    # 更新文章
    def update_article(self, articleid, type, headline, content, thumbnail, credit, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        row = db.session.query(Article).filter_by(articleid=articleid).first()
        row.type = type
        row.headline = headline
        row.content = content
        row.thumbnail = thumbnail
        row.credit = credit
        row.drafted = drafted
        row.checked = checked
        row.updatetime = now
        db.session.commit()
        return articleid

    # 查询文章表除草稿外的所有数据返回结果集，提供分页所需参数
    def find_all_except_draft(self, start, count):
        result = db.session.query(Article).filter(Article.drafted == 0).order_by(Article.articleid.desc()).limit(count)\
                            .offset(start).all()
        return result

    # 查询草稿外所有文章数
    def get_count_except_draft(self):
        total = db.session.query(Article).filter(Article.drafted == 0).count()
        return total

    # 文章分类查询，不含草稿
    def find_by_type_except_draft(self, type, start, count):
        if type == 0:
            result = self.find_all_except_draft(start, count)
            total = self.get_count_except_draft()
        else:
            result = db.session.query(Article).filter(Article.drafted == 0, Article.type == type)\
                                .order_by(Article.articleid.desc()).limit(count).offset(start).all()
            total = db.session.query(Article).filter(Article.drafted == 0,  Article.type == type).count()
        return result, total

    # 标题搜索，不含草稿，不分页
    def find_by_headline_except_draft(self, headline):
        result = db.session.query(Article).filter(Article.drafted == 0, Article.headline.like('%' + headline + '%'))\
                             .order_by(Article.articleid.desc()).all()
        return result

    # 切换文章的隐藏状态:1表示隐藏，0表示显示
    def switch_hidden(self, articleid):
        row = db.session.query(Article).filter_by(articleid=articleid).first()
        if row.hidden == 1:
            row.hidden = 0
        else:
            row.hidden = 1
        db.session.commit()
        return row.hidden  # 将当前最新状态返回给控制器层

    # 切换文章的推荐状态:1表示推荐，0表示正常
    def switch_recommended(self, articleid):
        row= db.session.query(Article).filter_by(articleid=articleid).first()
        if row.recommended == 1:
            row.recommended = 0
        else:
            row.recommended = 1
        db.session.commit()
        return row.recommended

    # 切换文章的审核状态: 1表示已审，0表示待审
    def switch_checked(self, articleid):
        row = db.session.query(Article).filter_by(articleid=articleid).first()
        if row.checked == 1:
            row.checked = 0
        else:
            row.checked = 1
        db.session.commit()
        return row.checked



if __name__ == '__main__':
    from app import app
    with app.app_context():
        data = (Article().query_article_id(2))
        print(data)
