'''用于定义首页内容'''
from common.pre_jsonify import pre_jsonify
from flask import Blueprint, jsonify

from modules.article import Article


index = Blueprint('index', __name__, static_url_path='/')

@index.route('/', methods=['GET'])
def home():
    '''处理首页内容'''
    query = Article().query_limits_join_users(0, 10)
    resp = []
    for articles, nickname in query:
        temp = pre_jsonify(articles)
        temp['nickname'] = nickname
        resp.append(temp)
    return jsonify(resp)