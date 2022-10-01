import json
import time

import requests
import re
import os
from html import unescape
from bs4 import BeautifulSoup

proxies ={
        'http': 'http://127.0.0.1:4780',
        'https': 'http://127.0.0.1:4780'  # https -> http
    }
headers={
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive'
    }

def get_url(url):
    with open("cookies.txt","r") as file:
        cookie = file.read()

    cookies = json.loads(cookie)
    res = requests.get(url,headers=headers,proxies=proxies,cookies=cookies)
    return res

def down_html(res,filename):

    soup = BeautifulSoup(res.text, "lxml")
    #filename = re.findall('[\u4e00-\u9fa5]+', str(soup.find_all("h1", {"class": "rich_media_title"})[0].text))

    path = f".\\公众号\\渗透师老A\\{filename}"
    os.mkdir(path)
    htmlpath = path + "\\" + str(filename) + ".html"
    with open(htmlpath, "wb") as file:
        file.write(res.content)
    return htmlpath

#获取页面中的图片并下载
def down_pic(res,filename,htmlpath):
    piclist = []
    soup = BeautifulSoup(res.text,"lxml")
    #aurl出来的是一个列表
    aurl = soup.find_all('img',{"class":"rich_pages wxw-img"})
    for each in aurl:
        piclist.append(each['data-src'])

    paTh = f"E:\\pythonnbxm\\wxgzh\\公众号\\渗透师老A\\{filename}"

    i=1
    new = []
    for item in piclist:

        pic = requests.get(item,proxies=proxies,headers=headers)
        picpath = paTh + "\\" + str(i) + ".jpg"
        newpicpath = str(i) + ".jpg"
        new.append(newpicpath)
        with open(picpath,"wb") as pic_file:
            pic_file.write(pic.content)
        i=i+1
    reimgurl(filename,new,piclist)

#替换原页面的img标签地址
def reimgurl(filename,new,old):
    oldpath = f".\\公众号\\渗透师老A\\{filename}" + "\\" + str(filename) + ".html"
    newpath = f".\\公众号\\渗透师老A\\{filename}" + "\\" + "new_" + str(filename) + ".html"
    with open(oldpath, encoding="utf-8")as f ,open(newpath, "w", encoding="utf-8") as fw:
        for line in f:
            line = line.replace("&amp;", "&")

            for i in range(len(old)):
                #图片的src是集中在一行上的
                line = line.replace(old[i], new[i])
                new_line = line

            new_line = new_line.replace("data-src", "src")
            fw.write(new_line)

def extractUrl():
    urllist = []
    namelist = []
    with open("urllist.txt") as f:
        for line in f :
            urllist.append(line.split("<===>")[0])
            nameline = line.split("<===>")[1]
            nameline = nameline.replace("\n","")
            nameline = nameline.replace(" | ", "&")
            nameline = nameline.replace("|", "&")
            nameline = nameline.replace("/", "&")
            namelist.append("[" + nameline + "]")

    return urllist,namelist


if __name__ == '__main__':
    urllist,namelist = extractUrl()
    for i in range(len(urllist)):
        url = urllist[i]
        res = get_url(url)
        print(f"已获取到文章{namelist[i]}")
        file = f".\\公众号\\渗透师老A\\{namelist[i]}"
        #print(file)
        if os.path.exists(file):
            print("文件夹存在，跳过爬取")
        else:
            htmlpath= down_html(res,namelist[i])
            down_pic(res,namelist[i],htmlpath)
            time.sleep(15)

