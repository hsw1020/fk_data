import configparser
import json
from logging import exception
from flask import Blueprint
from db_class import *

from calculate import get_org
from flask import render_template,request,jsonify
calculate_manage = Blueprint('calculate_manage',__name__)

cf = configparser.ConfigParser()
cf.read("conf.ini")
file_dir=cf.get("mysql", "file_path")


@calculate_manage.route('/score_list')
def score_list():
    field_v = request.args.get('field')
    #scope_v = request.args.get('scope')
    pp_list=mxk_measure.query.filter_by(indicator_name=field_v).all()
    country_dict={}
    for pp in pp_list:
        year = pp.year
        region_code=pp.region_code
        indicator_name=pp.indicator_name
        score=pp.score
        if not region_code in country_dict:
            country_dict[region_code]={}
        if not year in country_dict[region_code]:
            country_dict[region_code][year] = score
    return jsonify(code=200,msg='ok',data=country_dict)
        


@calculate_manage.route('/list')
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
        pp=mxk_measure.query.filter_by(field=field_v,scope=scope_v).first()
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
        json_row['data'].append(row)
    json_row=jsonify(json_row)
    return json_row

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
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')
    region_code_v = request.args.get('region_code')

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
    try:
        get_org('tjk_indicator_measure',field_v,scope_v)
        return jsonify(code=200,msg='calculate done!')
    except Exception as e:
        return jsonify(code=500,msg=str(e))


@calculate_manage.route('/calculate_all')
def calculate_all():

    try:
        get_org('tjk_indicator_measure','all','all')
        return jsonify(code=200,msg='calculate done!')
    except Exception as e:
        return jsonify(code=500,msg=str(e))