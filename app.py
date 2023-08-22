from flask_sqlalchemy import SQLAlchemy
from blog_app import create_app

import pymysql
pymysql.install_as_MySQLdb()

app = create_app()

if __name__ == '__main__':
    # from controllers.article import article

    # app.register_blueprint(article)

    app.run(debug=True)
