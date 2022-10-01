import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import re

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

def getCookie():
    # 调用谷歌浏览器驱动
    driver = webdriver.Chrome()
    driver.get("https://mp.weixin.qq.com/")
    driver.find_element(by=By.LINK_TEXT, value="使用帐号登录").click()
    driver.find_element(by=By.NAME, value="account").clear()
    # 公众号的账号
    driver.find_element(by=By.NAME, value="account").send_keys("L542387046@163.com")
    time.sleep(2)
    driver.find_element(by=By.NAME, value="password").clear()
    driver.find_element(by=By.NAME, value="password").send_keys("L542387046")
    driver.find_element(by=By.CLASS_NAME, value="icon_checkbox").click()

    time.sleep(2)
    driver.find_element(by=By.CLASS_NAME, value="btn_login").click()
    time.sleep(15)
    # 此时会弹出扫码页面，需要微信扫码
    cookies = driver.get_cookies()  # 获取登录后的cookies
    #print(cookies)
    cookie = {}
    for items in cookies:
        cookie[items.get("name")] = items.get("value")
    return cookie

def getToken(cookie):
    url = "https://mp.weixin.qq.com/"
    res = requests.get(url,proxies=proxies,headers=headers,cookies=cookie)

    token = re.findall(r'token=(\d+)', str(res.text))[0]
    return token

if __name__ == '__main__':
    cookie=getCookie()
    with open('cookies.txt', "w")as file:
        file.write(json.dumps(cookie))

    token=getToken(cookie)
    print(token)






