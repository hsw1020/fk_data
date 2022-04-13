import configparser
import json,time,os
from logging import exception
from flask import Blueprint
from flask.helpers import make_response, send_from_directory
from db_class import *
from flask import render_template,request,jsonify
data_manage = Blueprint('data_manage',__name__)
from .value_import import gao
cf = configparser.ConfigParser()
current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")




@data_manage.route('/add', methods=['POST'])
def add():

    args = (request.form.to_dict())
    args_field = args['field'].strip()
    args_scope = args['scope'].strip()
    args_year = args['year'].strip()
    args_radioval=args['radioval'].strip()
    
    user_name='wsh'
    pp=mxk_value.query.filter_by(field=args_field,scope=args_scope).first()
    sta = pp
    if sta is True:
        #旧数据处理
        #sta = mysql_operation.delete_indicator_list(Condition)
        #返回结果给前端
        return jsonify(code=400,msg="The old data exists") 
    #接收excle文件并保存到指定路径
    file = request.files.get('file')
    if file is None:
        return jsonify(code=400,msg="No files were received that needed to be uploaded") 
    file_path = file_dir+'mxk_value/' + file.filename
    #print(file,type(file),'/n',dir(file),'/n',request.files)
    #print(file.filename,type(file.filename))
    file.save(file_path)
    

    result=gao(file_path, args_year, args_field, args_scope, user_name,args_radioval)
    return result

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
            pp_value=mxk_value.query.filter_by(field=field,scope=scope).all()
            year_list=[]
            for p in pp_value:
                year_p=p.year
                if not year_p in year_list:
                    year_list.append(year_p)
            sorted(year_list,reverse=True)
            scope_dict={
                'scope_name':scope,
                'years_exist':year_list
            }
            data_dict[field].append(scope_dict)
            fs.append(fs_str)
        else:
            continue
    return jsonify(code=200,msg='ok',data=data_dict)

@data_manage.route('/list_detail_year')
def list_detail_year():
    country_dict={}
    fan_country_dict={}
    pp_list=mxk_region.query.all()
    for pp in pp_list:
        region_name=pp.region_name
        unique_code=pp.unique_code
        country_dict[unique_code]=region_name
        fan_country_dict[region_name]=unique_code

    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')
    #page_num=request.args.get('page_num')
    #pp_start=0+(int(page_num)-1)*10
    #pp_end=10+(int(page_num)-1)*10
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
        if dd in data_country_dict:
            data_list.append(data_country_dict[dd])


    data_1=data_list[0]
    header_list=[]
    n_c=1
    c2t_dict={}
    for dd in data_1:
        c_name='c{}'.format(n_c)
        n_c+=1
        c_row={
            'name':dd,
            'value':c_name
        }
        c2t_dict[dd]=c_name
        header_list.append(c_row)

    data_list_new=[]
    for dd in data_list:
        row_dict={}
        for row in dd:
            row_v=dd[row]
            row_k=c2t_dict[row]
            row_dict[row_k]=row_v
        data_list_new.append(row_dict)
    


    resutl={
        'header':header_list,
        'data':data_list_new,
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
    field_select = request.args.get('field_select')
    scope_select = request.args.get('scope_select')
    year_select = request.args.get('year_select')
    page_num=request.args.get('page_num')
    pp_start=0+(int(page_num)-1)*10
    pp_end=10+(int(page_num)-1)*10
    json_row={
            'status':'ok',
            'data':[]
        }
    fs_list=[]
    data_list=[]
    field_list=[]
    scope_list=[]
    year_list=[]

    if field_select and scope_select and year_select:
        pp_list=mxk_value.query.filter_by(field=field_select,scope=scope_select,year=year_select).order_by(mxk_value.create_time.asc()).all()
    elif field_select and scope_select and not year_select:
        pp_list=mxk_value.query.filter_by(field=field_select,scope=scope_select).order_by(mxk_value.create_time.asc()).all()
    elif  scope_select and year_select and not field_select:
        pp_list=mxk_value.query.filter_by(scope=scope_select,year=year_select).order_by(mxk_value.create_time.asc()).all()
    elif  scope_select and not year_select and not field_select:
        pp_list=mxk_value.query.filter_by(scope=scope_select).order_by(mxk_value.create_time.asc()).all()
    elif  not scope_select and year_select and field_select:
        pp_list=mxk_value.query.filter_by(field=field_select,year=year_select).order_by(mxk_value.create_time.asc()).all()
    elif  not scope_select and  year_select and not field_select:
        pp_list=mxk_value.query.filter_by(year=year_select).order_by(mxk_value.create_time.asc()).all()
    elif  not scope_select and not year_select and  field_select:
        pp_list=mxk_value.query.filter_by(field=field_select).order_by(mxk_value.create_time.asc()).all()
    elif  not scope_select and not year_select and  not field_select:
        pp_list=mxk_value.query.order_by(mxk_value.create_time.asc()).all()
    for pp in pp_list:
        field_v=pp.field
        scope_v=pp.scope
        year_v=pp.year
        if not {'field_name':field_v} in field_list:
            field_list.append({'field_name':field_v})
        if not {'scope_name':scope_v} in scope_list:
            scope_list.append({'scope_name':scope_v})
        if not {'year':year_v} in year_list:
            year_list.append({'year':year_v})
        fs_year=field_v+scope_v+str(year_v)
        if fs_year not in fs_list:
            data_list.append(pp)
            fs_list.append(fs_year)
    for data in data_list[pp_start:pp_end]:
        #id_v=data.id
        field_v=data.field
        scope_v=data.scope
        create_by_v=data.create_by
        create_time=data.create_time
        create_time=create_time.strftime('%Y-%m-%d %H:%M:%S') 
        year_v=data.year
        row={
            #'id':id_v,
            'field':field_v,
            'scope':scope_v,
            'create_by':create_by_v,
            'create_time':create_time,
            'year':year_v,
        }
        json_row['data'].append(row)
    total_rows=len(data_list)
    json_row['total']=total_rows
    json_row['pagesize']=10
    json_row['page_num']=page_num
    
    year_list.sort(key=lambda s: int(s["year"]),reverse=True)
    heaers={
        'field_list':field_list,
        'scope_list':scope_list,
        'year_list':year_list
    }
    json_row['heaers'] =heaers
    return jsonify(json_row)


#修改
@data_manage.route('/edit', methods=['POST'])
def dan_edit():
    country_dict={}
    fan_country_dict={}
    pp_list=mxk_region.query.all()
    for pp in pp_list:
        region_name=pp.region_name
        unique_code=pp.unique_code
        country_dict[unique_code]=region_name
        fan_country_dict[region_name]=unique_code

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
        db.session.commit()
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
