from app.mysql import project_info

class projects(object):

    def __init__(self,language,category):
        self.__language = language
        self.__category = category
        self.__projects = project_info.get(language,category)

    def getCategory(self):
        return self.__category

    def getLanguage(self):
        return self.__language

    def getProjects(self,col=0):
        if col == 0:
            return self.__projects
        else:
            parsedlist = [[] for i in range((self.getNumProjects()-1) // col + 1)]
            for i in range(self.getNumProjects()):
                parsedlist[i // col].append(self.__projects[i])
            return parsedlist

    def getNumProjects(self):
        return len(self.__projects)


    def isNone(self):
        if len(self.__projects) == 0:
            return True
        else:
            return False