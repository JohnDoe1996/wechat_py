# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import myscse
  
class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
  
    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="john" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法
  
    #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr


    def POST(self):
        str_xml = web.data() #获得post来的数据
        self.xml = etree.fromstring(str_xml)#进行XML解析
        mstype = self.xml.find("MsgType").text
        self.fromUser = self.xml.find("FromUserName").text
        self.toUser = self.xml.find("ToUserName").text

        if mstype == "event":
            return self.receiveEvent()
    
        if mstype == 'text':
            return self.receiveText()

        if mstype == "image":
            return self.receiveImage()

        if mstype == "location":
            return self.rreceiveLocation();

        if mstype == "voice":
            return self.receiveVoice()

        if mstype == "video":
            return self.receiveVideo()

        if mstype == "link":
            return self.receiveLink()


    def receiveText(self):
        text = self.xml.find("Content").text
        user = text.split(" ")[0]
        pawd = text.split(" ")[1]
        act = text.split(" ")[2]
        act=act.encode("utf-8")
        if act == "星期一":
            cookie = myscse.login(user, pawd).subment()
            sch = myscse.schedule(cookie)
            content = sch.getText(1)
            return self.transmitText(content)
        elif act == "星期二":
            cookie = myscse.login(user, pawd).subment()
            sch = myscse.schedule(cookie)
            content = sch.getText(2)
            return self.transmitText(content)
        elif act == "星期三":
            cookie = myscse.login(user, pawd).subment()
            sch = myscse.schedule(cookie)
            content = sch.getText(3)
            return self.transmitText(content)
        elif act == "星期四":
            cookie = myscse.login(user, pawd).subment()
            sch = myscse.schedule(cookie)
            content = sch.getText(4)
            return self.transmitText(content)
        elif act == "星期五":
            cookie = myscse.login(user, pawd).subment()
            sch = myscse.schedule(cookie)
            content = sch.getText(5)
            return self.transmitText(content)
        elif act == "考勤":
            cookie = myscse.login(user, pawd).subment()
            che = myscse.checking(cookie)
            content = che.getText()
            return self.transmitText(content)
        elif act == "个人信息" or act == "个人" or act == "信息":
            cookie = myscse.login(user, pawd).subment()
            per = myscse.personal(cookie)
            content = per.getTextInformation()
            return self.transmitText(content)
        elif act == "违规" or act == "违规记录" or act == "晚归" or act == "晚归记录":
            cookie = myscse.login(user, pawd).subment()
            lat = myscse.late(cookie)
            content = lat.getText()
            return self.transmitText(content)
        elif act=="考试" or act=="考试时间":
            cookie = myscse.login(user, pawd).subment()
            tes = myscse.test(cookie)
            string = tes.getText()
            return self.transmitWordNews("考试时间",string)
        elif act == "课程代码" or act == "代码" or act == "课程":
            cookie = myscse.login(user, pawd).subment()
            cod = myscse.personal(cookie)
            string = cod.getTextCode()
            return self.transmitWordNews("课程代码", string)
        elif act == "成绩" or act=="考试成绩":
            cookie = myscse.login(user, pawd).subment()
            gra = myscse.personal(cookie)
            string = gra.getTextGrade()
            return self.transmitWordNews("本学期成绩", string)
        elif act == "绩点":
            cookie = myscse.login(user, pawd).subment()
            gpa = myscse.personal(cookie)
            content = gpa.getTextGPA()
            return self.transmitText(content)

        else:
            return self.transmitText("不能的消息识别内容")


    def receiveEvent(self):
        event = self.xml.find('Event').text
        if event=="subscribe":
            content = u"欢迎关注我们的公众号！我们将会带给你方便的校园服务，点击菜单获取帮助吧！"
            return self.transmitText(content)
        elif event=="unsubscribe":
            content = u"虽然你离开了我们，但是我们一定会做的更好的，期待你下一次的关注！"
            return self.transmitText(content)
        elif event=="CLICK":
            return self.clickEvent()


    def clickEvent(self):
        eventkey = self.xml.find('EventKey').text
        if eventkey==u"map":
            imgStr = "oUMQCYYjXLndNUCNPOtvkzYUsepEwhO-X49h65IhO1plI17XPiLXqG9hdLGcSRxE"
            return self.transmitImage(imgStr)
        elif eventkey==u"calendar":
            imgStr = "JXSLV9vKjmJO-0FUHpnawCSb_EX7w5hkmAC-cn4ZH9hXtj4W7UZWKHbnIe4s9vJ9"
            return self.transmitImage(imgStr)
        elif eventkey==u"grxx":
            str = u"发送：学号(空格)密码(空格)个人，即可查询你的个人信息，如\n" + \
                u"1740000000 123 个人\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)
        elif eventkey==u"kcb":
            str = u"发送：学号(空格)密码(空格)星期几，即可查询你某一天的课程，如\n" + \
                u"1740000000 123 星期一\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)
        elif eventkey==u"wgjl":
            str = u"发送：学号(空格)密码(空格)违规，即可查询你的晚归、违规用电记录，如\n" + \
                u"1740000000 123 违规\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)
        elif eventkey==u"kcdm":
            str = u"发送：学号(空格)密码(空格)代码，即可查询你本学期课程的代码，如\n" + \
                u"1740000000 123 代码\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)
        elif eventkey==u"cj":
            str = u"发送：学号(空格)密码(空格)成绩，即可查询你本学期的考试成绩，如\n" + \
                u"1740000000 123 成绩\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)
        elif eventkey==u"kssj":
            str = u"发送：学号(空格)密码(空格)考试，即可查询你本学期的考试时间考场...，如\n" + \
                u"1740000000 123 考试\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)
        elif eventkey==u"jd":
            str = u"发送：学号(空格)密码(空格)绩点，即可查询你的当前绩点和计算绩点，如\n" + \
                u"1740000000 123 绩点\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)
        elif eventkey==u"kq":
            str = u"发送：学号(空格)密码(空格)考勤，即可查询你本学期的考勤情况...，如\n" + \
                u"1740000000 123 考勤\n\n如果提示服务出错请多发几遍"
            return self.transmitText(str)

        else:
            return self.transmitText(u"未能识别的指令")



    def receiveImage(self):
        try:
            picurl = self.xml.find('PicUrl').text
            content = u"你发送的是图片，地址为："+picurl
            return self.transmitText(content)
        except:
            content = u"图片识别失败，请尝试重发"
            return self.transmitText(content)

    def receiveVoice(self):
        voice = self.xml.find("MediaId").text
        content = u"你发送的是语音，媒体ID为："+voice
        return  self.transmitText(content)

    def receiveVideo(self):
        video = self.xml.find("MediaId").text
        content = u"你发送的是视频，媒体ID为："+video
        return  self.transmitText(content)

    def rreceiveLocation(self):
        x = self.xml.find("Location_X").text
        y = self.xml.find("Location_Y").text
        scale = self.xml.find("Scale").text
        label = self.xml.find("Label").text
        content = u"你发送的是位置，维度为："+ x + u"；纬度为："+ y + u"；缩放级别为：" + scale + u"；位置为：" +label
        return  self.transmitText(content)

    def receiveLink(self):
        title = self.xml.find("Title").text
        description = self.xml.find("Description").text
        url = self.xml.find("Url").text
        content = u"你发送的是连接，标题为："+ title + u"；内容为：" + description + u"；连接地址为："+ url
        return  self.transmitText(content)

    def transmitText(self,content):
        return self.render.reply_text(self.fromUser,self.toUser,int(time.time()), content)

    def transmitWordNews(self,title,description):
        return self.render.reply_wordNews(self.fromUser,self.toUser,int(time.time()), title,description)

    def transmitImage(self,media_id):
        return self.render.reply_image(self.fromUser,self.toUser,int(time.time()), media_id)