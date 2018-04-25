from app import app
from flask import jsonify,request,render_template,url_for,make_response
import datetime
import mysql.connector
import json
import time

from app.api import database

codes = {"-1":"传入参数错误",
         "-2":"请求方式不支持",
         "-3":"服务器内部错误",
         "-4":"你还没登陆呢",
         "-5":"Cookie过期，请重新登陆",
         "-6":"操作越权",
         "1":"登陆成功",
         "2":"用户名不存在",
         "3":"密码错误",
         "4":"注册成功",
         "5":"用户名已存在",
         "6":"信息获取成功",
         "7":"该用户不存在",
         "8":"成功获取用户信息",
         "9":"成功登出",
         "10":"清除所有消息记录成功",
         "11":"",
         "12":"发送的不可为空",
         "13":"发送成功",
         "14": "成功获取用户id",}

user_groups = {"0":"guest",
               "1":"noraml user",
               "2":"advanced user",
               "3":"admin"}

def newjson(code,data = ""):
    return jsonify({"code":code,"message":codes[code],"data":data})

from app.api import login
from app.api import register
from app.api import msgget
from app.api import logout
from app.api import msgsend
from app.api import msgclear

