def pre_jsonify(data):
    ''' 
    对module查询数据进行预处理，使其可以进一步利用jsonify函数转为json数据格式.
    返回一个k:v类型
    '''
    dict_data = {}
    for k, v in data.__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict_data[k] = v
    return dict_data