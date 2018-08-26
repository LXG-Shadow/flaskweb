code_msg = {"404":["Page Not Found","没有该页面或页面已被删除"],
            "500":["Internal Server Error","服务器内部错误，请联系管理员提交问题"],
            "405":["Method Not Allowed","请使用正确方式调用api"]}


class errorpage(object):

    def __init__(self,errorcode):
        self.__code = errorcode
        self.__title = code_msg[str(errorcode)][0]
        self.__msg = code_msg[str(errorcode)][1]

    def getCode(self):
        return self.__code

    def getTitle(self):
        return self.__title


    def getMsg(self):
        return self.__msg