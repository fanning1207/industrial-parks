# -*- coding: utf-8 -*-
"""
Created on Sun May 12 01:36:02 2019

@author: fanning1207
"""

import os
import json
import pandas as pd
import pymysql
import requests
import random 
from time import sleep


sql = 'SELECT park_id,pname FROM park WHERE shape IS NULL AND area IS NULL AND pic IS NULL'

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

file_name = "temp.json"

for i in range(len(datalist.park_id)):
    
    park_url = "https://ditu.amap.com/detail/get/detail?id=" + datalist.park_id[i]
    
    r = requests.get(park_url)
    with open(file_name, 'w', encoding = 'utf-16') as f:
        f.write(r.text)

    if os.path.getsize(file_name)!=68:
        
        with open(file_name, 'r', encoding = 'utf-16') as f:
            park_all = json.load(f)
            
        try:
            shape = park_all['data']['spec']['mining_shape']['shape']
        except:
            shape = "NA"
            
        add_it0 = 'update park set shape = "' + shape + '" where park_id = "' + datalist.park_id[i] +'"'
        cursor.execute(add_it0)
        db.commit()        
        
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
        
        sleep(random.uniform(3,7))
    else:
        break
    
    print(i)
db.close()

#os.path.getctime