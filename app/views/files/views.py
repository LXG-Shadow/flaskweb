from flask import abort, render_template, request,redirect,url_for
from flask_babel import lazy_gettext as _l
from . import files
from ...model.file import file
from app.decorator import get_user, get_siteInfo


@files.route("/detail/<int:id>", endpoint="detail")
@get_siteInfo(_l("File Detail"))
@get_user
def files_detail(*args, **kwargs):
    id = kwargs.pop("id")
    if id == 0:
        alias = request.args.get("alias", "", type=str)
        if not alias:
            abort(404)
        file0 = file.initFromAlias(alias)
        if file0.isNone():
            abort(404)
        return redirect(url_for("files.detail",id=file0.id))
    file0 = file.initFromId(id)
    if file0.isNone():
        abort(404)
    if not file0.isAccessible(kwargs["user"]):
        abort(403)
    return render_template("files/file_detail.html", file=file0, **kwargs)
