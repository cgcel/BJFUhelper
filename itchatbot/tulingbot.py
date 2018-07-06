# -*- coding: utf-8 -*-
# author: Chan

import requests
import json
from bs4 import BeautifulSoup as bs


url_main = 'http://www.tuling123.com/openapi/api?key='
api_key = 'ab6a8447954a4d428535f9bf8267e389'


class Tuling(object):
    def getmsg(self, text):
        url_get = url_main+api_key+'&info='+text

        # 我们通过如下命令发送一个post请求
        r = requests.get(url_get)
        soup = bs(r.content, 'html.parser')
        jsondata = json.loads(soup.get_text())
        # print(jsondata)
        data=''
        try:
            data=data+jsondata['text']
        except:
            pass
        try:
            data=data+jsondata['url']
        except:
            pass
        return data


# if __name__ == '__main__':
#     Tuling().getmsg('北京林业大学公交去中发')
