import requests
import json
import base
import time

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

def start(url):
    res = requestHttp(url).json()
    if res['status_code'] == 0:
        data = res['data']['data']
        list = []
        commonList = []
        for val in data:
            res = {}
            if(val['item'] == None) :
                continue
            res['aid'] = val['item']['item_id']
            res['item_type'] = val['item']['item_type']

            res['author_id'] = val['item']['author']['id']
            res['author_name'] = val['item']['author']['name']
            res['author_avatar'] = val['item']['author']['avatar']['url_list'][0]['url']

            res['comment_count'] = val['item']['stats']['comment_count']
            res['like_count'] = val['item']['stats']['like_count']
            res['share_count'] = val['item']['stats']['share_count']

            type = 0
            if res['item_type'] == 1:
                res['content'] = val['item']['note']['text']
                imgs = val['item']['note']['multi_image']
                if len(imgs) != 0:  # 图片
                    type = 1
                    imglist = []
                    for img in imgs:
                        pic = {}
                        pic['url'] = img['url_list'][0]['url']
                        pic['is_gif'] = img['is_gif']
                        imglist.append(pic)
                    res['link'] = json.dumps(imglist)
                else:
                    type = 3
            elif res['item_type'] == 2:
                type = 2
                res['content'] = val['item']['video']['text']
                res['video_id'] = val['item']['video']['video_id']
                res['video_url'] = val['item']['video']['video_download']['url_list'][0]['url']
                res['video_cover_image'] = val['item']['video']['video_download']['cover_image']['url_list'][0]['url']

            res['type'] = type
            res.pop('item_type')
            list.append(res)

            # 评论
            itemId = res['aid']
            comList = getCommone(itemId)
            commonList.append(comList)

        return list, commonList
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
                commentData['aid'] = itemId
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

i=1
while True:
    url = 'https://lf.snssdk.com/bds/feed/stream/?api_version=2&cursor=1556023627900&auto_play=1&feed_count=6&list_type=1&direction=1&iid=70327398297&device_id=67532086177&ac=wifi&channel=sem_baidu_ppx_gj&aid=1319&app_name=super&version_code=174&version_name=1.7.4&device_platform=android&ssmix=a&device_type=HUAWEI+MLA-AL10&device_brand=HUAWEI&language=zh&os_api=22&os_version=5.1.1&uuid=67532086177&openudid=8e158228a4e44380&manifest_version_code=174&resolution=720*1280&dpi=240&update_version_code=1743&_rticket=1556023920595&app_region=CN&sys_region=CN&time_zone=Asia%2FShanghai&app_language=ZH&carrier_region=CN&ts=1556023922&as=a2b5e02b62276c4a5f4244&cp=017bc1512bfeb2a1e2McUg&mas=00afad9aa2d27731ac4e85a568ddd6235d131373135993b913f953'
    list, commonList = start(url)
    base.setContents(list, 3)
    base.setComments(commonList, 3)
    time.sleep(1)
    i+=1