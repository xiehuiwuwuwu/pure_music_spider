#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import time

#songKey     = []  #存放歌曲key（url相关）
songNames   = []  #存放歌曲名称
Author      = []  #存放歌手名称
 
for k in range(20):
  
  k       = str(k)
  url     = "https://www.hifini.com/index-" + k + ".htm"   #网站前20页的网址
  html    = requests.get(url)    #网页的html
  strr    = html.text 	
  pat1    = 'thread-......htm'     #获取ID的正则 

  song_id = re.findall(pat1,strr)   	#前20页所有歌曲的ID
  song_id = set(song_id)

  for i in song_id:
      song_html      = requests.get("https://www.hifini.com/"+i)	#拼接成歌曲的html
      strr2          = song_html.text
      realsong_url   = re.findall(' url: \'(.*?)\',',strr2,re.S)    #获取歌曲URL的正则
      songNames      = re.findall(' title: \'(.*?)\',',strr2,re.S)	 #获取歌曲名的正则
      PicUrl         = re.findall(' pic: \'(.*?)\'',strr2,re.S) 	#获取图片URL的正则
      Author         = re.findall(' author:\'(.*?)\',',strr2,re.S) 	 #获取歌手名的正则
    
      Realsong_url   = "".join(realsong_url)
      SongNames      = "".join(songNames)
      Picurl         = "".join(PicUrl)
      AuThor         = "".join(Author)
   
      print("www.hifini.com/" + Realsong_url)
      print("song_name = "    + SongNames)
      print("picture_url = "  + Picurl)
      print("author = "       + AuThor) 
      print()
        
