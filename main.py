#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import time

def url_2_strr(s):		#url网址转换成文本格式
    html = requests.get(s)
    strr = html.text
    return strr

def get_songid(regular,strr):		#在首页的url获取歌曲的ID
    songid = re.findall(regular,strr)
    songid = set(songid)
    return songid

def get_target(regular,strr):		#通过正则表达式获取target
    target = re.findall(regular,strr,re.S)
    return target

def spider():		#基本流程
    for k in range(20):			#前20页   !!!改进!!!
        k                = str(k)
        url              = "https://www.hifini.com/index-" + k + ".htm"   #网站前20页的网址
        strr             = url_2_strr(url)
        songid           = get_songid('thread-......htm',strr)

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
     

            print("www.hifini.com/" + Realsong_url)
            print("song_name = "    + SongNames)
            print("picture_url = "  + Picurl)
            print("author = "       + AuThor)
            print()

if __name__ == '__main__':
    spider()       
