# -*- coding: utf-8 -*-
# author: Chan

import requests
import json
from bs4 import BeautifulSoup as bs


class Weather():
    def __init__(self):
        self.url_get = 'https://api.weather.com/v3/location/search?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&language=zh-CN&locationType=locale&query='
        self.url_main = 'https://weather.com/zh-CN/weather/today/l/'
        
        self.headers = {
            'Referer': 'https://weather.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36X-DevTools-Emulate-Network-Conditions-Client-Id: 21FBE8B36ECC250A16B97A36B4ABB84C'
            }


    def get_soup(self,url):
        r = requests.get(url, headers=self.headers)
        soup = bs(r.content, 'html.parser')
        jsondata = json.loads(soup.get_text())
        place_id = jsondata['location']['placeId'][0]
        # print(place_id)
        url = self.url_main+place_id
        r = requests.get(url, headers=self.headers)
        soup = bs(r.content, 'html.parser')
        # print(soup.prettify())
        return soup


    def daily_weather(self,city):
        try:
            H = []
            url = self.url_get+city
            # print(url)
            soup = Weather().get_soup(url)
            cityname = soup.find_all("h1", {"class": "h4 today_nowcard-location"})
            cityname = cityname[0].get_text().strip()
            time = soup.find_all("p", {"class": "today_nowcard-timestamp"})
            time = time[0].get_text().strip()
            temp = soup.find_all("div", {"class": "today_nowcard-temp"})
            temp = temp[0].get_text().strip()
            phrase = soup.find_all("div", {"class": "today_nowcard-phrase"})
            phrase = phrase[0].get_text().strip()
            hilo = soup.find_all("div", {"class": "today_nowcard-hilo"})
            hilo = hilo[0].get_text().strip().split('°')
            for i in range(0, len(hilo)):
                H.append(hilo[i])
            HILO = '°'.join(H)
            # print(HILO)
            text=cityname+time+'\n'+temp+'\n'+phrase+'\n'+HILO
            return text
        except:
            return

    def later_weather(self,city):
        try:
            url = self.url_get+city
            soup = Weather().get_soup(url)
            cityname = soup.find_all("h1", {"class": "h4 today_nowcard-location"})
            cityname = cityname[0].get_text().strip()
            time = soup.find_all("h2", {"class": "heading"})
            time = time[0].get_text().strip()
            dp0 = soup.find_all("span", {"class": "today-daypart-title"})
            dp1 = soup.find_all("span", {"class": "today-daypart-wxphrase"})
            dp2 = soup.find_all("span", {"class": "precip-val"})
            DP0 = [dp0[0].get_text().strip(), dp1[0].get_text().strip(), "降水概率",
                dp2[0].get_text().strip()]
            DP1 = [dp0[1].get_text().strip(), dp1[1].get_text().strip(), "降水概率",
                dp2[1].get_text().strip()]
            DP2 = [dp0[2].get_text().strip(), dp1[2].get_text().strip(), "降水概率",
                dp2[2].get_text().strip()]
            DP3 = [dp0[3].get_text().strip(), dp1[3].get_text().strip(), "降水概率",
                dp2[3].get_text().strip()]
            DP4 = [dp0[4].get_text().strip(), dp1[4].get_text().strip(), "降水概率",
                dp2[4].get_text().strip()]
            str0 = ','.join(DP0)
            str1 = ','.join(DP1)
            str2 = ','.join(DP2)
            str3 = ','.join(DP3)
            str4 = ','.join(DP4)
            text=cityname+time+'\n'+ str0+'\n'+ str1+'\n'+ str2+'\n'+ str3+'\n'+ str4
            return text
        except:
            return

# if __name__=='__main__':
#     text=Weather().later_weather('北京')
#     print (text)