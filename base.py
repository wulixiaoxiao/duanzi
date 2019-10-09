import db
import time

def setReplay(replayList, type = 1):
    for data in replayList:
        try:
            if len(data) > 0 :
                for item in data:
                    item['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['pid'] = type
                    db.db().insert('replay', item)
        except Exception as e:
            print(e)

def setContents(duanzilist, type = 1):
    for data in duanzilist:
        try:
            data['aid'] = data['aid']
            data['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data['pid'] = type
            db.db().insert('duanzi', data)
        except Exception as e:
            print(e)


def setPics(piclist, type = 1):
    for data in piclist:
        try:
            data['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data['pid'] = type
            db.db().insert('meizitu', data)
        except Exception as e:
            print(e)



def setComments(comments, type = 3):
    for itemCom in comments:
        for com in itemCom:
            try:
                com['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                com['pid'] = type
                db.db().insert('comments', com)
            except Exception as e:
                print(e)




