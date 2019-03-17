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
import requests
from bs4 import BeautifulSoup
import os


def request_download(pic_name, IMAGE_URL):
    r = requests.get(IMAGE_URL)
    with open('./image/' + str(feed_cnt) + '/' + pic_name + '.png', 'wb') as pic_file:
        pic_file.write(r.content)  

# 系列class查找器
def has_class_bd(tag):
    return tag.has_attr('class') and tag['class'] == ['bd']

def has_class_md(tag):
    return tag.has_attr('class') and tag['class'] == ['md']

def has_class_ft(tag):
    return tag.has_attr('class') and tag['class'] == ['ft']

def has_class_rt(tag):
    return tag.has_attr('class') and ('rt_content' in tag['class'])

def has_class_comments_content(tag):
    return tag.has_attr('class') and tag['class'] == ['comments_content']


def MakeDir(folderName):
    new_path = './image/'+folderName
    if not os.path.exists(new_path):
        os.mkdir(new_path)


feed_cnt = 0

def parse_text(bd_item, WriteFile): # 解析bd标签内的文字
    WriteFile.write(str(bd_item.a.text)+' : ')
    WriteFile.write(str(bd_item.pre.text)+'\n')
    
def parse_pic(md_item, WriteFile): # 解析md标签内的图片
    cnt = 1
    global feed_cnt
    pic = md_item.find_all('a')
    for i in pic:
        pic_URL = str(i['href'])
        if pic_URL.startswith('http'):
            MakeDir(str(feed_cnt))
            try:
                request_download(str(cnt), pic_URL)
            except:
                print("wrong pic URLs! : ", pic_URL)
            WriteFile.write('    >> image/' + str(feed_cnt) + '/' + str(cnt) + '.png ' + '\n')
            #WriteFile.write(pic_URL+'\n')

            cnt += 1

def parse_time(ft_item, WriteFile): # 解析ft标签内的时间戳
    ft = ft_item.find('a')
    if ft.has_attr('title'):
        print('posted at ', ft['title'])
        WriteFile.write('--- ' + str(ft['title']) + ' ---\n')
    else:
        print(" parse time FAIL !")

def parse_rt(rt_item, WriteFile): # 解析rt标签内的转发信息
    WriteFile.write('    ') # 转发的原文内容缩进一点
    parse_text(rt_item.find(has_class_bd), WriteFile)
    if rt_item.find(has_class_md):
        WriteFile.write('    图片见上\n') # 懒得区分原创图和转发图了orz

def parse_comments(comment_list, WriteFile):
    # TODO
    '''
    for item in comment_list:
        print(item.prettify())
    '''


def parse_1_feed(feed, WriteFile):
    ''' bd : 文字内容  
            a.string 用户名 *
            pre 文字内容 *
        md ：图片内容
            a ['href'] 图片网址
        ft ：时间戳
            a  title是日期时间
        md rt_content ：转发内容
            bd ：转发的文字
            md：图片
        box_extra bor3 : 评论框
            comments_content：评论内容 （待分析）
    '''
    global feed_cnt
    feed_cnt += 1
    print('parsing feed: ', feed_cnt)

    parse_text(feed.find(has_class_bd), WriteFile)

    parse_pic(feed.find(has_class_md), WriteFile)

    parse_time(feed.find(has_class_ft), WriteFile)

    if feed.find(has_class_rt):
        parse_rt(feed.find(has_class_rt), WriteFile)
    
    if feed.find(has_class_comments_content):
        parse_comments(feed.find_all(has_class_comments_content), WriteFile)


    WriteFile.write('\n') # 结尾添加换行


new_file = open('output.txt','w',encoding="utf-8")
new_file.close()

driver = webdriver.Chrome('/Users/godlike/Desktop/work/awesome-python-login-model/qqzone/chromedriver')  # 选择浏览器，此处我选择的Chrome
QQ_NUMBER = input('请输入你的QQ号')
PASSWORD = input('请输入你的QQ密码')

# driver.get('http://i.qq.com/')
driver.get('http://user.qzone.qq.com/534440305/311')
driver.switch_to.frame('login_frame')
driver.find_element_by_id('switcher_plogin').click()

driver.find_element_by_name('u').clear()
driver.find_element_by_name('u').send_keys(QQ_NUMBER)  # 此处输入你的QQ号
driver.find_element_by_name('p').clear()
driver.find_element_by_name('p').send_keys(PASSWORD)  # 此处输入你的QQ密码

driver.execute_script("document.getElementById('login_button').parentNode.hidefocus=false;")

driver.find_element_by_xpath('//*[@id="loginform"]/div[4]/a').click()
driver.find_element_by_id('login_button').click()

time.sleep(1)  


driver.get('http://user.qzone.qq.com/534440305/311')
time.sleep(3)  
driver.switch_to.frame('app_canvas_frame')
page_num = 0

for page in range(112):
    with open('output.txt','a',encoding="utf-8") as f:

        soup = BeautifulSoup(driver.page_source, "html.parser")

        msgList = soup.find(id="msgList")

        for msg_item in msgList.find_all('li'):
            feed_content = msg_item.find_all('div')

            for div_item in feed_content:
                #print(div_item)
                if 'class' in div_item.attrs:
                    if div_item['class'] == ['box', 'bgr3']:
                        parse_1_feed(div_item, f)


    page_id = 'pager_num_' + str(0+page_num) + '_' + str(2 + page_num)
    btn = driver.find_element_by_id(page_id)
    #btn = driver.find_element_by_link_text('2')
    btn.click()
    page_num += 1
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> done page ", page_num)
    time.sleep(5)
    driver.switch_to.parent_frame()
    driver.switch_to.frame('app_canvas_frame')
    

driver.close()

'''
btn = driver.find_element_by_id('pager_num_0_2')
btn.click()
time.sleep(3)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>page 2")
driver.switch_to.parent_frame()
driver.switch_to.frame('app_canvas_frame')
soup = BeautifulSoup(driver.page_source, "html.parser")
msgList = soup.find(id="msgList")

for msg_item in msgList.li.next_siblings:
    feed_content = msg_item.find_all('div')
    for div_item in feed_content:
        #print(div_item)
        if 'class' in div_item.attrs:
            if div_item['class'] == ['box', 'bgr3']:
                parse_1_feed(div_item)
'''



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
'''