#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-7
"""

import time  # 用来延时
from selenium import webdriver

driver = webdriver.Chrome()  # 选择浏览器，此处我选择的Chrome
QQ_NUMBER = input('请输入你的QQ号')
PASSWORD = input('请输入你的QQ密码')

# driver.get('http://i.qq.com/')
driver.get('http://user.qzone.qq.com/534440305/311')
driver.switch_to.frame('login_frame')
driver.find_element_by_id('switcher_plogin').click()

driver.find_element_by_name('u').clear()
driver.find_element_by_name('u').send_keys(QQ_NUMBER)  # 此处输入你的QQ号
time.sleep(2)
driver.find_element_by_name('p').clear()
driver.find_element_by_name('p').send_keys(PASSWORD)  # 此处输入你的QQ密码

driver.execute_script("document.getElementById('login_button').parentNode.hidefocus=false;")

driver.find_element_by_xpath('//*[@id="loginform"]/div[4]/a').click()
driver.find_element_by_id('login_button').click()

time.sleep(5)  
# btns = driver.find_elements_by_css_selector('a.item.qz_like_btn_v3')  # 此处是CSS选择器
# btns = driver.find_element_by_class_name('menu_item_311')
'''
btns = driver.find_element_by_link_text('说说')
print (btns)
#for btn in btns:
    #print(btn)
btns.click()
time.sleep(5)
'''
'''
time.sleep(10)
btns = driver.find_elements_by_css_selector('a.item.qz_like_btn_v3')  # 此处是CSS选择器
print (btns)
for btn in btns:
    #print(btn)
    btn.click()
'''

driver.switch_to.frame('app_canvas_frame')

#将页面滚动条拖到底部
js="var q=document.documentElement.scrollTop=10000"
driver.execute_script(js)
time.sleep(5)

content = driver.find_elements_by_css_selector('.content')
stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
for con,sti in zip(content,stime):
    data = {
        'time':sti.text,
        'shuos':con.text
    }
    print(data)

js="var q=document.documentElement.scrollTop=10000"
driver.execute_script(js)
time.sleep(5)




btn = driver.find_element_by_id('pager_num_0_2')
#btn = driver.find_element_by_link_text('2')
btn.click()
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>page 2")
driver.switch_to.parent_frame()
driver.switch_to.frame('app_canvas_frame')
time.sleep(5)
content = driver.find_elements_by_css_selector('.content')
stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
for con,sti in zip(content,stime):
    data = {
        'time':sti.text,
        'shuos':con.text
    }
    print(data)