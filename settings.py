import configparser

class Baseconfig():
    cf = configparser.ConfigParser()
    cf.read("conf.ini")
    mysql_uri = cf.get("mysql", "uri")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = mysql_uri
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS= True
    SQLALCHEMY_ECHO = True
class Testconfig(Baseconfig):
    TEST_MODE=True
class Production(Baseconfig):
    pass
config={
    'testing':Testconfig,
    'production':Production
}