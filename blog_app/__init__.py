"""
    应用工厂创建Flask实例，完成实例的配置，返回实例app
"""

from flask import Flask
import os
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

# 创建db对象
db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='mysql://root:123456@mysql:3306/blog_app?charset=utf8',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 通过app的config连接数据库
    db.init_app(app)

    CORS(app, supports_credentials=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from controllers.article import article
    from controllers.index import index

    app.register_blueprint(article)
    app.register_blueprint(index)


    return app
