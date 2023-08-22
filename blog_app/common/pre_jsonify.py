def pre_jsonify(data):
    ''' 对module查询数据进行预处理，使其可以进一步利用jsonify函数转为json数据格式 '''
    ret = []
    # # 解析每条数据
    # for row in data:
    #     # 字典包装数据
    dict = {}
    for k, v in data.__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    ret.append(dict)
    return ret