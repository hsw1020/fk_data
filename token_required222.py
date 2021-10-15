from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request,jsonify,current_app
from db_class import Users
import functools

def create_token(user):
    s=Serializer(current_app.config['SECRET_KEY'],expires_in=36000)
    token=s.dumps({'user_name':user})
    return token

def login_r(func):
    @functools.wraps(func)
    def verify_token(*args,**kwargs):
        try:
            token_v=request.headers['z_token']
        except:
            return jsonify(code=4001,msg='token缺失！')
        
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            s.loads(token_v)
        except:
            return jsonify(code=4002,msg='token已失效')
        
        return func(*args,**kwargs)
    return verify_token

