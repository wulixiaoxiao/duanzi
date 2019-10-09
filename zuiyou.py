import requests
import json

def requestHttp(url):
    header = {
        '{"direction":"down","h_model":"iPhone 7","h_ch":"appstore","h_ua":"Mozilla\/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit\/605.1.15 (KHTML, like Gecko) Mobile\/15E148 Zuiyou\/4.9.2","h_app":"zuiyou","c_types":[1,2,3,9,10,7,8,11,20,21,14,22],"h_nt":1,"h_av":"4.9.2","tab":"rec","h_did":"bceee6681925e59e9635b4ffa4ab1c02","filter":"all","h_os":1220000,"h_ts":1556455952565,"h_m":116125069,"token":"T3KaNSt4A3Gj5jClQMcjf1jXe-7MnnTQJVnWh5PmRtzPddLyeGUqhb0MN95YQ4H_FE0jO","h_dt":1,"sdk_ver":{"tt_aid":"5001334","tx_aid":"1106701811","tx":"4.7.6","tt":"1.9.4"}}------WebKitFormBoundary7MA4YWxkTrZu0gW--'
    }

    data = {"direction": "down", "h_model": "iPhone 7", "h_ch": "appstore", "h_ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Zuiyou/4.9.2", "h_app": "zuiyou", "c_types": [1, 2, 3, 9, 10, 7, 8, 11, 20, 21, 14, 22], "h_nt": 1, "h_av": "4.9.2", "tab": "rec", "h_did": "bceee6681925e59e9635b4ffa4ab1c02", "filter": "all", "h_os": 1220000, "h_ts": 1556455952565, "h_m": 116125069, "token": "T3KaNSt4A3Gj5jClQMcjf1jXe-7MnnTQJVnWh5PmRtzPddLyeGUqhb0MN95YQ4H_FE0jO", "h_dt": 1, "sdk_ver": {"tt_aid": "5001334", "tx_aid": "1106701811", "tx": "4.7.6", "tt": "1.9.4"}}
    res = requests.post(url, json=data, headers=header, verify=False)
    return res



url = 'https://api.izuiyou.com/index/recommend?sign=bcb78f99b063e5a058648743f4198804'
res = requestHttp(url)
if res['status_code'] == 0:
    data = res['data']['data']
    for val in data:
        pass


str = ''