# -*- coding: utf-8 -*-
# @File  : VqqSpider.py 
# @Author: kimoto
# @Date  : 2019/5/9
# @Desc  : 腾讯视频爬虫半成品

import os
import requests
import shutil
from multiprocessing import Lock,Pool

s = ""
url = "https:/"
path = os.path.join(os.getcwd(), "vs")
respath = os.path.join(os.getcwd(), "res")
headers = {
    "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}

def cmb(path, name):
    #files = os.listdir(path)
    _from = os.path.join(path, )
    exec = r"copy/b " + os.path.join(os.getcwd(), path) + r"\*.ts " + respath + r"\{}.mp4"
    print(exec)

def download(url, path):

    for i in range(1, 60):
        req_url = url + "{}.ts".format(i)
        #print(req_url)
        name = "{}.ts".format(str(i).zfill(0))
        resp = requests.get(req_url)
        print(resp.status_code)
        if(resp.status_code == 200):
            with open(os.path.join(path, name), 'wb') as movie_content:
                movie_content.writelines(resp)
        else:
            break



def downloads(resp, name):
    with open(os.path.join(path, name), 'wb') as movie_content:
        movie_content.writelines(resp)
    print(name + " is download")

if __name__ == '__main__':

    with open("url.txt", "r") as f:
        s = str(f.read())
        f.close()

    baseurl = s.split("?")[0]
    tmp = baseurl.split(".ts")[0]
    url = tmp[0: len(tmp)-1]


    if(os.path.exists(path)):
        shutil.rmtree(path)
    os.makedirs(path)

    if(os.path.exists(respath) == False):
        os.makedirs(respath)

    print("正在下载缓存...")
    pool = Pool(processes=15)

    i=1
    while(True):
        req_url = url + "{}.ts".format(i)
        name = "{}.ts".format(str(i).zfill(6))
        resp = requests.get(req_url, headers=headers)
        i += 1
        if(resp.status_code==200):
            pool.apply_async(downloads, (resp, name))
        else:
            break

    res = os.path.join(respath, "new.mp4")
    exec = r"copy/b " + os.path.join(path, "*.ts") + " " + res
    print(exec)
    os.system(exec)
    print("下载完成")

"""
    download(url, path)

    res = os.path.join(respath, "new.mp4")
    exec = r"copy/b " + os.path.join(path, "*.ts") + " " + res
    print(exec)
    os.system(exec)
    print("下载完成")
"""