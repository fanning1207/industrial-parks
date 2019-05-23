# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:37:25 2019

@author: fanning1207
"""

import os
import json
import pandas as pd
import pymysql
import requests
import math
import time


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

key1 = key1
key2 = key2
key3 = key3

for j in range(6000):
    
    if j<2000:
        key = key1
    else:
        if j>=4000:
            key = key3
        else:
            key = key2
    
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
    time.sleep(3)
    print(j)