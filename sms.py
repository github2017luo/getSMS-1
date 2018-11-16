# coding:utf-8
import time
import threading
import requests
from six.moves import queue as Queue
from bs4 import BeautifulSoup

PHONE = Queue.Queue()  # 手机号码队列

# def aaa(i):
#     time.sleep(5)
#     PHONE.put(i)

# def bbb():
#     print(PHONE.get())

# PHONE.put(1)
# PHONE.put(2)
# PHONE.put(3)
# PHONE.put(4)

# threading.Thread(target=bbb,name="a").start()
# threading.Thread(target=bbb,name="b").start()
# threading.Thread(target=bbb,name="c").start()
# threading.Thread(target=bbb,name="d").start()
# threading.Thread(target=aaa, args=(1,),name="e").start()
# threading.Thread(target=aaa,args=(5,),name="f").start()
# threading.Thread(target=bbb,name="g").start()
# threading.Thread(target=bbb,name="h").start()


def getPhoneNum():
    phone_list = {}
    try:
        resp = requests.get("https://www.pdflibr.com/")
        if resp.status_code == 200:
            html = BeautifulSoup(resp.text, 'lxml')
            phone_row = html.select("div.sms-number-list.row")
        for n in phone_row:
            phone = n.find("h3").get_text()
            url = n.find("a").get("href")
            if url in phone_list:
                phone_list[url]["phone"].append(phone)
            else:
                phone_list[url] = {"url": url, "phone": [phone]}
        phone_list = list(phone_list.values())
    except:
        pass
    return phone_list


class smsCollect(object):

    def __init__(self):
        self.queue = Queue.Queue()
        self.setNum()

    def getNum(self):
        num = self.queue.get()
        return num

    def setNum(self):
        phone_list = getPhoneNum()
        if not phone_list:
            for i in phone_list:
                self.queue.put(i)
        else:
            print("目标网页获取电话失败！请检查网络。")
