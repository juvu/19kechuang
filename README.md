# README
这是一个Bilibili爬虫。
## 爬取到的内容
1. "title" 标题
2. "class1" 类别1
3. "class2" 类别2
4. "time" 视频发布时间
5. "rank" 排行
6. "uid" up主id
7. "data": {
    1. "aid" av_id
    2. "view" 浏览量
    3. "danmaku" 弹幕量
    4. "reply" 评论量
    5. "favorite" 收藏数
    6. "coin" 硬币数
    7. "share" 分享数
    8. "now_rank" 当前排名
    9. "his_rank" 历史最高排名
    10. "like" 喜欢数
    11. "dislike" 不喜欢数
    12. "no_reprint" 版数
    13. "copyright" 版权相关
    }
8. "av_id" 
9. "c_id"
10. "d": {
    1. "text" 弹幕文本
    2. "second" 弹幕出现的时间，单位为秒
    3. "mode" 123滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕
    4. "size" 字号 12非常小, 16特小, 18小, 25中, 36大, 45很大, 64特别大
    5. "color" 颜色，以HTML颜色的十进制为准
    6. "time" Unix格式的时间戳 基准时间为 1970-1-1 08:00:00
    7. "pool" 弹幕池 0普通池 1字幕池 2特殊池（目前特殊池为高级弹幕专用
    8. "u_id" 发送者id 用于“屏蔽此弹幕的发送者”功能
    9. "id" 弹幕数据库中id 用于“历史弹幕”功能
}

## 之后可以做的
1. 标签
