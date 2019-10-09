import requests
from pyquery import PyQuery as pq
import db
import base

baseUrl = 'http://www.budejie.com'

def getContent(url):
    data = pq(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'})
    data = data('.j-r-list ul').children()
    listlen = data.length
    i = 0
    duanzilist = []
    replayList = []
    while i < 10:
        try:
            newdata = {}
            now_data = pq(data[i])
            # 链接
            newdata['url'] = (pq(now_data('.j-r-list-c-desc a')).attr('href'))
            newdata['aid'] = newdata['url'].split('-')[1].split('.')[0]
            # 内容
            newdata['content'] = pq(now_data('.j-r-list-c-desc')).text()
            # 是否有图片
            if pq(now_data('.j-r-list-c-img')).length > 0:
                newdata['link'] = pq(now_data('.j-r-list-c-img img')).attr('data-original')
            newdata['type'] = 1

            replayList.append(getReplay(newdata['aid']))
            duanzilist.append(newdata)
        except Exception as e:
            print(e)
        i += 1
    return duanzilist, replayList


def getReplay(aid):
    url = 'http://api.budejie.com/api/api_open.php?a=datalist&per=5&c=comment&hot=1&appname=www&client=www&device=pc&data_id='+aid+'&page=1'
    results = requests.get(url).json()
    replayList = []
    if len(results) > 0:
        results = results['hot']
        for item in results:
            res = {}
            res['aid'] = aid
            res['replay_name'] = item['user']['username']
            res['replay_content'] = item['content']
            replayList.append(res)
    return replayList



i=1
while i < 100:
    print('http://www.budejie.com/'+str(i))
    duanzilist, replayList = getContent('http://www.budejie.com/'+str(i))
    base.setContents(duanzilist, 2)
    base.setReplay(replayList, 2)
    i+=1