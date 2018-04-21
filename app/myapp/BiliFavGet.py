from urllib import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class linkform(FlaskForm):
    favlink = StringField('输入收藏夹地址:', validators=[DataRequired()])
    number = StringField("输入获取的个数(按时间顺序，前n个):", validators=[DataRequired()])
    submit = SubmitField('开始')



def getdata(preurl,avsc) :
    wholeurl = preurl + str(avsc.pn[-1])
    wholeHTML = request.urlopen(wholeurl).read().decode("utf-8")
    st = wholeHTML.find("aid",0)+5
    ed = wholeHTML.find(",",st)
    avsc.avs.append(wholeHTML[st:ed:])
    avsc.avslink.append("https://www.bilibili.com/video/av" + avsc.avs[-1])
    st = wholeHTML.find("pic",ed)+6
    ed = wholeHTML.find(",",st)-1
    avsc.avspic.append(wholeHTML[st:ed:])
    st = wholeHTML.find("title",ed)+8
    ed = wholeHTML.find(",\"",st)-1
    avsc.avstitle.append(wholeHTML[st:ed:])
    return avsc



def outputdata(urlin,number):
    class avclass(object) :
        def __init__(self):
            self.pn = [0]
            self.avs = ["AV"]
            self.avstitle = ["Title"]
            self.avspic = ["Pic"]
            self.avslink = ["Av Link"]
    avsc = avclass()
    vmid = ""
    fid = ""
    number = int(number)
    urlin = str(urlin)
    if urlin[-1] != "/" :
        urlin = urlin + "/"
    vmid = urlin[urlin.find("com", 0) + 4:urlin.find("/#", 0):]
    fid = urlin[urlin.find("fid", 0) + 4:-1:]
    preurl = "https://api.bilibili.com/x/v2/fav/video?vmid=" + vmid + "&ps=1&fid=" + fid + "&pn="
    for i in range(1, number + 1, 1):
        avsc.pn.append(i)
        avsc = getdata(preurl, avsc)
    return avsc