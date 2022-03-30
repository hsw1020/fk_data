import functools
from flask import request,jsonify,current_app,session
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from db_class import Users



def login_r(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        if_login=session.get('login_in')
        print(if_login)
        if if_login:
            return view_func(*args,**kwargs)
        else:
            return jsonify(code = 4101,msg = "登录已过期")

        

    return verify_token