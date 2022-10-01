import json
import time

import requests
from wxgzh import wechatlogin

'''
1.先获取公众号所有的url
2.多线程爬取，保存在列表中
3.分别保存在html文件里
'''

headers={
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive'
    }
proxies ={
        'http': 'http://127.0.0.1:4780',
        'https': 'http://127.0.0.1:4780'  # https -> http
    }

def list_url(url):
    with open("cookies.txt", "r") as file:
        cookie = file.read()
    cookies = json.loads(cookie)

    token = wechatlogin.getToken(cookies)
    print(token)

    urllist = []

    with open("urllist.txt","r") as files:
        pages = len(files.readlines()) / 4


    sum = int(input("输入你要爬取的页数:")) #10 #1
    print(f"当前已经爬取到的页码为{pages},建议您从{pages + 1}开始爬取 \n")
    itm = int(input("输入你要开始爬取的页数:")) #11 #1
    item1 =sum +itm
    print("建议下一次从页数:"+ str(item1) + "开始爬取")
    sum = itm + sum - 1  #20 #1
    for i in range(itm-1,sum): #10~19
        item = (i) * 4
        newUrl = url + token + f"&lang=zh_CN&f=json&ajax=1&begin={item}"
        urllist.append(newUrl)
    return urllist

def get_url(url):

    with open("cookies.txt", "r") as file:
        cookie = file.read()
    cookies = json.loads(cookie)
    #urlres = [] #把页面的回显整合到列表里
    #cookie = {'slave_sid': 'R1lkazc0alpyOHlmb1IyWUxFNkxfTjhuNkRwaHNsYVhsMnNCOU1pR3RBd1hRSTcyM3Z5aFpMM3BsTXNqSlFyVWd1czBkUWtfVFZNaTVvSVlNR200eTVXSUNXSXFaMk5pSjhvVExBc0V2VjIzYnJnSWZocGZjZEFGWDFSOHhROTgyeExOaXVDNE91M3RhMnhq', 'openid2ticket_oLhmswKOf_Sdjo5G5y-x74bCZid0': 'hTm4QKLKy4g6fkWoy0XseFqME+c792pn9nIw0BP9IyQ=', 'remember_acct': 'L542387046%40163.com', 'data_ticket': 'FuVBeWdLTxuh0Tlc02NhaUYgC4CAlLb0WkXSQ4vBvxx5O5xDtNsnOXNjIE1oZe2v', 'uuid': 'cfa0d8ae9b621af4bf444d1f1b504244', 'cert': 'hkRSbIdjJZayCOxRlrQUGqY3uHbjnX4W', 'mm_lang': 'zh_CN', 'ticket_id': 'gh_b07b7a390189', 'slave_bizuin': '3232504110', '_clck': '3232504110|1|f5a|0', 'wxuin': '64466587119491', 'data_bizuin': '3232504110', 'noticeLoginFlag': '1', 'slave_user': 'gh_b07b7a390189', 'ticket': 'dc5264f8e35abfca8f291e1f9770041b61ea8a90', 'bizuin': '3232504110', 'rand_info': 'CAESIBP4rcgyT5g3BqeplnYYb40z6+Grntys/StpU5EGkXPQ', 'xid': 'b7017ce714240ab2dc550409ce66f279', 'ua_id': 'Fk04fh0o9nFKkqVWAAAAAK6NauARDiQ537COQt8IxjQ='}

    res = requests.get(url=url,headers=headers,proxies=proxies,cookies=cookies)

    return res

def listUrl(wxJson):
    urlList = []
    urlTitle = []
    urldetile=[]
    for i in range(4):
        urlList.append(wxJson['app_msg_list'][i]['link'])
        urlTitle.append(wxJson['app_msg_list'][i]['title'])

    urldetile.append(urlList)
    urldetile.append(urlTitle)
    return urldetile

def find_html(urldetile):
    urlList=urldetile[0]
    urlHtml = []
    for item in urlList:
        res= requests.get(item,headers=headers,proxies=proxies)
        urlHtml.append(res)
    return urlHtml

def down_html(urlHtml,urldetile):
    urlTitle = urldetile[1]
    for item in range(len(urlHtml)):
        with open('C:\\Users\\林泽兴\\Desktop\\jav\\wechat\\'+urlTitle[item]+'.html','wb+')as f:
            f.write(urlHtml[item].content)

def wite_url(urldetile):
    title = urldetile[0]
    urllist = urldetile[1]
    with open('urllist.txt', 'a')as file:
        for item in range(4):
            file.write(title[item]+"<===>"+urllist[item])
            file.write("\n")


def main():
    url=input("输入你要爬取的微信公众号:")

    urllist = list_url(url)
    for item in urllist:
        time.sleep(15)
        res = get_url(item)
        print(res.text)
        wxJson = json.loads(res.text)
        urldetile = listUrl(wxJson)
        wite_url(urldetile)
        #urlHtml=find_html(urldetile)
        #down_html(urlHtml,urldetile)
        print(urldetile)


if __name__ == '__main__':
    main()