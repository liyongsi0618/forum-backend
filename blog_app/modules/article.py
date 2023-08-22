from sqlalchemy import Column, DateTime, Integer, MetaData, SmallInteger, String, Table, Text
from app import app, db


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

    # 根据articleid查询文章信息
    def query_article_id(self, articleid):
        result = db.session.query(Article).filter_by(articleid=articleid).first()
        return result


if __name__ == '__main__':
    with app.app_context():
        print(Article().query_article_id(2))
