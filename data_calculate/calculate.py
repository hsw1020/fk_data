
# coding: utf-8

# In[2]:

import configparser
import pandas as pd
import numpy as np
import re
import time
from sqlalchemy import create_engine
import pymysql
cf = configparser.ConfigParser()
cf.read("conf.ini")
mysql_uri = cf.get("mysql", "uri")

# In[47]:

engine=create_engine(mysql_uri)
user=re.findall('//(.*?):',mysql_uri)[0]

password=re.findall('//.*:(.*?)@',mysql_uri)[0]
host=re.findall('@(.*?):',mysql_uri)[0]
port=re.findall('.*:.*:.*:(.*)/',mysql_uri)[0]
ku=re.findall('.*:.*:.*:.*/(.*)',mysql_uri)[0]

db=pymysql.connect(host=host,user=user,passwd=password,database=ku,port=int(port))
def truncate_table(table,db):
    db = db
    #使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql='truncate table '+table
    try:
        # 执行SQL语句
        ds=cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print("失败")
        print(e)
        #发生错误时回滚
        db.rollback()
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        #db.close()


# In[48]:


def input_table(data,table,db):
    db =db
    #使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    columns = ','.join(list(data.columns))

    data_list=[tuple(i) for i in data.values]
    s_count = (len(data_list[0])) * "%s,"
    #print(s_count)
    
    insert_sql = "insert into " +table+ " (" + columns + ") values (" + s_count[:-1] + ")"
    #print(insert_sql)
    #print(data_list)
    try:
        #print(data.apply(tuple, axis=1))
        cursor.executemany(insert_sql,data_list)
        print('完成计算！')
        db.commit()
    except Exception as e:
        print('失败！')
        print(e)
        db.rollback()
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        #db.close()


# In[49]:


def delete_data(field_,scope_,data_table,db):
    db = db
    #使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql='DELETE from '+ data_table + ' where field='+'''"'''+ field_ +'''"'''+ ' AND scope='+'''"'''+ scope_ +'''"'''
    # print(sql)
    try:
        # 执行SQL语句
        ds=cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print("失败")
        print(e)
        #发生错误时回滚
        db.rollback()
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        #db.close()


# In[50]:


def level_():
    data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',engine)
    data_mxk_indicator_system['indicator_id']=data_mxk_indicator_system['indicator_id'].astype('str')
    data_level_1=data_mxk_indicator_system[data_mxk_indicator_system['parentId'].isnull()]
    
    data_level_1=data_level_1.loc[:,['indicator_id', 'field', 'scope', 'indicator_name', 'profile',
       'summary', 'parentId', 'sort', 'weight']]
    data_level_1['level']='根级'
    
    data_level_2=pd.merge(data_level_1,
         data_mxk_indicator_system,
         how='inner',
        left_on='indicator_id',
        right_on='parentId')
    
    data_level_2=data_level_2.loc[:,['indicator_id_y','field_y','scope_y',#'scope_y',
                    'indicator_name_y','profile_y','summary_y',
                    'parentId_y','sort_y','weight_y']]
    data_level_2=data_level_2.rename(columns={'indicator_id_y':'indicator_id','field_y':'field',
                                              'scope_y':'scope','indicator_name_y':'indicator_name',
                                              'profile_y':'profile','summary_y':'summary','parentId_y':'parentId',
                                              'sort_y':'sort','weight_y':'weight'})
    data_level_2['level']='一级'
    
    data_level_3=pd.merge(data_level_2,
         data_mxk_indicator_system,
         how='inner',
        left_on='indicator_id',
        right_on='parentId')
    
    data_level_3=data_level_3.loc[:,['indicator_id_y','field_y','scope_y',
                    'indicator_name_y','profile_y','summary_y',
                    'parentId_y','sort_y','weight_y']]
    data_level_3=data_level_3.rename(columns={'indicator_id_y':'indicator_id','field_y':'field',
                                              'scope_y':'scope','indicator_name_y':'indicator_name',
                                              'profile_y':'profile','summary_y':'summary','parentId_y':'parentId',
                                              'sort_y':'sort','weight_y':'weight'})
    data_level_3['level']='二级'
    
    data_level_4=pd.merge(data_level_3,
         data_mxk_indicator_system,
         how='inner',
        left_on='indicator_id',
        right_on='parentId')
    
    
    data_level_4=data_level_4.loc[:,['indicator_id_y','field_y','scope_y',
                    'indicator_name_y','profile_y','summary_y',
                    'parentId_y','sort_y','weight_y']]
    data_level_4=data_level_4.rename(columns={'indicator_id_y':'indicator_id','field_y':'field',
                                              'scope_y':'scope','indicator_name_y':'indicator_name',
                                              'profile_y':'profile','summary_y':'summary','parentId_y':'parentId',
                                              'sort_y':'sort','weight_y':'weight'})
    data_level_4['level']='三级'
    
    data_level_5=pd.merge(data_level_4,
         data_mxk_indicator_system,
         how='inner',
        left_on='indicator_id',
        right_on='parentId')
    
    data_level_concat=pd.concat([data_level_1,data_level_2,data_level_3,data_level_4])
    
    data_level_1_2=pd.merge(data_level_1,data_level_2,how='left',left_on=['field','indicator_id'],right_on=['field','parentId'])
    
    data_level_1_2=data_level_1_2.rename(columns={'indicator_id_x':'indicator_id_0',
                            'field':'field',
                            'scope_x' :'scope_0', 
                            'indicator_name_x':'indicator_name_0',
                            'profile_x':'profile_0',
                            'summary_x':'summary_0',
                            'parentId_x':'parentId_0',
                            'sort_x':'sort_0',
                            'weight_x':'weight_0',
                            'level_x':'level_0',
                            'indicator_id_y':'indicator_id_1',
                            'scope_y':'scope_1',
                            'indicator_name_y':'indicator_name_1',
                            'profile_y':'profile_1',
                            'summary_y':'summar2_1',
                            'parentId_y':'parentId_1',
                            'sort_y':'sort_1',
                            'weight_y':'weight_1',
                            'level_y':'level_1'})
    
    data_level_1_2_3=pd.merge(data_level_1_2,data_level_3,how='left',left_on=['field','indicator_id_1'],right_on=['field','parentId'])
    
    data_level_1_2_3=data_level_1_2_3.rename(columns={'indicator_id':'indicator_id_2', 
                                 'scope':'scope_2', 'indicator_name':'indicator_name_2',
                                 'profile':'profile_2', 'summary':'summary_2',
                                 'parentId':'parentId_2', 'sort':'sort_2', 
                                 'weight':'weight_2', 'level':'level_2'})
    
    data_level_1_2_3_4=pd.merge(data_level_1_2_3,data_level_4,how='left',left_on=['field','indicator_id_2'],right_on=['field','parentId'])
    
    data_level_1_2_3_4=data_level_1_2_3_4.rename(columns={'indicator_id':'indicator_id_3', 
                                                      'scope':'scope_3', 'indicator_name':'indicator_name_3',
                                                      'profile':'profile_3', 'summary':'summary_3',
                                                      'parentId':'parentId_3', 'sort':'sort_3',
                                                      'weight':'weight_3', 'level':'level_3'})
    return data_level_1_2_3_4


# In[51]:


def choice_nation_org(field_,scope_):
    if field_.find('all')>-1:
        data_tjk_indicator_value=pd.read_sql_table('tjk_indicator_value',engine)
    else:
        data_tjk_indicator_value=pd.read_sql_table('tjk_indicator_value',engine)
        data_tjk_indicator_value=data_tjk_indicator_value[(data_tjk_indicator_value['field']==field_) & 
                                                          (data_tjk_indicator_value['scope']==scope_)]
    #print(data_tjk_indicator_value.head())
    data_tjk_indicator_value['region_code']=np.where(data_tjk_indicator_value['org_id'].isnull(),
             data_tjk_indicator_value['region_code'],
             data_tjk_indicator_value['region_code'].astype(str)+'_'+data_tjk_indicator_value['org_name'])
    
    data_tjk_indicator_value['eva_level']=np.where(data_tjk_indicator_value['org_id'].isnull(),'占位符',data_tjk_indicator_value['eva_level'])
    
    return data_tjk_indicator_value


# In[52]:


#三级分值计算
def level_3_calculation(field_,scope_):
    #data_tjk_indicator_value=pd.read_sql_table('tjk_indicator_value',engine)

    data_tjk_indicator_value=choice_nation_org(field_,scope_)
    data_tjk_indicator_value['indicator_value_0_1']=data_tjk_indicator_value.groupby(['field',
                                                                                      'scope',
                                                                                      'year',
                                                                                      'eva_level',
                                                                                      'indicator_name'])['indicator_value'].apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    
    data_tjk_indicator_value['score']=data_tjk_indicator_value['indicator_value_0_1']
    data_3=data_tjk_indicator_value.loc[:,['field','year','region_code','eva_level','scope',
                                'indicator_id','indicator_name','score']]
    
    data_3['score']=np.where(data_3['score']==0,0.00001,data_3['score'])
    
    return data_3


# In[53]:


#二级分值计算
def level_2_calculation(field_,scope_):
    data_0803=level_()
    data_3=level_3_calculation(field_,scope_)
    level_2_data=pd.merge(data_3,
         data_0803,
         how='inner',
         left_on=['indicator_id'],
         right_on=['indicator_id_3'])
    
    level_2_data['score']=level_2_data['score'].astype(float)
    level_2_data['weight_3']=level_2_data['weight_3'].astype(float)
    level_2_data['step_2']=level_2_data['score']*level_2_data['weight_3']
    #print(level_2_data.head())
    level_2=pd.DataFrame()

    level_2['level_3_sum']=level_2_data.groupby(['field_x','scope','year','eva_level','region_code','indicator_id_1',
                                        'indicator_name_1','indicator_id_2','indicator_name_2'])['step_2'].sum()
    
    level_2=level_2.reset_index()
    
    level_2['score']=np.where(level_2['level_3_sum']==0,0.00001,level_2['level_3_sum'])
    
    #0-1标准化
    level_2['indicator_value_0_1']=level_2.groupby(['field_x','scope','year','eva_level',
                                                'indicator_id_1','indicator_name_1',
                                                'indicator_id_2','indicator_name_2'])['score'].apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    
    level_2['indicator_value_0_1']=np.where(level_2['indicator_value_0_1']==0,0.00001,level_2['indicator_value_0_1'])
    
    level_2=level_2.loc[:,['field_x','scope','year','region_code','eva_level','indicator_id_2','indicator_name_2','indicator_value_0_1']]
    data_2=level_2.rename(columns={'field_x':'field','indicator_name_2':'indicator_name','indicator_id_2':'indicator_id',
                                'indicator_value_0_1':'score'})
    
    return data_2


# In[54]:


#一级分值计算
def level_1_calculation(field_,scope_):
    data_0803=level_()
    data_2=level_2_calculation(field_,scope_)
    level_3_data=pd.merge(data_2,
         data_0803,
         how='inner',
         left_on='indicator_id',
         right_on='indicator_id_2')
    
    level_3_data['score']=level_3_data['score'].astype(float)
    level_3_data['weight_2']=level_3_data['weight_2'].astype(float)
    
    level_3_data['step_1']=level_3_data['score']*level_3_data['weight_2']
    
    level_3_data_=level_3_data.loc[:,['field_x','scope','year','eva_level','region_code','indicator_id_1',
                    'indicator_name_1','score','weight_2','step_1']]
    level_3_data_.drop_duplicates(inplace=True)
    
    level_1=pd.DataFrame()
    level_1['level_2_sum']=level_3_data_.groupby(['field_x','scope','year','eva_level','region_code','indicator_id_1',
                                        'indicator_name_1'])['step_1'].sum()
    level_1=level_1.reset_index()
    level_1['score']=np.where(level_1['level_2_sum']==0,0.00001,level_1['level_2_sum'])
    
    level_1['indicator_value_0_1']=level_1.groupby(['field_x','scope','year','eva_level',
                                                'indicator_id_1','indicator_name_1'
                                                ])['score'].apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    
    level_1['indicator_value_0_1']=np.where(level_1['indicator_value_0_1']==0,0.00001,level_1['indicator_value_0_1'])
    #print(level_1.columns)
    level_1=level_1.loc[:,['field_x','scope','year','eva_level','region_code','indicator_id_1','indicator_name_1','indicator_value_0_1']]
    data_1=level_1.rename(columns={'field_x':'field','indicator_name_1':'indicator_name','indicator_id_1':'indicator_id',
                                'indicator_value_0_1':'score'})
    return data_1


# In[55]:


def level_root_calculation(field_,scope_):
    data_0803=level_()
    data_1=level_1_calculation(field_,scope_)
    level_root_data=pd.merge(data_1,
         data_0803,
         how='inner',
         left_on='indicator_id',
         right_on='indicator_id_1')
    level_root_data['score']=level_root_data['score'].astype(float)
    level_root_data['weight_1']=level_root_data['weight_1'].astype(float)
    
    level_root_data['step_0']=level_root_data['score']*level_root_data['weight_1']
    
    level_root_data_=level_root_data.loc[:,['field_x','scope','year','eva_level','region_code','indicator_id_0',
                    'indicator_name_0','score','weight_1','step_0']]
    level_root_data_.drop_duplicates(inplace=True)
    
    level_0=pd.DataFrame()
    
    level_0['level_1_sum']=level_root_data_.groupby(['field_x','scope','year','eva_level','region_code','indicator_id_0',
                                        'indicator_name_0'])['step_0'].sum()
    
    level_0=level_0.reset_index()
    level_0['score']=np.where(level_0['level_1_sum']==0,0.00001,level_0['level_1_sum'])
    
    level_0['indicator_value_0_1']=level_0.groupby(['field_x','scope','year','eva_level',
                                                'indicator_id_0','indicator_name_0'
                                                ])['score'].apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    
    level_0['indicator_value_0_1']=np.where(level_0['indicator_value_0_1']==0,0.00001,level_0['indicator_value_0_1'])
    #print(level_0.head())
    level_0=level_0.loc[:,['field_x','scope','year','eva_level','region_code','indicator_id_0','indicator_name_0','indicator_value_0_1']]
    data_0=level_0.rename(columns={'field_x':'field','indicator_name_0':'indicator_name','indicator_id_0':'indicator_id',
                                'indicator_value_0_1':'score'})
    return data_0


# In[56]:


def data_input(field_,scope_):
    data_3=level_3_calculation(field_,scope_)
    data_2=level_2_calculation(field_,scope_)
    data_1=level_1_calculation(field_,scope_)
    data_0=level_root_calculation(field_,scope_)
    data_inner=pd.concat([data_0,data_1,data_2,data_3])
    data_inner['score']=np.where(data_inner['score'].isnull()==True,None,(data_inner['score']*100).round(2))
    #data_inner.to_sql(data_table,engine,if_exists='append',index=False)
    return data_inner


# In[57]:


def get_org(data_table,field_,scope_):
    df=data_input(field_,scope_)
    
    dict_org=pd.read_sql_table('dict_org',engine)
    df['region_code']=np.where(df['region_code'].str.contains('_'),df['region_code'],df['region_code']+str('_'))
    df['region_code_']=df['region_code'].str.split('_',expand=True)[0]
    df['org_name_']=df['region_code'].str.split('_',expand=True)[1]
    df_org=pd.merge(df,
             dict_org,
             how='left',left_on='org_name_',right_on='military_name_cn',sort=True)
    #print(df_org.columns)
    df_org=df_org.loc[:,['field', 'indicator_id', 'region_code_',
                         'indicator_name','scope','score',
                         'year','id','military_level','military_name_cn']]
    
    df_org=df_org.drop_duplicates()
    df_org=df_org.rename(columns={'region_code_':'region_code',
                                  'id':'org_id',
                                  'military_level':'eva_level',
                                  'military_name_cn':'org_name'})
    #print(df_org.head())
    df_org=df_org.drop_duplicates()

    df_org['create_time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    df_org['create_time']=df_org['create_time'].astype(str)
    
    df_org['org_id']=np.where(df_org['org_id'].isnull(),None,df_org['org_id'])
    df_org['eva_level']=np.where(df_org['eva_level'].isnull(),None,df_org['eva_level'])
    df_org['org_name']=np.where(df_org['org_name'].isnull(),None,df_org['org_name'])

    df_org['field']=np.where(df_org['field'].isnull(),None,df_org['field'])
    df_org['indicator_id']=np.where(df_org['indicator_id'].isnull(),None,df_org['indicator_id'])
    df_org['region_code']=np.where(df_org['region_code'].isnull(),None,df_org['region_code'])
    df_org['indicator_name']=np.where(df_org['indicator_name'].isnull(),None,df_org['indicator_name'])

    df_org['scope']=np.where(df_org['scope'].isnull(),None,df_org['scope'])
    df_org['score']=np.where(df_org['score'].isnull(),None,df_org['score'])
    df_org['year']=np.where(df_org['year'].isnull(),None,df_org['year'])
    df_org=df_org.reset_index(drop=True)
    #df_org.to_excel('111.xlsx')
    #df_org.to_csv(r'E:\sy\规模结构库_新\11_result_csv.csv',index=False)
    if field_.find('all')>-1:
        truncate_table(data_table,db)
        #print('------')
        input_table(df_org,data_table,db)
        #df_org.to_sql(data_table,engine,if_exists='append',index=False)
    # elif field_.find('规模结构')>-1 & scope_.find('周边国家')>-1:
    #     df_org_=df_org[(df_org['field'].str.contains(field_)) & (df_org['scope'].str.contains(scope_))]
    #     input_table(df_org_,data_table,db)
    else:
        #df_org.to_sql(data_table,engine,if_exists='append',index=False)
        delete_data(field_,scope_,data_table,db)
        df_org_=df_org[(df_org['field'].str.contains(field_)) & (df_org['scope'].str.contains(scope_))]
        input_table(df_org_,data_table,db)
    return df_org


# In[60]:




# # In[59]:


# db=pymysql.connect(host="localhost",user="root",passwd="12345.zcf",database="fjkz")
    
# data_table='tjk_indicator_calculation_20210819_copy1'

# #field_='all'
# field_='规模结构'
# #field_='all'
# scope_='周边国家'

# delete_data(field_,scope_,data_table,db)


# # In[ ]:


# #当field_='规模结构'，scope_='周边国家'时，则表中数据删除，插入新计算的数据

