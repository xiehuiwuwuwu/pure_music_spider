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

class Typename(Enum):
    CHINESE = 1
    JAPANDKORE = 15
    EURANDUSE = 10
    REMIXE = 11
    PURE = 12
    DIFFERENTE = 13 

con            = pymysql.connect(host = '8.131.54.184', user = 'root', passwd = '609597441@GHQq', charset = 'utf8')             #连接数据库
cur            = con.cursor()                           #获取游标
print("connection successful！")                  #连接成功提示
cur.execute("use pure_music;")                     #使用库中pure_music表
lock = threading.Lock()

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

def spider():		#按页数抓取-基本流程 
    
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}   #linux下谷歌浏览器请求头

    for k in range(30):			#前20页   !!!改进!!!
        k                = str(k)
        url              = "https://www.hifini.com/index-" + k + ".htm"   #网站前20页的网址
        strr             = url_2_strr(url,headers)
        songid           = get_songid('thread-[1-9][0-9][0-9]*.htm',strr)

        for i in songid:
            strr2        = url_2_strr(("https://www.hifini.com/"+i))		#每一首歌曲的html转换成的文本格式

            realsong_url = get_target(' url: \'(.*?)\',',strr2)			#获取target的正则
            songNames    = get_target(' title: \'(.*?)\',',strr2)		#
            PicUrl       = get_target(' pic: \'(.*?)\'',strr2)			#
            Author       = get_target(' author:\'(.*?)\',',strr2)		#

            Realsong_url = "".join(realsong_url)
            SongNames    = "".join(songNames)
            Picurl       = "".join(PicUrl)
            AuThor       = "".join(Author)

           # remove_empty(Realsong_url,SongNames,Picurl,AuThor)
            if len(Realsong_url) == 0 and len(songNames) == 0 and len(PicUrl) == 0 and len(Author) == 0:     #剔除无效结果
                continue
     
            print("songid = " + i)
            print("www.hifini.com/" + Realsong_url)
            print("song_name = "    + SongNames)
            print("picture_url = "  + Picurl)
            print("author = "       + AuThor)
            print()

def spider_type_chinese(): 		#按类别抓取-华语歌曲

    #headers        = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}   #linux下谷歌浏览器请求头

    for page in range(30):
        headers = { "User-Agent": random.choice(user_agent)}

        page = str(page)
        chinese_url = "https://www.hifini.com/forum-1-" + page + ".htm?orderby=tid" 

    #chinese_url    = "https://www.hifini.com/forum-1-1.htm?orderby=lastpid"        #华语类别第一页url
        chinese_strr   = url_2_strr(chinese_url,headers)
        chinese_songid = get_songid('thread-([1-9][0-9][0-9]*)',chinese_strr)
        repeatnumber = 0

       # con            = pymysql.connect(host = '45.77.113.46', user = 'root', passwd = '609597441@GHQq', charset = 'utf8')             #连接数据库
       # cur            = con.cursor()                           #获取游标
       # print("connection successful！")                  #连接成功提示
       # cur.execute("use pure_music;")                     #使用库中pure_music表
    
        for i in chinese_songid:
            song_url   = "https://www.hifini.com/thread-" + i + ".htm"       
            song_strr  = url_2_strr(song_url,headers)
            songName   = get_target(' title: \'(.*?)\',',song_strr)			#可能出现空songname的情况-有id找不到name--bug
            songAuthor = get_target(' author:\'(.*?)\',',song_strr)
            songPic    = get_target(' pic: \'(.*?)\'',song_strr)
        
            if len(songName):		#剔除无效结果
                pass
            else:
                continue
            if len(songAuthor):
                pass
            else:
                continue

            songtype    = "华语"
            songtypenum = "0"                        #定义类别协议  ： 华语 = 0
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            print("ID = " + i)                                #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtype)

            j = int(i)

            lock.acquire()
            try:                                   #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                  #执行完必须提交
                print("success to commit " + song_name)       
            except:
                print("!!!error to commit " + song_name + "!!!")
                repeatnumber += 1
            finally:
                lock.release()
                print()
        if repeatnumber > 23:
           # con.close()
            return

        #con.close()                      #数据库连接关闭

def spider_type_JapAndKor():
    #headers           = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    for page in range(30):
        headers = { "User-Agent": random.choice(user_agent)}
        page = str(page)
        japAndkor_url     = "https://www.hifini.com/forum-15-" + page + ".htm?orderby=tid"
        japAndkor_strr    = url_2_strr(japAndkor_url,headers)
        japAndkor_songid  = get_songid('thread-([1-9][0-9][0-9]*)', japAndkor_strr)
        repeatnumber = 0
        for i in japAndkor_songid:
            song_url   = "https://www.hifini.com/thread-" + i + ".htm"
            song_strr  = url_2_strr(song_url,headers)
            songName   = get_target(' title: \'(.*?)\',',song_strr)                     #可能出现空songname的情况-有id找不到name--bug
            songAuthor = get_target(' author:\'(.*?)\',',song_strr)
            songPic    = get_target(' pic: \'(.*?)\'',song_strr)

            if len(songName):           #剔除无效结果
                pass
            else:
                continue
            if len(songAuthor):
                pass
            else:
                continue

            songtype    = "日韩"
            songtypenum = "1"                        #定义类别协议  ： 华语 = 0   日韩 = 1
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            print("ID = " + i)                                #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtype)

            j = int(i)
            lock.acquire()
            try:                                   #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                  #执行完必须提交
                print("success to commit " + song_name)
            except:
                print("!!!error to commit " + song_name + "!!!")
                repeatnumber += 1
            finally:
                lock.release()
                print()
            
        if repeatnumber > 18:
            
            return



def spider_type_eurAndUs():
    #headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    for page in range(30):
        headers = { "User-Agent": random.choice(user_agent)}
        page = str(page)
        eurAndUs_url     = "https://www.hifini.com/forum-10-" + page + ".htm?orderby=tid"
        eurAndUs_strr    = url_2_strr(eurAndUs_url,headers)
        eurAndUs_songid  = get_songid('thread-([1-9][0-9][0-9]*)', eurAndUs_strr)
        repeatnumber = 0
        for i in eurAndUs_songid:
            song_url   = "https://www.hifini.com/thread-" + i + ".htm"
            song_strr  = url_2_strr(song_url,headers)
            songName   = get_target(' title: \'(.*?)\',',song_strr)                     #可能出现空songname的情况-有id找不到name--bug
            songAuthor = get_target(' author:\'(.*?)\',',song_strr)
            songPic    = get_target(' pic: \'(.*?)\'',song_strr)

            if len(songName):           #剔除无效结果
                pass
            else:
                continue
            if len(songAuthor):
                pass
            else:
                continue

            songtype    = "欧美"
            songtypenum = "2"                        #定义类别协议  ： 华语 = 0   日韩 = 1   欧美 = 2
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            print("ID = " + i)                                #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtype)

            j = int(i)
            lock.acquire()
            try:                                   #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                  #执行完必须提交
                print("success to commit " + song_name)
            except:
                print("!!!error to commit " + song_name + "!!!")
                repeatnumber += 1
            finally:
                lock.release()
                print()

        if repeatnumber > 18:

            return

def spider_type_Remix():
    #headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    for page in range(30):
        headers = { "User-Agent": random.choice(user_agent)}
        page = str(page)
        remix_url     = "https://www.hifini.com/forum-11-" + page + ".htm?orderby=tid"
        remix_strr    = url_2_strr(remix_url,headers)
        remix_songid  = get_songid('thread-([1-9][0-9][0-9]*)', remix_strr)
        repeatnumber = 0
        for i in remix_songid:
            song_url   = "https://www.hifini.com/thread-" + i + ".htm"
            song_strr  = url_2_strr(song_url,headers)
            songName   = get_target(' title: \'(.*?)\',',song_strr)                     #可能出现空songname的情况-有id找不到name--bug
            songAuthor = get_target(' author:\'(.*?)\',',song_strr)
            songPic    = get_target(' pic: \'(.*?)\'',song_strr)

            if len(songName):           #剔除无效结果
                pass
            else:
                continue
            if len(songAuthor):
                pass
            else:
                continue

            songtype    = "remix"
            songtypenum = "3"                        #定义类别协议  ： 华语 = 0   日韩 = 1   欧美 = 2   remix = 3
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            print("ID = " + i)                                #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtype)

            j = int(i)
            lock.acquire()
            try:                                   #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                  #执行完必须提交
                print("success to commit " + song_name)
            except:
                print("!!!error to commit " + song_name + "!!!")
                repeatnumber += 1
            finally:
                lock.release()
                print()
            
        if repeatnumber > 18:

            return

def spider_type_pure():
    #headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    for page in range(30):
        headers = { "User-Agent": random.choice(user_agent)}
        page = str(page)
        pure_url     = "https://www.hifini.com/forum-12-" + page + ".htm?orderby=tid"
        pure_strr    = url_2_strr(pure_url,headers)
        pure_songid  = get_songid('thread-([1-9][0-9][0-9]*)', pure_strr)
        repeatnumber = 0
        for i in pure_songid:
            song_url   = "https://www.hifini.com/thread-" + i + ".htm"
            song_strr  = url_2_strr(song_url,headers)
            songName   = get_target(' title: \'(.*?)\',',song_strr)                     #可能出现空songname的情况-有id找不到name--bug
            songAuthor = get_target(' author:\'(.*?)\',',song_strr)
            songPic    = get_target(' pic: \'(.*?)\'',song_strr)

            if len(songName):           #剔除无效结果
                pass
            else:
                continue
            if len(songAuthor):
                pass
            else:
                continue

            songtype    = "pure"
            songtypenum = "4"                        #定义类别协议  ： 华语 = 0   日韩 = 1   欧美 = 2   remix = 3   纯音乐 = 4
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            print("ID = " + i)                                #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtype)

            j = int(i)
            lock.acquire()
            try:                                   #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                  #执行完必须提交
                print("success to commit " + song_name)
            except:
                print("!!!error to commit " + song_name + "!!!")
                repeatnumber += 1
            finally:
                lock.release()
                print()
            
        if repeatnumber > 18:

            return

def spider_type_different():
    #headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    for page in range(30):
        headers = { "User-Agent": random.choice(user_agent)}
        page = str(page)
        different_url     = "https://www.hifini.com/forum-13-" + page + ".htm?orderby=tid"
        different_strr    = url_2_strr(different_url,headers)
        different_songid  = get_songid('thread-([1-9][0-9][0-9]*)', different_strr)
        repeatnumber = 0
        for i in different_songid:
            song_url   = "https://www.hifini.com/thread-" + i + ".htm"
            song_strr  = url_2_strr(song_url,headers)
            songName   = get_target(' title: \'(.*?)\',',song_strr)                     #可能出现空songname的情况-有id找不到name--bug
            songAuthor = get_target(' author:\'(.*?)\',',song_strr)
            songPic    = get_target(' pic: \'(.*?)\'',song_strr)

            if len(songName):           #剔除无效结果
                pass
            else:
                continue
            if len(songAuthor):
                pass
            else:
                continue

            songtype    = "different"
            songtypenum = "5"                        #定义类别协议  ： 华语 = 0   日韩 = 1   欧美 = 2   remix = 3   纯音乐 = 4    different = 5
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            print("ID = " + i)                                #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtype)

            j = int(i)
            lock.acquire()
            try:                                   #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                  #执行完必须提交
                print("success to commit " + song_name)
            except:
                print("!!!error to commit " + song_name + "!!!")
                repeatnumber += 1
            finally:
                lock.release()
                print()
            
        if repeatnumber > 18:

            return

def spidercommon(pages,typename):
    for page in range(pages):
        headers = { "User-Agent": random.choice(user_agent)}
        page = str(page)
        #common_url = "https://www.hifini.com/forum-13-" + page + ".htm?orderby=tid"
        common_url = "https://www.hifini.com/forum-" + str(typename.value) + "-" + page + ".htm?orderby=tid"
        #print(common_url)
        common_strr = url_2_strr(common_url,headers)
        #print(common_strr)
        #return
        common_songid = get_songid('thread-([1-9][0-9][0-9]*)',common_strr)
        repeatnumber = 0
        #print(*common_songid)
        #print("1111111222222223333333") 
        for i in common_songid:
            song_url   = "https://www.hifini.com/thread-" + i + ".htm"
            song_strr  = url_2_strr(song_url,headers)
            songName   = get_target(' title: \'(.*?)\',',song_strr)                     #可能出现空songname的情况-有id找不到name--bug
            songAuthor = get_target(' author:\'(.*?)\',',song_strr)
            songPic    = get_target(' pic: \'(.*?)\'',song_strr)

            #songtype    = "different"
            songtypenum = str(typename.value)                        #定义类别协议  ： 华语 = 1   日韩 =  15  欧美 = 10   remix =  11  纯音乐= 12   different = 13
            song_name   = "".join(songName)
            song_author = "".join(songAuthor)
            song_pic    = "".join(songPic)

            if len(song_name):           #剔除无效结果
                pass
            else:
                continue
            if len(song_author):
                pass
            else:
                continue

            print("ID = " + i)                                #提供调试打印
            print("".join(songName))
            print("".join(songAuthor))
            print("".join(songPic))
            print(songtypenum)

            j = int(i)
            
            lock.acquire()
            try:                                   #添加异常抛出   执行数据库的数据插入
                cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
                con.commit()                  #执行完必须提交
                #featch = cur.fetchall()

                print("success to commit " + song_name)
            except Exception as err:
                print("!!!error to commit " + song_name + "!!!")
                #print(featch)
                print("Error %s for sql" % (err))
                fo = open("log","a") 
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

    # spider_type_chinese()
    # spider_type_JapAndKor()   
    # spider_type_eurAndUs()
    # spider_type_Remix()
    # spider_type_pure()
    # spider_type_different()

    #spidercommon(10,Typename.REMIXE)
    
    con.close()

