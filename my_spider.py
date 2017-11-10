# -*- coding = UTF-8 -*-
from urllib import request
import time
from bs4 import BeautifulSoup
import urllib
if __name__=="__main__":
    head={}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    Str = input("输入小说的名字")
    file = open('note\\'+Str+'.txt', 'w', encoding='utf-8')
    Str = urllib.request.quote(Str)
    print(Str)
    #http://www.biquge5200.com/modules/article/search.php?searchkey=%E5%A5%A5%E5%8F%A4%E6%96%AF%E9%83%BD
    search_url="http://www.biquge5200.com/modules/article/search.php?searchkey="+Str
    http_req = request.Request(url=search_url,headers=head)
    http_response = request.urlopen(http_req)
    http_content = http_response.read().decode("gbk","ignore")
    http_content_soup = BeautifulSoup(http_content,"lxml")
    url_list = http_content_soup.find_all('td')
    url_list_soup = BeautifulSoup(str(url_list),"lxml")
    text_url = url_list_soup.find_all(class_="odd")
    tar_url=""
    for link in text_url:
        if link.a is not None:
            tar_url = link.a.get('href')
            break

    text_req = request.Request(url=tar_url,headers=head)
    text_response = request.urlopen(text_req)
    text_html = text_response.read().decode('gbk','ignore')
    text_html_soup = BeautifulSoup(text_html,'lxml')
    title_dl_soup = text_html_soup.find_all("dl")
    title_soup = BeautifulSoup(str(title_dl_soup),'lxml')
    flag = False
    for i in title_soup.dl.children:
        if i =="\n":
            continue
        if "正文" in str(i.string):
            flag = True
            continue
        if flag:
            charptr = i.string
            print(charptr)
            cur_url = i.a.get("href")
            cur_req = request.Request(url=cur_url,headers=head)
            cur_response = request.urlopen(cur_req)
            cur_html = cur_response.read().decode("gbk","ignore")
            cur_html_soup = BeautifulSoup(cur_html,"lxml")
            text = cur_html_soup.find_all("div",id="content")
            text_soup = BeautifulSoup(str(text),"lxml")
            content = text_soup.div
            file.write(charptr + '\n\n')
            for j in content.text:
                if j =='\r':
                    file.write('\n')
                if j!=' ':
                    file.write(j)
            file.write("\n\n")
            time.sleep(0.5)
    file.close()
    print("小说下载完毕")