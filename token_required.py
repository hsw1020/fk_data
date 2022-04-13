import functools
from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from db_class import Users



def login_r(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        x_gorgan=request.cookies.get('x_gorgan')
        s = Serializer(current_app.config["SECRET_KEY"])
        
        try:
            s.loads(x_gorgan)
            return view_func(*args,**kwargs)
        except:
            return jsonify(code = 4101,msg = "登录已过期")

        

    return verify_token