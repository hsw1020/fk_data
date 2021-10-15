# -*- coding: utf-8 -*-
import configparser,os

import datetime

from flask import Blueprint, json,jsonify,request
from flask.helpers import make_response, send_from_directory



cf = configparser.ConfigParser()

current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")

model_manage=Blueprint('model_manage',__name__)

@model_manage.route('/list')
def list():
    page_num = request.args.get('page_num')
    page_start=0+(int(page_num)-1)*10
    page_end=10+(int(page_num)-1)*10
    file_path=file_dir+'moren/'
    file_list=os.listdir(file_path)
    file_info_list=[]
    for ff in file_list:
        ff_path=file_path+ff
        file_create_time=os.path.getctime(ff_path)
        file_create_date = datetime.datetime.fromtimestamp(file_create_time)
        file_create_time=file_create_date.strftime('%Y-%m-%d %H:%M:%S') 
        field_name=ff.split('_')[1].split('.')[0]

        ff_row={
            'field_name':field_name,
            'created_time':file_create_time
        }

        file_info_list.append(ff_row)
    file_info_list.sort(key=lambda stu: stu["created_time"])
    file_info_list=file_info_list[page_start:page_end]
    total_files=len(file_info_list)
    return jsonify(code=200,data=file_info_list,page_num=page_num,page_size=10,total=total_files)




@model_manage.route('/add', methods=['POST'])
def add():
    args = (request.form.to_dict())
    args_field = args['field'].strip()
    
    file = request.files.get('file')
    
    if file is None:
        return jsonify(code=400,msg="请提交文件") 
    file_houzhui=file.filename.split('.')[1]
    if not file_houzhui =='xlsx':
        return jsonify(code=400,msg="请提交xlsx文件") 
    file_path=file_dir+'moren/'
    file_list=os.listdir(file_path)
    
    file_name='model_{}.'.format(args_field)
    file_name=file_name+file_houzhui
    if file_name in file_list:
        return jsonify(code=400,msg='文件已存在!')
    file_path = file_path+ file_name
    file.save(file_path)
    return jsonify(code=200,msg='add success')



@model_manage.route('/view')
def view():

    field = request.args.get('field')
    file_name='model_{}.xlsx'.format(field)
    file_path=file_dir+'moren/'
    
    response = make_response(send_from_directory(file_path, file_name, as_attachment=True))

    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_path.encode().decode('latin-1'))

    return send_from_directory(file_path, file_name, as_attachment=True)


@model_manage.route('/del')
def del_():

    field = request.args.get('field')
    file_name='model_{}.xlsx'.format(field)
    file_path=file_dir+'moren/'
    try:
        os.remove(file_path + file_name)
        return jsonify(code=200,msg='delete successful')
    except Exception  as e:
        return jsonify(code=400,msg=str(e))
    