# -*- coding:UTF -8 -*-
from urllib import request
from bs4 import BeautifulSoup
import re
import sys
if __name__=="__main":
    #创建txt文件
    file = open('奥古之都之路.txt','w',encoding='utf-8')
    #小说目录
    target_url = "http://www.biqukan.com/3_3398/"
    #模拟访问
    head={}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    target_req = request.Request(url=target_url,headers =  head)
    target_response = request.urlopen(target_req)
    target_html = target_response.read().decode('gbk','ignore')
    #创建bs对象
    list_soup = BeautifulSoup(target_html,'lxml')
    #搜索文档树 找出div标签中class为listmain的所有子标签
    chapters = list_soup.find_all('div',class_='listmian')
    #使用查询结果再创建一个bs对象，对其继续进行解析
    download_soup = BeautifulSoup(str(chapters),'lxml')
    #计算章节个数
    numbers = (len(download_soup.dl.contents)-1)/2-8
    index = 1
    #开始记录内容标志位 只要正文卷下面的链接 最新章节列表链接剔除
    begin_flag = False
    #遍历dl标签下所有子节点
    for child in download_soup.dl.children:
        if child !='\n':
            #找到正文卷，标志位启用
            begin_flag = True
            #爬起链接并下载链接内容
        if begin_flag == True and child.a!=None:
            download_url = "http://www.biqukan.com" + child.a.get('href')
            download_req = request.Request(url = download_url,headers = head)
            download_response = request.urlopen(download_req)
            download_html = download_response.read().decode('gbk','ignore')
            download_name =child.string
            texts_soup =  BeautifulSoup(download_html,'lxml')
            texts = texts_soup.find_all(id = 'content',class_="showtxt")
            texts_soup = BeautifulSoup(str(texts),'lxml')
            wrire_flag = True
            file.write(download_name+'\n\n')
            #将爬取内容写入文件
            for each in texts_soup.div.text.replace('\xa0',''):
                if each =='h':
                    write_flag = False
                if write_flag == True and each !=" ":
                    file.write(each)
                if write_flag == True and each =='\r':
                    file.write('\n')
            file.write('\n\n')
            #打印爬取速度
            sys.stdout.write("已下载:%.3f%%" %float(index/numbers)+"\r")
            sys.stdout.flush()
            index+=1
    file.close()