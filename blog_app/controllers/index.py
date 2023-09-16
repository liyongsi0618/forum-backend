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

@index.route('/page/page-count', methods=['GET'])
def page_count():
    article = Article()
    total_page = math.ceil(article.get_total_page() / 10)
    return jsonify(total_page)

@index.route('/page/<int:page>', methods=['GET'])
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

@index.route('/type/page-count/<int:type>', methods=['GET'])
def type_page_count(type):
    article = Article()
    total_page = math.ceil(article.get_count_by_type(type) / 10)
    return jsonify(total_page)

@index.route('/type/<int:type>-<int:page>', methods=['GET'])
def classify(type, page):
    start = (page - 1) * 10
    article = Article()
    query = article.query_by_type(type, start, 10)
    
    resp = []
    for articles, nickname in query:
        temp = pre_jsonify(articles)
        temp['nickname'] = nickname
        resp.append(temp)
    return jsonify(resp)

@index.route('/search/<search_word>', methods=['GET'])
def search(search_word):
    search_word = search_word.strip()
    if  search_word == '' or '%' in search_word or len(search_word) > 10 or len(search_word) < 2:
        return "搜索词长度需在2至10个字符内，且不应包含%"
    else:
        article = Article()
        query = article.query_by_search(search_word)
        resp = []
        for articles, nickname in query:
            temp = pre_jsonify(articles)
            temp['nickname'] = nickname
            resp.append(temp)
        return jsonify(resp)

@index.route('/latest', methods=['GET'])
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

@index.route('/most-read', methods=['GET'])
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

@index.route('/recommend', methods=['GET'])
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