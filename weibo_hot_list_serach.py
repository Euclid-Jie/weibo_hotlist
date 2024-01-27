import requests
import json
import datetime
import pytz
from EuclidDataTools import CsvClient
import pandas as pd
from pathlib import Path

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
myCol = CsvClient(subFolder="hotlist", FileName=f"{year}_{month}_{day}.csv")


def _deal_sigle_hot_data(raw_data: dict) -> dict:
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

# convert today's data for ranking
# 完全是为了符合js那边的格式, 因为我看不到js那边的代码, 所以只能这样了
example = pd.read_csv(Path("docs/example.csv"), encoding="gbk", low_memory=False)
data = pd.read_csv(myCol.FullFilePath, encoding="utf_8_sig")
data["time"] = pd.to_datetime(data["time"], format="%Y-%m-%d:%H:%M:%S")

for i in range(0, 24):
    data_later_hour = data[data["time"] > pd.to_datetime(f"{year}-{month}-{day}:{i}:00:00", format="%Y-%m-%d:%H:%M:%S")]
    example["name"] = data_later_hour["word"]
    example["value"] = data_later_hour["hot"]
    example["date"] = data_later_hour["time"].dt.strftime("%Y-%m-%d %H:%M")
    example = example[~example["name"].isna()]
    
    # save data
    example.to_csv(Path(f"docs/{i}/ranking_data.csv"), index=False, encoding="utf-8-sig")
