import configparser
from operator import imod
import os
from data_manage import data_manage
from login_mmm import login_mmm
from calculate_manage import calculate_manage
#
from token_required import login_r
from flask import g
from flask import Flask
import json,time,datetime
from flask.scaffold import F
from datetime import datetime, date
from flask_cors import cross_origin
import numpy as np
from flask import render_template,request,jsonify
from queue import Queue
from threading import Thread
#导入数据库类
from flask_sqlalchemy import SQLAlchemy
from db_class import *
from flask_cors import CORS
#
from flask.json import JSONEncoder
#跨域
from flask import Response
#重写json格式化

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, obj)

def Response_headers(content):
    resp = Response(content)
    #返回数据添加头部信息
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

import pymysql
pymysql.install_as_MySQLdb()
import excel_2_sql
cf = configparser.ConfigParser()
cf.read("conf.ini")
mysql_uri = cf.get("mysql", "uri")
file_dir=cf.get("mysql", "file_path")
app = Flask(__name__,template_folder='templates',static_folder="static")
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.json_encoder = CustomJSONEncoder
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
CORS(app, supports_credentials=True)
app.secret_key = 'abc'

db.init_app(app)
#db = SQLAlchemy(app)


#反递归添加children
def find_id_max(data,id_max):
    id_max=id_max
    for d in data:
        if 'indicator_id' in d:
            id_max=max(id_max,d['indicator_id'])
        if 'children' in d:
            find_id_max(d['children'],id_max)
            
def fan_gao_list(sys_json,data_list,parent_id,pp_id_max):
    parent_id=parent_id
    data_list=data_list
    sort=1
    col_list=['create_by','create_time','field','indicator_name','profile','scope','summary','updateTime','update_by','weight']
    
    for sj in sys_json:

        row={
            'parentId':parent_id,
            'sort':sort
        }
        if 'indicator_id' in sj:
            indicator_id=sj['indicator_id']
            #sj['indicator_id']=indicator_id
            row['indicator_id']=indicator_id
            
        else:
            pp_id_max+=1
            indicator_id=pp_id_max
            row['indicator_id']=indicator_id
            sj['indicator_id']=indicator_id

        for col in col_list:
            if col in sj:
                row[col]=sj[col]
            else:
                row[col]=None

        
        data_list.append(row)
        sort+=1
    for sj in sys_json:
        if 'children' in  sj :
            if sj['children']:
                
                indicator_id=sj['indicator_id']
                fan_gao_list(sj['children'],data_list,indicator_id,pp_id_max)

    
#递归添加children
def gao_list(pp_list):
    parent_dict={}
    info_dict={}
    data_list=[]
    n=1
    for pp in pp_list:

        
        in_id=str(pp.indicator_id)
        parent_id=str(pp.parentId)
        #所有parentid 做dict
        if parent_id not in parent_dict:
            parent_dict[parent_id]=[]
            parent_dict[parent_id].append(in_id)
        else :
            parent_dict[parent_id].append(in_id)

        create_by=pp.create_by
        create_time=pp.create_time
        field=pp.field
        indicator_id=pp.indicator_id
        indicator_name=pp.indicator_name
        parentId=pp.parentId
        profile=pp.profile
        scope=pp.scope
        summary=pp.summary
        updateTime=pp.updateTime
        update_by=pp.update_by
        weight=pp.weight
        sort_v=pp.sort
        

        info_dict[str(in_id)]={
            'children':[],
            'create_by':create_by,
            'create_time':create_time,
            'field':field,
            'indicator_id':indicator_id,
            'indicator_name':indicator_name,
            'parentId':parentId,
            'profile':profile,
            'scope':scope,
            'summary':summary,
            'updateTime':updateTime,
            'update_by':update_by,
            'weight':weight,
            'sort':sort_v
        }
        n+=1

    pp_first=pp_list[0]
    index_first=str(pp_first.indicator_id)
    c_list=parent_dict[index_first]
    row=info_dict[index_first]
    add_children(row,c_list,info_dict,parent_dict)
    return jsonify([row])
        
def add_children(dd,c_list,info_dict,parent_dict):
    
    if  c_list==[]:
        return
    else:
        
        for cc in c_list:
            #if cc in parent_dict:
            child_row_info=info_dict[cc]
            try:
                dd['children'].append(child_row_info)
                
            except:
                pass
        dd_children_sort=sorted(dd['children'],key= lambda st : st['sort'])
        dd['children']=dd_children_sort
        for ddd in dd['children']:
            ddd_id=str(ddd['indicator_id'])
            if ddd_id in parent_dict:
                c_list_new=parent_dict[ddd_id]
                add_children(ddd,c_list_new,info_dict,parent_dict)
            else:
                continue


                
@app.route('/mxk/indicator/query/json/')

def json_show():
    if 'indicator_id' in request.values:
        indicator_id_v = request.values.get('indicator_id')
        pp=Mxk_indicator_system.query.filter_by(indicator_id=indicator_id_v).first()
        
        json_row=[{
            'create_by':pp.create_by,
            'create_time':pp.create_time,
            'indicator_id':pp.indicator_id,
            'indicator_name':pp.indicator_name,
            'parentId':pp.parentId,
            'profile':pp.profile,
            'summary':pp.summary,
            'updateTime':pp.updateTime,
            'update_by':pp.update_by,
            'weight':pp.weight            
        }]
        json_row=jsonify(json_row)
        return json_row
    else:
        field_v = request.values.get('field')
        scope_v = request.values.get('scope')
        pp_list=Mxk_indicator_system.query.filter_by(field=field_v,scope=scope_v).all()

        data_list=[]
        json_row=gao_list(pp_list)
    #for kk in info_dict:
    #    vv=info_dict[kk]
    #    in_id=vv['indicator_id']
#
    #    create_by=vv['create_by']
    #    create_time=vv['create_time']
    #    field=vv['field']
    #    indicator_name=vv['indicator_name']
    #    parentId=vv['parentId']
    #    profile=vv['profile']
    #    scope=vv['scope']
    #    summary=vv['summary']
    #    updateTime=vv['updateTime']
    #    update_by=vv['update_by']
    #    weight=vv['weight']

    
        return json_row
        
        #data_list.append(row)
        



@app.route('/mxk/indicator/query/list/')
#@login_r #必须登录的装饰器校验
def list_show():
    data_list=[]
    data_dict={'data':[]}
    pp_list=mxk_indicator_json.query.all()
    for pp in pp_list:
        row=[pp.field,pp.scope]
        if row not in data_list:
            data_list.append(row)


            pp_json=pp.indicator_system
            data_row_dict={
                'create_by': pp_json[0]['create_by'],
                'create_time': pp_json[0]['create_time'],
                'field': pp_json[0]['field'],
                'indicator_id': pp_json[0]['indicator_id'],
                'scope': pp_json[0]['scope'],
                'updateTime': pp.update_time,
                'update_by': pp_json[0]['update_by']
            }
            data_dict['data'].append(data_row_dict)
    data_dict['flag']='200'
    data_dict=jsonify(data_dict)
    return data_dict
#删除
@app.route('/mxk/indicator/del/', methods=[ 'GET'])
def del_indicator():
    try:
        field_v = request.args.get('field')
        scope_v = request.args.get('scope')
        del_sys_list=Mxk_indicator_system.query.filter_by(scope=scope_v,field=field_v).all()
        del_json=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
        
        db.session.delete(del_json)
        for del_sys in del_sys_list:
            db.session.delete(del_sys)
            
        
        return 'successful deleted!'
    except Exception as e:
        return str(e)

#修改指标

@app.route('/mxk/indicator/edit/', methods=[ 'GET','POST'])
def edit_indicator():
    
    if request.method == "GET":
        field_v = request.args.get('field')
        scope_v = request.args.get('scope')
        if 'submit' not in request.args:
            F5_v = request.args.get('F5')

            db.session.commit()
            pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()

            #print(pp)
            
            while not pp:
                db.session.commit()
                pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
                
            indicator_system_json=pp.indicator_system
            json_row=[{'indicator_system':json.dumps(indicator_system_json)}]
            json_row=jsonify(json_row)
            #json_row = Response_headers(json_row)

            return json_row
        else:#sys最大id
            try:
                pp_id_max=Mxk_indicator_system.query.order_by(Mxk_indicator_system.indicator_id.desc()).first().indicator_id
            except:
                pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
                while not pp:
                    db.session.commit()
                    pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
                indicator_system_json=pp.indicator_system
                pp_id_max=find_id_max(indicator_system_json,1)
            old_sys_list=Mxk_indicator_system.query.filter_by(scope=scope_v,field=field_v).all()
            for old_sys in old_sys_list:
                db.session.delete(old_sys)
            db.session.commit()
            
            
            pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
            while not pp:
                db.session.commit()
                pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()

            indicator_system_json=pp.indicator_system
            data_list=[]
            
            fan_gao_list(indicator_system_json,data_list,None,pp_id_max)
            #确认修改 写入sys
            for row in data_list:
                #row=[create_by,create_time,field,indicator_id,indicator_name,parentId,profile,scope,summary,updateTime,update_by,weight,sort]
                indicator_id_v=row['indicator_id']
                field_v=row['field']
                scope_v=row['scope']
                indicator_name_v=row['indicator_name']
                profile_v=row['profile']
                summary_v=row['summary']
                parentId_v=row['parentId']
                sort_v=row['sort']
                weight_v=row['weight']
                create_by_v=row['create_by']
                create_time_v=row['create_time']
                updateTime_v=row['updateTime']
                update_by_v=row['update_by']
                
                

                json_add=Mxk_indicator_system(indicator_id=indicator_id_v,field=field_v,scope=scope_v,indicator_name=indicator_name_v,profile=profile_v,summary=summary_v,parentId=parentId_v,sort=sort_v,weight=weight_v,create_by=create_by_v,create_time=create_time_v,updateTime=updateTime_v,update_by=update_by_v)  
                db.session.add(json_add)
            db.session.commit()
            return '保存成功'


            


    if request.method == "POST":
        args = request.json
        indicator_system_json=args[0]
        scope_v=indicator_system_json['scope']
        field_v=indicator_system_json['field']
        

        
        #json_delete=mxk_indicator_json.query.filter_by(field=field_v,scope=scope_v)  
        pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
        create_time_v=pp.create_time
        create_by_v=pp.create_by
        if create_time_v:
            pass
            
        else:
            create_time_v='2021-08-30 15:22:24'
        id_old=pp.id
        type_old=pp.type
        year_old=pp.year
        
        is_delete_old=pp.is_delete


        db.session.delete(pp)
        db.session.commit()

        updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        update_by_v='user2'
        indicator_system_json['update_time']=updateTime
        indicator_system_json['update_by']=update_by_v
        args=[indicator_system_json]
        json_add=mxk_indicator_json(id=id_old,type=type_old,year=year_old,is_delete=is_delete_old,field=field_v,scope=scope_v,create_time=create_time_v,create_by=create_by_v,update_time=updateTime,update_by=update_by_v,indicator_system=args)  
        db.session.add(json_add)
        db.session.commit()

        return "json update successd  --  edit"

#新建指标
@app.route('/mxk/indicator/add/', methods=['POST','GET'])
def add_indicator():
    if request.method=='GET':
        field_v = request.args.get('field')
        scope_v = request.args.get('scope')
        file_moren=file_dir+'moren/'
        file_list=os.listdir(file_moren)
        tar_file_name=file_moren+'model.xlsx'
        for file in file_list:
            if field_v in file:
                tar_file_name=file_moren+file
                break

        file_path=tar_file_name
        args_field = field_v.strip()
        args_scope = scope_v.strip()
        #--------------------
        pp=mxk_indicator_json.query.filter_by(field=args_field,scope=args_scope).first()

        sta = pp
        if sta is True:
            #旧数据处理
            #sta = mysql_operation.delete_indicator_list(Condition)
            #返回结果给前端
            return "The old data exists"

        data_list = excel_2_sql.add_2_sql(field_v,scope_v,file_path)
        dd0=data_list[0]
        scope0=dd0[4]
        field0=dd0[1]
        pp=Mxk_indicator_system.query.filter_by(field=field0,scope=scope0).first()
        if pp:
            sta=='system data exist!'
        else:
            n=1
            for dd in data_list:
                sort_v=n

                n+=1
                indid=dd[2]
                indi_name=dd[0]
                scope_v=dd[4]
                field_v=dd[1]
                parent_id=dd[3]
                if np.isnan(parent_id):
                    parent_id=None



                create_by='user1'
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                update_by='user1'



                mxk_indicator_system_1=Mxk_indicator_system(sort=sort_v,create_by=create_by,create_time=create_time,updateTime=updateTime,update_by=update_by,indicator_id=indid,indicator_name=indi_name,field=field_v,scope=scope_v,parentId=parent_id)  
                db.session.add(mxk_indicator_system_1)
            db.session.commit()
            pp_list=Mxk_indicator_system.query.filter_by(field=args_field,scope=args_scope).all()

            json_row=gao_list(pp_list)



            pp=mxk_indicator_json.query.filter_by(field=args_field,scope=args_scope).first()
            try:
                pp_id_max=mxk_indicator_json.query.order_by(mxk_indicator_json.id.desc()).first().id
            except:
                pp_id_max=0
            if not pp:
                id_new=pp_id_max+1
                create_by='user1'
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                update_by='user1'
                mxk_indicator_json_1=mxk_indicator_json(create_by=create_by,create_time=create_time,update_time=updateTime,update_by=update_by,id=id_new,field=args_field,scope=args_scope,indicator_system=json_row.json)  
                db.session.add(mxk_indicator_json_1)
            else:
                result=mxk_indicator_json.query.filter_by(field=args_field,scope=args_scope).first()
                result.indicator_system = json_row

            db.session.commit()
            sta='ok'  


        if sta == 'ok':
            sta = 'add successd'
        else:
            sta =  'add failed'
        return sta
        #查询需要转存的数据
    elif request.method=='POST':
        app.logger.info('indicator add start')

        args = (request.form.to_dict())
        if args.get('field')  is None:
            return "The parameter 'field' is missing  --  indicator/add/"
        elif args.get('scope')  is None:
            return "The parameter 'scope' is missing  --  indicator/add/"

        #接收excle文件并保存到指定路径
        file = request.files.get('file')
        if file is None:
            return "No files were received that needed to be uploaded"

        file_path = file_dir+'mxk/' + file.filename
        #print(file,type(file),'/n',dir(file),'/n',request.files)
        #print(file.filename,type(file.filename))
        file.save(file_path)

        #查询是否存在同名指标数据，如果存在，直接更新还是返回结果给前端，跳到修改页面

        #query_json = "WHERE field = '{}' AND scope = '{}'  ".format(args['field'],args['scope']) 

        old_query_arg = {}
        #arg["table"] = "json"
        args_field = args['field'].strip()
        args_scope = args['scope'].strip()
        #--------------------
        pp=mxk_indicator_json.query.filter_by(field=args_field,scope=args_scope).first()

        sta = pp
        if sta is True:
            #旧数据处理
            #sta = mysql_operation.delete_indicator_list(Condition)
            #返回结果给前端
            return "The old data exists"

        data_list = excel_2_sql.add_2_sql(args['field'],args['scope'],file_path)
        dd0=data_list[0]
        scope0=dd0[4]
        field0=dd0[1]
        pp=Mxk_indicator_system.query.filter_by(field=field0,scope=scope0).first()
        if pp:
            sta=='system data exist!'
        else:
            n=1
            for dd in data_list:
                sort_v=n

                n+=1
                indid=dd[2]
                indi_name=dd[0]
                scope_v=dd[4]
                field_v=dd[1]
                parent_id=dd[3]
                if np.isnan(parent_id):
                    parent_id=None



                create_by='user1'
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                update_by='user1'



                mxk_indicator_system_1=Mxk_indicator_system(sort=sort_v,create_by=create_by,create_time=create_time,updateTime=updateTime,update_by=update_by,indicator_id=indid,indicator_name=indi_name,field=field_v,scope=scope_v,parentId=parent_id)  
                db.session.add(mxk_indicator_system_1)
            db.session.commit()
            pp_list=Mxk_indicator_system.query.filter_by(field=args_field,scope=args_scope).all()

            json_row=gao_list(pp_list)



            pp=mxk_indicator_json.query.filter_by(field=args_field,scope=args_scope).first()
            try:
                pp_id_max=mxk_indicator_json.query.order_by(mxk_indicator_json.id.desc()).first().id
            except:
                pp_id_max=0
            if not pp:
                id_new=pp_id_max+1
                create_by='user1'
                create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                update_by='user1'
                mxk_indicator_json_1=mxk_indicator_json(create_by=create_by,create_time=create_time,update_time=updateTime,update_by=update_by,id=id_new,field=args_field,scope=args_scope,indicator_system=json_row.json)  
                db.session.add(mxk_indicator_json_1)
            else:
                result=mxk_indicator_json.query.filter_by(field=args_field,scope=args_scope).first()
                result.indicator_system = json_row

            db.session.commit()
            sta='ok'  


        if sta == 'ok':
            sta = 'add successd'
        else:
            sta =  'add failed'
        return sta
        #查询需要转存的数据
        
    



    
if __name__ == '__main__':
    app.register_blueprint(calculate_manage,url_prefix='/calculate_manage')
    app.register_blueprint(data_manage,url_prefix='/data_manage')
    app.register_blueprint(login_mmm,url_prefix='/login_mmm')
    app.run(port=9095,host='0.0.0.0')
 