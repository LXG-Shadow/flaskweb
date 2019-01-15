from flask import request,abort
from app import newjson
from app.model import user
from base64 import urlsafe_b64decode

def admin_auth_api(funa):
    def auth_wrapper(*args,**kwargs):
        auth = request.cookies.get("_auth")
        if auth is None:
            abort(401)
        if not user.checkAuthString(auth):
            abort(401)
        user0 = user.initFromPayload(auth.split(".")[1])
        if user0.is_anonymous():
            abort(401)
        if user0.group.permission < 3:
            abort(403)
        return funa(*args, **kwargs,user=user0)
    return auth_wrapper

def admin_auth_view(funa):
    def auth_wrapper(*args,**kwargs):
        auth = request.cookies.get("_auth")
        if auth is None:
            abort(401)
        if not user.checkAuthString(auth):
            abort(401)
        user0 = user.initFromPayload(auth.split(".")[1])
        if user0.is_anonymous():
            abort(401)
        if user0.group.permission < 3:
            abort(403)
        return funa(*args,**kwargs,user=user0)
    return auth_wrapper