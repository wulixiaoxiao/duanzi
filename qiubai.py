import requests
from pyquery import PyQuery as pq
import db
import time

baseUrl = 'https://www.qiushibaike.com'

def getContent(url):
    data = pq(url)
    data = data('.recommend-article')
    data = data('ul li')
    listlen = data.length
    print(listlen)
    i = 0
    duanzilist = []
    replayList = []
    while i < listlen:
        try:
            newdata = {}
            now_data = pq(data[i])

            # 链接
            newdata['url'] = (pq(now_data('a')[1]).attr('href'))
            newdata['aid'] = newdata['url'].split("/", 2)[2]
            # 内容
            type = pq(now_data('.recmd-tag')).text()
            if "图" in type:
                type = 1
            elif ":" in type:
                type = 2
            elif "纯文" == type:
                type = 3
            else:
                break
            if type == 1:
                newdata['title'], newdata['content'], newdata['link'] = getImg(newdata['aid'])
            elif type == 2:
                newdata['title'], newdata['content'], newdata['link'] = getVideo(newdata['aid'])
            elif type == 3:
                newdata['title'], newdata['content'], newdata['link'] = getText(newdata['aid'])

            newdata['type'] = type
            replayRes = getComments(newdata['aid'])
            replayList.append(replayRes)
            duanzilist.append(newdata)
        except Exception as e:
            print(e)
        i += 1
    return duanzilist, replayList

def getComments(aid):
    url = baseUrl + "/article/" + aid
    data = pq(url)
    data = pq(data('#r' + aid + ' .comment-block'))

    replayList = []
    for item in data.items():
        item = pq(item)
        item = pq(item('.replay'))
        res = {}
        res['aid'] = aid
        res['replay_name'] = pq(item('a')).attr('title')
        res['replay_content'] = pq(item('span')).text()
        replayList.append(res)
    return replayList

def getImg(aid):
    url = baseUrl + "/article/" + aid
    data = pq(url)
    content = pq(data('.content')).text()
    title = content[:20] + '...'
    links = pq(data('.thumb img'))

    link = ''
    for l in links:
        link += pq(l).attr('src') + ','
    link = link[:len(link)-1]
    return title, content, link

def getVideo(aid):
    url = baseUrl + "/article/" + aid
    data = pq(url)
    content = pq(data('.content')).text()
    title = content[:20] + '...'
    link = pq(data('#article-video source')).attr('src')
    return title, content, link

def getText(aid):
    url = baseUrl + "/article/" + aid
    data = pq(url)
    content = pq(data('.content')).text()
    title = content[:20] + '...'
    link = ''
    return title, content, link

def setReplay(replayList):
    for data in replayList:
        try:
            if len(data) > 0 :
                for item in data:
                    item['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    db.db().insert('replay', item)
        except Exception as e:
            print(e)

def setContents(duanzilist):
    for data in duanzilist:
        try:
            data['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            db.db().insert('duanzi', data)
        except Exception as e:
            print(e)

i=1
while i < 100:
    duanzilist, replayList = getContent('https://www.qiushibaike.com/8hr/page/'+str(i))
    setContents(duanzilist)
    setReplay(replayList)
    i+=1