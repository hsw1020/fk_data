
# coding: utf-8

# In[1]:

from flask.json import jsonify
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import time
import configparser
cf = configparser.ConfigParser()
cf.read("conf.ini")
mysql_uri = cf.get("mysql", "uri")
engine=create_engine(mysql_uri)


# In[42]:


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
    data_.to_excel('222.xlsx')
    return data_


# In[3]:


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
    data_['update_time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return data_


# In[4]:


def nation(data_nation,year,field,scope,user_name):
#     list_1=[]
#     list_col=data_nation.columns.tolist()
#     for i in range(data_nation.shape[0]):
#         for j in range(len(list_col)):
#             col_name=list_col[j]
#             col_value=data_nation.loc[i,list_col[j]]
#             dict_1={'col_name':col_name,'col_value':col_value}
#             list_1.append(dict_1)
    
#     data_nation_df=pd.DataFrame(list_1)
    data_dict_region=pd.read_sql_table('dict_region',engine)
    data_dict_org=pd.read_sql_table('dict_org',engine)
    data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',engine)
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
    input_table(data_nation_1_)
    return data_nation_1_


# In[186]:


def org(data_org,data_dict_region,year,field,scope,user_name):
#     list_2=[]
#     list_col=data_org.columns.tolist()
#     for i in range(data_org.shape[0]):
#         for j in range(len(list_col)):
#             col_name=list_col[j]
#             col_value=data_org.loc[i,list_col[j]]
#             dict_1={'col_name':col_name,'col_value':col_value}
#             list_2.append(dict_1)
#     data_org_df=pd.DataFrame(list_2)
    data_dict_region=pd.read_sql_table('dict_region',engine)
    data_dict_org=pd.read_sql_table('dict_org',engine)
    data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',engine)
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
    input_table(data_org_2)
    return data_org_2


# In[187]:


def input_table(table):
    # table.to_sql('mxk_indicator_result_20210809',engine,if_exists='append',index=False)
    table.to_sql('tjk_indicator_eva',engine,if_exists='append',index=False)


# In[268]:


#excel中有空值，则打印：excel中存在空值
#excel空表，

#excel中纯数字判断，所存在的数据必须是纯数字；
def digital_judgment(data):
    data_error=[]
    data_shape=data.shape[0]
    if int(data_shape)>=1:
        data_=data[data['col_name']!='key'].reset_index(drop=True)
        #print(data_.head())
        #print(data_.shape[0])
        for ii in range(data_.shape[0]):
            col_value=data_.loc[ii,'col_value']
            if str(col_value).find('nan')>-1:
                #value='excel中存在空值'
                data_error.append('excel中存在空值')
            else:
                try:
                    value=float(col_value)
                except:
                    value='数据内容有误'
                    data_error.append('数据内容有误')
                    break
#         if str(value).find('数据内容有误')>-1 or str(value).find('excel中存在空值')>-1:
#             data_error.append(value)
    else:
        data_error.append('数据不能为空')
    #返回是0，则数据内容没有错误，若返回大于0，则数据内容有问题。
    return len(data_error)


# In[269]:


#三级指标
def system_level(data):
    #根级
    list_root=[]
    for i in range(data.shape[0]):
        data_parentId=data.loc[i,'parentId']
        data_indicator_id=data.loc[i,'indicator_id']
        if data_parentId is None:
            list_root.append(data_indicator_id)
    #一级
    list_one=[]
    for ii in range(len(list_root)):
        root=list_root[ii]
        #print(type(one))
        for i in range(data.shape[0]):
            if data.loc[i,'parentId'] is not None:
                data_parentId=data.loc[i,'parentId']
                #print(int(data_parentId)-int(one))
                data_indicator_id=data.loc[i,'indicator_id']
                if int(data_parentId)-int(root)==0:
                    list_one.append(data_indicator_id)
    #二级
    list_two=[]
    for ii in range(len(list_one)):
        one=list_one[ii]
        #print(type(one))
        for i in range(data.shape[0]):
            if data.loc[i,'parentId'] is not None:
                #data_field=data.loc[i,'field']
                #data_scope=data.loc[i,'scope']
                data_parentId=data.loc[i,'parentId']
                data_indicator_id=data.loc[i,'indicator_id']
                #data_indicator_name=data.loc[i,'indicator_name']
                if int(data_parentId)-int(one)==0:
                    list_two.append(data_indicator_id)
    #三级
    list_three=[]
    for ii in range(len(list_two)):
        two=list_two[ii]
        #print(type(one))
        for i in range(data.shape[0]):
            if data.loc[i,'parentId'] is not None:
                data_field=data.loc[i,'field']
                data_scope=data.loc[i,'scope']
                data_parentId=data.loc[i,'parentId']
                data_indicator_id=data.loc[i,'indicator_id']
                data_indicator_name=data.loc[i,'indicator_name']
                if int(data_parentId)-int(two)==0:
                    disct={
                        'field':data_field,
                        'scope':data_scope,
                        'indicator_name':data_indicator_name
                          }
                    list_three.append(disct)
    level_three=pd.DataFrame(list_three)
    return level_three


# In[270]:


#判断三级指标是否多，或者少
def digital_judgment_system_level(level_three,field,scope,xls_columns):
    data_=level_three[(level_three['field'].str.contains(field)) & (level_three['scope'].str.contains(scope))]

    data_tolist=data_.loc[:,'indicator_name'].tolist()
    xls_columns=xls_columns.tolist()[1:]
    
    a=list(set(data_tolist).difference(set(xls_columns)))
    #print(a)
    #print('----------------------------')
    b=list(set(xls_columns).difference(set(data_tolist)))
    #print(xls_columns)
    #print(b)
    #print('----------------------------')
    if len(a)>0:
        result='三级指标缺少：'+",".join(a)
    elif len(b)>0:
        result='三级指标多了：'+",".join(b)
    else:
        result='三级指标正常'
    return result


# In[271]:


def data_verification(path,user_name,arg,year,field,scope):
    data_dict_region=pd.read_sql_table('dict_region',engine)
    data_dict_org=pd.read_sql_table('dict_org',engine)
    data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',engine)
    level_three=system_level(data_mxk_indicator_system)
   
    data_read=pd.read_excel(path)
    
    data_base=public_part(data_read)
    xls_columns=data_read.columns
   
    three_result=digital_judgment_system_level(level_three,field,scope,xls_columns)
    #print(three_result)
    number_=digital_judgment(data_base)
        #print(three_result)
    if (number_==0) and (three_result.find('三级指标正常'))>-1:
        #print('没问题')
        
        if arg=='nation':
            nation(data_read,year,field,scope,user_name)
        else:
            org(data_read,data_dict_region,year,field,scope,user_name)
        result='导入成功！'
    else:
        if number_!=0:
            result='excel中数据有问题'
            #print('excel中数据有问题')
        elif three_result.find('三级指标正常')<0:
            result='三级指标不匹配'
            #print('三级指标不匹配')
    return result


# In[273]:

def gao(path,year,field,scope,user_name,nation_org):
    try:
        # engine=create_engine('mysql+pymysql://root:12345.zcf@localhost/fjkz')


        #path=r'D:\work\数据添加\部署\mxk_value\value_media_nation_2021.xlsx'
        #year='2021'
        #field='媒体力量'
        #scope='媒体力量'
        #user_name='张冲锋'
        result=data_verification(path,user_name,nation_org,year,field,scope)
        if result != '导入成功！':
            return jsonify(code=400,msg=result)
        return jsonify(code=200,msg=result)
    except Exception as e:
        result=str(e)

        return jsonify(code=400,msg=result)
#path=r'D:\work\数据添加\value_luoyi_nation_10086.xlsx'
#year='2039'
#field='规模结构'
#scope='台湾部队'
#user_name='张冲锋'
#gao(path,year,field,scope,user_name,'org')