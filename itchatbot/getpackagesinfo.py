# -*- coding: utf-8 -*-
# author: Chan

import requests
import json
from bs4 import BeautifulSoup as bs

url_main = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text='
url_info = 'http://www.kuaidi100.com/query?type='


class kuaidi():
    def __init__(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.kuaidi100.com',
            'Origin': 'http://www.kuaidi100.com',
            'Referer': 'http://www.kuaidi100.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session = requests.Session()
        self.session.headers.update(headers)

    def getinfo(self, num):
        self.num = num
        self.param = {
            'resultv2': '1',
            'text': self.num
        }
        resp1 = self.session.post(url_main+self.num, params=self.param)
        soup = bs(resp1.content, "html.parser")
        jsondata = json.loads(soup.get_text())
        self.comcode = jsondata['auto'][0]['comCode']
        resp2 = self.session.get(url_info+self.comcode+'&postid='+self.num)
        info = bs(resp2.content, "html.parser")
        packagedata = json.loads(info.get_text())
        packageinfo = packagedata['data']
        text = "单号: "+num+'\n' + "更新时间: " + \
            packageinfo[0]['time']+'\n' + "动态: " + packageinfo[0]['context']
        return text

    def plusgetinfo(self, comcode, num):
        self.num = num
        # self.param = {
        #     'resultv2': '1',
        #     'text': self.num
        # }
        resp2 = self.session.get(url_info+comcode+'&postid=' + str(num))
        soup = bs(resp2.content, "html.parser")
        jsondata = json.loads(soup.get_text())
        self.comcode = jsondata['auto'][0]['comCode']
        resp2 = self.session.get(url_info+self.comcode+'&postid='+self.num)
        info = bs(resp2.content, "html.parser")
        packagedata = json.loads(info.get_text())
        packageinfo = packagedata['data']
        text = "单号: "+num+'\n' + "更新时间: " + \
            packageinfo[0]['time']+'\n' + "动态: " + packageinfo[0]['context']
        return text


# if __name__ == '__main__':
#     kd = kuaidi()
#     print(kd.package('000'))
