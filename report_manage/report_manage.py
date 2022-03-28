import configparser
import json,os,time
from logging import exception
from flask import Blueprint
from db_class import *
from flask.helpers import make_response, send_from_directory
from flask import render_template,request,jsonify
report_manage = Blueprint('report_manage',__name__)

cf = configparser.ConfigParser()

current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")

@report_manage.route('/add',methods=['POST'])
def add_():
    try:
        updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        args = (request.form.to_dict())
        field = args['field'].strip()
        scope = args['scope'].strip()
        year=args['year'].strip()
        region_code=args['region_code'].strip()
        org_code=args['org_code'].strip()
        report_type=args['report_type'].strip()
        
        
        create_by=args['create_by'].strip()
        file = request.files.get('file')
        file_name= '{}_{}_{}_{}'.format(field,scope.replace('/',''),year,file.filename)
        file_path = 'report_file/'+file_name
        file.save(file_path)
        report_name=file.filename
        cgk_report_add=cgk_report(
            field=field,
            scope=scope,
            year=year,
            region_code=region_code,
            org_code=org_code,
            keywords=report_type,
            report_name=report_name,
            path=file_path,
            create_by=create_by,
            create_time=updateTime

        )
        db.session.add(cgk_report_add)
        db.session.commit()
        return jsonify(code=200,msg='ok')
    except Exception as e:
        return jsonify(code=400,msg=str(e))

@report_manage.route('/region_select')
def region_select():
    try:
        pp_list=mxk_org.query.all()
        org_code2name={}
        for pp in pp_list:
            org_name=pp.military_name_cn
            org_code=pp.id
            org_code2name[str(org_code)]=org_name
        field = request.args.get('field')
        scope = request.args.get('scope')
        data_list=[]
        region_code2name={}
        pp_list=mxk_region.query.all()
        for pp in pp_list:
            region_name=pp.region_name
            region_code=pp.unique_code
            region_code2name[region_code]=region_name
        pp_list=mxk_measure.query.filter_by(field=field,scope=scope).all()

        
    
        

        for pp in pp_list:
            region_code=pp.region_code
            org_code=pp.org_id
            if org_code:   
                region_name=org_code2name[org_code]
                region_code=org_code
            else:
                region_name=region_code2name[region_code]
            region_row={'region_name':region_name,'region_code':region_code}
            if not region_row in data_list:
                data_list.append(region_row)

        return jsonify(code=200,msg='ok',data=data_list)
    except Exception as e:
        return jsonify(code=400,msg=str(e))
@report_manage.route('/field_select')
def field_select():
    try:
        pp_list=mxk_org.query.all()
        org_code2name={}
        for pp in pp_list:
            org_name=pp.military_name_cn
            org_code=pp.id
            org_code2name[str(org_code)]=org_name
        region_code2name={}
        pp_list=mxk_region.query.all()
        for pp in pp_list:
            region_name=pp.region_name
            region_code=pp.unique_code
                
            region_code2name[region_code]=region_name
        data_dict={}
        data_list2=[]
        pp_list=mxk_measure.query.all()
        for pp in pp_list:
            field=pp.field
            if not field in data_dict:
                data_dict[field]={}
            scope=pp.scope
            if not scope in data_dict[field]:
                data_dict[field][scope]=[]
            region_code=pp.region_code
            org_code=pp.org_id
            if region_code:
                region_name=region_code2name[region_code]
            else:
                region_name=org_code2name[org_code]
                region_code=org_code
            region_row={'region_name':region_name,'region_code':region_code}
            if region_row not in data_dict[field][scope]:
                data_dict[field][scope].append(region_row)
        for field in data_dict:
            scope_dict=data_dict[field]
            scope_list=[]
            for sc in scope_dict:
                region_list=scope_dict[sc]
                row1={'scope':sc}
                scope_list.append(row1)
                
            row={'field':field,'scope_list':scope_list}
            data_list2.append(row)
        return jsonify(code=200,msg='ok',data=data_list2)
    except Exception as e:
        return jsonify(code=400,msg=str(e))



@report_manage.route('/list')
def list1():
    #field_v = request.args.get('field')
    page_num = request.args.get('page_num')
    page_start=0+(int(page_num)-1)*10
    page_end=10+(int(page_num)-1)*10
    fs_list=[]
    data_list=[]

    #pp_list=mxk_value.query.all()
    
    region_code2name={}
    pp_list=mxk_region.query.all()
    for pp in pp_list:
        region_name=pp.region_name
        region_code=pp.unique_code
        region_code2name[region_code]=region_name
    pp_list=cgk_report.query.order_by(cgk_report.create_time.desc()).all()
    for pp in pp_list:
        id=pp.id
        field=pp.field
        scope=pp.scope
        year=pp.year
        region_code=pp.region_code
        if region_code:
            region_name=region_code2name[region_code]
        else:
            region_name=''
        org_code=pp.org_code
        report_type=pp.keywords
        report_name=pp.report_name
        path=pp.path
        create_by=pp.create_by
        create_time=pp.create_time
       
   
        
        row={
            'id':pp.id,
            'field':pp.field,
            'scope':pp.scope,
            'year':pp.year,
            'region_code':region_name,
            'org_code':pp.org_code,
            'report_type':pp.keywords,
            'report_name':report_name,
            'report_name_no':pp.report_name.split('.')[0],
            'path':pp.path,
            'create_by':pp.create_by,
            'create_time':pp.create_time
        }
        data_list.append(row)
    page_total=len(data_list)
    page_size=10
    data_out=data_list[page_start:page_end]

    return jsonify(code=200,data=data_out,page_total=page_total,page_size=page_size,msg='ok')

@report_manage.route('/view')
def view():

    field = request.args.get('field')
    scope = request.args.get('scope')
    year = request.args.get('year')
    report_name = request.args.get('report_name')

    file_name= '{}_{}_{}_{}'.format(field,scope.replace('/',''),year,report_name)
    file_path = 'report_file/'
    response = make_response(send_from_directory(file_path, file_name, as_attachment=True))

    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_path.encode().decode('latin-1'))

    return send_from_directory(file_path, file_name, as_attachment=True)

@report_manage.route('/del')
def del_():

    field = request.args.get('field')
    scope = request.args.get('scope')
    year = request.args.get('year')
    report_name = request.args.get('report_name')
    file_name= '{}_{}_{}_{}'.format(field,scope.replace('/',''),year,report_name)
    file_path = 'report_file/'+file_name

    try:
        os.remove(file_path)
        cgk_report_del=cgk_report.query.filter_by(
            field=field,
            scope=scope,
            year=year,
            report_name=report_name,
            path=file_path,

        ).first()
        db.session.delete(cgk_report_del)
        db.session.commit()
        return jsonify(code=200,msg='delete successful')
    except Exception  as e:
        return jsonify(code=400,msg=str(e))