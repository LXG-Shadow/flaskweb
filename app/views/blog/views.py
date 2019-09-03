from flask import request,render_template,abort
from . import blog
from ...decorator import get_user,get_blogInfo
from ...model.blog import articles,article
import datetime,urllib

@blog.route("/",methods=["GET","POST"])
@blog.route("",endpoint="index",methods=["GET","POST"])
@get_user
@get_blogInfo("Blog")
def blog_index(**kwargs):
    page = request.args.get('page', 1, type=int)
    articles0 = articles.initFromAll(page)
    if articles0.isNone():
        abort(404)
    return render_template('blog/index.html', pagination=articles0,
                           **kwargs)


@blog.route("/tag/<string:tag>",endpoint="tag",methods=["GET","POST"])
@get_user
@get_blogInfo("Tag")
def blog_index(**kwargs):
    tag = urllib.parse.unquote(kwargs.pop("tag"))
    kwargs["siteInfo"].parameter["tag"] = tag
    page = request.args.get('page', 1, type=int)
    articles0 = articles.initFromTag(tag,page)
    if articles0.isNone():
        abort(404)
    return render_template('blog/index.html', pagination=articles0,
                           **kwargs)

@blog.route("/article-detail/<int:id>",endpoint="article-detail",methods=["GET","POST"])
@get_user
@get_blogInfo("Detail")
def blog_article_detail(**kwargs):
    id = kwargs.pop("id")
    if id == 0:
        title = request.args.get('title', None, type=str)
        if title is None:
            abort(404)
        article0 = article.initFromTitle(title)
    else:
        article0 = article.initFromId(id)
    if article0.is_none():
        abort(404)
    if article0.is_hide() and article0.user.id != kwargs["user"].id and kwargs["user"].group.permission <3:
        abort(404)
    article0.add_view()
    return render_template("blog/index.html",article = article0,**kwargs)