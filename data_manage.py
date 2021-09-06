import configparser
import json
from logging import exception
from flask import Blueprint
from db_class import *
from flask import render_template,request,jsonify
data_manage = Blueprint('data_manage',__name__)
from value_import import gao
cf = configparser.ConfigParser()
cf.read("conf.ini")
file_dir=cf.get("mysql", "file_path")


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

@data_manage.route('/list_detail_year')
def list_detail_year():

    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')
    pp_list=mxk_value.query.filter_by(field=field_v,scope=scope_v,year=year_v).all()
    data=[]
    for pp in pp_list:
        row={'id':pp.id,
            'field':pp.field,
            'scope':pp.scope,
            'year':pp.year,
            'region_code':pp.region_code,
            'region_name':pp.region_name,
            'indicator_id':pp.indicator_id,
            'indicator_name':pp.indicator_name,
            'indicator_symbol':pp.indicator_symbol,
            'indicator_value':pp.indicator_value,
            'indicator_unit':pp.indicator_unit,
            'eva_level':pp.eva_level,
            'org_id':pp.org_id,
            'org_name':pp.org_name,
            'data_year':pp.data_year,
            'data_desc':pp.data_desc,
            'source':pp.source,
            'way':pp.way,
            'create_by':pp.create_by,
            'create_time':pp.create_time,
            'update_by':pp.update_by,
            'update_time':pp.update_time
        }

        data.append(row)
    resutl={
        'data':data,
        'status':'ok'
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
    pp_list=mxk_value.query.all()
    for pp in pp_list:
        field_v=pp.field
        scope_v=pp.scope
        fs=field_v+scope_v
        if fs not in fs_list:
            data_list.append(pp)
            fs_list.append(fs)
    for data in data_list:
        #id_v=data.id
        field_v=data.field
        scope_v=data.scope
        update_by_v=data.update_by
        update_time_v=data.update_time
        row={
            #'id':id_v,
            'field':field_v,
            'scope':scope_v,
            'update_by':update_by_v,
            'update_time':update_time_v
        }
        json_row['data'].append(row)
    json_row=jsonify(json_row)
    return json_row


#修改
@data_manage.route('/edit', methods=['POST'])
def dan_edit():
    id_v=request.form['id']
    col_name=request.form['col_name']

    new_value=request.form['new_value']
    try:
        mxk_value1= mxk_value.query.filter_by(id=int(id_v)).first()
        #动态赋值
        setattr(mxk_value1,col_name,new_value)

        db.session.commit()
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