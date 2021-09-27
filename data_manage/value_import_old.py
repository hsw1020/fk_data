
# coding: utf-8

# In[88]:


from flask.json import jsonify
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import time
import configparser
cf = configparser.ConfigParser()
cf.read("conf.ini")
mysql_uri = cf.get("mysql", "uri")

# In[154]:



def public_part(data):
    list_1=[]
    list_col=data.columns.tolist()
    for i in range(data.shape[0]):
        for j in range(len(list_col)):
            col_name=list_col[j]
            col_value=data.loc[i,list_col[j]]
            dict_1={'col_name':col_name,'col_value':col_value}
            list_1.append(dict_1)
    data_=pd.DataFrame(list_1)
    return data_


# In[155]:


def public_col(data_,year,user_name):
    data_['year']=year
#     data_['filed']=filed
#     data_['scope']=scope
    #data_['user_name']=user_name
    
    data_['indicator_symbol']=None
    data_['indicator_unit']=None

    #data_['region_code']=None
    # data_org['eva_level']=None
    # data_org['org_name']=None

    data_['data_year']=None
    data_['data_desc']=None

    data_['source']=None
    data_['way']=None
    data_['create_by']=user_name
    data_['create_time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data_['update_by']=None
    data_['update_time']=None
    return data_


# In[169]:


def nation(data_nation,year,field,scope,user_name,data_dict_region,data_mxk_indicator_system,engine):
#     list_1=[]
#     list_col=data_nation.columns.tolist()
#     for i in range(data_nation.shape[0]):
#         for j in range(len(list_col)):
#             col_name=list_col[j]
#             col_value=data_nation.loc[i,list_col[j]]
#             dict_1={'col_name':col_name,'col_value':col_value}
#             list_1.append(dict_1)
    
#     data_nation_df=pd.DataFrame(list_1)

    data_nation_df=public_part(data_nation)
    data_nation_df['values']=np.where(data_nation_df['col_value'].str.contains('[0-9]{1,}'),None,data_nation_df['col_value'])

    data_nation_df['values']=data_nation_df['values'].fillna(method='ffill')
    data_nation_df['result']=data_nation_df['col_value'].str.contains('[0-9]{1,}')==False
    data_nation_df=data_nation_df[data_nation_df['result']==False]
    nation_col_name_inner=pd.merge(data_dict_region,data_nation_df,how='inner',left_on='region_name',right_on='values')
    #nation_col_name_inner.to_excel('nation_.xlsx')
    
    data_nation=pd.merge(data_mxk_indicator_system,nation_col_name_inner,how='inner',left_on='indicator_name',right_on='col_name')
    #data_nation.to_excel('1aa.xlsx')
    data_nation_1=data_nation.loc[:,['indicator_id','indicator_name','unique_code','col_value','field','scope']]
    data_nation_1.rename(columns={'unique_code':'region_code','col_value':'indicator_value'},inplace=True)
    data_nation_1=public_col(data_nation_1,year,user_name)
    data_nation_1_=data_nation_1[(data_nation_1['field'].str.contains(field)) & (data_nation_1['scope'].str.contains(scope))]
    #data_nation_1.to_excel('2aa.xlsx')
    data_nation_1['eva_level']=None
    data_nation_1['org_name']=None
    result=input_table(data_nation_1_,engine)
    return result


# In[170]:


def org(data_org,data_dict_region,year,field,scope,user_name,data_dict_org,data_mxk_indicator_system,engine):
#     list_2=[]
#     list_col=data_org.columns.tolist()
#     for i in range(data_org.shape[0]):
#         for j in range(len(list_col)):
#             col_name=list_col[j]
#             col_value=data_org.loc[i,list_col[j]]
#             dict_1={'col_name':col_name,'col_value':col_value}
#             list_2.append(dict_1)
#     data_org_df=pd.DataFrame(list_2)

    data_org_df=public_part(data_org)

    data_org_df['values']=np.where(data_org_df['col_value'].str.contains('^[0-9]{1,}$'),None,data_org_df['col_value'])

    data_org_df['values']=data_org_df['values'].fillna(method='ffill')
    data_org_df=data_org_df[data_org_df['col_name']!='key']
    #data_org_df.to_excel('aaaa.xlsx',index=False)

    org_col_name_inner=pd.merge(data_dict_org,data_org_df,how='inner',left_on='military_name_cn',right_on='values')
    org_col_name_inner.to_excel('ba.xlsx',index=False)
    data_org_1=pd.merge(data_mxk_indicator_system,org_col_name_inner,how='inner',left_on='indicator_name',right_on='col_name')

    data_org_1_=data_org_1[(data_org_1['field'].str.contains(field)) & (data_org_1['scope'].str.contains(scope))]
    #print(data_org_1.columns)
    data_org_1_1=data_org_1_.loc[:,['indicator_id','field','scope',
                                 'indicator_name','id','military_level',
                                 'military_name_cn','col_value','region']]
    #data_org_1_1.to_excel('1.xlsx')
    data_org_2=pd.merge(data_org_1_1,data_dict_region,how='left',left_on='region',right_on='region_name')
    #print(data_org_2.head(2))
    data_org_2=data_org_2.loc[:,['indicator_id','field','scope',
                                 'indicator_name','id_x','military_level',
                                 'military_name_cn','col_value','unique_code']]
    data_org_2.rename(columns={'id_x':'org_id','military_level':'eva_level',
                         'military_name_cn':'org_name','col_value':'indicator_value','unique_code':'region_code'},inplace=True)
    
    data_org_2=public_col(data_org_2,year,user_name)
    #data_org_2.to_excel('1qqq.xlsx')
    result=input_table(data_org_2,engine)
    return result


# In[171]:


def input_table(table,engine):
    # table.to_sql('tjk_indicator_measure_20210809',engine,if_exists='append',index=False)
    try:
        table.to_sql('tjk_indicator_value',engine,if_exists='append',index=False)
        status=1
        
    except Exception as e:
        status=str(e)
    return status
# In[172]:


def gao(path,year,field,scope,user_name,nation_org):
    try:
        # engine=create_engine('mysql+pymysql://root:12345.zcf@localhost/fjkz')
        engine=create_engine(mysql_uri)
        data_dict_region=pd.read_sql_table('dict_region',engine)
        data_dict_org=pd.read_sql_table('dict_org',engine)
        data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',engine)

        #path=r'D:\work\数据添加\部署\mxk_value\value_media_nation_2021.xlsx'
        #year='2021'
        #field='媒体力量'
        #scope='媒体力量'
        #user_name='张冲锋'
        if nation_org =='nation':
            data_nation=pd.read_excel(path)
            result=nation(data_nation,year,field,scope,user_name,data_dict_region,data_mxk_indicator_system,engine)
        else:
            data_org=pd.read_excel(path)
            result=org(data_org,data_dict_region,year,field,scope,user_name,data_dict_org,data_mxk_indicator_system,engine)
        
    except Exception as e:
        result=str(e)
    if result ==1:
        return jsonify(code=200,msg='add success')
        
    else:
        return jsonify(code=400,msg='file err!')


#path=r'D:\work\数据添加\value_scale_org.xlsx'
#year='2001'
#field='媒体力量'
#scope='周边国家'
#user_name='wsh2'
#nation_org='org'
#gao(path,year,field,scope,user_name,nation_org)