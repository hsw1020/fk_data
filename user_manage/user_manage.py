
import time
from flask import Blueprint,request
from flask.json import jsonify
from sqlalchemy import exc
from db_class import *

from sqlalchemy.exc import SQLAlchemyError




user_manage=Blueprint('user_manage',__name__)
@user_manage.route('/del')
def del_():
    name = request.args.get('name')
    pp=Users.query.filter_by(name=name).first()
    db.session.delete(pp)
    db.session.commit()
    return jsonify(code=200,msg='删除成功！')

@user_manage.route('/list')
def list():
    page_num = request.args.get('page_num')
    page_start=0+(int(page_num)-1)*10
    page_end=10+(int(page_num)-1)*10
    user_list=[]
    pp_list=Users.query.all()
    for pp in pp_list:
        name=pp.name
        staff_name=pp.staff_name
        gender=pp.gender
        department=pp.department
        user_role=pp.user_role
        create_time=pp.create_time

        row_dict={
            'name':name,
            'staff_name':staff_name,
            'gender':gender,
            'department':department,
            'user_role':user_role,
            'create_time':create_time.strftime('%Y-%m-%d %H:%M:%S') 
        }
        user_list.append(row_dict)
    total_user=len(user_list)
    return jsonify(code=200,msg='ok',page_size=10,total=total_user,page_num=page_num,data=user_list[page_start:page_end])


@user_manage.route('/create_user',methods=['POST'])
def create_user():
    try:
        name=request.form['name']
        password=request.form['password']
        staff_name=request.form['staff_name']
        gender=request.form['gender']
        department=request.form['department']
        user_role=request.form['user_role']
        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        Users_add=Users(
            name=name,
            staff_name=staff_name,
            gender=gender,
            department=department,
            user_role=int(user_role),
            create_time=create_time
        )
        Users_add.hash_password(password)
        db.session.add(Users_add)
        db.session.commit()
        return jsonify(code=200,msg='用户创建成功')
    except Exception as e:
        return jsonify(code=400,msg=str(e))


@user_manage.route('/edit_user',methods=['POST'])
def edit_user():
    try:
        name=request.form['name']
        new_name=request.form['new_name']
        new_password=request.form['new_password']
        new_staff_name=request.form['new_staff_name']
        new_gender=request.form['new_gender']
        new_department=request.form['new_department']
        new_user_role=request.form['new_user_role']

        Users_edit=Users.query.filter_by(
            name=name 
        ).first()
        Users_edit.name=new_name
        Users_edit.password=new_password
        Users_edit.staff_name=new_staff_name
        Users_edit.gender=new_gender
        Users_edit.department=new_department
        Users_edit.user_role=new_user_role

        Users_edit.hash_password(new_password)
        db.session.commit()
        return jsonify(code=200,msg='用户编辑成功')
    except Exception as e:
        return jsonify(code=400,msg=str(e))