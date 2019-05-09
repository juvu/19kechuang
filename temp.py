import json
import datetime
## 导入
d=dict()
filename = "E:/github/kechuang/21351430.json" 
with open(filename,"r",encoding="utf-8") as f:
    d=json.load(f)
    print("Load Successful! ")
## 查看弹幕数量
len(d["d"])
## 查看最早的弹幕发送时间
time = [int(x["time"]) for x in d["d"]]
t = min(time)
ans = time.strftime("%Y/%m/%d %H:%M:%S", t)
print(ans)
# dateArray = datetime.datetime.utcfromtimestamp(t)
# ans = dateArray.strftime("%Y-%m-%d %H:%M:%S")
# print(ans)

## 排序
d1 = sorted(d["d"], key=lambda d:d["time"]) 

## 分词
word_list = [x["text"] for x in d["d"]]
text_all =' '.join(word_list)
import jieba
text = jieba.lcut(text_all, cut_all=False)
