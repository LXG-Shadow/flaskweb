from flask import jsonify

codes = {"-1":"传入参数错误",
         "-2":"请求方式不支持",
         "-3":"服务器内部错误",
         "1":"获取成功",
         "2":"请输入正确的收藏夹链接哦",
         "3":"收藏夹不存在或没有公开,请重试"}

user_groups = {"0":"guest",
               "1":"noraml user",
               "2":"advanced user",
               "3":"admin"}

def newjson(code,data = ""):
    return jsonify({"code":code,"message":codes[code],"data":data})


from app.api.projects import *
