from flask import Blueprint


article = Blueprint('article', __name__)

@article.route
def get_article():
    