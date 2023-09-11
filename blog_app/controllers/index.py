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
        # abort(404)
        pass

    article = Article()
    start = (page - 1) * 10
    result = article.find_by_headline(keyword, start, 10)
    total = math.ceil(article.get_count_by_headline(keyword) / 10)
    return 


@index.route('/latest')
# 最新文章信息，id及headline
def latest():
    article = Article()
    results = article.query_latest_9()
    lst = []
    for data in results:
        temp = {}
        temp['articleid'], temp['headline'] = data
        lst.append(temp)
    return jsonify(lst)


@index.route('/most-read')
# 最多阅读文章信息，id及headline
def most_read():
    article = Article()
    results = article.query_most_read_9()
    lst = []
    for data in results:
        temp = {}
        temp['articleid'], temp['headline'] = data
        lst.append(temp)
    return jsonify(lst)

@index.route('/recommend')
# 编辑推荐文章信息，id及headline
def recommend():
    article = Article()
    results = article.query_recommended_9()
    lst = []
    for data in results:
        temp = {}
        temp['articleid'], temp['headline'] = data
        lst.append(temp)
    return jsonify(lst)