from flask_sqlalchemy import SQLAlchemy
from blog_app import create_app

import pymysql
pymysql.install_as_MySQLdb()

app = create_app()


db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)
