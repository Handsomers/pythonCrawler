# Python爬虫脚本说明

## 1.爬取天气状态（简单）

本脚本是爬取深圳（可改为你的城市）近一周天气的脚本，这是网站网址

[深圳天气预报,深圳7天天气预报,深圳15天天气预报,深圳天气查询 (weather.com.cn)](http://www.weather.com.cn/weather15d/101280601.shtml)

![image-20230505120407266.png](https://github.com/Handsomers/pythonCrawler/blob/master/images/image-20230505120407266.png?raw=true)(https://github.com/Handsomers/pythonCrawler/blob/master/images/image-20230505124417714.png?raw=true)
### 需要具备的知识：

1.BeautifulSoup库及其基本函数的使用

运行python打印的效果如下：

```
周五（12日）
多云转阴
东风
<3级
周六（13日）
多云转雨
东南风
<3级
周日（14日）
雨转阴
南风转东北风
<3级
周一（15日）
雨
东风
<3级
周二（16日）
雨转阴
北风转东北风
<3级
周三（17日）
阴转雨
东北风转东风
<3级
周四（18日）
雨
东风
<3级
周五（19日）
阴
东风
<3级
```

## 2.爬取某个网站的图片并保存

网站：[广东技术师范大学 (gpnu.edu.cn)](https://gpnu.edu.cn/index.htm)

![image-20230505124417714.png](https://github.com/Handsomers/pythonCrawler/blob/master/images/image-20230505124417714.png?raw=true)

### 爬取的代码

```
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
```

### 爬取的效果

![image-20230505124530042.png](https://github.com/Handsomers/pythonCrawler/blob/master/images/image-20230505124530042.png?raw=true)

## 3.爬取豆瓣250热门电影的信息

网站网址：[豆瓣电影 Top 250 (douban.com)](https://movie.douban.com/top250?start=)

![image-20230505124934153.png](https://github.com/Handsomers/pythonCrawler/blob/master/images/image-20230505124934153.png?raw=true)

### 爬取代码

```
from bs4 import BeautifulSoup #解析网页
import re #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定url，获取网页数据
import xlwt  #进行excel操作
import sqlite3  #进行SQLite数据库操作

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #爬取网页
    datalist = getData(baseurl)
    #保存数据
    savepath = "豆瓣电影Top250.xls"
    saveData(datalist,savepath)
#电影链接
findLink = re.compile(r'<a href="(.*?)">')
#封面图片
findImgSrc = re.compile(r'<img.*src="(.*?)".*>',re.S)
#电影名称
findTitle = re.compile(r'<span class="title">(.*)</span>')
#评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#电影详细内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)


        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            #print(item)
            data = []
            item = str(item)

            Link = re.findall(findLink,item)[0]
            data.append(Link)

            ImgSrc = re.findall(findImgSrc,item)[0]
            data.append(ImgSrc)

            Title = re.findall(findTitle,item)
            if len(Title)==2:
                ctitle = Title[0]
                data.append(ctitle)
                otitle = Title[1].replace("/","")
                data.append(otitle)
            else:
                data.append(Title[0])
                data.append(' ')

            Rating = re.findall(findRating,item)[0]
            data.append(Rating)

            Judge = re.findall(findJudge,item)[0]
            data.append(Judge)

            Inq = re.findall(findInq,item)
            if len(Inq) !=0:
                Inq = Inq[0].replace("。","")
                data.append(Inq)
            else:
                data.append(" ")

            Bd = re.findall(findBd,item)[0]
            Bd = re.sub('<br(\s+)?/>(\s+)?'," ",Bd)
            data.append(Bd.strip())

            datalist.append(data)    #把处理好的一个电影信息存储到datalist中
    #解析网页
    return datalist

#获取指定一个网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.116 Safari/537.36"
    } #伪装成网页的形式，请求网页信息
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
#保存数据
def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    col = ("电影详情链接","封面链接","影片中文名","影片外国名","评分","评价数","概况","相关信息","")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save('豆瓣电影Top250.xls')


main()
print("爬取完毕")
```

### 爬取效果

![image-20230505125127736.png](https://github.com/Handsomers/pythonCrawler/blob/master/images/image-20230505125127736.png?raw=true)
