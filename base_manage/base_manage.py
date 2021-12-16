import configparser
from openpyxl import Workbook
import json,time,os
from logging import exception
from flask import Blueprint
from flask.helpers import make_response, send_from_directory
from db_class import *
from flask import render_template,request,jsonify
base_manage = Blueprint('base_manage',__name__)
cf = configparser.ConfigParser()
current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")


def gao(level_3_list_notrans,level_3_list,year,field):
    header_list=level_3_list
    region_dict={}
    pp_list= mxk_region.query.all()
    
    info_dict={}
    
    for pp in pp_list:
        region_code=pp.unique_code
        region_name=pp.region_name
        region_dict[region_code]=region_name
    header2_list=['来源']
    for header in header_list:
        
        pp_list=mxk_base.query.filter_by(indicator_name=header,year=year).all()
        if pp_list:
            for pp in pp_list:
                region_code=pp.region_code
                region_name=region_dict[region_code]
                source=pp.source
                
                if not region_name in info_dict:
                    info_dict[region_name]={}
                indicator_value=pp.indicator_value
                info_dict[region_name][header]=indicator_value
            header2_list.append(source)
        else:
            header2_list.append('')
    score_list=[]
    header_dict={}

    wb_new=Workbook()
    ws_new=wb_new.active
    header_list.insert(0,'key') 
    level_3_list_notrans.insert(0,'原始指标')
    ws_new.append(level_3_list_notrans)
    ws_new.append(header_list)
    ws_new.append(header2_list)
    for region in info_dict:
    
        indicator_info=info_dict[region]
        row=[region]
        header_defalt=level_3_list[1:]
        for indicator_name in header_defalt:
            if indicator_name in indicator_info:
                row.append(indicator_info[indicator_name])
            else:
                row.append('')
       
        
        ws_new.append(row)
    file_path='{}_{}_output.xlsx'.format(field,year)
    wb_new.save('base_file/'+file_path)
    return file_path
@base_manage.route('/base_export', methods=['GET'])
def base_export():
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    year_v = request.args.get('year')
    indicator_trans_list=mxk_indicator_trans.query.filter_by(field=field_v).all()
    indicator_trans_dict={}

    for indicator in indicator_trans_list:
        indicator_name=indicator.indicator_name
        indicator_name_trans=indicator.indicator_name_trans
        indicator_trans_dict[indicator_name]=indicator_name_trans
    try :
        pp_list=Mxk_indicator_system.query.filter_by(scope=scope_v,field=field_v).all()
        for pp in pp_list:
            if not pp.parentId:
                parent1_id=str(pp.indicator_id)
                break
        p1_list=[]
        p2_list=[]
        for pp in pp_list:
            parentId=pp.parentId
            indicator_id=str(pp.indicator_id)
            if str(parentId) == parent1_id:
                p1_list.append(indicator_id)
        for pp in pp_list:
            parentId=pp.parentId
            indicator_id=str(pp.indicator_id)
            if str(parentId) in p1_list:
                p2_list.append(indicator_id)
        level_3_list_notrans=[]
        level_3_list=[]
        for pp in pp_list:
            parentId=pp.parentId
            indicator_id=str(pp.indicator_id)
            if parentId not in p2_list:
                continue
            indicator_name=pp.indicator_name
            if indicator_name in indicator_trans_dict:
                level_3_list_notrans.append(indicator_name)
                level_3_list.append(indicator_trans_dict[indicator_name])
            else:
                level_3_list_notrans.append(indicator_name)
                level_3_list.append(indicator_name)
        file_path=gao(level_3_list_notrans,level_3_list,year_v,field_v)
        response = make_response(send_from_directory('base_file', file_path, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file_path.encode().decode('latin-1'))
        return send_from_directory('base_file', file_path, as_attachment=True)
    except Exception as e:
        return jsonify(code=400,msg=str(e)) 