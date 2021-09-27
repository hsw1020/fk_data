
from flask import Blueprint,request
from flask.json import jsonify
from db_class import *

from sqlalchemy.exc import SQLAlchemyError




bianzhi_manage=Blueprint('bianzhi_manage',__name__)

@bianzhi_manage.route('/list_country')
def list_country():
    page_num=request.args.get('page_num')
    pp_start=0+(int(page_num)-1)*10
    pp_end=10+(int(page_num)-1)*10
    pp_list=mxk_org.query.all()
    country_dict={}
    for pp in pp_list:
        region_name=pp.region
        military_level=pp.military_level
        military_name_cn=pp.military_name_cn

        base_cn=pp.base_cn
        base_en=pp.base_en
        latitude=pp.latitude
        longitude=pp.longitude

        if not military_level:
            continue

            
        if not region_name in country_dict:
            country_dict[region_name]={}
        if not military_level  in country_dict[region_name]:
            
            country_dict[region_name][military_level]=[]
        military_name_dict={
            'military_name_cn':military_name_cn,
            'base_cn':base_cn,
            'base_en':base_en,
            'latitude':latitude,
            'longitude':longitude
        }
        if not military_name_cn:
            continue
        country_dict[region_name][military_level].append(military_name_dict)
    data_list=[]
    for cc in country_dict:
        level_dict=country_dict[cc]
        level_list=[]
        for ll in level_dict:
            military_name_cn_list=level_dict[ll]
            ll_name_dict={
               'level': ll,
               'military_name_cn_list': military_name_cn_list
            }
            level_list.append(ll_name_dict)


        row_dict={
            'nation':cc,
            'level_list':level_list
        }
        data_list.append(row_dict)
    total_num=len(data_list)
    data_list=data_list[pp_start:pp_end]
    return jsonify(code=200,data=data_list,msg='ok',page_num=page_num,page_size=10,total=total_num)

@bianzhi_manage.route('/del')
def del_():
    nation=request.args.get('nation')
    level=request.args.get('level')
    name=request.args.get('name')

    if nation and level and name:
        del_value_list=mxk_org.query.filter_by(region=nation,military_level=level,military_name_cn=name).all()

    


    if nation and level and not name:
        del_value_list=mxk_org.query.filter_by(region=nation,military_level=level).all()
        
    if nation and not level and not name:
        del_value_list=mxk_org.query.filter_by(region=nation).all()
    for del_value in del_value_list:
        db.session.delete(del_value)
    
    if not del_value_list:
        return jsonify(code=400,msg='无数据可删')
    db.session.commit()
    return jsonify(code=200,msg='delete success')

@bianzhi_manage.route('/add_region')
def add_region():
    region_name=request.args.get('region_name')
    unique_code=request.args.get('unique_code')
    sort=int(request.args.get('sort'))
    pp=mxk_region.query.filter_by(region_name=region_name).first()
    if pp:
        return jsonify(code=400,msg='region_name 已存在！')
    pp=mxk_region.query.filter_by(sort=sort).first()
    if pp:
        return jsonify(code=400,msg='sort 已存在！')
    pp=mxk_region.query.filter_by(unique_code=unique_code).first()
    if pp:
        return jsonify(code=400,msg='unique_code 已存在！')
    mxk_region_add=mxk_region(region_name=region_name,unique_code=unique_code,sort=sort)
    db.session.add(mxk_region_add)
    db.session.commit()

    return jsonify(code=200,msg='region added success') 


@bianzhi_manage.route('/region_select')
def region_select():
    pp_list=mxk_region.query.all()
    region_list=[]
    for pp in pp_list:
        region_name=pp.region_name
        if not region_name in region_list:
            region_list.append(region_name)
    return jsonify(code=200,data=region_list,msg='ok')

@bianzhi_manage.route('/jdlv_select')
def jdlv_select():
    region=request.args.get('region')
    pp_list=mxk_org.query.filter_by(region=region).all()
    jdlv_list=[]
    data_list=[]
    for pp in pp_list:
        jdlv=pp.military_level
        sort_level=pp.sort_level
        if not jdlv in jdlv_list:
            data_list.append({
                'military_level':jdlv,
                'sort_level':sort_level
            })
            jdlv_list.append(jdlv)
            
    return jsonify(code=200,data=data_list,msg='ok')



@bianzhi_manage.route('/add_jdlv')
def add_jdlv():
    region=request.args.get('region')
    military_level=request.args.get('military_level')
    sort_level=int(request.args.get('sort_level'))
    #sort_military=int(request.args.get('sort_military'))
    pp=mxk_org.query.filter_by(sort_level=sort_level).first()
    if pp:
        return jsonify(code=400,msg='sort_level exist')
    
    pp=mxk_org.query.filter_by(region=region,military_level=military_level).first()
    if pp:
        return jsonify(code=400,msg='military_level 已存在！')
    mxk_org_add=mxk_org(region=region,military_level=military_level,sort_level=sort_level)
    db.session.add(mxk_org_add)
    db.session.commit()

    return jsonify(code=200,msg='military_level added success') 

@bianzhi_manage.route('/add_jdname')
def add_jdname():
    region=request.args.get('region')
    military_level=request.args.get('military_level')
    military_name_cn=request.args.get('military_name_cn')
    base_cn=request.args.get('base_cn')
    base_en=request.args.get('base_en')
    latitude=request.args.get('latitude')
    longitude=request.args.get('longitude')
    
    sort_military=int(request.args.get('sort_military'))
    
    sort_level=mxk_org.query.filter_by(
        region=region,
        military_level=military_level
    ).first().sort_level
    pp=mxk_org.query.filter_by(sort_military=sort_military).first()
    if pp:
        return jsonify(code=400,msg='sort_military exist')
    pp=mxk_org.query.filter_by(region=region,military_name_cn=military_name_cn,military_level=military_level).first()
    if pp:
        return jsonify(code=400,msg='military_name_cn 已存在！')
    mxk_org_add=mxk_org(
        region=region,
        military_level=military_level,
        military_name_cn=military_name_cn,
        base_cn=base_cn,
        base_en=base_en,
        latitude=latitude,
        longitude=longitude,
        sort_level=sort_level,
        sort_military=sort_military
    )
    db.session.add(mxk_org_add)
    pp_jdlv_kong=mxk_org.query.filter_by(
        region=region,
        military_level=military_level,
        military_name_cn=None
    ).all()
    for pp in pp_jdlv_kong:
        db.session.delete(pp)
    db.session.commit()

    return jsonify(code=200,msg='military_name_cn added success') 


#编辑





@bianzhi_manage.route('/edit_region',methods=['GET','POST'])
def edit_region():
    if request.method=='GET':
        region_name=request.args.get('region_name')
        pp=mxk_region.query.filter_by(region_name=region_name).first()
        unique_code=pp.unique_code
        sort=pp.sort
        data={
            'region_name':region_name,
            'unique_code':unique_code,
            'sort_level':sort
        }
        return jsonify(code=200,msg='ok',data=data)
    else:
        
        region_name=request.form['region_name']
        unique_code=request.form['unique_code']
        sort=request.form['sort']
        #unique_code=request.form['unique_code']
        region_name_new=request.form['region_name_new']
        unique_code_new=request.form['unique_code_new']
        sort_new=request.form['sort_new']
        
        pp=mxk_region.query.filter_by(region_name=region_name_new).first()
        if pp and region_name_new!=region_name:
            return jsonify(code=400,msg='region_name 已存在！')
        
        pp=mxk_region.query.filter_by(unique_code=unique_code_new).first()
        if pp and region_name_new!=region_name :
            return jsonify(code=400,msg='unique_code 已存在！')
        pp=mxk_region.query.filter_by(sort=sort_new).first()
        if pp and sort!=sort_new:
            return jsonify(code=400,msg='sort 已存在！')
        pp_old= mxk_region.query.filter_by(
            region_name=region_name,
            #unique_code=unique_code
        ).first()
        pp_old.region_name=region_name_new
        pp_old.unique_code=unique_code_new
        pp_old.sort=sort_new
        db.session.commit()
        return jsonify(code=200,msg='edit successful')



    return jsonify(code=200,msg='region added success') 
@bianzhi_manage.route('/edit_jdlv',methods=['GET','POST'])
def edit_jdlv():
    if request.method=='GET':
        region=request.args.get('region')
        military_level=request.args.get('military_level')
        pp=mxk_org.query.filter_by(region=region,military_level=military_level).first()
        sort_level=pp.sort_level
    
        data={
            'region':region,
            'military_level':military_level,
            'sort_level':sort_level
        }
        return jsonify(code=200,msg='ok',data=data)
    else:
        region=request.form['region']
        military_level=request.form['military_level']
        sort=request.form['sort']
        
        region_new=request.form['region_new']
        military_level_new=request.form['military_level_new']
        sort_new=request.form['sort_new']
        pp=mxk_org.query.filter_by(sort_level=sort_new).first()
        if pp and sort!=sort_new:
            return jsonify(code=400,msg='sort_level 已存在！')
        
        pp=mxk_org.query.filter_by(region=region,military_level=military_level_new).first()
        if pp and military_level_new!=military_level:
            return jsonify(code=400,msg='military_level 已存在！')
        pp_old_list= mxk_org.query.filter_by(
            region=region,
            military_level=military_level
        ).all()
        if not pp_old_list:
            return jsonify(code=400,msg='未存在该 military_level')
        for pp_old in pp_old_list:
            pp_old.region=region_new
            pp_old.military_level=military_level_new
            pp_old.sort_level=sort_new
        
        db.session.commit()
        return jsonify(code=200,msg='edit successful')


@bianzhi_manage.route('/edit_jdname',methods=['GET','POST'])
def edit_jdname():
    if request.method=='GET':
        region=request.args.get('region')
        military_level=request.args.get('military_level')
        military_name_cn=request.args.get('military_name_cn')
        pp=mxk_org.query.filter_by(region=region,military_level=military_level,military_name_cn=military_name_cn).first()
        base_cn=pp.base_cn
        base_en=pp.base_en
        latitude=pp.latitude
        longitude=pp.longitude
        #sort_level=pp.sort_level
        sort_military=pp.sort_military
        


        data={
            'region':region,
            'military_level':military_level,
            'military_name_cn':military_name_cn,
            'base_cn':base_cn,
            'base_en':base_en,
            'latitude':latitude,
            'longitude':longitude,
            'sort_military':sort_military
        }
        return jsonify(code=200,msg='ok',data=data)
    else:
        try:
            region=request.form['region']
            military_level=request.form['military_level']
            military_name_cn=request.form['military_name_cn']
            sort_military=request.form['sort_military_new']
            region_new=request.form['region_new']
            military_level_new=request.form['military_level_new']
            military_name_cn_new=request.form['military_name_cn_new']

            base_cn_new=request.form['base_cn_new']
            base_en_new=request.form['base_en_new']
            latitude_new=request.form['latitude_new']
            longitude_new=request.form['longitude_new']
            sort_military_new=request.form['sort_military_new']

            pp=mxk_org.query.filter_by(sort_military=sort_military_new).first()
            if pp and sort_military!=sort_military_new:
                return jsonify(code=400,msg='sort_military 已存在！')

            pp=mxk_org.query.filter_by(region=region,military_level=military_level_new,military_name_cn=military_name_cn_new).first()
            if pp and military_name_cn_new!=military_name_cn:
                return jsonify(code=400,msg='military_name_cn_new 已存在！')
            pp_old= mxk_org.query.filter_by(
                region=region,
                military_level=military_level,
                military_name_cn=military_name_cn
            ).first()
            pp_old.region=region_new
            pp_old.military_level=military_level_new
            pp_old.military_name_cn=military_name_cn_new
            pp_old.base_cn=base_cn_new
            pp_old.base_en=base_en_new
            pp_old.latitude=latitude_new
            pp_old.longitude=longitude_new
            pp_old.sort_military=sort_military_new
            db.session.commit()
            return jsonify(code=200,msg='edit successful')
        except Exception as e:
            db.session.rollback()
            return jsonify(code=400,msg=str(e))