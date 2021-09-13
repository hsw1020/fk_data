import configparser
import json,time
from logging import exception
from flask import Blueprint
from flask.helpers import make_response, send_from_directory
from db_class import *
from flask import render_template,request,jsonify
data_manage = Blueprint('data_manage',__name__)
from .value_import import gao
cf = configparser.ConfigParser()
cf.read("./conf.ini")
file_dir=cf.get("mysql", "file_path")

country_dict={
    '1':'美国',
    '2':'俄罗斯',
    '3':'台湾',
    '4':'日本',
    '5':'韩国',
    '6':'朝鲜',
    '7':'印度',
    '8':'菲律宾',
    '9':'越南',
    '10':'中国',
    '11':'澳大利亚',
    '12':'孟加拉国',
    '13':'文莱',
    '14':'柬埔寨',
    '15':'印度尼西亚',
    '16':'老挝',
    '17':'马来西亚',
    '18':'蒙古',
    '19':'缅甸',
    '20':'尼泊尔',
    '21':'新西兰',
    '22':'巴基斯坦',
    '23':'巴布亚新几内亚',
    '24':'新加坡',
    '25':'斯里兰卡',
    '26':'泰国'
}
fan_country_dict={
    '美国':'1',
    '俄罗斯':'2',
    '台湾':'3',
    '日本':'4',
    '韩国':'5',
    '朝鲜':'6',
    '印度':'7',
    '菲律宾':'8',
    '越南':'9',
    '中国':'10',
    '澳大利亚':'11',
    '孟加拉国':'12',
    '文莱':'13',
    '柬埔寨':'14',
    '印度尼西亚':'15',
    '老挝':'16',
    '马来西亚':'17',
    '蒙古':'18',
    '缅甸':'19',
    '尼泊尔':'20',
    '新西兰':'21',
    '巴基斯坦':'22',
    '巴布亚新几内亚':'23',
    '新加坡':'24',
    '斯里兰卡':'25',
    '泰国':'26'
}
@data_manage.route('/add', methods=['POST'])
def add():

    args = (request.form.to_dict())
    args_field = args['field'].strip()
    args_scope = args['scope'].strip()
    args_year = args['year'].strip()
    user_name='wsh'
    #接收excle文件并保存到指定路径
    file = request.files.get('file')
    file_path = file_dir+'mxk_value/' + file.filename
    #print(file,type(file),'/n',dir(file),'/n',request.files)
    #print(file.filename,type(file.filename))
    file.save(file_path)
    result=gao(file_path, args_year, args_field, args_scope, user_name)
    return jsonify(result)

@data_manage.route('/import_field_list')
def import_field_list():
    fs=[]
    data_dict={}
    pp_list=Mxk_indicator_system.query.all()
    for pp in pp_list:
        field=pp.field
        scope=pp.scope
        fs_str=field+scope
        
        if not fs_str in fs:

            if not field in data_dict:
                data_dict[field]=[]

            data_dict[field].append(scope)
            fs.append(fs_str)
        else:
            continue
    return jsonify(code=200,msg='ok',data=data_dict)

@data_manage.route('/list_detail_year')
def list_detail_year():

    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')
    pp_list=mxk_value.query.filter_by(field=field_v,scope=scope_v,year=year_v).all()
    
    data_country_dict={}
    for pp in pp_list:
        region_name=country_dict[pp.region_code]
        org_name=pp.org_name
        if org_name:
            if org_name not in data_country_dict:
                data_country_dict[org_name]={'国家名':region_name,'机构名':org_name}
            indicator_name=pp.indicator_name
            indicator_name=indicator_name.replace('[','【')
            indicator_name=indicator_name.replace(']','】')
            #if '[' in indicator_name:
            #    indicator_name_1=indicator_name.split('[')[0]
            #    indicator_name_2=indicator_name.split(']')[1]
            #    indicator_name=indicator_name_1+indicator_name_2
            indicator_value=pp.indicator_value
            
            data_country_dict[org_name][indicator_name]=indicator_value
        else:
            if region_name not in data_country_dict:
                data_country_dict[region_name]={'国家名':region_name,'机构名':region_name}
            indicator_name=pp.indicator_name
            indicator_name=indicator_name.replace('[','【')
            indicator_name=indicator_name.replace(']','】')
            #if '[' in indicator_name:
            #    indicator_name_1=indicator_name.split('[')[0]
            #    indicator_name_2=indicator_name.split(']')[1]
            #    indicator_name=indicator_name_1+indicator_name_2
            indicator_value=pp.indicator_value
            data_country_dict[region_name][indicator_name]=indicator_value

        


    data_list=[]
    for dd in data_country_dict:
        data_list.append(data_country_dict[dd])
    resutl={
        'data':data_list,
        'status':'ok',
        'total':len(data_list),
        'pagesize':10
    }
    resutl=jsonify(resutl)
    return resutl

@data_manage.route('/list_detail')
def list_detail():
    year_list=[]
    data_list=[]
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    pp_list=mxk_value.query.filter_by(field=field_v,scope=scope_v).all()
    for pp in pp_list:
        year_v=pp.year
        if not year_v in year_list:
            create_by=pp.create_by
            create_time=pp.create_time
            update_by=pp.update_by
            update_time=pp.update_time
            row={
                'id':pp.id,
                'create_by':create_by,
                'create_time':create_time,
                'update_by':update_by,
                'update_time':update_time,
                'year_v':year_v
                
            }
            year_list.append(year_v)
            data_list.append(row)

    data={
        'data':data_list,
        'status':'ok'
    } 
    return jsonify(data)
@data_manage.route('/list')
def list():
    #field_v = request.args.get('field')
    #scope_v = request.args.get('scope')
    json_row={
            'status':'ok',
            'data':[]
        }
    fs_list=[]
    data_list=[]
    pp_list=mxk_value.query.order_by(mxk_value.update_time.desc()).all()
    for pp in pp_list:
        field_v=pp.field
        scope_v=pp.scope
        year_v=pp.year
        fs_year=field_v+scope_v+year_v
        if fs_year not in fs_list:
            data_list.append(pp)
            fs_list.append(fs_year)
    for data in data_list:
        #id_v=data.id
        field_v=data.field
        scope_v=data.scope
        update_by_v=data.update_by
        update_time_v=data.update_time
        year_v=data.year
        row={
            #'id':id_v,
            'field':field_v,
            'scope':scope_v,
            'update_by':update_by_v,
            'update_time':update_time_v,
            'year':year_v
        }
        json_row['data'].append(row)
    total_rows=len(data_list)
    json_row['total']=total_rows
    json_row['pagesize']=10
    json_row=jsonify(json_row)
    return json_row


#修改
@data_manage.route('/edit', methods=['POST'])
def dan_edit():
    org_name=request.form['org_name']
    region_name=request.form['region_name']
    if org_name==region_name:
        org_name=None
    indicator_name=request.form['indicator_name']

    indicator_name=indicator_name.replace('【','[')
    indicator_name=indicator_name.replace('】',']')
    field=request.form['field']
    scope=request.form['scope']
    year=request.form['year']
    new_value=request.form['new_value']
    region_code=fan_country_dict[region_name]
    updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        mxk_value1= mxk_value.query.filter_by(
            org_name=org_name,
            region_code=region_code,
            indicator_name=indicator_name,
            field=field,
            scope=scope,
            year=year
        ).first()
        #动态赋值
        mxk_value1.indicator_value=new_value
        mxk_value1.update_time=updateTime
        mxk_value1.update_by='user2'
        
        #db.session.commit()
        result = {
            'status':'ok'

        }
    except Exception as e :
        result = {
            'status':'bad',
            'err':str(e)

        }  
    return jsonify(result)

@data_manage.route('/del_field')
def del_field():
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    del_value_list=mxk_value.query.filter_by(scope=scope_v,field=field_v).all()
    try:
        for del_value in del_value_list:
            db.session.delete(del_value)

        result = {
                'status':'ok',

            }  
    except Exception as e :
        result = {
            'status':'bad',
            'err':str(e)

        }  
    return jsonify(result)

@data_manage.route('/del_nian')
def del_nian():
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')

    del_value_list=mxk_value.query.filter_by(field=field_v,scope=scope_v,year=year_v).all()
    try:
        for del_value in del_value_list:
            db.session.delete(del_value)
        
        result = {
                'status':'ok',
    
            }  
    except Exception as e :
        result = {
            'status':'bad',
            'err':str(e)

        }  
    return jsonify(result)

@data_manage.route('/value_down')
def value_down():
    filename = 'value_media_nation_2021.xlsx'
    filepath= file_dir+'mxk_value/'
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')

    response = make_response(send_from_directory(filepath, filename, as_attachment=True))

    response.headers["Content-Disposition"] = "attachment; filename={}".format(filepath.encode().decode('latin-1'))

    return send_from_directory(filepath, filename, as_attachment=True)
