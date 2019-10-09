### 美桌 cosplay区图片

import requests
from lxml import html
import base
import json
import threading
import os
import time
import hashlib

def getHtml(url):
    headers = {
        'User-Agent': "PostmanRuntime/7.13.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "756784cd-83b1-4e9f-948e-0c10167c05cb,da8188be-dbb6-4e09-ab1c-7d10ca54216d",
        'Host': "www.win4000.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    selector = html.fromstring(requests.get(url, headers=headers, verify=False).content)
    return selector

# 获取主页列表
def start(baseUrl):
    selector = getHtml(baseUrl)
    childList = selector.xpath('//div[@class="list_cont Left_list_cont  Left_list_cont2"]//ul/li/a/@href')
    titleList = selector.xpath('//div[@class="list_cont Left_list_cont  Left_list_cont2"]//ul/li/a/img/@title')
    thumbList = selector.xpath('//div[@class="list_cont Left_list_cont  Left_list_cont2"]//ul/li/a/img/@src')

    for key, childUrl in enumerate(childList):
        parentNode = {}
        parentNode['title'] = titleList[key]
        parentNode['thumb'] = thumbList[key]
        # 获取该链接下所有图片
        piclist = getContent(childUrl)
        parentNode['piclist'] = json.dumps(piclist)
        insertData = [parentNode]
        base.setPics(insertData, 9)
        downloadPic(parentNode['title'], piclist)
    print("已完成。。。。。")



def getContent(baseUrl):
    k = 10
    baseUrl = baseUrl[:-5]
    piclist = []
    while True:
        url = baseUrl + '_' + str(k) + '.html'
        selector = getHtml(url)
        piclink = selector.xpath('//div[@id="pic-meinv"]/a/img/@url')
        if len(piclink) <= 0:
            break
        piclist.append(piclink[0])
        k += 1
        time.sleep(0.2)

    return piclist


def downloadPic(title, piclist):
    k = 1
    # 存放路径
    dirPath = os.getcwd()+"/images/"
    hl = hashlib.md5()
    hl.update(title.encode(encoding='utf-8'))
    dirName = hl.hexdigest()
    dirName = dirPath + dirName
    # 新建文件夹

    if not os.path.isdir(dirName):
        os.makedirs(dirName)

    for picurl in piclist:
        # 文件写入的名称：当前路径／文件夹／文件名
        filename = '%s/%s.jpg' % (dirName, k)
        print(u'开始下载图片:%s 第%s张' % (title, k))

        with open(filename, "wb") as jpg:
            jpg.write(requests.get(picurl).content)
            time.sleep(0.5)
        k += 1


if __name__ == '__main__':
    k = 2
    while k < 5:
        url = 'http://www.win4000.com/meinvtag26_'+str(k)+'.html'
        start(url)
        k += 1


