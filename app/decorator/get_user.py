from flask import request
from app.model import user
from functools import wraps
from base64 import urlsafe_b64decode

def get_user(funa):

    @wraps(funa)
    def user_wrapper(*args,**kwargs):
        auth = request.cookies.get("auth")
        if auth is None:
            return funa(**kwargs,user=user.initNone())
        auth = urlsafe_b64decode(auth).decode()
        auth = auth.split("_")
        if len(auth) < 2:
            return funa(**kwargs,user=user.initNone())
        usr = user.initFromId(auth[0])
        if usr.is_anonymous() or not usr.is_authenticate(psd=auth[1]):
            return funa(**kwargs,user=user.initNone())
        return funa(**kwargs,user=usr)

    return user_wrapper