# coding:utf-8
import time
import threading
import requests
from datetime import datetime
import re
import queue as Queue
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
        if phone_list:
            for i in phone_list:
                self.queue.put(i)
        else:
            print("目标网页获取电话失败！请检查网络。")

    def getSms(self, times="",title="",num=4):
        """
        获取验证码
        Args：
            times：验证码发送时间
            title：验证码头部标题
            num：验证码位数
        Return：验证码
        """
        obj = self.getNum()
        phone = obj["phone"].pop(0)
        if phone[0:3] != "+86":
            obj["phone"].append(phone)
            phone = obj["phone"].pop(0)
        code = ''  # 保存验证码
        tryNum = 0
        while tryNum < 5:
            try:
                resp = requests.get("https://www.pdflibr.com"+obj['url'])
                if resp.status_code == 200:
                    html = BeautifulSoup(resp.text, 'lxml')
                    tr = html.select("section:nth-of-type(2) tbody tr")
                    for i in tr:
                        timeArray = time.strptime(i.find("time").get_text(), "%Y-%m-%d %H:%M:%S")
                        timestamp = time.mktime(timeArray)
                        if timestamp>times:
                            text = re.findall(r''+title+'.*[\d]{4}', i.get_text())
                            if text:
                                code = re.findall(r'[\d]{4}',text[0])
                                if code:
                                    tryNum=6
                                    return code[0]
            except:
                tryNum += 1
                pass


smsCollect().getSms(10,"阿里巴巴")
