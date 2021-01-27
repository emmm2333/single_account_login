

class Config(object):
    SECRET_KEY = 'secret key!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/single_account_login_demo?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
