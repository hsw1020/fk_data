from flask import jsonify
def gao_list(pp_list):
    parent_dict={}
    info_dict={}
    data_list=[]
    n=1
    for pp in pp_list:

        
        in_id=str(pp.indicator_id)
        parent_id=str(pp.parentId)
        #所有parentid 做dict
        if parent_id not in parent_dict:
            parent_dict[parent_id]=[]
            parent_dict[parent_id].append(in_id)
        else :
            parent_dict[parent_id].append(in_id)

        create_by=pp.create_by
        create_time=pp.create_time
        field=pp.field
        indicator_id=pp.indicator_id
        indicator_name=pp.indicator_name
        parentId=pp.parentId
        profile=pp.profile
        scope=pp.scope
        summary=pp.summary
        updateTime=pp.updateTime
        update_by=pp.update_by
        weight=pp.weight
        sort_v=pp.sort
        

        info_dict[str(in_id)]={
            'children':[],
            'create_by':create_by,
            'create_time':create_time,
            'field':field,
            'indicator_id':indicator_id,
            'indicator_name':indicator_name,
            'parentId':parentId,
            'profile':profile,
            'scope':scope,
            'summary':summary,
            'updateTime':updateTime,
            'update_by':update_by,
            'weight':weight,
            'sort':sort_v
        }
        n+=1

    pp_first=pp_list[0]
    index_first=str(pp_first.indicator_id)
    c_list=parent_dict[index_first]
    row=info_dict[index_first]
    add_children(row,c_list,info_dict,parent_dict)
    return jsonify([row])
        
def add_children(dd,c_list,info_dict,parent_dict):
    
    if  c_list==[]:
        return
    else:
        
        for cc in c_list:
            #if cc in parent_dict:
            child_row_info=info_dict[cc]
            try:
                dd['children'].append(child_row_info)
                
            except:
                pass
        dd_children_sort=sorted(dd['children'],key= lambda st : st['sort'])
        dd['children']=dd_children_sort
        for ddd in dd['children']:
            ddd_id=str(ddd['indicator_id'])
            if ddd_id in parent_dict:
                c_list_new=parent_dict[ddd_id]
                add_children(ddd,c_list_new,info_dict,parent_dict)
            else:
                continue

def fan_gao_list(sys_json,data_list,parent_id,pp_id_max):
    parent_id=parent_id
    data_list=data_list
    sort=1
    col_list=['create_by','create_time','field','indicator_name','profile','scope','summary','updateTime','update_by','weight']
    
    for sj in sys_json:

        row={
            'parentId':parent_id,
            'sort':sort
        }
        if 'indicator_id' in sj:
            indicator_id=sj['indicator_id']
            #sj['indicator_id']=indicator_id
            row['indicator_id']=indicator_id
            
        else:
            pp_id_max+=1
            indicator_id=pp_id_max
            row['indicator_id']=indicator_id
            sj['indicator_id']=indicator_id

        for col in col_list:
            if col in sj:
                row[col]=sj[col]
            else:
                row[col]=None

        
        data_list.append(row)
        sort+=1
    for sj in sys_json:
        if 'children' in  sj :
            if sj['children']:
                
                indicator_id=sj['indicator_id']
                fan_gao_list(sj['children'],data_list,indicator_id,pp_id_max)

def find_id_max(data,id_max):
    id_max=id_max
    for d in data:
        if 'indicator_id' in d:
            id_max=max(id_max,d['indicator_id'])
        if 'children' in d:
            find_id_max(d['children'],id_max)                