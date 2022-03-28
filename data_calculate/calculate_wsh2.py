from werkzeug.utils import redirect
from db_class import *
import configparser
cf = configparser.ConfigParser()
def gui(mxk_value_dict):
    mxk_value_dict_gui={}

    x_dict={}
    for region in mxk_value_dict:
        for indicator_id in mxk_value_dict[region]:
            value=mxk_value_dict[region][indicator_id]
            if not indicator_id in x_dict:
                x_dict[indicator_id]=[]
            x_dict[indicator_id].append(value)
    for indicator_id in x_dict:
        value_list=x_dict[indicator_id]
        max_value=max(value_list)
        min_value=min(value_list)
        r = max_value - min_value
        value_list=[(x-min_value)/r for x in value_list]
        region_list=list(mxk_value_dict.keys())
        len_value=len(value_list)
        for i in range(len_value):
            if not region_list[i] in mxk_value_dict_gui:
                mxk_value_dict_gui[region_list[i]]={}
            value_gui=round(value_list[i]*100,2)
            mxk_value_dict_gui[region_list[i]][indicator_id]=value_gui
    return mxk_value_dict_gui

def get_org(field_v,scope_v):
    pp_list=Mxk_indicator_system.query.filter_by(field=field_v,scope=scope_v).all()
    root_indicator=''
    for pp in pp_list:
        indicator_name=pp.indicator_name
        indicator_id=str(pp.indicator_id)
        if field_v==indicator_name:
            root_indicator=indicator_id
            break
    indicator_1=[]
    indicator_1_dict={}
    for pp in pp_list:
        indicator_id=str(pp.indicator_id)
        parentId=pp.parentId
        weight=pp.weight
        if parentId == root_indicator:
            indicator_1.append(indicator_id)
            if parentId not in indicator_1_dict:
                indicator_1_dict[parentId] = [[indicator_id,weight]]
            else:
                indicator_1_dict[parentId].append([indicator_id,weight])

    indicator_2=[]
    indicator_2_dict={}
    for pp in pp_list:
        indicator_id=str(pp.indicator_id)
        weight=pp.weight
        parentId=pp.parentId
        if parentId in indicator_1:
            indicator_2.append(indicator_id)
            if parentId not in indicator_2_dict:
                indicator_2_dict[parentId]=[[indicator_id,weight]]
            else:
                indicator_2_dict[parentId].append([indicator_id,weight])
    indicator_3=[]
    indicator_3_dict={}
    for pp in pp_list:
        weight=pp.weight
        indicator_id=str(pp.indicator_id)
        parentId=pp.parentId
        if parentId in indicator_2:
            indicator_3.append(indicator_id)
            if parentId not in indicator_3_dict:
                indicator_3_dict[parentId]=[[indicator_id,weight]]
            else:
                indicator_3_dict[parentId].append([indicator_id,weight])

    pp_list=mxk_value.query.filter_by(field=field_v,scope=scope_v).all()
    region_dict={}

    
    mxk_value_dict={}
    for pp in pp_list:
        indicator_id=str(pp.indicator_id)
        region_code=pp.region_code
        indicator_value=pp.indicator_value
        if not region_code in mxk_value_dict:
            mxk_value_dict[region_code]={}
        mxk_value_dict[region_code][indicator_id]=indicator_value

    #归一化
    gui_3=gui(mxk_value_dict)
    
    gui_2_value={}
    for region in gui_3:
        gui_2_value[region]={}
        for indicator_id_2  in indicator_3_dict:
            value=0
            son_list=indicator_3_dict[indicator_id_2]
            for son in son_list:
                son_id=son[0]
                son_weight=son[1]
                value_son=gui_3[region][son_id]*son_weight
                value+=value_son
            gui_2_value[region][indicator_id_2]=value
    gui_2=gui(gui_2_value)
            
    gui_1_value={}
    for region in gui_2:
        gui_1_value[region]={}
        for indicator_id_1  in indicator_2_dict:
            value=0
            son_list=indicator_2_dict[indicator_id_1]
            for son in son_list:
                son_id=son[0]
                son_weight=son[1]
                value_son=gui_2[region][son_id]*son_weight
                value+=value_son
            gui_1_value[region][indicator_id_1]=value    
    gui_1=gui(gui_1_value)

    gui_0_value={}
    for region in gui_1:
        gui_0_value[region]={}
        for indicator_id_0  in indicator_1_dict:
            value=0
            son_list=indicator_1_dict[indicator_id_0]
            for son in son_list:
                son_id=son[0]
                son_weight=son[1]
                value_son=gui_1[region][son_id]*son_weight
                value+=value_son
            gui_0_value[region][indicator_id_0]=value 
    gui_0=gui(gui_0_value) 
    return 1




        
