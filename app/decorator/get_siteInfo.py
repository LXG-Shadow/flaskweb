from app.model.blog import blogInfo
from ..model import siteInfo
from functools import wraps


def get_siteInfo(title):
    def decorator(funa):
        @wraps(funa)
        def siteInfo_wrapper(*args, **kwargs):
            return funa(**kwargs, siteInfo=siteInfo(title=title))

        return siteInfo_wrapper

    return decorator


def get_blogInfo(title):
    def decorator(funa):
        @wraps(funa)
        def blogInfo_wrapper(*args, **kwargs):
            return funa(**kwargs, siteInfo=blogInfo(title=title))

        return blogInfo_wrapper

    return decorator
