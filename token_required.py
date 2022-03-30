import functools
from flask import request,jsonify,current_app,session
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from db_class import Users




def login_r(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            #在请求头上拿到token
            if_login=session.get('login_in')
        except Exception:
            #没接收的到token,给前端抛出错误
            #这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code = 4103,msg = '未登录')
        
        

        if if_login:
            return view_func(*args,**kwargs)
        else:
            return jsonify(code = 4103,msg = "未登录")

        

    return verify_token