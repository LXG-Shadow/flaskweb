from urllib import request
import json,time


rplchrdict_unix = {"/": "-",
             "\\": "-",
             ":": "-",
             "*": "-",
             "?": "-",
             "<": "-",
             ">": "-",
             "|": "-",
             "：" : "-",
             "\"" : "-",
             "→" : "-",
             " " : "' '",
             "&" : "-",
             "'" : "\"'\"",
             "(" : "-",
             ")" : "-"
            }

rplchrdict_windows = {"/": "-",
             "\\": "-",
             ":": "-",
             "*": "-",
             "?": "-",
             "<": "-",
             ">": "-",
             "|": "-",
             "：" : "-",
             "\"" : "-",
             "→" : "-",
             "&" : "-",
            }

unicdchr = {"\\u0026": "&",
              "\\u003c" : "<",
              "\\u003e" : ">"}


def rplchr(s,opsys) :
    if opsys == "Windows":
        chrdict = rplchrdict_windows
    else:
        chrdict = rplchrdict_unix

    newstr = ""
    for i in range(len(s)):
        if s[i] in chrdict:
            newstr += chrdict[s[i]]
        else:
            newstr += s[i]
    if s[0] == "-":
        s = "rmv"+s
    return newstr

def unicdefmt(s):
    for key, value in unicdchr.items():
        s = s.replace(key, value)
    return s


class favfolder(object):
    def __init__(self,mid,fid):
        self.__mid = mid
        self.__fid = fid
        self.__apiurl = "https://api.bilibili.com/x/space/fav/arc?vmid=%s&ps=30&fid=%s&pn=%s" % (mid, fid, "%s")
        if self.isValid():
            self.__data = self.reqData()
        else:
            self.__data = []

    @classmethod
    def initFromLink(cls,favlink):
        if favlink[-1] == "/":
            favlink = favlink[:-1:]
        # 获取mid
        mid = favlink[favlink.find("com/", 0) + 4:favlink.find("/", favlink.find("com/", 0)+4):]
        # 获取fid
        fid = favlink[favlink.find("fid", 0) + 4::]
        if not mid.isdigit():
            mid = ""
        if not fid.isdigit():
            fid = ""
        return cls(mid,fid)

    def isValid(self):
        if len(self.__mid) == 0 or len(self.__fid) == 0:
            return False
        else:
            return True

    def isNone(self):
        if len(self.__data) == 0:
            return True
        else:
            return False

    def getNumVideo(self):
        return len(self.__data)


    def getData(self,ps=30):
        parsedlist = [[] for i in range((self.getNumVideo() - 1) // ps + 1)]
        for i in range(self.getNumVideo()):
            parsedlist[i // ps].append(self.__data[i])
        return parsedlist


    def reqData(self):
        def tryget(wholeurl):
            try:
                wholeHTML = request.urlopen(wholeurl).read().decode("utf-8")
                jsondata = json.loads(wholeHTML)
            except:
                time.sleep(3)
                while True:
                    try:
                        wholeHTML = request.urlopen(wholeurl).read().decode("utf-8")
                        jsondata = json.loads(wholeHTML)
                        break
                    except:
                        time.sleep(3)
            return jsondata

        data = []
        pn = 1
        while True:
            wholeurl = self.__apiurl % pn
            jsondata = tryget(wholeurl)
            print(wholeurl)
            code = jsondata["code"]
            if code == 0:
                pass
            elif code == 11004 or code == 11010 or code == 53013:
                return []
            else:
                #print(code)
                while code != 0:
                    jsondata = tryget(wholeurl)
                    code = jsondata["code"]

            archives = jsondata["data"]["archives"]
            if len(archives) == 0:
                break

            for item in archives:
                data.append({"aid": str(item["aid"]),
                             "title": unicdefmt(str(item["title"])),
                             "pic": str(item["pic"]),
                             "upname": str(item["owner"]["name"]),
                             "mid": str(item["owner"]["mid"]),
                             "state": str(item["state"])})

            pn +=1
        return data