# 简介

爬取b站用户的基础公开信息

由于b站每一位用户都有一个独一无二的uid且无法注销用户，所以可以通过uid来获取b站所有用户的基础信息





# 数据库信息

数据库名字：bilibili_user_info

表:users_info

| 属性         | 数据类型     | 说明                                  |
| :----------- | :----------- | :------------------------------------ |
| uid          | bigint       | 用户唯一uid                           |
| name         | varchar(50)  | 用户昵称                              |
| sex          | varchar(20)  | 用户性别                              |
| sign         | varchar(255) | 用户简介                              |
| birthday     | date         | 用户生日                              |
| face         | varchar(255) | 用户头像URL                           |
| vip_type     | int          | 会员类型[^0 无会员 1普通会员 2大会员] |
| vip_status   | int          | 会员状态[^0无会员 1开启会员状态]      |
| sub_video    | int          | 投稿视频数量                          |
| sub_audio    | int          | 投稿音频数量                          |
| sub_album    | int          | 投稿相册数量                          |
| sub_article  | int          | 投稿专栏文章数量                      |
| archive_view | bigint       | 投稿作品总播放量                      |
| article_view | bigint       | 投稿作品总阅读量                      |
| following    | int          | 用户关注UP主的数量                    |
| follower     | bigint       | 用户粉丝数量                          |
| level        | int          | 用户等级                              |



# URL参数

## 用户个人信息获取 getUserInfo1()

```xml
https://api.bilibili.com/x/space/acc/info?mid=10&jsonp=jsonp
```

通过以上URL可以获取到用户的个人公开信息，其中mid代表UP主的uid

以下为获取到的基础信息

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "mid": 10,
    "name": "mikumiku没穿内裤",
    "sex": "保密",
    "face": "http://i1.hdslb.com/bfs/face/b9d2169b6d45779ea6caecec954236eef0675f95.gif",
    "sign": "裙下的风光，全都暴露~",
    "rank": 10000,
    "level": 5,
    "jointime": 0,
    "moral": 0,
    "silence": 0,
    "birthday": "01-01",
    "coins": 0,
    "fans_badge": false,
    "official": {
      "role": 0,
      "title": "",
      "desc": ""
    },
    "vip": {
      "type": 2,
      "status": 1,
      "theme_type": 0
    },
    "is_followed": false,
    "top_photo": "http://i1.hdslb.com/bfs/space/3ab888c1d149e864ab44802dea8c1443e940fa0d.png",
    "theme": {}
  }
}
```



## 用户粉丝数量以及详细数据 getUserInfo2()

```xml
https://api.bilibili.com/x/relation/stat?vmid=72270557&jsonp=jsonp
```

通过以上URL可以得到用户的粉丝数量以及用户关注UP主数量的详细数据，其中

最终得到的结果如下所示

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "mid": 72270557,
    "following": 49,
    "whisper": 0,
    "black": 0,
    "follower": 478961
  }
}
```

其中『"follower": 478961』为粉丝数量

『"following": 49』为关注的UP主数量

## 用户投稿数量获取 getUserInfo3()

```xml
https://api.bilibili.com/x/space/navnum?mid=72270557&jsonp=jsonp
```

获取用户所有投稿数量，包括视频、音频、相簿、专栏等

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "video": 35,
    "bangumi": 17,
    "cinema": 1,
    "channel": {
      "master": 6,
      "guest": 6
    },
    "favourite": {
      "master": 4,
      "guest": 4
    },
    "tag": 0,
    "article": 3,
    "playlist": 0,
    "album": 71,
    "audio": 0
  }
}
```

其中『"video": 35』为投稿视频数量

其中『"audio": 0』为投稿音频数量

其中『"article": 3』为投稿专栏数量

其中『"album": 71』为投稿相簿数量

## 用户所有投稿的作品的播放数与阅读数 getUserInfo4()

```xml
https://api.bilibili.com/x/space/upstat?mid=72270557&jsonp=jsonp
```

```json
{
  "code": 0,
  "message": "0",
  "ttl": 1,
  "data": {
    "archive": {
      "view": 11805324
    },
    "article": {
      "view": 43045
    }
  }
}
```

其中『"view": 11805324』为总播放量

『"view": 43045』为总阅读量

