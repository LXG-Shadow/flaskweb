from flask import request,abort
from app import newjson
from app.model import user
from base64 import urlsafe_b64decode

def admin_auth_api(funa):
    def auth_wrapper(*args,**kwargs):
        auth = request.cookies.get("auth")
        if auth is None:
            return newjson(7)
        auth = urlsafe_b64decode(auth).decode()
        auth = auth.split("_")
        if len(auth) < 2:
            abort(401)
        usr = user.initFromId(auth[0])
        if usr.is_anonymous() or not usr.is_authenticate(psd=auth[1]):
            abort(401)
        if usr.group.permission < 3:
            abort(403)
        return funa(*args, **kwargs,user=usr)
    return auth_wrapper

def admin_auth_view(funa):
    def auth_wrapper(*args,**kwargs):
        auth = request.cookies.get("auth")
        if auth is None:
            abort(401)
        auth = urlsafe_b64decode(auth).decode()
        auth = auth.split("_")
        if len(auth) < 2:
            abort(401)
        usr =user.initFromId(auth[0])
        if usr.is_anonymous() or not usr.is_authenticate(psd=auth[1]):
            abort(401)
        if usr.group.permission < 3:
            abort(403)
        return funa(*args,**kwargs,user=usr)
    return auth_wrapper