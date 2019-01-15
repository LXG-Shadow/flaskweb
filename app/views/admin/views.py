from flask import redirect, render_template, request, abort,url_for
from flask_babel import lazy_gettext as _l
from app import codesmap
from ...decorator.admin_auth import admin_auth_view
from ...decorator import get_siteInfo
from ...model.user import users, user
from ...model.blog import articles, article
from ...model.file import file, files
from ...model.mysql.blog.article_db import articleType_db, articleSource_db
from .forms import UserEditForm, UserRegisterForm, PageDownForm, DeleteForm, AdvancedPageDownForm,FileUploadForm,FileEditForm
from . import admin


@admin.route("/", endpoint="index", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("Admin Backend"))
def admin_index(**kwargs):
    return render_template("/admin/index.html", **kwargs)


@admin.route("/user-manage", endpoint="user-manage", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("User Management"))
def admin_user_manage(**kwargs):
    page = request.args.get('page', 1, type=int)
    users0 = users.initFromAll(page)
    if users0.isNone():
        abort(404)
    return render_template("/admin/user/user_manage.html", pagination=users0.pagination, **kwargs)


@admin.route("/user-manage/edit/<int:id>", endpoint="user-edit", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("User Profile Editor"))
def admin_user_edit(**kwargs):
    form = UserEditForm()
    user0 = user.initFromId(kwargs["id"])
    if user0.is_anonymous():
        abort(404)
    if request.method == "POST":
        if form.validate_on_submit():
            form.id.data = user0.id
            username = form.username.data
            email = form.email.data
            group = form.group.data
            if len(form.password.data) == 0:
                status = user.edit(kwargs["id"], username, email, group_id=group.id)
            elif len(form.password.data) > 16 or len(form.password.data) < 6:
                return render_template('/admin/user/user_manage_edit.html', message=("warning", codesmap[str(-1)]),
                                       form=form, **kwargs)
            else:
                status = user.edit(kwargs["id"], username, email, password=form.password.data, group_id=group.id)

            if status[0]:
                form.password.data = ""
                return render_template('/admin/user/user_manage_edit.html', form=form,
                                       message=("success", codesmap[str(status[1])]), **kwargs)
            else:
                form.id.data = user0.id
                form.username.data = user0.name
                form.email.data = user0.email
                return render_template('/admin/user/user_manage_edit.html', form=form,
                                       message=("warning", codesmap[str(status[1])]), **kwargs)
        return render_template('/admin/user/user_manage_edit.html', message=("warning", codesmap[str(-1)]),
                               form=form, **kwargs)
    form.id.data = user0.id
    form.username.data = user0.name
    form.email.data = user0.email
    form.group.data = user0.getGroup()
    return render_template("/admin/user/user_manage_edit.html", form=form, **kwargs)


@admin.route("/user-manage/register", endpoint="user-register", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("New User"))
def admin_user_register(**kwargs):
    form = UserRegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            group = form.group.data
            status = user.register(username, password, email, group_id=group.id)
            if status[0]:
                form.id.data = status[2]
                return render_template('/admin/user/user_manage_edit.html', form=form,
                                       message=("success", codesmap[str(status[1])]), **kwargs)
            else:
                return render_template('/admin/user/user_manage_edit.html', form=form,
                                       message=("warning", codesmap[str(status[1])]), **kwargs)
        return render_template('/admin/user/user_manage_edit.html',
                               message=("warning", codesmap[str(-1)]),
                               form=form, **kwargs)
    form.id.data = "AutoGenerate"
    return render_template("/admin/user/user_manage_edit.html", form=form, **kwargs)


article_manage_para = {"user": lambda value: ("user_id", user.initFromName(value).id),
                       "title": lambda value: ("title", value),
                       "source": lambda value: ("source", articleSource_db.get_by_name(value)),
                       "type": lambda value: ("type", articleType_db.get_by_name(value))}


@admin.route("/article-manage", endpoint="article-manage", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("Article Management"))
def admin_article_manage(**kwargs):
    form = DeleteForm()
    page = request.args.get('page', 1, type=int)
    para, para1 = {}, {}
    for key, value in request.args.items():
        if value:
            try:
                key0, value0 = article_manage_para[key](value)
                para1[key0] = value0
                para[key] = value
            except:
                pass
    if request.method == "POST":
        if form.validate_on_submit():
            id = int(form.id.data)
            status = article.delete(id)
            articles0 = articles.initFromPara(page, **para1)
            if status[0]:
                return render_template('/admin/article-manage/article_manage.html', pagination=articles0.pagination,
                                       form=form, para=para,
                                       message=("success", codesmap[str(status[1])]),
                                       **kwargs)
            else:
                return render_template('/admin/article-manage/article_manage.html', pagination=articles0.pagination,
                                       form=form, para=para,
                                       message=("warning", codesmap[str(status[1])]),
                                       **kwargs)
    articles0 = articles.initFromPara(page, **para1)
    return render_template("/admin/article-manage/article_manage.html", pagination=articles0.pagination, form=form,
                           para=para, **kwargs)


@admin.route("/article-manage/edit/<int:id>", endpoint="article-edit", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("Edit Article"))
def admin_article_edit(**kwargs):
    form = AdvancedPageDownForm()
    article0 = article.initFromId(kwargs["id"])
    if article0.is_none():
        abort(404)
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            source = form.source.data
            type = form.type.data
            summary = form.summary.data
            content_raw = form.content.data
            if form.no_clean:
                no_clean = form.no_clean.data
            else:
                no_clean = False
            status = article.edit(kwargs["id"], title, content_raw, summary, type.id, source.id, advanced=no_clean)
            if status[0]:
                return render_template('/space/article-manage/add.html', form=form, edit=True,
                                       message=("success", codesmap[str(status[1])]),
                                       article_id=status[2], **kwargs)
            else:
                return render_template('/space/article-manage/add.html', form=form,
                                       message=("warning", codesmap[str(status[1])]),
                                       article_id=article0.id, edit=True, **kwargs)
        return render_template('/space/article-manage/add.html',
                               message=("warning", codesmap[str(-1)]),
                               form=form, edit=True, **kwargs)
    form.title.data = article0.title
    form.type.data = article0.type
    form.source.data = article0.source
    form.summary.data = article0.summary
    form.content.data = article0.content_raw
    return render_template('/space/article-manage/add.html', form=form, article_id=article0.id,
                           edit=True, **kwargs)


@admin.route("/article-manage/delete/<int:id>", endpoint="article-delete", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("Delete Article"))
def space_article_delete(**kwargs):
    form = DeleteForm()
    article0 = article.initFromId(kwargs["id"])
    if article0.is_none():
        abort(404)
    if request.method == "POST":
        if form.validate_on_submit():
            status = article.delete(kwargs["id"])
            if status[0]:
                return render_template('/space/article-manage/delete_success.html', article=article0,
                                       **kwargs)
    return render_template('/space/article-manage/delete.html', form=form, article=article0,
                           **kwargs)


file_manage_para = {"alias": lambda value: ("alias", value)}


@admin.route("/file-manage", endpoint="file-manage", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("File Management"))
def admin_file_manage(**kwargs):
    form = DeleteForm()
    page = request.args.get('page', 1, type=int)
    para, para1 = {}, {}
    for key, value in request.args.items():
        if value:
            try:
                key0, value0 = file_manage_para[key](value)
                para1[key0] = value0
                para[key] = value
            except:
                pass
    if request.method == "POST":
        if form.validate_on_submit():
            id = int(form.id.data)
            status = file.delete(id)
            files0 = files.initFromPara(page, **para1)
            if status[0]:
                return render_template('/admin/file-manage/file_manage.html', pagination=files0.pagination, form=form, para=para,
                                       message=("success", codesmap[str(status[1])]),
                                       **kwargs)
            else:
                return render_template('/admin/file-manage/file_manage.html', pagination=files0.pagination, form=form, para=para,
                                       message=("warning", codesmap[str(status[1])]),
                                       **kwargs)
    files0 = files.initFromPara(page, **para1)
    return render_template("/admin/file-manage/file_manage.html", pagination=files0.pagination, form = form,
                           para=para, **kwargs)

@admin.route("/file-manage/upload", endpoint="file-upload", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("New File"))
def admin_file_upload(**kwargs):
    form = FileUploadForm()
    if request.method == "POST":
        if form.validate_on_submit():
            alias = form.alias.data
            description = form.description.data
            external = form.external.data
            permission = form.permission.data
            link = form.link.data
            password = form.password.data
            status = file.upload(alias, description,permission.permission, external, link, password)
            if status[0]:
                return redirect(url_for("admin.file-edit",id=status[2]))
            else:
                return render_template('/admin/file-manage/file_manage_edit.html', form=form,
                                       message=("warning", codesmap[str(status[1])]), **kwargs)
        return render_template('/admin/file-manage/file_manage_edit.html',
                               message=("danger", codesmap[str(-1)]),
                               form=form, **kwargs)
    form.id.data = "AutoGenerate"
    return render_template("/admin/file-manage/file_manage_edit.html", form=form, **kwargs)

@admin.route("/file-manage/edit/<int:id>", endpoint="file-edit", methods=["GET", "POST"])
@admin_auth_view
@get_siteInfo(_l("File Information Editor"))
def admin_file_edit(**kwargs):
    form = FileEditForm()
    file0 = file.initFromId(kwargs["id"])
    if file0.isNone():
        abort(404)
    if request.method == "POST":
        if form.validate_on_submit():
            alias = form.alias.data
            description = form.description.data
            external = form.external.data
            permission = form.permission.data
            link = form.link.data
            password = form.password.data
            status = file.edit(kwargs["id"], alias, description,permission.permission, external, link, password)
            if status[0]:
                return render_template('/admin/file-manage/file_manage_edit.html', form=form,
                                       message=("success", codesmap[str(status[1])]), **kwargs)
            else:
                form.alias.data = file0.alias
                return render_template('/admin/file-manage/file_manage_edit.html', form=form,
                                       message=("warning", codesmap[str(status[1])]), **kwargs)
        return render_template('/admin/file-manage/file_manage_edit.html', message=("warning", codesmap[str(-1)]),
                               form=form, **kwargs)
    form.id.data = file0.id
    form.alias.data = file0.alias
    form.external.data = file0.external
    form.description.data = file0.description
    #form.permission.data  = file0.permission
    form.link.data = file0.link
    form.password.data = file0.password
    return render_template("/admin/file-manage/file_manage_edit.html", form=form, **kwargs)