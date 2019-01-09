from flask import request

class siteInfo(object):
    def __init__(self,title="LXG_Shadow"):
        self.title = title
        self.blueprint = request.blueprint
        self.endpoint = request.endpoint
        self.parameter = {}

