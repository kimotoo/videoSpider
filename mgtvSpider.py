# -*- coding: utf-8 -*-
# @File  : mgtvSpider.py 
# @Author: kimoto531
# @Date  : 2020/4/19
# @Desc  : mgtvSpider v1.0 用于抓取mgtv视频

import  requests
import time
import json
import os

headers = {
    "Cookie" : "PM_CHKID=692f948edad34535;uuid=c46791129007e565a1cc14538cdf2fdc; loginAccount=kezhao754%40sogou.com; vipStatus=1",
    "User-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Referer" : "https://www.mgtv.com/b/334727/7919446.html?fpa=15801&fpos=3&lastp=ch_home"
}

video_id = "7919446"
tk2 = "5gzM1YjM3gTNx0Ddpx2Y8FDMzAjLz4CM9IXZ2xHMzATM98mbwxXY1MmMjFWZzUWYiFTLkJDMh1SM1QGNtUDN3IWL1QjZykzY4QTPklGZ"
suuid = "c08d0d51-dd6d-4ce7-963c-5d6833beaed0"

def parseURL(url):
    """
    :param url: https://pcweb.api.mgtv.com/player/video?did=48c92f45-b745-4d51-a02d-1bae3eac2c5a
                    &suuid=a140cbbf-c035-4757-bae1-f373b094bbb6&cxid=
                    &tk2=5ITM4YjM3gTNx0Ddpx2Y8FDMzAjLz4CM9IXZ2xHMzATM98mbwxXY1MmMjFWZzUWYiFTLkJDMh1SM1QGNtUDN3IWL1QjZykzY4QTPklGZ
                    &video_id=7919446&type=pch5&_support=10000000&auth_mode=1&callback=jsonp_1587268129029_58427
    :return: video_id, tk2, suuid
    """



def GetM3u8(video_id, tk2, suuid):

    pm2_url = "https://pcweb.api.mgtv.com/player/video?suuid={}&video_id={}&tk2={}".format(suuid, video_id, tk2)
    pm2Data = requests.get(pm2_url, headers=headers).json()
    pm2 = pm2Data["data"]["atc"]["pm2"]
    getSource_url = "https://pcweb.api.mgtv.com/player/getSource?video_id={}&tk2={}&pm2={}".format(video_id, tk2, pm2)
    sourceData = requests.get(getSource_url, headers=headers).json()
    items = sourceData["data"]["stream"]
    for item in items:
        if(item["url"] != ""):
            atcl_url = "https://web-disp.titan.mgtv.com/{}".format(item["url"])
    #print(atcl_url)
    atclData = requests.get(atcl_url, headers=headers).json()
    #print(atclData)
    m3u8_url = atclData["info"]
    #print(m3u8_url)
    return m3u8_url

def parseM3u8(m3u8_url):

    m3u8Data = requests.get(m3u8_url, headers=headers).text
    #print(m3u8Data)
    head = m3u8_url.split("mp4")[0]+"mp4/"
    urls = []
    lines = m3u8Data.split()
    #print(lines)
    for line in lines:
        if(line.startswith("#")):
            continue
        print(head+line)
        urls.append(head+line)

    if(len(urls) != 0):
        return urls

def download_ts(urls, ts_path):

    if(os.path.exists(ts_path)==False):
        os.mkdir(ts_path)
    i=0
    print("正在下载ts...")
    for url in urls:
        try:
            resp = requests.get(url, headers=headers)
            file_name = os.path.join(ts_path, str(i).zfill(6))
            with open(ts_path, "wb") as ts_content:
                ts_content.writelines(resp)
        except:
            print("下载ts时出错：{}".format(Exception))


