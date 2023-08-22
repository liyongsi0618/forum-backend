from common.pre_jsonify import pre_jsonify
from flask import Blueprint, jsonify


article = Blueprint('article', __name__, static_url_path='/')


from modules.article import Article

@article.route('/article/<int:articleid>', methods=['GET'])
def get_article(articleid):
    result = Article().query_article_id(articleid)
    return jsonify(pre_jsonify(result))

