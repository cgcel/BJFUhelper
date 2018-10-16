# -*- coding:utf-8 -*-
# author: Chan

import requests
from bs4 import BeautifulSoup as bs
import re
from NewjwxtInfo import newjwxt


url_base = 'http://newjwxt.bjfu.edu.cn'
url_main = 'http://newjwxt.bjfu.edu.cn/jsxsd/xspj/xspj_find.do?Ves632DSdyV=NEW_XSD_JXPJ'
url_post = 'http://newjwxt.bjfu.edu.cn/jsxsd/xspj/xspj_save.do'

pattern = re.compile(r'javascript:JsMod1\(\'(.+)\">评教')


class JXPJ(object):
    def __init__(self, chat_id):
        self.session = newjwxt().login(chat_id)

    # 获取学期评教url
    def get_url(self):
        r = self.session.get(url_main)
        soup = bs(r.content, 'html.parser')
        s = soup.find_all("a", {"title": "点击进入评价"})
        url = url_base + s[0]['href']
        return url

    # 获取待评教课程url
    def get_courses(self):
        url_target = self.get_url()
        r = self.session.get(url_target)
        result = pattern.findall(r.text)
        target_urls = []
        for part in result:
            target_urls.append(url_base + part.split('\'')[0])
        return target_urls

    # 构造formdata并评教
    def evaluate(self):
        target_urls = self.get_courses()
        for url in target_urls:
            formdata = {}
            r = self.session.get(url)
            soup = bs(r.content, 'html.parser')
            result = soup.find_all("input", {"type": "hidden"})
            part1 = result[1:11]
            formdata['issubmit'] = 0  # 0--保存 1--提交
            for part in part1:
                formdata[part['name']] = part['value']
            for part in result[11:]:
                formdata[part['name']] = part['value']
            part2 = soup.find_all("input", {"name": "pj06xh"})
            for part in part2:
                num = part['value']
                s = "pj0601id_"
                data = soup.find_all("input", {"name": s+num})[1]['value']
                formdata[s+num] = data
            part3 = soup.find_all("input", {"name": "xszwpjxh"})
            for part in part3:
                num = part['value']
                s = "pj0601id_"
                data = soup.find_all("input", {"name": s+num})[1]['value']
                formdata[s+num] = data
            self.session.post(url_post, formdata)
        return "评教完成:)"