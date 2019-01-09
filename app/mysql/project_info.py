from app.mysql import *

def get(language,category):
    rawdata = getData("projects",*("project_name","project_desc","project_link"),project_language = language,project_category = category)
    if len(rawdata) == 0:
        return []
    data = []
    for name,desc,link in rawdata:
        data.append({"name":name,"desc":desc,"link":link})
    return data