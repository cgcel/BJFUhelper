# -*- coding: utf-8 -*-
# author: Chan

import requests
import time
from bs4 import BeautifulSoup as bs


url_start = 'http://newjwxt.bjfu.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL'  # GET
url_main = 'http://newjwxt.bjfu.edu.cn/jsxsd/framework/xsMain.jsp'  # GET
url_login = 'http://newjwxt.bjfu.edu.cn/jsxsd/xk/LoginToXk'  # POST
url_classes = 'http://newjwxt.bjfu.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL'

num = {
    "1": "F6EBEDA273684E0E8C279B052110493E-",
    "2": "901DA391778C45EFBB20ED21186C64DA-",
    "3": "7944FA120D354BB78F8E8235A1426640-",
    "4": "BD68B87447F84DDDA93A7838E9BD582A-",
    "5": "7CA568FE8A7E435DA4F126BE3DCA29C5-",
    "6": "B939AB7EA3A7406BB191A3F46EDB9B19-",
    "7": "B37542CECDFB4C2EAEFB4A6216942A46-"
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
    "3": "5节:",
    "4": "67节:",
    "5": "89节:",
    "6": "1011节",
    "7": "1112节"
}

user_data = {}


class newjwxt(object):
    def __init__(self):

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'newjwxt.bjfu.edu.cn',
            'Referer': 'http://newjwxt.bjfu.edu.cn/Logon.do?method=logon',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.get(url_start)

    def login(self, chat_id):
        postdata = {
            'USERNAME': user_data[chat_id][0],
            'PASSWORD': user_data[chat_id][1]
        }
        self.session.post(url_login, data=postdata)
        return self.session.get(url_main).status_code

    def info(self, chat_id):
        r = self.session.get(url_main)
        soup = bs(r.content, "html.parser")
        basic_info = soup.find_all("div", {"class": "Nsb_top_menu_nc"})
        info = basic_info[0].text.strip()
        return info

    def get_classes(self, delta, weekday):
        localtime = time.localtime()
        courses = {}
        cur_courses = {}
        t = 0
        r = self.session.get(url_classes)
        soup = bs(r.content, "html.parser")
        for z in range(1, 8):
            id = num[str(z)] + weekday  # "4-2"
            Classes = soup.find_all("div", {"id": id})
            if '---------------------' in Classes[0]:
                classes = Classes[0].text.replace(
                    '---------------------', '@').replace(",", "&").split('@')
            else:
                classes = [Classes[0].text.strip().replace(",", "&")
                           ]  # .split(',')
            l = len(classes)
            if classes == ['']:
                t = t+1
                if t == 8:
                    cur_courses.clear()
                    return cur_courses
            Weeks = Classes[0].find_all("font", {"title": "周次(节次)"})
            L = len(Weeks)
            for i in range(0, l):
                try:
                    classes[i] = class_num[str(z)]+classes[i]
                    weeks = Weeks[i].text.replace("(周)", "").split(",")
                    w = []
                    for parts in weeks:
                        if '-' in parts:
                            part_infos = parts.split("-")
                            week_start = int(part_infos[0])
                            week_end = int(part_infos[1])
                            for week in range(week_start, week_end+1):
                                w.append(week)
                        else:
                            part_infos = parts.split(",")
                            for part in part_infos:
                                w.append(int(part))
                    W = repr(w)
                    courses[W] = classes[i]
                except:
                    pass
        for key in courses.keys():
            if str(delta) in key:
                cur_courses[key] = courses[key]
        return cur_courses

    def get_extracourses(self):
        r = self.session.get(url_classes)
        soup = bs(r.content, "html.parser")
        try:
            result = soup.find(
                "td", {"colspan": "7", "align": "left", "style": "color: red;"})
            return result.text
        except:
            return "无安排"
