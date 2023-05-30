# 爬取微博热点评论

# 获取当前热搜信息
import json
import time

import requests

from service.feelcheck import write


# 获取某个信息
def get_data(hot_band_url, data_goods, cookie, name):
    mydata_pa = []
    headers = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39',
        'cookie': cookie,
        'Accept': 'application/json, text/plain, */*'
    }
    id = 0
    try:
        for k in data_goods:
            print(hot_band_url + k)
            data = requests.get(hot_band_url + k, headers=headers)  # 请求
            # time.sleep(1)  # 防止被监控
            data = data.json()
            data = data['data']['data']
            for k in data:
                res = {}
                text = get_split(k['text'])
                if text != "":
                    res['id'] = id
                    res['source'] = k['source']
                    res['console'] = get_split(k['text'])
                    mydata_pa.append(res)
                    id += 1
        print("开始写数据")
        write(mydata_pa, name)
        return mydata_pa
    except:
        res = []
        return res


# 截取评论
def get_split(comments):
    start = str(comments).find("<")
    return comments[0:start]


# 识别多页评论数据
def get_readUrl(data_url):
    data = data_url
    data_goods = []
    str_data = data.split("hotflow")
    for k in str_data:
        if len(k) > 10:
            data = k[:78]
            print(data)
            data_goods.append(data)
    return data_goods

#
# if __name__ == '__main__':
#     data = get_readUrl()
#     get_data(hot_band_url, data)
