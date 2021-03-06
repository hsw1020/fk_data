import json
from flask import Blueprint,make_response
from db_class import *
from flask import render_template,request,jsonify
login_mmm = Blueprint('login_mmm',__name__)
import time
import base64
import hmac
from token_required import *



#注册接口
@login_mmm.route('/register',methods=['POST'])
def register():
    username = request.form.get('username')
    pwd = request.form.get('password')
    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user_exist=Users.query.filter_by(name=username).first()
    if user_exist:
        result ={
            'status':'username is existed!'
        }
    else:
        
        user_add=Users(name=username,create_time=create_time)
        user_add.hash_password(pwd)
        db.session.add(user_add)
        db.session.commit()
        result ={
            'status':'user created!'
        }


    return result



@login_mmm.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    token=''
    obj = Users.query.filter_by(name=username).first()
    if not obj:
        result={
            'status':'未找到该用户'
        }
        code_fan=401
    else:    
        if obj.verify_password(password):
            s = Serializer(current_app.config["SECRET_KEY"],expires_in=36000)
            token = s.dumps({"id":username}).decode("ascii")

            
            result={
                'status':'登录成功',
            }
            code_fan=200
        else:
            result={
                'status':'密码错误'
            }
            code_fan=402
        data={
            'code':code_fan,
            'msg':result
        }
    
    res=make_response(json.dumps(data))
    res.set_cookie('x_gorgan',token)
    res.mimetype='application/json'
    return res