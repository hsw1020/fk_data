import configparser
import json,os
from logging import exception
from flask import Blueprint
from db_class import *

from .calculate import get_org
from flask import render_template,request,jsonify
calculate_manage = Blueprint('calculate_manage',__name__)

cf = configparser.ConfigParser()

current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")


@calculate_manage.route('/score_list')
def score_list():

    country_code2name={}
    fan_country_dict={}
    pp_list=mxk_region.query.all()
    for pp in pp_list:
        region_name=pp.region_name
        unique_code=pp.unique_code
        country_code2name[unique_code]=region_name
        fan_country_dict[region_name]=unique_code



    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    pp_list=mxk_measure.query.filter_by(field=field_v,scope=scope_v,indicator_name=field_v).all()
    country_dict={}
    header_list=[]
    list1=[]
    for pp in pp_list:
        year = pp.year
        header_list.append(year)
        region_code=pp.region_code
        region_name=country_code2name[region_code]
        org_name=pp.org_name
        if org_name:
            region_name=org_name
        #indicator_name=pp.indicator_name
        score=pp.score
        if not region_name in country_dict:
            

            country_dict[region_name]=[{'nation':region_name}]
        score_year={
            'year':year,
            'score':score
        }
        country_dict[region_name].append(score_year)
    header_list=sorted(set(header_list))
    country_dict_v=country_dict.values()
    data_list=list(country_dict_v)
    data_list_new=[]
    for dd in data_list:
        guo=dd[0]
        dd=sorted(dd[1:], key=lambda r: r['year'],reverse = False)
        dd.insert(0,guo)
        data_list_new.append(dd)
    data_out={
        'header_year':header_list,
        'body_country':data_list_new
    }
    return jsonify(code=200,msg='ok',data=data_out)
        

#数据更新时间
@calculate_manage.route('/list')
def list1():
    #field_v = request.args.get('field')
    page_num = request.args.get('page_num')
    page_start=0+(int(page_num)-1)*10
    page_end=10+(int(page_num)-1)*10
    fs_list=[]
    data_list=[]
    data_out=[]
    #pp_list=mxk_value.query.all()
    pp_list=mxk_value.query.order_by(mxk_value.update_time.desc()).all()
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
        pp=mxk_measure.query.filter_by(field=field_v,scope=scope_v).order_by(mxk_measure.create_time.desc()).first()
        if pp:
            cal_time=pp.create_time
        else:
            cal_time=None
        update_by_v=data.update_by
        update_time_v=data.update_time
        
        row={
            #'id':id_v,
            'field':field_v,
            'scope':scope_v,
            'update_by':update_by_v,
            'update_time':update_time_v,
            'cal_time':cal_time
        }
        data_out.append(row)
    page_total=len(data_out)
    page_size=10
    data_out=data_out[page_start:page_end]

    return jsonify(code=200,data=data_out,page_total=page_total,page_size=page_size,msg='ok')

def gao_fen(jiegou,k_score_dict):
    for jie in jiegou:

        ini_id=jie['indicator_id']
        if str(ini_id) in k_score_dict:
            score=k_score_dict[str(ini_id)]
        else:
            continue
        jie['score']=score
        if 'children' in jie:
            gao_fen(jie['children'],k_score_dict)

        


@calculate_manage.route('/calculate_result')
def calculate_result():
    country_code2name={}
    fan_country_dict={}
    pp_list=mxk_region.query.all()
    for pp in pp_list:
        region_name=pp.region_name
        unique_code=pp.unique_code
        country_code2name[unique_code]=region_name
        fan_country_dict[region_name]=unique_code
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')
    region_name = request.args.get('region_name')
    region_code_v=fan_country_dict[region_name]

    jiegou=mxk_indicator_json.query.filter_by(field=field_v,scope=scope_v).first()
    jiegou=jiegou.indicator_system
    pp_list=mxk_measure.query.filter_by(year=year_v,region_code=region_code_v,field=field_v,scope=scope_v).all()
    k_score_dict={}
    for pp in pp_list:
        indicator_id=pp.indicator_id
        score=pp.score
        k_score_dict[str(indicator_id)]=score

    gao_fen(jiegou,k_score_dict)
    
    return jsonify(code=200,msg='ok',data=jiegou)


@calculate_manage.route('/calculate')
def calculate():
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    pp_list=Mxk_indicator_system.query.filter_by(field=field_v,scope=scope_v).all()
    for pp in pp_list:
        indicator_name=pp.indicator_name
        weight=pp.weight
        if field_v!=indicator_name and not weight:
            if not weight==0:
                return jsonify(code=400,msg='评价主题为{}，评价对象为{}中{}的权重存在空值，无法计算！'.format(field_v,scope_v,indicator_name))

    try:
        get_org('tjk_indicator_measure',field_v,scope_v)
        return jsonify(code=200,msg='calculate done!')
    except Exception as e:
        return jsonify(code=400,msg=str(e))


@calculate_manage.route('/calculate_all')
def calculate_all():
    pp_value_list=mxk_value.query.all()
    pp_value_field_list={}
    for pp_value in pp_value_list:
        field=pp_value.field
        scope=pp_value.scope
        if not field in pp_value_field_list:
            pp_value_field_list[field]=[scope]
        else:
            if scope not in pp_value_field_list[field]:
                pp_value_field_list[field].append(scope)
    pp_sys_list=Mxk_indicator_system.query.all()
    for pp in pp_sys_list:
        field_v=pp.field
        scope_v=pp.scope
        indicator_name=pp.indicator_name
        weight=pp.weight
        if field_v!=indicator_name and not weight:
            if  field_v in pp_value_field_list:
                if scope_v in pp_value_field_list[field_v]:
                    return jsonify(code=400,msg='评价主题为{}，评价对象为{}的指标体系权重存在空值，无法计算！'.format(field_v,scope_v))
    try:
        get_org('tjk_indicator_measure','all','all')
        return jsonify(code=200,msg='calculate done!')
    except Exception as e:
        return jsonify(code=400,msg=str(e))