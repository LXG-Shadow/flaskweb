from flask import url_for
from app.mysql.live2d_db import live2dModel_db, live2dTip_db,live2dConfig_db
import os, json,urllib,requests


def loadJsonFile(url):
    try:
        return requests.get(url).json()
    except:
        return None


def urljoin(*args):
    url = []
    for u in args:
        if u[-1] == "/":
            u = u[:-1:]
        url.extend(u.split("/"))
    return "/".join(url)

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
        data = loadJsonFile(urljoin(self.path,"model.json"))
        textures = loadJsonFile(urljoin(self.path,"textures.json"))
        try:
            textures = textures[self.textureId]
        except:
            textures = textures[0]
        textures = list(map(lambda texture:urljoin(self.path,texture),textures))

        data["textures"] = textures

        if not data.get("model") is None:
            data["model"] = urljoin(self.path,data["model"])

        if not data.get("pose") is None:
            data["pose"] = urljoin(self.path,data["pose"])

        if not data.get("motions") is None:
            for key in data["motions"].keys():
                for item in data["motions"][key]:
                    item["file"] = urljoin(self.path, item["file"])

        if not data.get("expressions") is None:
            for item in data["expressions"]:
                item["file"] = urljoin(self.path, item["file"])


        if not data.get("physics") is None:
            data["physics"] = urljoin(self.path, data["physics"])

        return data


class live2dConfig(object):
    def __init__(self, config="default", tip="default", model="kesshouban"):
        if live2dConfig_db.get_by_name(config) is None:
            config = "default"
        self.name = config
        self.configUrl = live2dConfig_db.get_by_name(config).path

        if live2dTip_db.get_by_name(tip) is None:
            tip = "default"
        self.tipsUrl = live2dTip_db.get_by_name(tip).path

        self.modelChangeApi = url_for("api.live2d-model-change")
        self.modelGetApi = url_for("api.live2d-model-get")
        self.model = live2dModel.initByName(model)

    def dump(self):
        try:
            data = loadJsonFile(self.configUrl)
            data["tips"]["Url"] = self.tipsUrl
            data["model"]["ChangeApi"] = self.modelChangeApi
            data["model"]["GetApi"] = self.modelGetApi
            data["model"]["Id"] = self.model.id
            data["model"]["Name"] = self.model.name
            data["model"]["TextureId"] = self.model.textureId
            data["model"]["Url"] = self.modelGetApi+"?id=%s&textureid=%s" % (self.model.id,self.model.textureId)
            return data
        except:
            return {}