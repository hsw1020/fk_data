import configparser
import model_manage
from settings import config
from Utils.recursion import *
import os
from flask.helpers import make_response, send_from_directory
from login_mmm import login_mmm
from model_manage.model import model_manage
from data_calculate.calculate_manage import calculate_manage
from bianzhi_manage.bianzhi import bianzhi_manage
#
from report_manage.report_manage import report_manage
from user_manage.user_manage import user_manage
from tongji_manage.tongji_manage import tongji_manage

from base_manage.base_manage import base_manage
from data_manage.data_manage import data_manage
from weight_manage.weight_manage import weight_manage
from fenxi_manage.fenxi_manage import fenxi_manage
from token_required import login_r
from flask import g
from flask import Flask
import json,time,datetime
from datetime import  date
from flask_cors import cross_origin
import numpy as np
from flask import render_template,request,jsonify
#导入数据库类
from db_class import *
from flask_cors import CORS
#
#跨域
from flask import Response
#重写json格式化




from Utils.excel_2_sql0  import dtest,gao
cf = configparser.ConfigParser()
cf.read("conf.ini")
mysql_uri = cf.get("mysql", "uri")
file_dir=cf.get("mysql", "file_path")

app = Flask(__name__,template_folder='templates',static_folder="static")
app.config.from_object(config.get('production','production'))
CORS(app, supports_credentials=True)
app.secret_key = 'abc'

db.init_app(app)

#反递归添加children
         
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


    
        return json_row

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
                'updateTime':pp.update_time.strftime('%Y-%m-%d %H:%M:%S'),
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
        del_value_list=mxk_value.query.filter_by(scope=scope_v,field=field_v).all()
        del_measure_list=mxk_measure.query.filter_by(scope=scope_v,field=field_v).all()
        del_fenxi_list=mxk_analysis.query.filter_by(scope=scope_v,field=field_v).all()
        db.session.delete(del_json)
        for del_sys in del_sys_list:
            db.session.delete(del_sys)
        for del_value in del_value_list:
            db.session.delete(del_value)
        for del_measure in del_measure_list:
            db.session.delete(del_measure)    
        for del_fenxi in del_fenxi_list:
            db.session.delete(del_fenxi)  
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
            nn=1
            while not pp and nn<10:
                db.session.commit()
                pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
                time.sleep(0.5)
                nn+=1
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
                nn=1
                while not pp and nn<10:
                    db.session.commit()
                    pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
                    time.sleep(0.5)
                    nn+=1
                indicator_system_json=pp.indicator_system
                pp_id_max=find_id_max(indicator_system_json,1)
            old_sys_list=Mxk_indicator_system.query.filter_by(scope=scope_v,field=field_v).all()
            for old_sys in old_sys_list:
                db.session.delete(old_sys)
            db.session.commit()
            
            
            pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
            nn2=1
            while not pp and nn2<10:
                db.session.commit()
                pp=mxk_indicator_json.query.filter_by(scope=scope_v,field=field_v).first()
                time.sleep(0.5)
                nn2+=1
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

        l1_indicators=indicator_system_json['children']
        l1_indicators_name=[]
        l2_indicators_name=[]
        l3_indicators_name=[]
        l2_indicators=[]
        for ll in l1_indicators:
            l1_indicators_name.append(ll['indicator_name'])
            if 'children' in ll:
                childrens=ll['children']
                for cc in childrens:
                    l2_indicators.append(cc)
        l3_indicators=[]
        for ll in l2_indicators:
            l2_indicators_name.append(ll['indicator_name'])
            if 'children' in ll:
                childrens=ll['children']
                for cc in childrens:
                    l3_indicators.append(cc)
        for ll in l3_indicators:
            l3_indicators_name.append(ll['indicator_name'])
        sumary_text_l1=''
        for l1 in l1_indicators_name:
            sumary_text_l1+=l1+'、'
        sumary_text_l1=sumary_text_l1.strip('、')
        sumary_l1_num=len(l1_indicators_name)
        sumary_l2_num=len(l2_indicators_name)
        sumary_l3_num=len(l3_indicators_name)

        sumary_text=f'{field_v}的评估指标，包括{sumary_text_l1}等{sumary_l1_num}个一级指标，{sumary_l2_num}个二级指标，{sumary_l3_num}个三级指标。'


        indicator_system_json['summary']=sumary_text
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
        create_by='user1'
        file_moren=file_dir+'moren/'
        file_list=os.listdir(file_moren)
        tar_file_name=file_moren+'model_默认.xlsx'
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
        try:
            dtest=dtest(file_path)
            if len(dtest)>0:
                sta='出现重复指标项：{}'.format(dtest)
                return jsonify(code=401,msg=sta) 
            data_list = gao(file_path,args_field,args_scope,create_by)
            if len(data_list)==0:
                sta='file err!'
                return jsonify(code=400,msg=sta) 
        except:
            sta='file err!'
            return jsonify(code=400,msg=sta) 
        dd0=data_list[0]
        scope0=dd0[4]
        field0=dd0[1]
        pp=Mxk_indicator_system.query.filter_by(field=field0,scope=scope0).first()
        if pp:
            sta=='system data exist!'
            return jsonify(code=400,msg=sta)
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
            return jsonify(code=400,msg="The parameter 'field' is missing  --  indicator/add/")
        elif args.get('scope')  is None:
            return jsonify(code=400,msg="The parameter 'scope' is missing  --  indicator/add/") 

        #接收excle文件并保存到指定路径
        file = request.files.get('file')
        if file is None:
            return jsonify(code=400,msg="No files were received that needed to be uploaded") 
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
        create_by='user1'
        #--------------------
        pp=mxk_indicator_json.query.filter_by(field=args_field,scope=args_scope).first()

        sta = pp
        if sta is True:
            #旧数据处理
            #sta = mysql_operation.delete_indicator_list(Condition)
            #返回结果给前端
            return jsonify(code=400,msg="The old data exists") 
            
        try:
            dtest=dtest(file_path)
            if len(dtest)>0:
                sta='出现重复指标项：{}'.format(dtest)
                return jsonify(code=401,msg=sta) 
            data_list = gao(file_path,args_field,args_scope,create_by)
            data_list_type=type(data_list)
            if data_list_type==int:
                return jsonify(code=405,msg='导入的文件中指标与评价主题/评价对象重名，请重命名该指标名称。') 
            elif len(data_list) ==0:
                sta='file err!'
                return jsonify(code=400,msg=sta) 
            
            
        except Exception as e :
            sta='file err!'
            return jsonify(code=400,msg=sta) 
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


            indicator_l0 =Mxk_indicator_system.query.filter_by(field=args_field,indicator_name=args_field).first()
            indicator_l0_id=str(indicator_l0.indicator_id)
            
            pp_list=Mxk_indicator_system.query.filter_by(field=args_field,scope=args_scope).all()
            indicator_l1_id=[]
            indicator_l2_id=[]
            indicator_l3_id=[]
            indicator_l1_name=[]
            indicator_l2_name=[]
            indicator_l3_name=[]
            for pp in pp_list:
                pp_id= str(pp.indicator_id)
                pp_parent_id=pp.parentId
                pp_name=pp.indicator_name
                if pp_parent_id==indicator_l0_id:
                    indicator_l1_id.append(pp_id)
                    indicator_l1_name.append(pp_name)
            for pp in pp_list:
                pp_id= str(pp.indicator_id)
                pp_parent_id=pp.parentId
                pp_name=pp.indicator_name
                if pp_parent_id in indicator_l1_id:
                    indicator_l2_id.append(pp_id)
                    indicator_l2_name.append(pp_name)
            for pp in pp_list:
                pp_id= str(pp.indicator_id)
                pp_parent_id=pp.parentId
                pp_name=pp.indicator_name
                if pp_parent_id in indicator_l2_id:
                    indicator_l3_name.append(pp_name)

                sumary_text_l1=''
                for l1 in indicator_l1_name:
                    sumary_text_l1+=l1+'、'
                sumary_text_l1=sumary_text_l1.strip('、')
                sumary_l1_num=len(indicator_l1_name)
                sumary_l2_num=len(indicator_l2_name)
                sumary_l3_num=len(indicator_l3_name)

                sumary_text=f'{args_field}的评估指标，包括{sumary_text_l1}等{sumary_l1_num}个一级指标，{sumary_l2_num}个二级指标，{sumary_l3_num}个三级指标。'
            
            indicator_l0 =Mxk_indicator_system.query.filter_by(field=args_field,indicator_name=args_field).first()
            indicator_l0.summary=sumary_text
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
            return jsonify(code=200,msg=sta)
        else:
            sta =  'add failed'
            return jsonify(code=400,msg=sta)
        
        
        #查询需要转存的数据
        
@app.route('/mxk/indicator/value_down')
def value_down():
    field_v = request.args.get('field')
    #scope_v = request.args.get('scope')
    if '规模结构' in field_v:
        filename='model_规模结构.xlsx'
    elif '军费预算' in field_v:
        filename='model_军费预算.xlsx'

    elif '媒体力量' in field_v:
        filename='model_媒体力量.xlsx'

    else:
        filename='model_默认.xlsx'
    
    
    filepath= file_dir+'moren/'
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')

    response = make_response(send_from_directory(filepath, filename, as_attachment=True))

    response.headers["Content-Disposition"] = "attachment; filename={}".format(filepath.encode().decode('latin-1'))

    return send_from_directory(filepath, filename, as_attachment=True)




    
if __name__ == '__main__':
    app.register_blueprint(calculate_manage,url_prefix='/mxk/calculate_manage')
    app.register_blueprint(data_manage,url_prefix='/mxk/data_manage')
    app.register_blueprint(login_mmm,url_prefix='/mxk/login_mmm')
    app.register_blueprint(model_manage,url_prefix='/mxk/model_manage')
    app.register_blueprint(bianzhi_manage,url_prefix='/mxk/bianzhi_manage')
    app.register_blueprint(user_manage,url_prefix='/mxk/user_manage')
    app.register_blueprint(weight_manage,url_prefix='/mxk/weight_manage')
    app.register_blueprint(fenxi_manage,url_prefix='/mxk/fenxi_manage')
    app.register_blueprint(base_manage,url_prefix='/mxk/base_manage')
    app.register_blueprint(report_manage,url_prefix='/mxk/report_manage')
    app.register_blueprint(tongji_manage,url_prefix='/mxk/tongji_manage')
    app.run(port=9095,host='0.0.0.0')
 