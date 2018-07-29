# -*- coding: utf-8 -*-
# author: Chan

import requests
import json

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
        jsondata = json.loads(resp1.content)
        self.comcode = jsondata['auto'][0]['comCode']
        resp2 = self.session.get(url_info+self.comcode+'&postid='+self.num)
        packagedata = json.loads(resp2.content)
        if packagedata['message'] != "ok":
            text = packagedata["message"]
            return text
        elif packagedata['message'] == "ok":
            packageinfo = packagedata['data']
            text = "单号: {}\n公司: {}\n更新时间: {}\n动态: {}".format(
                num, packagedata['com'], packageinfo[0]['time'], packageinfo[0]['context'])
            return text

    def plusgetinfo(self, comcode, num):
        self.num = num
        resp2 = self.session.get(url_info+comcode+'&postid=' + str(num))
        packagedata = json.loads(resp2.content)
        if packagedata['message'] != "ok":
            text = packagedata["message"]
            return text
        elif packagedata['message'] == "ok":
            packageinfo = packagedata['data']
            text = "单号: {}\n公司: {}\n更新时间: {}\n动态: {}".format(
                num, packagedata['com'], packageinfo[0]['time'], packageinfo[0]['context'])
            return text
