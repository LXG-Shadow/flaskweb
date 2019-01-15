from flask import abort, render_template, request
from flask_babel import lazy_gettext as _l
from . import files
from ...model.file import file
from app.decorator import get_user, get_siteInfo


@files.route("/detail", endpoint="detail")
@get_siteInfo(_l("File Detail"))
@get_user
def files_detail(*args, **kwargs):
    id = request.args.get('id', 0, type=int)
    alias = request.args.get("alias", "", type=str)
    if not id and not alias:
        abort(404)
    if id:
        file0 = file.initFromId(id)
    else:
        file0 = file.initFromAlias(alias)
    if file0.isNone():
        abort(404)
    if not file0.isAccessible(kwargs["user"]):
        abort(403)
    return render_template("/files/file_detail.html", file=file0, **kwargs)

# @files.route("/share",endpoint="share")
# @get_siteInfo("文件分享")
# @get_user
# def files_share(*args, **kwargs):
#     id = request.args.get('id', 0, type=int)
#     alias = request.args.get("alias", "", type=str)
#     if not id and not alias:
#         abort(404)
#     if id:
#         file0 = file.initFromId(id)
#     else:
#         file0 = file.initFromAlias(alias)
#     if file0.isNone():
#         abort(404)
#     if not file0.isAccessible(kwargs["user"]):
#         abort(403)
#     return render_template("/files/file_share.html",file=file0,**kwargs)
