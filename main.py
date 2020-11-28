#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import time
import datetime
import pymysql

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

    for k in range(20):			#前20页   !!!改进!!!
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

    headers        = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}   #linux下谷歌浏览器请求头

    chinese_url    = "https://www.hifini.com/forum-1-1.htm?orderby=lastpid"        #华语类别第一页url
    chinese_strr   = url_2_strr(chinese_url,headers)
    chinese_songid = get_songid('thread-([1-9][0-9][0-9])*',chinese_strr)

    con            = pymysql.connect(host = '45.77.113.46', user = 'root', passwd = '609597441@GHQq', charset = 'utf8')             #连接数据库
    cur            = con.cursor()                           #获取游标
    print("connection successful！")                  #连接成功提示
    cur.execute("use pure_music;")                     #使用库中pure_music表
    
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

        try:                                   #添加异常抛出   执行数据库的数据插入
            cur.execute("INSERT INTO music_table(music_id,song_name,author,pic_url,type) VALUES(%s,%s,%s,%s,%s)",(j,song_name,song_author,song_pic,songtypenum))
            con.commit()                  #执行完必须提交
            print("success to commit " + song_name)       
        except:
            print("!!!error to commit " + song_name + "!!!")
        print()

    con.close()                      #数据库连接关闭

def spider_type_JapAndKor():
    headers           = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'} 
    
    japAndkor_url     = "https://www.hifini.com/forum-15-1.htm?orderby=lastpid"
    japAndkor_strr    = url_2_strr(japAndkor_url,headers)
    japAndkor_songid  = get_songid('thread-[1-9][0-9][0-9]*', japAndkor_strr)   	
    print(*japAndkor_songid)

if __name__ == '__main__':
    spider_type_chinese()   
