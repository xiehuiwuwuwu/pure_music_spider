#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import time
import datetime
import pymysql
import threading
import random
from enum import Enum
import traceback
import sys

class Typename(Enum):       #歌曲类别的枚举
    CHINESE    = 1
    JAPANDKORE = 15
    EURANDUSE  = 10
    REMIXE     = 11
    PURE       = 12
    DIFFERENTE = 13 

con            = pymysql.connect(host = '8.131.54.184', user = 'root', passwd = '*********', charset = 'utf8')             #连接数据库
cur            = con.cursor()                           #获取游标
print("connection successful！")                        #连接成功提示
cur.execute("use pure_music;")                          #使用库中pure_music表
lock           = threading.Lock()                       #使用线程锁

user_agent = [  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"  ,  "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]


def url_2_strr(s,header=''):		#url网址转换成文本格式   #添加请求头header防止初步反爬
    html = requests.get(s,header)
    strr = html.text
    return strr

def get_songid(regular,strr):		#在首页的url获取歌曲的ID
    songid = re.findall(regular,strr)
    songid = set(songid)
    return songid

def get_target(regular,strr):		#通过正则表达式获取target
    target = re.findall(regular,strr,re.S)
    return target

def spidercommon(pages,typename):       #抓取流程 参数：pages--指定爬取页数（int)   typename--指定爬取的歌曲类型（enum）
    for page in range(pages):
        headers         = { "User-Agent": random.choice(user_agent)}
        page            = str(page)
        common_url      = "https://www.hifini.com/forum-" + str(typename.value) + "-" + page + ".htm?orderby=tid"
        common_strr     = url_2_strr(common_url,headers)
        common_songid   = get_songid('thread-([1-9][0-9][0-9]*)',common_strr)
        repeatnumber    = 0 
        for i in common_songid:
            song_url    = "https://www.hifini.com/thread-" + i + ".htm"
            song_strr   = url_2_strr(song_url,headers)
            songName    = get_target(' title: \'(.*?)\',',song_strr)                     #可能出现空songname的情况-有id找不到name--bug
            songAuthor  = get_target(' author:\'(.*?)\',',song_strr)
            songPic     = get_target(' pic: \'(.*?)\'',song_strr)

            songtypenum = str(typename.value)                        #定义类别协议  ： 华语 = 1   日韩 =  15  欧美 = 10   remix =  11  纯音乐= 12   different = 13
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            if len(song_name):                            #剔除无效结果
                pass
            else:
                continue
            if len(song_author):
                pass
            else:
                continue

            print("ID = " + i)                            #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtypenum)

            j = int(i)
            
            lock.acquire()
            try:                                          #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                              #执行完必须提交
                print("success to commit " + song_name)
            except Exception as err:
                print("!!!error to commit " + song_name + "!!!")
                print("Error %s for sql" % (err))
                fo = open("log","a")                       #log文件写入
                fo.write(str(err) + song_name + "\n")
                fo.close()
                repeatnumber += 1
            finally:
                lock.release()
                print()
        if repeatnumber > 27:
            return

if __name__ == '__main__':
    t1 = threading.Thread(target=spidercommon, args=(10,Typename.CHINESE))
    t2 = threading.Thread(target=spidercommon, args=(10,Typename.JAPANDKORE))
    t3 = threading.Thread(target=spidercommon, args=(10,Typename.REMIXE))
    t4 = threading.Thread(target=spidercommon, args=(10,Typename.EURANDUSE))
    t5 = threading.Thread(target=spidercommon, args=(10,Typename.PURE))
    t6 = threading.Thread(target=spidercommon, args=(10,Typename.DIFFERENTE))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    con.close()

