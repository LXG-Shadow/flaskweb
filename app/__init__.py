from flask import Flask,jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from config import config
import os



base_dir = os.path.dirname(os.path.abspath(__file__))
bootstrap = Bootstrap()
db = SQLAlchemy()
pagedown = PageDown()

codesmap = {"-1":"传入参数错误",
            "-2":"请求方式不支持",
            "-3":"服务器内部错误",
            "1":"获取成功",
            "2":"请输入正确的收藏夹链接哦",
            "3":"收藏夹不存在或没有公开(或用户隐私设置未打开), 请重试",
            "4":"用户名已存在",
            "5":"邮箱已存在",
            "6":"注册成功",
            "7":"未登录",
            "8":"用户名或密码错误",
            "9":"登陆成功",
            "10":"登出成功",
            "11":"文章标题重复",
            "12":"发表文章成功",
            "13":"没有此文章",
            "14":"更新文章成功",
            "15":"删除文章成功",
            "16":"修改成功",
            "17":"没有该文件或文件已被删除",
            "18":"删除文件成功",
            "19":"添加文件成功",
            "20":"文件信息修改成功",
            "21":"相同名称已存在"}

def newjson(code,data = ""):
    return jsonify({"code":code,"message":codesmap[code],"data":data})


def tb(app):
    #from app.model.mysql.blog import article_db,articleSource_db,articleType_db,articleTypeSetting
    #from app.model.mysql import user_db
    #from app.model.mysql.blog import article_db
    #from app.model.mysql.file_db import file_db
    from app.model.mysql.live2d_db import live2dTip_db,live2dModel_db
    #db.drop_all(app=app)
    db.create_all(app=app)


def app_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)


def app_blueprints(app):
    from .views.projects import projects as projects_blueprint
    from .views.auth import auth as auth_blueprint
    from .views.blog import blog as blog_blueprint
    from .views.space import space as space_blueprint
    from .views.admin import admin as admin_blueprint
    from .views.files import files as files_blueprint
    from .views import main as main_blueprint
    from .api import api as api_blueprint

    app.register_blueprint(projects_blueprint,url_prefix='/projects')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint,url_prefix= "/api")
    app.register_blueprint(auth_blueprint,url_prefix="/auth")
    app.register_blueprint(blog_blueprint, url_prefix="/blog")
    app.register_blueprint(space_blueprint, url_prefix="/space")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(files_blueprint, url_prefix="/files")

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app_extensions(app)
    app_blueprints(app)

    #tb(app)

    return app