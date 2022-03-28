import configparser
from datetime import MAXYEAR
import json,time,os
from flask import Blueprint
from flask.helpers import make_response, send_from_directory
from db_class import *
from flask import render_template,request,jsonify
from Utils.year_filter import year_filter
tongji_manage = Blueprint('tongji_manage',__name__)
cf = configparser.ConfigParser()
current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")




@tongji_manage.route('/list', methods=['GET'])
def list():
    region_list=mxk_region.query.all()
    regon_dict={}

    for r in region_list:
        region_name=r.region_name
        region_code=r.unique_code
        regon_dict[region_name]=region_code
    field = request.args.get('field')
    region = request.args.get('region')
    region_code=regon_dict[region]
    if field=='全部':
        pp_list=mxk_base.query.filter_by(region_code=region_code).order_by(mxk_base.year.asc()).all()
        indicator_name_list=mxk_base.query.filter_by(region_code=region_code).with_entities(mxk_base.indicator_name).distinct().all()
    else:  
        pp_list=mxk_base.query.filter_by(region_code=region_code,field=field).order_by(mxk_base.year.asc()).all()
        indicator_name_list=mxk_base.query.filter_by(region_code=region_code,field=field).with_entities(mxk_base.indicator_name).distinct().all()
    none_indicator_name_year=year_filter.find_none_year(pp_list)

    info_dict={}
    for pp in pp_list:
        indicator_name=pp.indicator_name
        year=int(pp.year)
        if not indicator_name in info_dict:
            info_dict[indicator_name]=[]
            year_none_list=none_indicator_name_year[indicator_name]
            for none_year in year_none_list:
                row={
                    'year':none_year,
                    'indicator_value':None,
                    'source':None
                }
                info_dict[indicator_name].append(row)

        indicator_value=pp.indicator_value
        source=pp.source
        row={
            'year':year,
            'indicator_value':indicator_value,
            'source':source
            }
        info_dict[indicator_name].append(row)

    info_dict=year_filter.year_sort(info_dict)
    total=len(indicator_name_list)
    return jsonify(code=200,msg='ok',total=total,data=info_dict)
    
@tongji_manage.route('/many_select', methods=['GET'])
def many_select():
    regon_list=[]
    region_list=mxk_region.query.all()
    for r in region_list:
        region_name=r.region_name
        region_code=r.unique_code
        row={'region':region_name}
        regon_list.append(row)


    indicator_list=mxk_base.query.with_entities(mxk_base.field).distinct().all()
    indicator_list_=[]
    for indicator in indicator_list:
        indicator_list_.append({'type_name':indicator[0]})
    row2={
        'region_list':regon_list,
        'indicator_list':indicator_list_
    }
    return jsonify(code=200,msg='ok',data=row2)
@tongji_manage.route('/add', methods=['POST'])
def add():
    region_list=mxk_region.query.all()
    regon_dict={}

    for r in region_list:
        region_name=r.region_name
        region_code=r.unique_code
        regon_dict[region_name]=region_code
    args = (request.form.to_dict())
    data = json.loads(request.get_data(as_text=True))    
    field = data['field']
    region_name = data['region_name']
    region_code=regon_dict[region_name]
    indicator_name= data['indicator_name']
    year_data=data['year_data']
    updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for y in year_data:
        year=y['year']
        indicator_value=y['indicator_value']
        source=y['source']
        base_exist=mxk_base.query.filter_by(region_code=region_code,field=field,year=year,indicator_name=indicator_name).first()
        if base_exist:
            return jsonify(code=400,msg=f'{year}年的{field}主题下的{indicator_name} 已存在！')
        mxk_base_add=mxk_base(
            field=field,
            region_name=region_name,
            region_code=region_code,
            year=year,
            indicator_name=indicator_name,
            indicator_value=indicator_value,
            source=source,
            create_time=updateTime
        )
        db.session.add(mxk_base_add)
    db.session.commit()
    return jsonify(code=200,msg='添加成功！')


@tongji_manage.route('/edit', methods=['POST'])
def edit():
    region_list=mxk_region.query.all()
    regon_dict={}

    for r in region_list:
        region_name=r.region_name
        region_code=r.unique_code
        regon_dict[region_name]=region_code
    
    data = json.loads(request.get_data(as_text=True))    
    field = data['field']
    
    region_name = data['region_name']
    region_code=regon_dict[region_name]
    indicator_name= data['indicator_name']
    year_data=data['year_data']
    
    db.session.query(mxk_base).filter(mxk_base.region_code==region_code,mxk_base.field==field,mxk_base.indicator_name==indicator_name).delete()
    updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for y in year_data:
        year=y['year']
        indicator_value=y['indicator_value']
        source=y['source']
        mxk_base_add=mxk_base(
            field=field,
            region_code=region_code,
            year=year,
            region_name=region_name,
            indicator_name=indicator_name,
            indicator_value=indicator_value,
            source=source,
            create_time=updateTime
        )
        db.session.add(mxk_base_add)
    db.session.commit()
    return jsonify(code=200,msg='修改成功！')

@tongji_manage.route('/del', methods=['GET'])
def del_():
    region_list=mxk_region.query.all()
    regon_dict={}

    for r in region_list:
        region_name=r.region_name
        region_code=r.unique_code
        regon_dict[region_name]=region_code
    field = request.args.get('field')
    region_name = request.args.get('region_name')
    region_code=regon_dict[region_name]
    indicator_name= request.args.get('indicator_name')
    mxk_base_del_list=mxk_base.query.filter_by(field=field,region_code=region_code,indicator_name=indicator_name).all()
    for mxk_base_del in mxk_base_del_list:
        db.session.delete(mxk_base_del)
    db.session.commit()
    return jsonify(code=200,msg='删除成功！')