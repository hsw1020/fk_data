
from passlib.apps import custom_app_context as pwd_context
from extensions import db
class Mxk_indicator_system(db.Model):
    #__abstract__ = True
    __tablename__ = 'mxk_indicator_system'
    indicator_id = db.Column(db.Integer,primary_key=True)
    field = db.Column(db.String(255),nullable=False,unique=True)
    scope = db.Column(db.String(255),nullable=False,unique=True)
    indicator_name = db.Column(db.String(255),nullable=False,unique=True)
    profile = db.Column(db.String(255),nullable=False,unique=True)
    summary = db.Column(db.String(255),nullable=False,unique=True)
    parentId = db.Column(db.String(255),nullable=False,unique=True)
    sort = db.Column(db.Integer,nullable=False,unique=True)
    weight = db.Column(db.String(255),nullable=False,unique=True)
    create_by = db.Column(db.String(255),nullable=False,unique=True)
    create_time = db.Column(db.DateTime,nullable=False,unique=True)
    updateTime = db.Column(db.DateTime,nullable=False,unique=True)
    update_by = db.Column(db.String(255),nullable=False,unique=True)
class mxk_indicator_json(db.Model):
    #__abstract__ = True
    __tablename__ = 'mxk_indicator_json'
    id= db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(255),nullable=False,unique=True)
    field = db.Column(db.String(255),nullable=False,unique=True)
    scope = db.Column(db.String(255),nullable=False,unique=True)
    year = db.Column(db.String(255),nullable=False,unique=True)
    indicator_system= db.Column(db.JSON,nullable=False,unique=True)
    is_delete= db.Column(db.Integer)
    create_by = db.Column(db.String(255),nullable=False,unique=True)
    create_time = db.Column(db.DateTime,nullable=False,unique=True)
    update_by = db.Column(db.String(255),nullable=False,unique=True)
    update_time = db.Column(db.DateTime,nullable=False,unique=True)

class mxk_value(db.Model):
    __tablename__ = 'tjk_indicator_eva'
    id = db.Column(db.Integer,primary_key=True)
    field = db.Column(db.String(255),nullable=False,unique=True)
    scope = db.Column(db.String(255),nullable=False,unique=True)
    year = db.Column(db.String(255),nullable=False,unique=True)
    region_code = db.Column(db.String(255),nullable=False,unique=True)
    region_name = db.Column(db.String(255),nullable=False,unique=True)
    indicator_id = db.Column(db.String(255),nullable=False,unique=True)
    indicator_name = db.Column(db.String(255),nullable=False,unique=True)
    indicator_symbol = db.Column(db.String(255),nullable=False,unique=True)
    indicator_value = db.Column(db.String(255),nullable=False,unique=True)
    indicator_unit = db.Column(db.String(255),nullable=False,unique=True)
    eva_level = db.Column(db.String(255),nullable=False,unique=True)
    org_id = db.Column(db.String(255),nullable=False,unique=True)
    org_name = db.Column(db.String(255),nullable=False,unique=True)
    data_year = db.Column(db.String(255),nullable=False,unique=True)
    data_desc = db.Column(db.String(255),nullable=False,unique=True)
    source = db.Column(db.String(255),nullable=False,unique=True)
    way = db.Column(db.String(255),nullable=False,unique=True)
    create_by = db.Column(db.String(255),nullable=False,unique=True)
    create_time = db.Column(db.DateTime,nullable=False,unique=True)
    update_by = db.Column(db.String(255),nullable=False,unique=True)
    update_time = db.Column(db.DateTime,nullable=False,unique=True)


class Users(db.Model):
    __tablename__ = 'user'#对应mysql数据库表
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(64), unique=True, index=True)
    password= db.Column(db.String(64), unique=True, index=True)
    staff_name= db.Column(db.String(64), unique=True, index=True)
    gender= db.Column(db.String(64), unique=True, index=True)
    department= db.Column(db.String(64), unique=True, index=True)
    user_role= db.Column(db.Integer)
    create_time= db.Column(db.DateTime,nullable=False,unique=True)

    def hash_password(self, password): #给密码加密方法
        self.password = pwd_context.encrypt(password)
 
    def verify_password(self, password): #验证密码方法
        return pwd_context.verify(password, self.password)






class mxk_measure(db.Model):
    __tablename__ = 'mxk_indicator_result'

    id= db.Column(db.Integer,primary_key=True)
    field = db.Column(db.String(255),nullable=False,unique=True)
    scope = db.Column(db.String(255),nullable=False,unique=True)
    year = db.Column(db.String(255),nullable=False,unique=True)
    indicator_id = db.Column(db.String(255),nullable=False,unique=True)
    indicator_name = db.Column(db.String(255),nullable=False,unique=True)
    region_code = db.Column(db.String(255),nullable=False,unique=True)
    score = db.Column(db.String(255),nullable=False,unique=True)
    eva_level = db.Column(db.String(255),nullable=False,unique=True)
    org_id = db.Column(db.String(255),nullable=False,unique=True)
    org_name = db.Column(db.String(255),nullable=False,unique=True)
    create_time= db.Column(db.DateTime,nullable=False,unique=True)
    rank_=db.Column(db.Integer,nullable=False,unique=True)



class mxk_org(db.Model):
    __tablename__ = 'dict_org'
    id= db.Column(db.Integer,primary_key=True)
    region= db.Column(db.String(255),nullable=False,unique=True)
    type= db.Column(db.String(255),nullable=False,unique=True)
    military_level= db.Column(db.String(255),nullable=False,unique=True)
    military_name_cn= db.Column(db.String(255),nullable=False,unique=True)
    base_cn= db.Column(db.String(255),nullable=False,unique=True)
    base_en= db.Column(db.String(255),nullable=False,unique=True)
    latitude= db.Column(db.String(255),nullable=False,unique=True)
    longitude= db.Column(db.String(255),nullable=False,unique=True)
    sort_level=db.Column(db.Integer)
    sort_military=db.Column(db.Integer)


class mxk_region(db.Model):
    __tablename__ = 'dict_region'
    id=db.Column(db.Integer,primary_key=True)
    region_name=db.Column(db.String(255),nullable=False,unique=True)
    unique_code=db.Column(db.String(255),nullable=False,unique=True)
    sort=db.Column(db.Integer)

class mxk_analysis(db.Model):
    __tablename__ = 'cgk_analysis'

    id=db.Column(db.Integer,primary_key=True)
    field=db.Column(db.String(255),nullable=False,unique=True)
    scope=db.Column(db.String(255),nullable=False,unique=True)
    year=db.Column(db.String(255),nullable=False,unique=True)
    region_code=db.Column(db.String(255),nullable=False,unique=True)
    org_code=db.Column(db.String(255),nullable=False,unique=True)
    profile=db.Column(db.String(255),nullable=False,unique=True)
    summary=db.Column(db.String(255),nullable=False,unique=True)
    create_time=db.Column(db.DateTime,nullable=False,unique=True)
    update_time=db.Column(db.DateTime,nullable=False,unique=True)


class mxk_base(db.Model):
    __tablename__ = 'tjk_indicator_base'

    id=db.Column(db.Integer,primary_key=True)
    field=db.Column(db.String(255),nullable=False,unique=True)
    scope=db.Column(db.String(255),nullable=False,unique=True)
    year=db.Column(db.String(255),nullable=False,unique=True)
    region_code=db.Column(db.String(255),nullable=False,unique=True)
    region_name=db.Column(db.String(255),nullable=False,unique=True)
    indicator_name=db.Column(db.String(255),nullable=False,unique=True)
    indicator_symbol=db.Column(db.String(255),nullable=False,unique=True)
    indicator_value=db.Column(db.String(255),nullable=False,unique=True)
    indicator_unit=db.Column(db.String(255),nullable=False,unique=True)
    org_id=db.Column(db.String(255),nullable=False,unique=True)
    org_name=db.Column(db.String(255),nullable=False,unique=True)
    data_year=db.Column(db.String(255),nullable=False,unique=True)
    data_desc=db.Column(db.String(255),nullable=False,unique=True)
    data_source=db.Column(db.String(255),nullable=False,unique=True)
    source=db.Column(db.String(255),nullable=False,unique=True)
    way=db.Column(db.String(255),nullable=False,unique=True)
    create_by=db.Column(db.String(255),nullable=False,unique=True)
    create_time=db.Column(db.DateTime,nullable=False,unique=True)
    update_by=db.Column(db.String(255),nullable=False,unique=True)
    update_time=db.Column(db.DateTime,nullable=False,unique=True)


class mxk_indicator_trans(db.Model):
    __tablename__ = 'mxk_indicator_trans'
    id=db.Column(db.Integer,primary_key=True)
    field=db.Column(db.String(255),nullable=False,unique=True)
    scope=db.Column(db.String(255),nullable=False,unique=True)
    indicator_name=db.Column(db.String(255),nullable=False,unique=True)
    indicator_name_trans=db.Column(db.String(255),nullable=False,unique=True)

class cgk_report(db.Model):
    __tablename__ = 'cgk_report'
    id=db.Column(db.Integer,primary_key=True)
    field=db.Column(db.String(255),nullable=False,unique=True)
    scope=db.Column(db.String(255),nullable=False,unique=True)
    year=db.Column(db.String(255),nullable=False,unique=True)
    region_code=db.Column(db.String(255),nullable=False,unique=True)
    org_code=db.Column(db.String(255),nullable=False,unique=True)
    keywords=db.Column(db.String(255),nullable=False,unique=True)
    report_name=db.Column(db.String(255),nullable=False,unique=True)
    path=db.Column(db.String(255),nullable=False,unique=True)
    create_by=db.Column(db.String(255),nullable=False,unique=True)
    create_time=db.Column(db.DateTime,nullable=False,unique=True)
