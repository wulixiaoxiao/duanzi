import requests
import json
import db
import time
import threading

def requestHttp(url):
    headers = {
        'Host': 'lf.snssdk.com',
        'User-Agent': 'com.sup.android.superb/174 (Linux; U; Android 5.1.1; zh_CN; HUAWEI MLA-AL10; Build/HUAWEIMLA-AL10; Cronet/58.0.2991.0)',
        'Connection': 'keep-alive',
        'Cookie': 'install_id=70327398297; ttreq=1$3ff7bd7afcd0c17e0a5f204d6131b632edb4f955; odin_tt=ce37de7a14f64f8a15c2d531514e01938d42625f86e5ae8faefa29185317248b675a7a1d76d3b84035fa822324eb2735abdef7e4a88be73d11403461a7b1df74',
        'Accept-Encoding': 'gzip',
        'X-SS-REQ-TICKET': '1556023920599',
        'sdk-version': "1",
        'X-SS-TC': '0',
        'X-SS-RS': '1',
        'X-Gorgon': '030096604400ee83f6c7a25d5cccd7e3db97327920f09f0b50c1',
        'X-Khronos': '1556023920',
    }

    res = requests.get(url, headers=headers, verify=False)
    return res

def updateDuanzi(info):
    url = 'https://h5.pipix.com/bds/webapi/item/detail/?item_id='+str(info['aid'])
    results = requestHttp(url).json()
    if results['status_code'] == 0:
        data = results['data']['item']
        res = {}
        res['aid'] = info['aid']
        res['like_count'] = data['stats']['like_count']
        res['comment_count'] = data['stats']['comment_count']
        res['share_count'] = data['stats']['share_count']
        res['video_url'] = data['origin_video_download']['url_list'][0]['url']
        res['video_cover_image'] = data['origin_video_download']['cover_image']['url_list'][0]['url']
        res['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        return res
    else:
        return []


def getCommone(itemId):
    i = 0
    list = []
    while i<2:
        offset = i*10
        url = 'https://lf.snssdk.com/bds/item/cell_comment/?item_id='+str(itemId)+'&offset='+str(offset)+'&api_version=1&iid=70327398297&device_id=67532086177&ac=wifi&channel=sem_baidu_ppx_gj&aid=1319&app_name=super&version_code=174&version_name=1.7.4&device_platform=android&ssmix=a&device_type=MI+6+&device_brand=Xiaomi&language=zh&os_api=22&os_version=5.1.1&uuid=67532086177&openudid=8e158228a4e44380&manifest_version_code=174&resolution=1280*720&dpi=240&update_version_code=1743&_rticket=1557239439626&app_region=CN&sys_region=CN&time_zone=Asia%2FShanghai&app_language=ZH&carrier_region=CN&ts=1557239439&as=a2d5599d9fb89c06814066&cp=9f84c551f21bd068e2Ycag&mas=007862c150cd20c44b56dce66e3cd0ec6553533313b3235333f9a3'
        res = requestHttp(url).json()
        if(res['status_code'] == 0) :
            res = res['data']['cell_comments']
            for com in res:
                if(com['cell_type'] == 1):
                    continue
                commentData = {}
                commentData['item_id'] = itemId
                commentData['display_time'] = com['display_time']
                commentData['comment_id'] = com['comment_info']['comment_id']
                commentData['type'] = com['comment_info']['type']          # 1文字2图片3视频
                # 用户信息
                commentData['name'] = com['comment_info']['user']['name']
                commentData['avatar'] = json.dumps(com['comment_info']['user']['avatar'])

                if (commentData['type'] == 1) :
                    commentData['text'] = com['comment_info']['text']
                    commentData['like_count'] = com['comment_info']['like_count']
                    commentData['reply_count'] = com['comment_info']['reply_count']

                elif(commentData['type'] == 2) :
                    commentData['text'] = com['comment_info']['text']
                    commentData['images'] = json.dumps(com['comment_info']['images'])
                    commentData['image_thumbs'] = json.dumps(com['comment_info']['image_thumbs'])
                    commentData['like_count'] = com['comment_info']['like_count']
                    commentData['reply_count'] = com['comment_info']['reply_count']
                elif(commentData['type'] == 3) :
                    commentData['text'] = com['comment_info']['text']
                    commentData['video'] = json.dumps(com['comment_info']['video'])
                    commentData['like_count'] = com['comment_info']['like_count']
                    commentData['reply_count'] = com['comment_info']['reply_count']

                list.append(commentData)
        i+=1
    return list


def start(id, limit, offset):
    where = 'pid=3 and type=2'
    if(id != 0):
        where += ' and id<'+str(id)
    duanziList = db.db().select('duanzi', where, '', 'id desc', limit, offset)
    # commentsList = db.db().select('comments', 'pid=3 and type=3')
    for res in duanziList:
        newVideoInfo = updateDuanzi(res)
        db.db().update('duanzi', 'aid=' + res['aid'], newVideoInfo)



if __name__ == '__main__':
    i = 0
    id = 0
    limit = 100
    while i <= 20:
        offset = i * limit
        # start(id, limit, offset)
        # exit()
        print(limit, offset)
        t = threading.Thread(target=start, args=(id, limit, offset), name='线程'+str(i))
        t.start()
        t.join()
        print('线程'+str(i)+'启动。。。。')
        i+=1

