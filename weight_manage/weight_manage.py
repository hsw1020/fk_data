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
            row=[pp.indicator_name]
            ws.append(row)
        file_name='weight_{}_{}.xlsx'.format(field,scope)
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
    return jsonify(code=200,msg='ok',data=weight_list)

    

    