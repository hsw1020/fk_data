# coding: utf-8

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import configparser
cf = configparser.ConfigParser()
cf.read("conf.ini")
mysql_uri = cf.get("mysql", "uri")
class E2Q:

    def __init__(self):
        #self.engine=create_engine('mysql+pymysql://user_doc:MYSQL8_document@192.168.43.189:10306/new_schema')
        self.engine=create_engine(mysql_uri)
    def data_range(self):
        # data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system_20210809',self.engine)
        data_mxk_indicator_system=pd.read_sql_table('mxk_indicator_system',self.engine)
        data_max=data_mxk_indicator_system['indicator_id'].max()
        if data_max>=0:
            data_max=data_max
        else:
            data_max=0
        return data_max+1


    def data_(self,data,data_index,field,scope):
        data['field']=field
        data['一级指标']=data['一级指标'].fillna(method='ffill')
        data['二级指标']=data['二级指标'].fillna(method='ffill')

        data_0=data[['field']].drop_duplicates().rename(columns={'field':'指标'})
        data_0['field']=data_0['指标']
        data_1=data[['一级指标','field']].drop_duplicates().rename(columns={'一级指标':'指标'})
        data_2=data[['二级指标','field']].drop_duplicates().rename(columns={'二级指标':'指标'})
        data_3=data[['三级指标','field']].drop_duplicates().rename(columns={'三级指标':'指标'})
        
        data_=pd.concat([data_0,data_1,data_2,data_3])
        data_['id']=range(data_index,data_.shape[0]+data_index)
        
        
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
        #print(type(result_4),result_4)
        data=self.data_input(result_4)
        return data


    def data_input(self,data):
        # data.to_sql('mxk_indicator_system_20210809',self.engine,if_exists='append',index=False)
        data=data.values
        return data

def add_2_sql(field,scope,path):
    e2q = E2Q()
    #path=r'/home/lz/python_workspace/MXK/20210809eva/tree_media_country.xlsx'
    #print(path)
    data=pd.read_excel(path)
    data_index=int(e2q.data_range())
    #print(data_index)
    data=e2q.data_(data,data_index,field,scope)
    return data


if __name__ == '__main__':
    
    # engine=create_engine('mysql+pymysql://root:12345.zcf@localhost/fjkz')
    # path=r'C:\Users\admin\Desktop\指标体系相关\指标体系相关\1指标体系样例_媒体力量.xlsx'

    engine=create_engine(mysql_uri)
    path=r'C:\Users\Administrator\Documents\WeChat Files\wangsihao031516\FileStorage\File\2021-11\军费开支-指标框架(1).xlsx'  #tree_media_country
    field='军费开支'
    scope='周边国家'
    add_2_sql(field,scope,path)
    # path=r'D:\20210809eva\tree_scale_country.xlsx'
    # field='规模结构'
    # scope='周边国家'

    # path=r'D:\20210809eva\tree_scale_twbd.xlsx'
    # field='规模结构'
    # scope='台湾部队'

    # print(path)
    # data=pd.read_excel(path)
    # data_index=int(data_range())
    # #print(data_index)
    # data_(data,data_index,field,scope)
    # print('ok')


