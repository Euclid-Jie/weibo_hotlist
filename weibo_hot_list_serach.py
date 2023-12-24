import requests
import json
import datetime
import pytz
from EuclidDataTools import CsvClient

# 获取数据
Url = "https://weibo.com/ajax/side/hotSearch"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)", "Host": "httpbin.org"}
response = requests.get(Url, timeout=60)  # 使用request获取网页
data = response.content.decode("utf-8", "ignore")  # 解码

# 记录时间
tz = pytz.timezone("Asia/Shanghai")
now_time = datetime.datetime.now(tz)
print(now_time)
year = now_time.year
month = now_time.month
day = now_time.day
hour = now_time.hour
min = now_time.minute
sec = now_time.second

# 保存数据
myCol = CsvClient(subFolder='hotlist', FileName=f"{year}_{month}_{day}.csv")

def _deal_sigle_hot_data(raw_data:dict)->dict:
    """
    处理单条热搜数据
    :param raw_data: 从网页获取的原始数据
    :return: 处理后的数据
    """
    data = {}
    try:
        data["is_ad"] = raw_data["is_ad"]
        return {}
    except KeyError:
        pass
    data["word"] = raw_data["word"]
    data["hot"] = raw_data["raw_hot"]
    data["mid"] = raw_data["mid"]
    return data

for i in json.loads(data)["data"]["realtime"]:
    
    single_data = _deal_sigle_hot_data(i)
    if len(single_data) != 0:
        single_data["time"] = f"{year}-{month}-{day}:{hour}:{min}:{sec}"
        myCol.insert_one(single_data)
