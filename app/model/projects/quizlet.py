import requests,re,ast,json


class quizlet_words(object):
    def __init__(self,id):
        self.id = id
        self.link = "https://quizlet.com/%s/flashcards" % id
        self.wd = []
        if self.isValid():
            self.wd = self.__reqData()

    @classmethod
    def initFromLink(cls,link):
        try:
            id = re.findall(r"com/.*?/", link)[0][4:-1:]
            return cls(id)
        except:
            return cls("-1")


    def __reqData(self):
        wd = None
        try:
            raw = requests.get(self.link)
            raw.encoding = "utf-8"
            for i in re.finditer(r"<script>.*?</script>", raw.text):
                if "Quizlet.cardsModeData" in i.group():
                    wd = i.group()
                    wd = wd[wd.find("=") + 2:wd.find("};") + 1:]
                    wd = json.loads(wd)
                    break
            wd = [{"word": i["word"], "def": i["definition"]} for i in wd["terms"]]
        except:
            pass

        if wd is None:
            return []
        return wd

    def isNone(self):
        return not bool(self.wd)

    def isValid(self):
        if self.id =="-1":
            return False
        return True

    def getData(self,ps=30):
        parsedlist = [[] for i in range((len(self.wd) - 1) // ps + 1)]
        for i in range(len(self.wd)):
            parsedlist[i // ps].append(self.wd[i])
        return parsedlist
