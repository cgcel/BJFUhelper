# -*- coding: utf-8 -*-
# author: Chan

import itchat
import requests
import time
import datetime
from itchat.content import *
from getpackagesinfo import kuaidi
from getweatherinfo import Weather
from getbjfuinfo import newjwxt
from tulingbot import Tuling
from wcainfo import WCA

user_data = {}

# starttime = [2018, 3, 4]
starttime = datetime.datetime(2018, 3, 4)


num = {
    "1": "DCE888360E8F4C2587C7EA77AEF8984D-",
    "2": "5B4FD4964CC34B838A4605BDE2339AAE-",
    "3": "FB9A9C19924C47ABBD9DCBE9DD4CDB5A-",
    "4": "509B500DA0964DF88D32333D1EB47F32-",
    "5": "297455C8C0DF4DD89A1B1F517930AA2A-"
}

Weekday = {
    "Mon": "1-2",
    "Tue": "2-2",
    "Wed": "3-2",
    "Thu": "4-2",
    "Fri": "5-2",
    "Sat": "6-2",
    "Sun": "7-2"
}

Weekday_num = {
    "1": "1-2",
    "2": "2-2",
    "3": "3-2",
    "4": "4-2",
    "5": "5-2",
    "6": "6-2",
    "7": "7-2"
}

weekday_alpha = {
    "1": "Mon.",
    "2": "Tue.",
    "3": "Wed.",
    "4": "Thu.",
    "5": "Fri.",
    "6": "Sat.",
    "7": "Sun."
}

class_num = {
    "1": "12节:",
    "2": "34节:",
    "3": "56节:",
    "4": "78节:",
    "5": "910节:"
}


@itchat.msg_register(itchat.content.FRIENDS)
def add_friend(msg):
    msg.user.verify()
    time.sleep(2)
    msg.user.send('Nice to meet you!\n请发送 help 获取帮助.')


@itchat.msg_register(itchat.content.TEXT)  # isGroupChat=True
def text_reply(msg):

    if 'help' in msg['Text']:
        text = '使用说明:\n登录北林教务系统:\nlogin <学号> <密码>\n删除账号: del\n今日课程: class\n明日课程: tomorrow\n本周课程: thisweek\n下周课程: nextweek\n查看周数: weeknum\n查快递: kd <快递单号>\n查天气: today <城市>\n查天气: later <城市>\n查wca信息: wca <姓名/wcaid>'
        return text

    if 'kd' in msg['Text']:
        try:
            num = msg['Text'].split()[1]
            reply = kuaidi().getinfo(num)
            # a or b的意思是，如果a有内容，那么返回a，否则返回b
            # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
            return reply
        except:
            return 'error.'

    if 'today' in msg['Text']:
        try:
            city = msg['Text'].split()[1]
            reply = Weather().daily_weather(city)
            if reply == None:
                return '查询失败.'
            else:
                return reply
        except:
            return 'error.'

    if 'later' in msg['Text']:
        try:
            city = msg['Text'].split()[1]
            reply = Weather().later_weather(city)
            if reply == None:
                return '查询失败.'
            else:
                return reply
        except:
            return 'error.'

    if 'wca' in msg['Text']:
        try:
            name = msg['Text'].split()[1]
            text = WCA().get_info(name)
            return text
        except:
            return 'error.'

    if 'login' in msg['Text']:
        chat_id = msg.fromUserName
        try:
            b = ''
            c = ''
            user_data[chat_id] = msg['Text'].split()[1]+',' + \
                msg['Text'].split()[2]
            new = newjwxt()
            new.login(chat_id, msg['Text'].split()[1], msg['Text'].split()[2])
            password = msg['Text'].split()[2]
            for byte in range(1, len(password)-1):
                c = c+password[byte].replace(password[byte], '*')
            b = password[0]+c+password[len(password)-1]
            text = new.info(chat_id).split('(')[0]
            return "姓名:"+text+'\n'+"学号:" + user_data[chat_id].split(',')[0]+'\n'+"密码:"+b
        except:
            return "登录失败,请检查账密 /help"

    if 'del' in msg['Text']:
        chat_id = msg.fromUserName
        try:
            del user_data[chat_id]
            return "数据已删除."
        except:
            return "没有该用户的数据."

    if 'class' in msg['Text']:
        chat_id = msg.fromUserName
        localtime = datetime.datetime.today()
        delta = int((localtime-starttime).days/7+1)
        weekday = Weekday[time.strftime("%a")]
        try:
            s = ''
            new = newjwxt()
            new.login(chat_id, user_data[chat_id].split(
                ',')[0], user_data[chat_id].split(',')[1])
            dic = new.get_classes(delta, weekday)
            if dic == {}:
                return "今天没有课!"
            elif dic != {}:
                dic = list(dic.values())
                for i in dic:
                    s = s+i+'\n'
                return "今日课程:\n"+s
        except:
            return "获取失败,请先登录 /help"

    if 'tomorrow' in msg['Text']:
        chat_id = msg.fromUserName
        localtime = datetime.datetime.today()
        delta = int((localtime-starttime).days/7+1)
        weekday = Weekday[time.strftime("%a")]
        weekday = str(int(weekday.split('-')[0])+1)+'-2'
        if (time.strftime("%a") == "Sun"):
            weekday = "1-2"
            delta = delta+1
        try:
            s = ''
            new = newjwxt()
            new.login(chat_id, user_data[chat_id].split(
                ',')[0], user_data[chat_id].split(',')[1])
            dic = new.get_classes(delta, weekday)
            if dic == {}:
                return "明天没有课!"
            elif dic != {}:
                # print(dic)
                dic = list(dic.values())
                # print (dic)
                for i in dic:
                    s = s+i+'\n'
                # print(s)
                return "明日课程:\n"+s
        except:
            return "获取失败,请先登录 /help"

    if 'weeknum' in msg['Text']:
        localtime = datetime.datetime.today()
        delta = int((localtime-starttime).days/7+1)
        return "本周为第"+repr(delta)+"周"

    if 'thisweek' in msg['Text']:
        localtime = datetime.datetime.today()
        delta = int((localtime-starttime).days/7+1)
        chat_id = msg.fromUserName
        S = ''
        try:
            for num in range(1, 8):
                weekday = Weekday_num[str(num)]
                s = ''
                new = newjwxt()
                new.login(chat_id, user_data[chat_id].split(
                    ',')[0], user_data[chat_id].split(',')[1])
                dic = new.get_classes(delta, weekday)
                if dic == {}:
                    s = s+weekday_alpha[str(num)]+'\n'+"没有课"+'\n'
                    S = S+s
                    # bot.send_message(chat_id=chat_id, text=s)
                elif dic != {}:
                    dic = list(dic.values())
                    S = S+weekday_alpha[str(num)]+'\n'
                    # s = s+'\n'
                    for i in dic:
                        S = S+i+'\n'
            return S
        except:
            return "获取失败 /help"

    if 'nextweek' in msg['Text']:
        localtime = datetime.datetime.today()
        delta = int(((localtime-starttime).days-1)/7)+2
        chat_id = msg.fromUserName
        S = ''
        try:
            for num in range(1, 8):
                weekday = Weekday_num[str(num)]
                s = ''
                new = newjwxt()
                new.login(chat_id, user_data[chat_id].split(
                    ',')[0], user_data[chat_id].split(',')[1])
                dic = new.get_classes(delta, weekday)
                if dic == {}:
                    s = s+weekday_alpha[str(num)]+'\n'+"没有课"+'\n'
                    S = S+s
                    # bot.send_message(chat_id=chat_id, text=s)
                elif dic != {}:
                    dic = list(dic.values())
                    S = S+weekday_alpha[str(num)]+'\n'
                    # s = s+'\n'
                    for i in dic:
                        S = S+i+'\n'
            return S
        except:
            return "获取失败 /help"

    else:
        # 图灵机器人回复
        text = Tuling().getmsg(msg['Text'])
        return text


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)  # isGroupChat=True
def text_reply(msg):

    # if '/help' in msg['Text']:
    #     text = '使用说明:\n查快递: kd <快递单号>\n查天气: today <城市> | later <城市>\n查wca信息: wca <姓名/wcaid>'
    #     return text+msg.

    if 'kd' in msg['Text']:
        try:
            num = msg['Text'].split()[1]
            reply = kuaidi().getinfo(num)
            # a or b的意思是，如果a有内容，那么返回a，否则返回b
            # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
            return reply
        except:
            return 'error.'

    if 'today' in msg['Text']:
        try:
            city = msg['Text'].split()[1]
            reply = Weather().daily_weather(city)
            if reply == None:
                return '查询失败.'
            else:
                return reply
        except:
            return 'error.'

    if 'later' in msg['Text']:
        try:
            city = msg['Text'].split()[1]
            reply = Weather().later_weather(city)
            if reply == None:
                return '查询失败.'
            else:
                return reply
        except:
            return 'error.'
    if 'wca' in msg['Text']:
        try:
            name = msg['Text'].split()[1]
            text = WCA().get_info(name)
            return text
        except:
            return 'error.'

    else:
        # 图灵机器人回复
        if msg.isAt:
            text = Tuling().getmsg(msg['Text'])
            return text



# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run()
