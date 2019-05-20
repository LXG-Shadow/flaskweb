from flask import request, abort, render_template, flash, redirect, url_for
from flask_babel import lazy_gettext as _l
from ... import codesmap
from .forms import PageDownForm, AdvancedPageDownForm, DeleteForm, ProfileEditForm
from . import space
from ...decorator import get_user, login_auth_view, get_blogInfo, get_siteInfo
from ...model import user
from ...model.blog import articles, article


@space.route("/<int:id>", endpoint="index")
@get_user
@get_siteInfo(_l("Space"))
def space_index(**kwargs):
    id = kwargs.pop("id")
    if id == 0:
        name = request.args.get('name', None, type=str)
        if name is None:
            abort(404)
        user0 = user.initFromName(name)
    else:
        user0 = user.initFromId(id)
    if user0.is_anonymous():
        abort(404)
    return render_template("/space/index.html", page_user=user0, **kwargs)


@space.route("/<int:id>/articles", endpoint="articles")
@get_user
@get_siteInfo(_l("All Articles"))
def space_articles(**kwargs):
    id = kwargs.pop("id")
    if id == 0:
        abort(404)
    user0 = user.initFromId(id)
    if user0.is_anonymous():
        abort(404)
    page = request.args.get('page', 1, type=int)
    articles0 = articles.initFromUser(user0.id, page)
    kwargs["siteInfo"].parameter["id"] = user0.id
    return render_template("/space/articles-display/articles.html", page_user=user0, pagination=articles0,
                           **kwargs)


@space.route("/edit", endpoint="edit", methods=["GET", "POST"])
@login_auth_view
@get_siteInfo(_l("Edit Profile"))
def space_edit(**kwargs):
    form = ProfileEditForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            status = user.edit(kwargs["user"].id, username, email)
            if status[0]:
                return redirect(url_for("space.index", id=kwargs["user"].id))
            else:
                return render_template('/space/profile-edit.html', form=form,
                                       message=("warning", codesmap[str(status[1])]),
                                       **kwargs)
        else:
            form.username.data = kwargs["user"].name
            form.email.data = kwargs["user"].email
            return render_template('/space/profile-edit.html', form=form, message=("danger", codesmap[-1]),
                                   **kwargs)
    form.username.data = kwargs["user"].name
    form.email.data = kwargs["user"].email
    return render_template('/space/profile-edit.html', form=form, **kwargs)


@space.route("/article-manage/add", endpoint="article-add", methods=["GET", "POST"])
@login_auth_view
@get_siteInfo(_l("New Article"))
def space_article_add(**kwargs):
    if kwargs["user"].group.permission >= 2:
        form = AdvancedPageDownForm()
    else:
        form = PageDownForm()
    if request.method == "GET":
        return render_template('/space/article-manage/add.html', form=form, **kwargs)
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
            tags = list(set([t for t in form.tags.data.split(" ") if t != ""]))
            status = article.add(title, content_raw, summary, type.id, source.id, kwargs["user"].id, tags,
                                 advanced=no_clean)
            if status[0]:
                return render_template('/space/article-manage/add.html', form=form, edit=True,
                                       message=("success", codesmap[str(status[1])]),
                                       article_id=status[2], **kwargs)
            else:
                return render_template('/space/article-manage/add.html', form=form,
                                       message=("warning", codesmap[str(status[1])]), **kwargs)
        return render_template('/space/article-manage/add.html',
                               message=("warning", codesmap[str(-1)]),
                               form=form, **kwargs)
    return render_template('/space/article-manage/add.html', form=PageDownForm(), **kwargs)


@space.route("article-manage/edit/<int:id>", endpoint="article-edit", methods=["GET", "POST"])
@login_auth_view
@get_siteInfo(_l("Edit Article"))
def space_aricle_edit(**kwargs):
    if kwargs["user"].group.permission >= 2:
        form = AdvancedPageDownForm()
    else:
        form = PageDownForm()
    article0 = article.initFromId(kwargs["id"])
    if article0.is_none():
        abort(404)
    if article0.user.id != kwargs["user"].id:
        abort(403)
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
            tags = list(set([t for t in form.tags.data.split(" ") if t != ""]))
            status = article.edit(kwargs["id"], title, content_raw, summary, type.id, source.id, tags,
                                  advanced=no_clean)
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
    form.tags.data = " ".join([t.name for t in article0.tags])
    return render_template('/space/article-manage/add.html', form=form, article_id=article0.id,
                           edit=True, **kwargs)


@space.route("/article-manage/delete/<int:id>", endpoint="article-delete", methods=["GET", "POST"])
@login_auth_view
@get_siteInfo(_l("Delete Article"))
def space_article_delete(**kwargs):
    form = DeleteForm()
    article0 = article.initFromId(kwargs["id"])
    if article0.is_none():
        abort(404)
    if article0.user.id != kwargs["user"].id:
        abort(403)
    if request.method == "POST":
        if form.validate_on_submit():
            status = article.delete(kwargs["id"])
            if status[0]:
                return render_template('/space/article-manage/delete_success.html', article=article0,
                                       **kwargs)
    return render_template('/space/article-manage/delete.html', form=form, article=article0,
                           **kwargs)
