#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import time

#songKey     = []  #存放歌曲key（url相关）
songNames   = []  #存放歌曲名称
Author      = []  #存放歌手名称

def url_2_strr(s):
    html = requests.get(s)
    strr = html.text
    return strr

def get_songid(regular,strr):
    songid = re.findall(regular,strr)
    songid = set(songid)
    return songid

def get_target(regular,strr):
    target = re.findall(regular,strr,re.S)
    return target

def spider():
    songid = []
    for k in range(20):
        k       = str(k)
        url     = "https://www.hifini.com/index-" + k + ".htm"   #网站前20页的网址
        strr = url_2_strr(url)
        songid  = get_songid('thread-......htm',strr)

        for i in songid:
            strr2 = url_2_strr(("https://www.hifini.com/"+i))

            realsong_url = get_target(' url: \'(.*?)\',',strr2)
            songNames = get_target(' title: \'(.*?)\',',strr2)
            PicUrl = get_target(' pic: \'(.*?)\'',strr2)
            Author = get_target(' author:\'(.*?)\',',strr2)

            Realsong_url   = "".join(realsong_url)
            SongNames      = "".join(songNames)
            Picurl         = "".join(PicUrl)
            AuThor         = "".join(Author)


            print("www.hifini.com/" + Realsong_url)
            print("song_name = "    + SongNames)
            print("picture_url = "  + Picurl)
            print("author = "       + AuThor)
            print()

if __name__ == '__main__':
    spider()       
