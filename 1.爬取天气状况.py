'''
Author: your name
Date: 2021-04-16 08:51:21
LastEditTime: 2021-04-16 10:15:59
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Learning\python网络爬虫\爬取天气状况.py
'''
'''
Author: your name
Date: 2021-04-16 08:51:21
LastEditTime: 2021-04-16 08:57:51
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Learning\python网络爬虫\爬取天气状况.py
'''
import urllib.request
from bs4 import BeautifulSoup
#打开网页，并解析网页
def getHtml(url):
    resp=urllib.request.urlopen(url)
    data=resp.read()
    html=data.decode()
    return html

#获得未来一周天气的信息并打印
def getWeather(li):
    # time是日期，wea是天气，wind是风向，wid1是风力大小
    print(li.find("span",attrs={"class":"time"}).text)
    
    print(li.find("span",attrs={"class":"wea"}).text)

    print(li.find("span",attrs={"class":"wind"}).text)
    
    print(li.find("span",attrs={"class":"wind1"}).text)

    p=li.find("span",attrs={"class":"wind"})
    sp=p.find_all("span")
    for s in sp:
        print(s["title"])

url="http://www.weather.com.cn/weather15d/101280601.shtml"
html=getHtml(url)
#调用BeautifulSoup函数并将解析后的编码赋值给soup
soup=BeautifulSoup(html,"html.parser")

ul=soup.find("ul",attrs={"class":"t clearfix"})

lis = ul.find_all("li")

for li in lis:
    getWeather(li)
