from flask import Flask,jsonify,request,current_app
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_babel import Babel
from config import config
import os



base_dir = os.path.dirname(os.path.abspath(__file__))
bootstrap = Bootstrap()
db = SQLAlchemy()
pagedown = PageDown()
babel = Babel()


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

codesmap = {"-1":_l("Invalid Parameters"),
            "-2":_l("This method is not supported by this URL"),
            "-3":_l("Server Internal Error"),
            "1":_l("Get Success"),
            "2":"请输入正确的收藏夹链接哦",
            "3":"收藏夹不存在或没有公开(或用户隐私设置未打开), 请重试",
            "4":_l("This username already exists"),
            "5":_l("This email already exists"),
            "6":_l("Register Success"),
            "7":_l("You have not login in"),
            "8":_l("Invalid username or password"),
            "9":_l("Login Success"),
            "10":_l("Logout Success"),
            "11":_l("This article title already exists"),
            "12":_l("Post article success"),
            "13":_l("This article not exists"),
            "14":_l("Updated article success"),
            "15":_l("Delete article success"),
            "16":_l("Updated success"),
            "17":_l("This file does not exists or already be deleted"),
            "18":_l("Delete file success"),
            "19":_l("Add file success"),
            "20":_l("Updated file information success"),
            "21":_l("Same name already exists")}

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
    babel.init_app(app)



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