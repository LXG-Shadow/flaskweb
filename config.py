import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'LXGSHADOWLLLLL1234569'
    JSON_AS_ASCII = False
    CSRF_ENABLED = True
    MYSQL_USER = "root"
    MYSQL_PSD = "root"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://lxgshado_admin:adminlyc6969@localhost:3306/lxgshado_website'
    ITEMS_PER_PAGE = 10
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/website'

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://lxgshado_admin:adminlyc6969@localhost:3306/lxgshado_website'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
