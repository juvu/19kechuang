# -*- coding:utf-8 -*-
AV_URL = r"https://www.bilibili.com/video/av{}"
PATH_TITLE = "//div[@id='viewbox_report']/h1/@title"
PATH_CLASS1 = "//span[@class='a-crumbs']/a/text()"
PATH_CLASS2 = "//span[@class='a-crumbs']/a[2]/text()"
# PATH_TIME = "//span[@class='a-crumbs']/following-sibling::span[1]/text()"
PATH_TIME = "//div[@class='video-data']/span[2]/text()"
PATH_RANK = "//div[@class='video-data']/span[3]/text()"
A_URL = r"https://api.bilibili.com/archive_stat/stat?aid={}"
PATH_DATA = "/html/body/pre/text()"
PATH_UID = "//a[@class='username is-vip']/@href"
RE = r"\"pages\"\:\[\{\"cid\":(.*?)\," # "pages":[{"cid":.*?,}] # .匹配任意字符
COMMENT_URL = "https://comment.bilibili.com/{}.xml"
D_NAME=["text", # 弹幕文本
    "second", # 弹幕出现的时间，单位为秒
    "mode", # 123滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕
    "size", # 字号 12非常小, 16特小, 18小, 25中, 36大, 45很大, 64特别大
    "color", # 颜色，以HTML颜色的十进制为准
    "time", # Unix格式的时间戳 基准时间为 1970-1-1 08:00:00
    "pool", # 弹幕池 0普通池 1字幕池 2特殊池（目前特殊池为高级弹幕专用
    "u_id", # 发送者id 用于“屏蔽此弹幕的发送者”功能
    "id", # 弹幕数据库中id 用于“历史弹幕”功能
    ]

AGENTPOOL_URL = r"http://lab.crossincode.com/proxy/get/?num=20&head=https"
USER_AGENT_LIST = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

import requests
from lxml import etree
import re
import json
import random

def getProxiesList():
    res = requests.get(url = AGENTPOOL_URL)
    res.encoding = 'utf-8'
    data1 = res.json()
    data = data1['proxies']
    proxies_list = [each['https'] for each in data]
    return proxies_list

class Bili(object):
    def __init__(self, av_id):
        self.av_id = av_id
        self.title = None # 标题
        self.class1 = None # 类别1
        self.class2 = None # 类别2
        self.time = None # 视频发布时间
        self.rank = None # 排行
        self.data = None
        self.cid = None
        self.d = None
        self.headers = None
        self.proxies = None
        global PROXIES_LIST

    def parse(self, url): # 获取HTML
        response = requests.get(url=url, headers=self.headers, proxies=self.proxies, verify=False)
        res = response.content.decode()
        return res

    def renewRequests(self):
        self.headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
        global PROXIES_LIST
        flag = True
        while(flag):
            try:
                t = random.choice(PROXIES_LIST)
                # self.proxies = {"http": "http://"+t, "https": "https://"+t}
                self.proxies = {"https": "https://"+t}
                requests.get("https://wenshu.court.gov.cn/", proxies=self.proxies)
                flag = False
            except requests.exceptions.ConnectionError as e:
                print(t,'ProxiesError:', e.args)
        return

    def getInfo(self, res): # 获取标题、类别
        html = etree.HTML(res) # 自动补全
        title = html.xpath(PATH_TITLE)[0]
        class1 = html.xpath(PATH_CLASS1)[0]
        class2 = html.xpath(PATH_CLASS2)[0]
        time = html.xpath(PATH_TIME)[0]
        rank = html.xpath(PATH_RANK)[0][2:] # 去除两个空格
        uid = html.xpath(PATH_UID)[0][21:]
        return (title, class1, class2, time, rank, uid)
        #class2 = html.xpath(PATH_CLASS2)[0]
        #return (title, class1, class2)

    def getData(self): # 获取总播放量、历史累计弹幕数、回复数、收藏数、硬币数、分享数、现在排名、历史最高排名、喜欢数、不喜欢数、版数、版权
        a_url = A_URL.format(self.av_id)
        data = requests.get(url = a_url, headers=self.headers, proxies=self.proxies, verify=False).json()["data"]
        return data

    def getCid(self, res): #获取Cid
        cid = re.findall(RE, res, re.S)[0]
        return cid

    def getDannmaku(self, res): #获取弹幕
        html = etree.HTML(res)
        text = html.xpath('//d/text()')
        infos = html.xpath('//d/@p')
        info = [i.split(',') for i in infos]
        d = [dict(zip(D_NAME,[x]+y)) for x,y in zip(text,info)]
        return d

    def save(self, name, content):
        with open("{}.json".format(name),"w",encoding="utf-8")as f:
            f.write(json.dumps(content,ensure_ascii=False,indent=4))
        print("Save Successful! ")

    def run(self):
        # 0 配置头、代理等
        global PROXIES_LIST
        self.renewRequests()
        # 1 获取html
        av_url = AV_URL.format(self.av_id)
        res = self.parse(av_url) # HTML
        # 2 提取info和cid
        (self.title, self.class1, self.class2, self.time, self.rank, self.uid) = self.getInfo(res)
        if (self.title==None):
            print("Title NOT FOUND")
            return
        self.cid = self.getCid(res)
        self.data = self.getData()
        # 3 获取弹幕
        comment_url = COMMENT_URL.format(self.cid)
        res_d = self.parse(comment_url).encode() # 弹幕的HTML
        # 4 提取
        self.d = self.getDannmaku(res_d)
        # 5 保存
        name = "{}".format(self.av_id)
        s = {"title":self.title, "class1":self.class1, "class2":self.class2, "time":self.time, "rank":self.rank, "uid":self.uid, "data":self.data, "av_id":self.av_id, "cid":self.cid, "d":self.d}
        self.save(name, s)

def main():
    # av_id = input('Please input an av id: ')  # 视频地址
    global PROXIES_LIST
    PROXIES_LIST = getProxiesList()
    av_id_list = {'21351430', '50311584'}
    for av_id in av_id_list:
        b = Bili(av_id)
        b.run()

main()
