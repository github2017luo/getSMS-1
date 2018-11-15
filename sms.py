import time
import threading
import requests
from six.moves import queue as Queue
from bs4 import BeautifulSoup

PHONE = Queue.Queue()  # 手机号码队列

# PHONE.put({"url": "111", "phone": [1111, 2222]})
# a = PHONE.get()
# print(a["num"][0])


def getPhoneNum():
    try:
        list={};
        resp = requests.get("https://www.pdflibr.com/")
        if resp.status_code == 200:
            html = BeautifulSoup(resp.text,'lxml')
            phone_list = html.select("div.sms-number-list.row")
        for n in phone_list:
            phone=n.find("h3").get_text()
            url=n.find("a").get("href")
            list[url]={"url": url, "phone": []}
             
# value_list = list(a.values())
        for n in list:
            print("1")
    except:
        # try again
        pass

getPhoneNum()
