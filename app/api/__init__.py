from flask import jsonify

from flask import Blueprint

api = Blueprint('api',__name__)

from app import codesmap,newjson,base_dir

from .projects import *
from .live2d_api import *
