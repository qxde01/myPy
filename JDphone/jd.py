# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 21:30:15 2014

@author: @第五逻辑 (新浪微博)
"""

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

#print sys.getdefaultencoding() 

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By

def strsub(sub=u'',p=list()):
    for x in p:
        if x.find(sub)==0:
            out=x.replace(sub,'')
            break
        else:out=u''
    return out
        
#############################################################
def JD_phone_list(url=u''):
    driver = webdriver.PhantomJS()
    driver.get(url)
    href=[]
    try:
        links=driver.find_elements_by_xpath("//ul[@class='list-h']//li//a[@target]")  
        links=[k.get_attribute('href') for k in links]
        driver.close
        links=list(set(links))
        for link in links:
            if link.find(u'http://item.jd.com')==0:
                href.append(link)
        print '  There is a total of  ',len(href),' phone product in this page.'
        return href
    except:
        print "  没有获取到手机网页列表！"
        return None
 #################################################################
def JD_phone_get(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    p_status=1
    try:
        g=driver.find_element_by_class_name('itemover-title').text
        if g==u'\u8be5\u5546\u54c1\u5df2\u4e0b\u67dc\uff0c\u975e\u5e38\u62b1\u6b49\uff01':
            p_status=0
            print '   该产品已下架！,url=',url
    except:
        p_status=1
        
    try:
        jd_price=driver.find_element_by_id('jd-price').text
        jd_price=jd_price.replace(u'\uffe5','')
    except:
        print '  价格获取失败'
        jd_price=u''
    try:         
        product_detail = driver.find_element_by_class_name('detail-list').text
        product_detail=product_detail.split(u'\n')
        ## 商品名称
        p_name=strsub(sub=u'\u5546\u54c1\u540d\u79f0\uff1a',p=product_detail)
        ## 商品编号
        p_id=strsub(sub=u'\u5546\u54c1\u7f16\u53f7\uff1a',p=product_detail)
        ## 品牌
        p_brand=strsub(sub=u'\u54c1\u724c\uff1a',p=product_detail)
        ## 上架时间
        p_addtime=strsub(sub=u'\u4e0a\u67b6\u65f6\u95f4\uff1a',p=product_detail)
        ## 商品毛重
        p_weight=strsub(sub=u'\u5546\u54c1\u6bdb\u91cd\uff1a',p=product_detail)
        ##商品产地
        p_place=strsub(sub=u'\u5546\u54c1\u4ea7\u5730\uff1a',p=product_detail)
        ## 网络
        p_network=strsub(sub=u'\u7f51\u7edc\uff1a',p=product_detail)
        ## 系统
        p_system=strsub(sub=u'\u7cfb\u7edf\uff1a',p=product_detail)
        ## CPU
        p_CPU=strsub(sub=u'CPU\uff1a',p=product_detail)
        ## 屏幕尺寸
        p_screenSize=strsub(sub=u'\u5c4f\u5e55\u5c3a\u5bf8\uff1a',p=product_detail)
        ## 机身颜色
        p_color=strsub(sub=u'\u673a\u8eab\u989c\u8272\uff1a',p=product_detail)
        ## 特点
        p_special=strsub(sub=u'\u7279\u70b9\uff1a',p=product_detail)
    except:
        print '  产品参数获取失败'
    p_comment=u''
    p_tags=u''
    try:    
        revurl='http://club.jd.com/review/'+p_id+'-0-1-0.html'
        driver.get(revurl)
        p_comment=driver.find_element_by_class_name('tab').text
        p_tags=driver.find_element_by_class_name('p-bfc').text
    except:
        print '  评论信息获取失败!'
        
    driver.close
    try:
        print "Getting phone infomation sucessfully from url:",url
        out={"p_url":url,'p_id':p_id,'p_status':p_status,'jd_price':jd_price,\
        "p_name":p_name,"p_brand":p_brand,"p_addtime":p_addtime,"p_weight":p_weight,\
        "p_place":p_place,"p_network":p_network,"p_system":p_system,"p_CPU":p_CPU,\
        "p_screenSize":p_screenSize,"p_color":p_color,"p_special":p_special,\
        "p_comment":p_comment,"p_tags":p_tags}
        return out
    except:
        print "  产品信息获取失败！"
        return None
        


