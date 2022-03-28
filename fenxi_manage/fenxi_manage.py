import configparser
from datetime import MAXYEAR
import json,time,os

from logging import exception
from typing import cast
from flask import Blueprint
from flask.helpers import make_response, send_from_directory
from numpy import integer
from db_class import *
from flask import render_template,request,jsonify
fenxi_manage = Blueprint('fenxi_manage',__name__)
cf = configparser.ConfigParser()
current_path = os.path.abspath(__file__)
root_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
conf_dir=root_dir+"/conf.ini"
cf.read(conf_dir)
file_dir=cf.get("mysql", "file_path")






@fenxi_manage.route('/generate')
def generate():
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    pp_list=mxk_analysis.query.filter_by(field=field_v,scope=scope_v).all()
    for pp in pp_list:
        db.session.delete(pp)
    db.session.commit()
    parent_0=Mxk_indicator_system.query.filter_by(field=field_v,scope=scope_v,indicator_name=field_v).first().indicator_id
    
    pp_list=Mxk_indicator_system.query.filter_by(field=field_v,scope=scope_v,parentId=parent_0).all()
    indicator_name_list=[x.indicator_name for x in pp_list]
    indicator_name_list.append(field_v)
    pp_list=mxk_measure.query.filter_by(field=field_v,scope=scope_v).all()
    max_year=mxk_measure.query.order_by(db.cast(mxk_measure.year,db.Integer).desc()).first().year
    max_field_year=mxk_measure.query.filter_by(field=field_v,scope=scope_v).order_by(db.cast(mxk_measure.year,db.Integer).desc()).first().year
    if not max_year == max_field_year:
        return jsonify(code=200,msg='文本生成失败，没有{}年的数据！'.format(max_year))
    last_year=str(int(max_year)-1)
    data_dict={}
    headers=[]
    update_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    zhengti_paiming={}
    try:
        year_list=[]
        for pp in pp_list:
            year=pp.year
            if not year in year_list:
                year_list.append(year)
            indicator_name=pp.indicator_name

            if indicator_name not in indicator_name_list or year not in [max_year,last_year]:
                continue
            if not indicator_name in headers:
                headers.append(indicator_name)
            score=pp.score
            region_code=pp.region_code
            org_id=pp.org_id
            if org_id:
                region_code=org_id+'_'+region_code

            #region_code=mxk_region.query.filter_by(region_code=region_code).first().region_code
            rank_=pp.rank_
            if not region_code in data_dict:
                data_dict[region_code]={}
            if not year in data_dict[region_code]:
                data_dict[region_code][year]={}

            data_dict[region_code][year][indicator_name]={'score':score,'rank':rank_}

        vs_data=[]
        
        region_info_dict={}
        for dd in data_dict:

            
            region_code=dd
            dd_dict={'region_code':region_code,'indicator_list':[]}

            if not max_year in data_dict[dd]:
                continue
            
            



            
            if last_year in  data_dict[dd]:
                if_2020=1
                data_2021=data_dict[dd][max_year]
                data_2020=data_dict[dd][last_year]
                
                for head in headers:

                    score_2021=data_2021[head]['score']
                    score_2020=data_2020[head]['score']
                    rank_2021=data_2021[head]['rank']
                    rank_2020=data_2020[head]['rank']
                    #score
                    score_up_down_num=float(score_2021)-float(score_2020)
                    score_up_down_num=round(score_up_down_num, 2)
                    if score_up_down_num >0:
                        score_up_down='上升'
                    elif score_up_down_num==0:
                        score_up_down='相同'
                    else:
                        score_up_down='下降'
                    #rank
                    rank_up_down_num=int(rank_2021)-int(rank_2020)
                    if rank_up_down_num >0:
                        rank_up_down='上升'
                    elif rank_up_down_num==0:
                        
                        rank_up_down='相同'
                    else:
                        rank_up_down='下降'
                    dd_dict['score_up_down_num']=abs(score_up_down_num)
                    dd_dict['score_up_down']=score_up_down     
                    dd_dict['rank_up_down_num']=abs(rank_up_down_num)
                    dd_dict['rank_up_down']=rank_up_down
                    row_dict={
                        'indicator_name':head,
                        'score_up_down_num':abs(score_up_down_num),
                        'score_up_down':score_up_down,
                        'rank_up_down_num':abs(rank_up_down_num),
                        'rank_up_down':rank_up_down
                    }
                    dd_dict['indicator_list'].append(row_dict)
                vs_data.append(dd_dict) 
                #搞1级指标
                
                for row in vs_data:

                    vs_str=''
                    row_str='在{}方面{}（{}）'
                    region_code=row['region_code']
                    indicator_list=row['indicator_list']
                    vs_zhibiao_str=''
                    for indicator in indicator_list:

                        indicator_name=indicator['indicator_name']

                        if indicator_name==field_v:
                            continue
                        score_up_down_num=indicator['score_up_down_num']
                        score_up_down=indicator['score_up_down']
                        rank_up_down_num=indicator['rank_up_down_num']
                        rank_up_down=indicator['rank_up_down']
                        indicator_str=row_str.format(indicator_name,score_up_down,score_up_down_num)
                        if '0.0' in indicator_str:
                            indicator_str='在{}方面与去年持平'.format(indicator_name)
                        vs_zhibiao_str+=indicator_str+'，'

                    vs_zhibiao_str=vs_zhibiao_str.strip('，')
                    region_info_dict[region_code]={'profile':vs_zhibiao_str}
                #搞0级指标
                for row in vs_data:

                    up_list=[]
                    down_list=[]
                    bubian_list=[]

                    region_code=row['region_code']
                    if '_' in region_code:
                        org_id=region_code.split('_')[0]
                        region_name=mxk_measure.query.filter_by(
                            org_id=org_id
                        ).first().org_name
                    else:
                        region_name=mxk_region.query.filter_by(
                            unique_code=region_code
                        ).first().region_name
                    indicator_list=row['indicator_list']
                    vs_zongjie_str='关键指标中，在'
                    for indicator in indicator_list:

                        indicator_name=indicator['indicator_name']



                        score_up_down_num=indicator['score_up_down_num']
                        score_up_down=indicator['score_up_down']
                        rank_up_down_num=indicator['rank_up_down_num']
                        rank_up_down=indicator['rank_up_down']
                        if  indicator_name==field_v:
                            if rank_up_down_num ==0:
                                if score_up_down_num!=0:
                                    str_0='与上年相比，{}在{}方面的能力与去年持平，排名与去年相同，整体得分{}{}分。'.format(
                                        region_name,
                                        indicator_name,
                                        score_up_down,
                                        score_up_down_num 
                                    )
                                else:
                                    str_0='与上年相比，{}在{}方面的能力与去年持平，排名与去年相同，整体得分与去年相同。'.format(
                                        region_name,
                                        indicator_name
                                    )
                            else: 
                                if score_up_down_num!=0:
                                    str_0='与上年相比，{}在{}方面的能力有所{}，排名{}{}位，整体得分{}{}分。'.format(
                                        region_name,
                                        indicator_name,
                                        rank_up_down,
                                        rank_up_down,
                                        rank_up_down_num,
                                        score_up_down,
                                        score_up_down_num
                                    )
                                else:
                                    str_0='与上年相比，{}在{}方面的能力有所{}，排名{}{}位，整体得分与去年相同。'.format(
                                        region_name,
                                        indicator_name,
                                        rank_up_down,
                                        rank_up_down,
                                        rank_up_down_num
                                    )
                        else:
                            if score_up_down =='上升':
                                up_list.append(indicator_name)
                            elif score_up_down =='相同':
                                bubian_list.append(indicator_name)
                            else:
                                down_list.append(indicator_name)
                    str_up=''
                    if len(up_list)>0:
                        for upp in up_list:
                            str_up+=upp+'、'
                        str_up=str_up.strip('、')
                        vs_zongjie_str+=str_up+'方面得分上升，'
                    str_bubian=''
                    if len(bubian_list)>0:
                        for bbian in bubian_list:
                            str_bubian+=bbian+'、'
                        str_bubian=str_bubian.strip('、')
                        vs_zongjie_str+=str_bubian+'方面得分不变，'
                    str_down=''
                    if len(down_list)>0:
                        for dd in down_list:
                            str_down+=dd+'、'
                        str_down=str_down.strip('、')
                        vs_zongjie_str+='在'+str_down+'方面得分下降，'
                    vs_zongjie_str=vs_zongjie_str.strip('，')
                    vs_zongjie_str+='。'
                    region_info_dict[region_code]['summary']=str_0+vs_zongjie_str
            else:
                if_2020=0
                data_2021=data_dict[dd][max_year]
                row_str=''
                for head in headers:

                    score_2021=data_2021[head]['score']
                    rank_2021=data_2021[head]['rank']
                    row_str+='在{}方面排名第{}，得分{}；'.format(head,rank_2021,score_2021)
                row_str=row_str.strip('；')+'。'
                if '_' in region_code:
                    org_code=region_code.split('_')[0]
                    region_code=region_code.split('_')[1]
                    mxk_analysis_add=mxk_analysis(
                        field=field_v,
                        scope=scope_v,
                        org_code=org_code,
                        region_code=region_code,
                        profile=row_str,
                        summary=row_str,
                        year=year,
                        update_time=update_time,
                        create_time=update_time     
                    )
                else:
                    mxk_analysis_add=mxk_analysis(
                        field=field_v,
                        scope=scope_v,
                        region_code=region_code,
                        profile=row_str,
                        summary=row_str,
                        year=year,
                        update_time=update_time,
                        create_time=update_time     
                    )
                db.session.add(mxk_analysis_add)
                
        #if if_2020: 
        
        for row in region_info_dict:
            region_code=row
            profile=region_info_dict[region_code]['profile']
            summary=region_info_dict[region_code]['summary']
            year=max_year
            if '_' in region_code:
                org_code=region_code.split('_')[0]
                region_code=region_code.split('_')[1]
                mxk_analysis_add=mxk_analysis(
                field=field_v,
                scope=scope_v,
                region_code=region_code,
                org_code=org_code,
                profile=profile,
                summary=summary,
                year=year,
                update_time=update_time,
                create_time=update_time          
            )
            else:
                mxk_analysis_add=mxk_analysis(
                field=field_v,
                scope=scope_v,
                region_code=region_code,
                profile=profile,
                summary=summary,
                year=year,
                update_time=update_time,
                create_time=update_time          
            )
            
            
            db.session.add(mxk_analysis_add)
        return jsonify(code=200,msg='文本生成成功')
    except Exception as e:

        return jsonify(code=400,msg=str(e))



@fenxi_manage.route('/list')
def list():
    page_num=request.args.get('page_num')
    pp_start=0+(int(page_num)-1)*10
    pp_end=10+(int(page_num)-1)*10
    pp_list=mxk_measure.query.all()
    f_s_list_measure=[]
    for pp in pp_list:
        scope=pp.scope
        field=pp.field
        f_s=field+'_'+scope
        if not f_s in f_s_list_measure:
            f_s_list_measure.append(f_s)
    pp_list=mxk_analysis.query.all()
    f_s_list_analysis=[]
    for pp in pp_list:
        scope=pp.scope
        field=pp.field
        f_s=field+'_'+scope
        if not f_s in f_s_list_analysis:
            f_s_list_analysis.append(f_s)
    fs_analysis_status=[]
    for fs in f_s_list_measure:
        field=fs.split('_')[0]
        scope=fs.split('_')[1]
        if fs in f_s_list_analysis:
            row={
                'field':field,
                'scope':scope,
                'status':'完整'
            }
        else:
            row={
                'field':field,
                'scope':scope,
                'status':'待补充'
            }
        
        fs_analysis_status.append(row)
    total_num=len(fs_analysis_status)
    return jsonify(code=200,msg='ok',data=fs_analysis_status[pp_start:pp_end],page_num=page_num,page_size=10,total=total_num)

@fenxi_manage.route('/detail')
def detail():
    field_v = request.args.get('field')
    scope_v = request.args.get('scope')
    org_code2name={}
    
    pp_list=mxk_org.query.all()
    military_level_list=[]
    for pp in pp_list:
        org_name=pp.military_name_cn
        military_level=pp.military_level
        if not military_level in military_level_list:
            military_level_list.append(military_level)
        org_code=pp.id
        org_code2name[str(org_code)]=[org_name,military_level]

    pp_list=mxk_analysis.query.filter_by(
        field=field_v,
        scope=scope_v
    ).all()
    data_list=[]
    for pp in pp_list:
        region_code=pp.region_code
        org_code=pp.org_code
        profile=pp.profile
        summary=pp.summary
        
        region_name=mxk_region.query.filter_by(
            unique_code=region_code
        ).first().region_name
        
        if org_code:
            org_name=org_code2name[org_code][0]
            military_level=org_code2name[org_code][1]
            #region_code=org_code
        else:
            org_name=''
            org_code=''
            military_level=''
            military_level_list=[]
        row_dict={
            'region_name':region_name,
            'region_code':region_code,
            'org_name':org_name,
            'org_code':org_code,
            'profile':profile,
            'summary':summary, #asd
            'military_level':military_level
        }
        data_list.append(row_dict)
    return jsonify(code=200,msg='ok',data=data_list,military_level_list=military_level_list)
@fenxi_manage.route('/edit_profile',methods=['POST'])
def edit_profile():
    try:
        update_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        args = (request.form.to_dict())
        field = args['field'].strip()
        scope = args['scope'].strip()
        region_code = args['region_code'].strip() 
        org_code = args['org_code'].strip()#asd
        if 'new_profile' in args:
            new_profile=args['new_profile']
            if org_code:
                old_mxk=mxk_analysis.query.filter_by(
                    field=field,
                    scope=scope,
                    org_code=org_code
                ).first()
            else:
                old_mxk=mxk_analysis.query.filter_by(
                    field=field,
                    scope=scope,
                    region_code=region_code
                ).first()
            old_mxk.profile=new_profile
            old_mxk.update_time=update_time
            return jsonify(code=200,msg='修改成功')
        if 'new_summary' in args:
            new_summary=args['new_summary']
            update_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            args = (request.form.to_dict())
            field = args['field'].strip()
            scope = args['scope'].strip()
            region_code = args['region_code'].strip()
            new_summary=args['new_summary']
            if org_code:
                old_mxk=mxk_analysis.query.filter_by(
                    field=field,
                    scope=scope,
                    org_code=org_code
                ).first()
            else:
                old_mxk=mxk_analysis.query.filter_by(
                    field=field,
                    scope=scope,
                    region_code=region_code
                ).first()
            old_mxk.summary=new_summary
            old_mxk.update_time=update_time
            return jsonify(code=200,msg='修改成功')
    except Exception as e:
        return jsonify(code=400,msg=str(e))

@fenxi_manage.route('/edit_summary',methods=['POST'])
def edit_summary():
    try:
        update_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        args = (request.form.to_dict())
        field = args['field'].strip()
        scope = args['scope'].strip()
        region_code = args['region_code'].strip()
        new_summary=args['new_summary']
        old_mxk=mxk_analysis.query.filter_by(
            field=field,
            scope=scope,
            region_code=region_code
        ).first()
        old_mxk.summary=new_summary
        old_mxk.update_time=update_time
        return jsonify(code=200,msg='修改成功')
    except Exception as e:
        return jsonify(code=400,msg=str(e))

    