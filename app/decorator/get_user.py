from flask import request
from app.model import user
from functools import wraps
from base64 import urlsafe_b64decode

def get_user(funa):

    @wraps(funa)
    def user_wrapper(*args,**kwargs):
        auth = request.cookies.get("_auth")
        if auth is None:
            return funa(**kwargs,user=user.initNone())
        if not user.checkAuthString(auth):
            return funa(**kwargs, user=user.initNone())
        return funa(**kwargs,user=user.initFromPayload(auth.split(".")[1]))
    return user_wrapper