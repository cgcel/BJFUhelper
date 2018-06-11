# -*- coding: utf-8 -*-
# author: Chan

import requests
from bs4 import BeautifulSoup as bs

url_main = 'https://cubingchina.com/results/person?region=World&gender=all&name='
url_get = 'https://cubingchina.com'

dict_type = {'222': '二阶',
             '333': '三阶',
             '333oh': '三单',
             '444': '四阶',
             '555': '五阶',
             '666': '六阶',
             '777': '七阶',
             '333bf': '三盲',
             '333fm': '最少步',
             '333ft': '脚拧',
             'clock': '魔表',
             'minx': '五魔',
             'pyram': '金字塔',
             'skewb': '斜转',
             'sq1': 'SQ1',
             '444bf': '四盲',
             '555bf': '五盲',
             '333mbf': '多盲'}


class WCA(object):
    def __init__(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'cubingchina.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        self.session = requests.session()
        self.session.headers.update(headers)

    def get_url(self, name):
        url = url_main+name
        r = self.session.get(url)
        soup = bs(r.content, 'html.parser')
        data = soup.find_all('tr', {"class": "odd"})
        a = soup.find_all('a', href=True)
        # print(a[31])
        link = str(a[31]).split('\"')[1]
        # print(link)
        return link

    def get_info(self, name):
        link = WCA().get_url(name)
        url = url_get+link
        # print(url)
        info = ""
        text = ""
        r = self.session.get(url)
        soup = bs(r.content, 'html.parser')
        # print(soup.prettify())
        data = soup.find_all("span", {"class": "info-value"})
        name = data[0].get_text().strip()
        country = data[1].get_text().strip()
        times = data[2].get_text().strip()
        wcaid = data[3].get_text().strip()
        sex = data[4].get_text().strip()
        experience = data[5].get_text().strip()
        info = "姓名:{}\nID:{}\n".format(name, wcaid)
        for part in list(dict_type.keys()):
            try:
                pb = soup.find_all(
                    "a", {"href": "/results/rankings?event="+part+"&region=China"})[0].get_text().strip()
                avg = soup.find_all(
                    "a", {"href": "/results/rankings?event="+part+"&type=average&region=China"})[0].get_text().strip()
                if len(avg) == 0:
                    text = text+dict_type[part]+': '+pb+'[best]\n'
                else:
                    text = text+dict_type[part]+': ' + \
                        pb + '[best] '+avg+'[avg]\n'
            except:
                pass
        return info+text
