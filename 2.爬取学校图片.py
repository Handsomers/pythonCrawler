'''
Author: your name
Date: 2021-04-11 09:51:55
LastEditTime: 2021-04-11 09:59:41
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Learning\python网络爬虫\爬取学生信息\html\img\demo.py
'''
import re
import urllib.request
from bs4 import BeautifulSoup

def  getHtml(url):
    html=""
    try:
        resp=urllib.request.urlopen(url)
        data=resp.read()
        html=data.decode()
    except Exception as err:
        print(err)
    return html

def search(html):
    root=BeautifulSoup(html,'lxml')
    images=root.find_all('img')
    for img in images:
        src=urllib.request.urljoin(url,img['src'])
        download(src)

def download(src):
    global count
    try:

        resp=urllib.request.urlopen(src)

        data=resp.read()

        if src.endswith('.jpg'):

            ext='.jpg'

        else:

            ext='.png'

        count+=1

        f=open("2.爬取学校图片\\"+str(count)+ext,"wb")
        f.write(data)
        f.close()
        print('downloaded',src)
    except Exception as err:
        print(err)
    return html

count=0
url='https://gpnu.edu.cn/index.htm'
html=getHtml(url)
search(html)