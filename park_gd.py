# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:23:53 2019

@author: fanning1207
"""

import requests
import os
import time
import glob
import json
import pandas as pd
import math
import pymysql

os.chdir('C:\\Users\\fanning1207\\Desktop')

#--------------------------------------down json--------------
with open('data2.json', 'r', encoding = 'utf-8') as f:
    city = json.load(f)
    
cityvalue=list(city.values())

city3=[]
for i in range(len(cityvalue)):
    term=cityvalue[i]
    city3.extend(list(term.keys()))
len(city3)


for j in range(len(city3)):
    city_now = city3[j]
    i=1
    url = "http://restapi.amap.com/v3/place/text?key=" + key3 + "&keywords=产业园区&types=产业园区&city=" + str(city_now) + "&children=&offset=50&page=" + str(i) + "&extensions=all"
    file_name = city_now + "_park_" + str(i) + ".json"
    r = requests.get(url)
    with open(file_name, 'w', encoding = 'utf-16') as f:
        f.write(r.text)
    
    with open(file_name, 'r', encoding = 'utf-16') as f:
        park_count = json.load(f)
    park_count_num = int(park_count["count"])
    
    if park_count_num>50:
        limi = math.ceil(park_count_num/50)+1
        for i in range(2,limi):
            url = "http://restapi.amap.com/v3/place/text?key=" + key3 + "&keywords=产业园区&types=产业园区&city=" +  str(city_now)  + "&children=&offset=50&page=" + str(i) + "&extensions=all"
            file_name = city_now + "_park_" + str(i) + ".json"
            r = requests.get(url)
            with open(file_name, 'w', encoding = 'utf-16') as f:
                f.write(r.text)
            time.sleep(1)
    print(j)

#----------------------------deal with json------------
park_id = []
parent = []
park_name = []
park_type = []
typecode = []
address = []
location = []
tel = []
postcode = []
website = []
pcode = []
pname = []
citycode = []
cityname = []
adcode = []
adname = []
gridcode = []

j=0                    
for f in glob.glob("*park*.json"):
    if os.path.getsize(f)>218:
        with open(f, "r", encoding = 'utf-16') as infile:
            temp = json.load(infile)["pois"]
            count=len(temp)
            for i in range(count):
                park_id.append(temp[i]["id"])
                parent.append(temp[i]["parent"])
                park_name.append(temp[i]["name"])
                park_type.append(temp[i]["type"])
                typecode.append(temp[i]["typecode"])
                address.append(temp[i]["address"])
                location.append(temp[i]["location"])
                tel.append(temp[i]["tel"])
                postcode.append(temp[i]["postcode"])
                website.append(temp[i]["website"])
                pcode.append(temp[i]["pcode"])
                pname.append(temp[i]["pname"])
                citycode.append(temp[i]["citycode"])
                cityname.append(temp[i]["cityname"])
                adcode.append(temp[i]["adcode"])
                adname.append(temp[i]["adname"])
                gridcode.append(temp[i]["gridcode"])
                j=j+1
                print(j)
            infile.close

datacp = {"park_id":park_id,"parent":parent,
          "park_name":park_name,
          "park_type":park_type,"typecode": typecode,
          "address":address,
            "location":location,
            "tel":tel,
            "postcode":postcode,
            "website":website,
            "pcode":pcode,
            "pname":pname,
            "citycode":citycode,
            "cityname":cityname,
            "adcode":adcode,
            "adname":adname,
            "gridcode":gridcode} 
    
datacp=pd.DataFrame(datacp)

datacp.to_csv("park.csv",index=False,sep=',',encoding="utf_8_sig")
        
#-----------------------------get shape-------------------
sql = 'SELECT park_id,pname FROM park'

db = pymysql.connect(host=host,
                       user=用户名,
                       passwd=用户密码,
                       db=数据库名,
                       port=3306,
                       charset="utf8")      

cursor = db.cursor()
cursor.execute(sql)
datalist= cursor.fetchall()
datalist  = pd.DataFrame(list(datalist),columns=('park_id','park_name'))

i = 165

park_url = "https://ditu.amap.com/detail/get/detail?id=" + datalist.park_id[i]

file_name = datalist.park_id[i] + ".json"
r = requests.get(park_url)
with open(file_name, 'w', encoding = 'utf-16') as f:
    f.write(r.text)

with open(file_name, 'r', encoding = 'utf-16') as f:
    park_all = json.load(f)
    
try:
    shape = park_all['data']['spec']['mining_shape']['shape']
    add_it0 = 'update park set shape = "' + shape + '" where park_id = "' + datalist.park_id[i] +'"'
    cursor.execute(add_it0)
    db.commit()
except:
    pass

try:
    area = park_all['data']['spec']['mining_shape']['area']
    add_it1 = 'update park set area = ' + area + ' where park_id = "' + datalist.park_id[i] +'"'
    cursor.execute(add_it1)
    db.commit()
except:
    pass

try:
    pic_cover = park_all['data']['pic_cover']['url']
    add_it2 = 'update park set pic = "' + pic_cover + '" where park_id = "' + datalist.park_id[i] +'"'
    cursor.execute(add_it2)
    db.commit()
except:
    pass

db.close()