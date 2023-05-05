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
