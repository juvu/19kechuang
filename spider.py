# -*- coding:utf-8 -*-


from myrequest import get
from lxml import etree
import re
import json
import time


def getInfo(res): # 获取标题、类别
    html = etree.HTML(res) # 自动补全
    PATH_TITLE = "//div[@id='viewbox_report']/h1/@title"
    title = html.xpath(PATH_TITLE)[0]
    PATH_CLASS1 = "//span[@class='a-crumbs']/a/text()"
    class1 = html.xpath(PATH_CLASS1)[0]
    PATH_CLASS2 = "//span[@class='a-crumbs']/a[2]/text()"
    class2 = html.xpath(PATH_CLASS2)[0]
    PATH_TIME = "//div[@class='video-data']/span[2]/text()"
    time = html.xpath(PATH_TIME)[0]
    PATH_RANK = "//div[@class='video-data']/span[3]/text()"
    try:
        rank = html.xpath(PATH_RANK)[0][2:] # 去除两个空格
    except:
        rank = ''
    PATH_UID = "//div[@class='name']/a/@href"
    # html.xpath(PATH_UID)
    uid = html.xpath(PATH_UID)[0][21:]
    return (title, class1, class2, time, rank, uid)

def getCid(res): #获取Cid
    RE_CID = r"\"pages\"\:\[\{\"cid\":(.*?)\," # "pages":[{"cid":.*?,}] # .匹配任意字符
    cid = re.findall(RE_CID, res, re.S)[0]
    return cid

def getDannmaku(res): #获取弹幕
    html = etree.HTML(res)
    PATH_TEXT = '//d/text()'
    text = html.xpath(PATH_TEXT)
    PATH_INFOS = '//d/@p'
    infos = html.xpath(PATH_INFOS)
    info = [i.split(',') for i in infos]
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
    d = [dict(zip(D_NAME, [x]+y)) for x, y in zip(text, info)]
    return d

def save(name, content):
    with open("{}.json".format(name), "w", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False, indent=4))

def run(av_id):
    # 获取视频页面的html
    AV_URL = r"https://www.bilibili.com/video/av{}"
    av_url = AV_URL.format(av_id)
    res = get(av_url) # HTML
    # 1 提取info和cid
    (title, class1, class2, time, rank, uid) = getInfo(res)
    if (title==None):
        print("Title NOT FOUND")
        return
    cid = getCid(res)
    # 获取api页面的html
    # 2 获取总播放量、历史累计弹幕数、回复数、收藏数、硬币数、分享数、现在排名、历史最高排名、喜欢数、不喜欢数、版数、版权
    A_URL = r"https://api.bilibili.com/archive_stat/stat?aid={}"
    a_url = A_URL.format(av_id)
    data = get(a_url, decode=False).json()["data"]
    # 获取comment
    COMMENT_URL = "https://comment.bilibili.com/{}.xml"
    comment_url = COMMENT_URL.format(cid)
    res_d = get(comment_url, decode=False).content # 弹幕的HTML
    # 3 获取弹幕
    d = getDannmaku(res_d)
    # 4 保存
    name = "{}".format(av_id)
    s = {"title":title, "class1":class1, "class2":class2, "time":time, "rank":rank, "uid":uid, "data":data, "av_id":av_id, "cid":cid, "d":d}
    save(name, s)
    print("{} Save Successful! ".format(av_id))

def main(av_list):
    av_id_list = [x if x[0].isdigit() else x[2:] for x in av_list]
    for av_id in av_id_list:
        run(av_id)
        time.sleep(5)
