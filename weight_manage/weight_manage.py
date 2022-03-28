import configparser
import pandas as pd
from openpyxl import Workbook
import json,time,os
from logging import exception
from flask import Blueprint
from flask.helpers import make_response, send_from_directory
from db_class import *
from flask import render_template,request,jsonify
weight_manage = Blueprint('weight_manage',__name__)
cf = configparser.ConfigParser()
current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")
file_path=file_dir+'weight/'


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

@weight_manage.route('/add',methods=['POST'])
def add_():
    args = (request.form.to_dict())
    field = args['field'].strip()
    scope = args['scope'].strip()
    file = request.files.get('file')
    if file is None:
        return jsonify(code=400,msg="请上传文件") 
    elif not 'xlsx' in  file.filename:
        return jsonify(code=400,msg="请上传xlsx文件") 
    file_path = file_dir+'weight/weight_import.xlsx'
    #print(file,type(file),'/n',dir(file),'/n',request.files)
    #print(file.filename,type(file.filename))
    file.save(file_path)
    data = pd.read_excel(file_path)
    for index,item in data.iterrows():
        indicator = item['indicator']
        weight = item['weight']
        try:
            float_weight=float(weight)
        except:
            return jsonify(code=400,msg='权重存在非数字!')
        sys_new=Mxk_indicator_system.query.filter_by(
            field=field,
            scope=scope,
            indicator_name=indicator).first()
        if not sys_new:
            return jsonify(code=400,msg='以下指标不存在:{}'.format(indicator))
        sys_new.weight=float_weight

    pp=mxk_indicator_json.query.filter_by(field=field,scope=scope).first()
    pp_list=Mxk_indicator_system.query.filter_by(field=field,scope=scope).all()

    json_row=gao_list(pp_list)
    if  pp:
        id=pp.id
        
        create_by=pp.create_by
        create_time=pp.create_time
        updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        update_by='user1'
        db.session.delete(pp)
        mxk_indicator_json_1=mxk_indicator_json(create_by=create_by,create_time=create_time,update_time=updateTime,update_by=update_by,id=id,field=field,scope=scope,indicator_system=json_row.json)  
        db.session.add(mxk_indicator_json_1)
    return jsonify(code=200,msg='权重导入成功')

    

@weight_manage.route('/view_model')
def view_model():
    
    file_name='deom_weight.xlsx'
    response = make_response(send_from_directory(file_path, file_name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_path.encode().decode('latin-1'))
    return send_from_directory(file_path, file_name, as_attachment=True)
        

@weight_manage.route('/dw_indicator')
def dw_indicator():
    field=request.args.get('field')
    scope=request.args.get('scope')
    try:
        pp_list=Mxk_indicator_system.query.filter_by(field=field,scope=scope).all()
        wb=Workbook()
        ws=wb.active
        header=['indicator','weight']
        ws.append(header)
        for pp in pp_list:
            if not pp.indicator_name == field:
                row=[pp.indicator_name]
                ws.append(row)
        file_scope=scope.replace('/','')
        file_field=field.replace('/','')
        file_name='weight_{}_{}.xlsx'.format(file_field,file_scope)
        wb.save(file_path+file_name)
        response = make_response(send_from_directory(file_path, file_name, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file_path.encode().decode('latin-1'))
        return send_from_directory(file_path, file_name, as_attachment=True)
    except Exception as e:
        return jsonify(code=400,msg=str(e))

@weight_manage.route('/weight_status')
def weight_status():
    #field=request.args.get('field')
    #scope=request.args.get('scope')
    page_num=request.args.get('page_num')
    pp_start=0+(int(page_num)-1)*10
    pp_end=10+(int(page_num)-1)*10

    pp_list=Mxk_indicator_system.query.all()
    weight_sta={}
    for pp in pp_list:
        indicator_name=pp.indicator_name
        weight=pp.weight
        field=pp.field
        scope=pp.scope
        field_scope=field+'_'+scope
        weight_sta[field_scope]='完整'
    for pp in pp_list:
        indicator_name=pp.indicator_name
        weight=pp.weight
        field=pp.field
        scope=pp.scope
        field_scope=field+'_'+scope
        if not field == indicator_name:
            if not weight ==0:
                if not weight:
                    weight_sta[field_scope]='有空值'
    weight_list=[]
    for field_scope in weight_sta:
        field=field_scope.split('_')[0]
        scope=field_scope.split('_')[1]
        status=weight_sta[field_scope]
        row={'field':field,'scope':scope,'weight_status':status}
        weight_list.append(row)
    total_num=len(weight_list)
    return jsonify(code=200,msg='ok',data=weight_list[pp_start:pp_end],page_num=page_num,page_size=10,total=total_num)

    

    