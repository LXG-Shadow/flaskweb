from .article import article
from ..info import siteInfo

class blogInfo(siteInfo):
    def __init__(self,title="Blog"):
        siteInfo.__init__(self,title=title)
        self.article_num = article.get_total_num()