#coding:utf-8

#引入相关模块
import requests
from bs4 import BeautifulSoup

url = "http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=%E4%B8%8A%E6%B5%B7%E6%B5%B7%E4%BA%8B%E5%A4%A7%E5%AD%A6"
#请求搜索上海海事大学关键字新闻网页的URL，获取其text文本

response = requests.get(url)  #对获取到的文本进行解析
html = response.text
soup=BeautifulSoup(html,features='lxml')  #根据HTML网页字符串创建BeautifulSoup对象
news=soup.find_all('div', {"class": "result"})
#times=soup.find_all('p',{"class":"c-author"})
#href=soup.find_all('h3',{"class":"c-title"})
'''
for l in href:    
    hs=l.find_all('a') #标题在a标签中
    for h in hs:
        title=h.text
        url=h['href']
        for t in news:
            time = t.find("p").get_text()  #时间在p标签中
            data = {'标题':title,
                    '链接':url,
                    '时间':time}
            print(data)
'''
for t in news:
    data = {
        "标题":t.find('a').text,
        "链接":t.find('a')['href'],
        "时间":t.find('p').get_text()
    }
    print(data)     