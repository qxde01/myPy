# -*- coding: utf-8 -*-
"""
Created on Tue Mar 04 10:15:40 2014

@author: @第五逻辑 (新浪微博)
"""

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')
from selenium import webdriver
import MySQLdb
from jd import JD_phone_list,JD_phone_get

#url='http://list.jd.com/9987-653-655-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-33.html'
#http://list.jd.com/9987-653-655-0-0-0-0-0-0-0-1-1-2-1-1-72-4137-33.html
#http://list.jd.com/9987-653-655-0-0-0-0-0-0-0-1-1-3-1-1-72-4137-33.html
# 连接数据库　
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='chin',db='jd',charset='utf8')
    cursor = conn.cursor()
except Exception, e:
    print e
    sys.exit()
    
start=5
end=10
for k in range(start,end+1):
    print "page:",k
    url=u'http://list.jd.com/9987-653-655-0-0-0-0-0-0-0-1-1-'+str(k)+'-1-1-72-4137-33.html'
    links=JD_phone_list(url)
    
    cur = conn.cursor()
    cur.execute('select p_url from tb_jd_phone')
    urls=cur.fetchall()
    cur.close()
    urls=[u[0] for u in urls]
    links=list(set(links).difference(set(urls))) 
    
    if len(links)> 0:
        for link in links:
            phone=JD_phone_get(url=link)
            sql='INSERT INTO tb_jd_phone(p_id , p_url,  p_name,p_status ,\
                p_brand , p_system , p_addtime , jd_price , p_weight,\
                p_network, p_color, p_CPU , p_screenSize, p_place , p_special,\
                p_tags , p_comment ) values ( ' \
                + str(phone["p_id"]) \
                + ',"'+ phone["p_url"] \
                + '","'+phone["p_name"] \
                + '","'+str(phone["p_status"]) \
                + '","'+phone["p_brand"] \
                + '","'+phone["p_system"] \
                + '","'+phone["p_addtime"] \
                + '","'+phone["jd_price"] \
                + '","'+phone["p_weight"] \
                + '","'+phone["p_network"] \
                + '","'+phone["p_color"] \
                + '","'+phone["p_CPU"] \
                + '","'+phone["p_screenSize"] \
                + '","'+phone["p_place"] \
                + '","'+phone["p_special"] \
                + '","'+phone["p_tags"] \
                + '","'+phone["p_comment"]+'" ) ;'
            try:
                cursor.execute(sql)
            except Exception, e:
                print e
        conn.commit()
cursor.close()
conn.close()            
'''
create table tb_jd_phone(p_id int not NULL,
                p_url varchar(256) DEFAULT NULL,
                p_name varchar(256) DEFAULT NULL,  
                p_status varchar(256) DEFAULT NULL,
                p_brand varchar(256) DEFAULT NULL,        
                p_system varchar(256) DEFAULT NULL,             
                p_addtime varchar(256) DEFAULT NULL,        
                jd_price varchar(256) DEFAULT NULL,  
                p_weight varchar(256) DEFAULT NULL,                                  
                p_network varchar(256) DEFAULT NULL,      
                p_color varchar(256) DEFAULT NULL,  
                p_CPU varchar(256) DEFAULT NULL,   
                p_screenSize varchar(256) DEFAULT NULL, 
                p_place varchar(256) DEFAULT NULL,        
                p_special varchar(256) DEFAULT NULL,      
                p_tags varchar(256) DEFAULT NULL,               
                p_comment varchar(256) DEFAULT NULL, 
                PRIMARY KEY (`p_id`)  
	) ENGINE=InnoDB  
	ROW_FORMAT=COMPRESSED  
	DEFAULT CHARSET=utf8;
 '''