# coding:utf-8
import requests
from lxml import html
import base
import json
import threading

# 获取主页列表
def getPage(baseUrl):
    headers = {
        'referer': 'https://www.mzitu.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    }
    selector = html.fromstring(requests.get(baseUrl, headers=headers, verify=False).content)

    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(i)
    return urls


# 图片链接列表，标题
# url是详情页链接
def getPiclink(url):
    headers = {
        'referer': 'https://www.mzitu.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    }
    sel = html.fromstring(requests.get(url, headers=headers, verify=False).content)
    # 图片总数 倒数第二项里
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]

    # 接下来的链接放到这个列表
    jpgList = []
    print("===》"+url)
    for i in range(int(total)):
        # 每一页
        link = '{}/{}'.format(url, i+1)
        headers = {
            'referer': 'https://www.mzitu.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
        s = html.fromstring(requests.get(link, headers=headers, verify=False).content)
        # 图片地址在src标签中
        jpg = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        # 图片链接放进列表
        jpgList.append(jpg)

    return title, json.dumps(jpgList), jpgList[0]

def getContent(baseUrl):
    urls = getPage(baseUrl)
    alllist = []
    for url in urls:
        res = {}
        res['aid'] = url.split('/')[3]
        res['title'], res['piclist'], res['thumb'] = getPiclink(url)
        alllist.append(res)
    base.setPics(alllist)

def start(begin, end):
    print(begin, end)
    while begin < end:
        baseUrl = 'https://www.mzitu.com/page/' + str(begin)
        getContent(baseUrl)
        print("正在下载第" + str(i) + "页。。。")
        begin += 1


if __name__ == '__main__':
    start(1, 10)
    # i = 0
    # while i <= 10:
    #     begin = i * 10 + 1
    #     end = (i+1) * 10
    #     t = threading.Thread(target=start, args=(begin, end), name='线程'+str(i))
    #     t.start()
    #     t.join()
    #     i+=1

