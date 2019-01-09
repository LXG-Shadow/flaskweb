from flask import request
from app import newjson,jsonify
from . import api,base_dir
from ..model.live2d import live2dConfig,live2dModel
import os,json

path = "live2d/model/bilibili-live/22/model.json"

def loadJsonFile(filedir,prefix="static"):
    data = {}
    with open(os.path.join(base_dir,prefix,filedir),"r",encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


@api.route("/live2d/config/get",endpoint="live2d-config-get",methods = ["GET","POST"])
def live2d_getConfig():
    config = request.values.get("config","default",type=str)
    tip = request.values.get("tip", "default", type=str)
    model = request.values.get("model","kesshouban",type=str)
    return newjson("1",data=live2dConfig(config,tip,model).dump())


@api.route("/live2d/model/get",endpoint="live2d-model-get",methods = ["GET","POST"])
def live2d_getModel():
    id = request.values.get("id",1,type=int)
    name = request.values.get("name","",type=str)
    textureId = request.values.get("tid",0,type=int)
    changeModel = request.values.get("cm", 0, type=int)
    changeTexture = request.values.get("ct",0,type=int)
    id += changeModel
    textureId += changeTexture
    if name != "":
        model = live2dModel.initByName(name,textureId)
    else:
        model = live2dModel.initById(id,textureId)
    return jsonify(model.dump())

@api.route("/live2d/model/change",endpoint="live2d-model-change",methods = ["GET","POST"])
def live2d_getModel():
    id = request.values.get("id",1,type=int)
    name = request.values.get("name","",type=str)
    textureId = request.values.get("tid",0,type=int)
    changeModel = request.values.get("cm", 0, type=int)
    changeTexture = request.values.get("ct",0,type=int)
    id += changeModel
    textureId += changeTexture
    if name != "":
        model = live2dModel.initByName(name,textureId)
    else:
        model = live2dModel.initById(id,textureId)
    return newjson("1",data={"Id":model.id,
                             "TextureId":model.textureId,
                             "Name":model.name})
