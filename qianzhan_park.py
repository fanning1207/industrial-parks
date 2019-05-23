# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 16:43:28 2019

@author: fanning1207
"""

from selenium import webdriver
import time
import os
#import pandas as pd
#import requests
#from bs4 import BeautifulSoup
import pandas as pd
import requests
import scrapy

os.chdir('C:\\Users\\fanning1207\\Desktop')

chrome=webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
chrome.get('https://d.qianzhan.com/yuanqu/')
chrome.maximize_window()


url=[]
park_name=[]

#136,131


for j in range(110,222):
    time.sleep(2)
    if j<221:
        num=16
    else:
        num=11
    for i in range(1,num):
        need='/html[1]/body[1]/div[3]/div[1]/table[1]/tbody[1]/tr['+str(i)+']/td[2]/a[1]'
        url.append(chrome.find_element_by_xpath(need).get_attribute('href'))
        park_name.append(chrome.find_element_by_xpath(need).text)
    if j<221:
        try:
            chrome.find_element_by_link_text(u'下一页').click()
        except:
            try:
                time.sleep(5)
                chrome.find_element_by_link_text(u'下一页').click()
            except:
                time.sleep(15)
                chrome.find_element_by_link_text(u'下一页').click()               
        time.sleep(3)
    print(j)

datacp = {'url':url,
          'park_name':park_name} 

datacp=pd.DataFrame(datacp)

datacp.to_csv("park.csv",index=False,sep=',',encoding="utf_8_sig")


for i in range(1,3311):
    url_park=url[i]
    url_park="https://d.qianzhan.com/yuanqu/getNearby"
    res=requests.get(url_park)
    print(res.headers)

    scrapy.Request(url=url_park,cookies={"qznewsite.uid":"bvfrx345rl55h245xkgutaub"}).headers.get('Referer', None)
   
    
header={"Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "qznewsite.uid=bvfrx345rl55h245xkgutaub",
        "DNT": "1",
        "Host": "d.qianzhan.com",
        "Origin": "https://d.qianzhan.com",
        "Referer": "https://d.qianzhan.com/yuanqu/yqmap?center=120.406047,36.403073&zoom=16&poly=120.402037,36.403383;120.407385,36.403223;120.407299,36.401816;120.401795,36.40198&yid=050cc9cf21740c66",
        "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）",
        "X-Requested-With": "XMLHttpRequest"}

url="https://d.qianzhan.com/yuanqu/getNearby"
    
requests.get(url,headers=header).json().encode('utf-8')



