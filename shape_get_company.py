# -*- coding: utf-8 -*-
"""
Created on Thu May  9 15:57:44 2019

@author: fanning1207
"""

import os
import json
import pandas as pd
import pymysql
import requests
import math
import time
import glob


sql = 'SELECT park_id,shape FROM park WHERE shape IS NOT NULL AND shape<>"NA" AND com_count IS NULL'

db = pymysql.connect(host=host,
                       user=用户名,
                       passwd=用户密码,
                       db=数据库名,
                       port=3306,
                       charset="utf8")     

cursor = db.cursor()
cursor.execute(sql)
datalist= cursor.fetchall()
datalist  = pd.DataFrame(list(datalist),columns=('park_id','shape'))

park_id = datalist['park_id']
shape = datalist['shape']

shape = [w.replace(';', '|') for w in shape]

for j in range(2000):
    
    key = key1
    
    i=1
    url = "http://restapi.amap.com/v3/place/polygon?key=" + key + "&polygon=" + str(shape[j]) + "&keywords=公司&types=&offset=50&page=" + str(i) + "&extensions=all"
    file_name = park_id[j] + "_shape_" + str(i) + ".json"
    
    try:
        r = requests.get(url)
        with open(file_name, 'w', encoding = 'utf-16') as f:
            f.write(r.text)
        
        if os.path.getsize(file_name)!=2:
            with open(file_name, 'r', encoding = 'utf-16') as f:
                park_count = json.load(f)
                park_count_num = int(park_count["count"])
                
        #        update_it = 'update park set com_count = ' + str(park_count_num) + ' where park_id = "' + datalist.park_id[i] +'"'
        #        cursor.execute(update_it)
        #        db.commit()    
        
            if park_count_num>50:
                limi = math.ceil(park_count_num/50)+1
                for i in range(2,limi):
                    url = "http://restapi.amap.com/v3/place/polygon?key=" + key + "&polygon=" + str(shape[j]) + "&keywords=公司&types=&offset=50&page=" + str(i) + "&extensions=all"
                    file_name = park_id[j] + "_shape_" + str(i) + ".json"
                    r = requests.get(url)
                    with open(file_name, 'w', encoding = 'utf-16') as f:
                        f.write(r.text)
                    time.sleep(3)
        else:
            os.remove(file_name)
    except:
        pass
    time.sleep(5)
    print(j)

#----------------------------deal with json------------
park_id = []
com_poi_id = []
com_parent = []
com_name = []
com_type = []
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
business_area =[]
pic = []
gridcode = []

j=0                    
for f in glob.glob("*shape*.json"):
    if os.path.getsize(f)>218 and time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getctime(f)))>'2019-05-17 0:0':
        try:
            with open(f, "r", encoding = 'utf-16') as infile:
                temp = json.load(infile)["pois"]
                count=len(temp)
                for i in range(count):
                    park_id.append(os.path.splitext(f)[0].split("_")[0])
                    com_poi_id.append(temp[i]["id"])
                    com_parent.append(temp[i]["parent"])
                    com_name.append(temp[i]["name"])
                    com_type.append(temp[i]["type"])
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
                    business_area.append(temp[i]["business_area"])
                    gridcode.append(temp[i]["gridcode"])
                    
                    try:
                        pic.append(temp[i]['photos'][0]['url'])
                    except:
                        pic.append('')
                    j=j+1
                    print(j)
                infile.close
        except:
            pass

datacp = {"park_id":park_id,
          "com_poi_id":com_poi_id,
          "com_parent":com_parent,
          "com_name":com_name,
          "com_type":com_type,
          "typecode": typecode,
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
            "business_area":business_area,
            "pic":pic,
            "gridcode":gridcode} 
    
datacp=pd.DataFrame(datacp)

datacp.replace('[]', '',  inplace=True)

datacp.to_csv("shape.csv",index=False,sep=',',encoding="utf_8_sig")

db.close()

#----------------------------------
i=0
for f in glob.glob("*shape_1.json"):
    if os.path.getsize(f)!=132:
        park_id = os.path.splitext(f)[0].split("_")[0]
        with open(f, 'r', encoding = 'utf-16') as file:
            park_count = json.load(file)
            park_count_num = int(park_count["count"])
            update_it = 'update park set com_count = ' + str(park_count_num) + ' where park_id = "' + park_id +'"'
            cursor.execute(update_it)
            db.commit()  
            i=i+1
            print(i)


