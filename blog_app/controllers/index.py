'''用于定义首页内容'''
import math
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

@index.route('/page/page-count')
def page_count():
    article = Article()
    total_page = math.ceil(article.get_total_page() / 10)
    return jsonify(total_page)

@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 10
    article = Article()
    query = article.query_limits_join_users(start, 10)
    
    resp = []
    for articles, nickname in query:
        temp = pre_jsonify(articles)
        temp['nickname'] = nickname
        resp.append(temp)
    return jsonify(resp)


@index.route('/type/<int:type>-<int:page>')
def classify(type, page):
    start = (page - 1) * 10
    article = Article()
    result = article.find_by_type(type, start, 10)
    total = math.ceil(article.get_count_by_type(type) / 10)
    return


@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    keyword = keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword) > 10:
        abort(404)

    article = Article()
    start = (page - 1) * 10
    result = article.find_by_headline(keyword, start, 10)
    total = math.ceil(article.get_count_by_headline(keyword) / 10)
    return 


@index.route('/recommend')
def recommend():
    article = Article()
    last, most, recommended = article.find_last_most_recommended()
    # 上述三个对象均为列表属性，但其内部元素类型为'sqlalchemy.engine.row.Row'
    # 无法直接进行jsonify操作
    # 使用自定义函数进行处理
    last_prejson, most_prejson, recommended_prejson = pre_jsonify2(last), pre_jsonify2(most), pre_jsonify2(recommended),
    return jsonify(last_prejson, most_prejson, recommended_prejson)