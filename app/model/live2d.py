from flask import url_for
from .mysql.live2d_db import live2dModel_db, live2dTip_db
from app import base_dir
import os, json


def loadJsonFile(filedir, prefix="static"):
    data = {}
    try:
        with open(os.path.join(base_dir, prefix, filedir), "r", encoding="utf-8") as f:
            data = json.loads(f.read())
    except:
        pass
    return data


class live2dModel(object):
    def __init__(self, id, name, path, textureId):
        self.id = id
        self.name = name
        self.path = path
        self.textureId = textureId

    @classmethod
    def initById(cls, id=1, textureId=0):
        model = live2dModel_db.get_by_id(id)
        if model is None:
            return cls.initById()
        return cls(model.id, model.name, model.path, textureId)

    @classmethod
    def initByName(cls, name="kesshouban", textureId=0):
        model = live2dModel_db.get_by_name(name)
        if model is None:
            return cls.initById()
        return cls(model.id, model.name, model.path, textureId)

    def dump(self):
        data = loadJsonFile(os.path.join(self.path,"model.json"))
        textures = loadJsonFile(os.path.join(self.path,"textures.json"))
        try:
            textures = textures[self.textureId]
        except:
            textures = textures[0]
        textures = list(map(lambda texture:"../../../../../.."+url_for("static",filename = os.path.join(self.path,texture)),textures))

        data["textures"] = textures

        data["model"] = "../../../../../.."+url_for("static",filename = os.path.join(self.path,"model.moc"))

        if not data.get("pose") is None:
            data["pose"] = "../../../../../.." + url_for("static", filename=os.path.join(self.path, "pose.josn"))

        if not data.get("motions") is None:
            for key in data["motions"].keys():
                for item in data["motions"][key]:
                    item["file"] = "../../../../../.."+url_for("static", filename=os.path.join(self.path, item["file"]))

        if not data.get("expressions") is None:
            for item in data["expressions"]:
                item["file"] = "../../../../../.."+url_for("static", filename=os.path.join(self.path, item["file"]))


        if not data.get("physics") is None:
            data["physics"] = "../../../../../.."+url_for("static", filename=os.path.join(self.path, data["physics"]))

        return data


class live2dConfig(object):
    def __init__(self, config="default", tip="default", model="kesshouban"):
        self.name = config

        if live2dTip_db.get_by_name(tip) is None:
            tip = "default"
        self.tipsUrl = url_for("static", filename=live2dTip_db.get_by_name(tip).path)

        self.modelChangeApi = url_for("api.live2d-model-change")
        self.modelGetApi = url_for("api.live2d-model-get")
        self.model = live2dModel.initByName(model)

    def dump(self):
        data = loadJsonFile("live2d/config/%s.json" % self.name)
        if not bool(data):
            data = loadJsonFile("live2d/config/default.json")

        data["tips"]["Url"] = self.tipsUrl

        data["model"]["ChangeApi"] = self.modelChangeApi
        data["model"]["GetApi"] = self.modelGetApi
        data["model"]["Id"] = self.model.id
        data["model"]["Name"] = self.model.name
        data["model"]["TextureId"] = self.model.textureId
        data["model"]["Url"] = self.modelGetApi+"?id=%s&textureid=%s" % (self.model.id,self.model.textureId)

        return data