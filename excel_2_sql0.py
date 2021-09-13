
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import configparser
cf = configparser.ConfigParser()
cf.read("conf.ini")
mysql_uri = cf.get("mysql", "uri")
engine=create_engine(mysql_uri)
# In[136]:


def level_test(data):
    #data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',engine)
    #level_=data_mxk_indicator_system[['indicator_name']].rename(columns={'indicator_name':'level_name'})
    levle_1=data[data['一级指标'].isnull()==False][['一级指标']].rename(columns={'一级指标':'level_name'})
    levle_2=data[data['二级指标'].isnull()==False][['二级指标']].rename(columns={'二级指标':'level_name'})
    levle_3=data[data['三级指标'].isnull()==False][['三级指标']].rename(columns={'三级指标':'level_name'})
    data_1_2_3=pd.concat([levle_1,levle_2,levle_3])
    data_1_2_3['level_name']=data_1_2_3['level_name'].str.strip()
    data_1_2_3_duplicated=data_1_2_3[data_1_2_3['level_name'].duplicated()==True]
    list_=np.array(data_1_2_3_duplicated).tolist()
    data_=",".join('%s' %a for a in list_)
    data_test=data_.replace("['",'').replace("']",'')
    return data_test


# In[137]:


def data_range():
    data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',engine)
    data_range=data_mxk_indicator_system['indicator_id'].max()
    if data_range>=0:
        data_range=data_range
    else:
        data_range=0
    return data_range+1


# In[143]:


def data_(data,data_range_,field,scope,create_by):
    data['field']=field
    data['一级指标']=data['一级指标'].fillna(method='ffill')
    data['二级指标']=data['二级指标'].fillna(method='ffill')

    data_0=data[['field']].drop_duplicates().rename(columns={'field':'指标'})
    data_0['field']=data_0['指标']
    data_1=data[['一级指标','field']].drop_duplicates().rename(columns={'一级指标':'指标'})
    data_2=data[['二级指标','field']].drop_duplicates().rename(columns={'二级指标':'指标'})
    data_3=data[['三级指标','field']].drop_duplicates().rename(columns={'三级指标':'指标'})
    
    data_=pd.concat([data_0,data_1,data_2,data_3])
    data_['id']=range(data_range_,data_.shape[0]+data_range_)
    
    
    #根级与一级关系
    data_0_1=data[['field','一级指标']].drop_duplicates()
    result_data_0_1=pd.merge(data_,
         data_0_1,
         how='inner',
         left_on='指标',
         right_on='field')
    
    #一级与二级关系
    data_1_2=data[['一级指标','二级指标']].drop_duplicates()
    result_1_2=pd.merge(data_,
         data_1_2,
         how='inner',
         left_on='指标',
         right_on='一级指标')
    
    #二级与三级关系
    data_2_3=data[['二级指标','三级指标']].drop_duplicates()
    result_2_3=pd.merge(data_,
         data_2_3,
         how='inner',
         left_on='指标',
         right_on='二级指标')
    
    result_1=pd.merge(data_,result_data_0_1,how='inner',left_on='指标',right_on='一级指标')
    result_1=result_1.rename(columns={'id_x':'indicator_id','指标_x':'indicator_name','id_y':'parentId'})
    
    result_1=pd.merge(data_,result_data_0_1,how='inner',left_on='指标',right_on='一级指标')
    result_1=result_1.rename(columns={'id_x':'indicator_id','指标_x':'indicator_name','id_y':'parentId'})
    result_1=result_1.loc[:,['indicator_id','indicator_name','parentId','field']]
    
    result_2=pd.merge(data_,result_1_2,how='inner',left_on='指标',right_on='二级指标')
    result_2=result_2.rename(columns={'id_x':'indicator_id','指标_x':'indicator_name','id_y':'parentId','field_x':'field'})
    result_2=result_2.loc[:,['indicator_id','indicator_name','parentId','field']]
    
    result_3=pd.merge(data_,result_2_3,how='inner',left_on='指标',right_on='三级指标')
    result_3=result_3.rename(columns={'id_x':'indicator_id','指标_x':'indicator_name','id_y':'parentId','field_x':'field'})
    result_3=result_3.loc[:,['indicator_id','indicator_name','parentId','field']]
    
    result_4=pd.merge(data_,
         pd.concat([result_1,result_2,result_3]),
        how='left',
        left_on=['指标','id'],
        right_on=['indicator_name','indicator_id'])
    result_4=result_4.loc[:,['指标','field_x','id','parentId']]
    result_4=result_4.rename(columns={'指标':'indicator_name','field_x':'field','id':'indicator_id'})
    result_4['scope']=scope
    #result_4['field']='规模结构'
    result_4['sort']=range(1,result_4.shape[0]+1)
    result_4['create_by']=create_by
    data=data_input(result_4)
    return data


# In[144]:


def data_input(data):
    data=data.values
    return data


# In[146]:
def dtest(path):
    data=pd.read_excel(path)
    dtest=level_test(data)
    return dtest



#if __name__ == '__main__':
#    
#    # engine=create_engine('mysql+pymysql://root:12345.zcf@localhost/fjkz')
#    engine=create_engine(mysql_uri)
#    path=r'tree_luoyi.xlsx'
#    # path=r'C:\Users\admin\Desktop\luoyi\tree_luoyi_test.xlsx'
#    # field='媒体力量'
#    # scope='test1'
#    field='333'
#    scope='111'
#    create_by='张冲锋'
#    data=pd.read_excel(path)
#    dtest=level_test(data)
#    print(dtest)
#    if len(dtest)>0:
#        dtest=dtest
#    else:
#        data_range_=int(data_range())
#        data_(data,data_range_,field,scope,create_by)
#    #print(data.head())

def gao(path,field,scope,create_by):
    
    data_range_=int(data_range())
    data=pd.read_excel(path)
    data_list=data_(data,data_range_,field,scope,create_by)
    return data_list
