from time import sleep
from multiprocessing import Pool

import pymysql
import requests,json,random
from urllib.parse import urlencode
from requests import RequestException



#浏览器列表
head1='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
head2='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
head3='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.12 Safari/537.36 Edg/76.0.182.6'
head=[head1,head2,head3]


# 浏览器标识
headers = {
    'user-agent': head[random.randint(0,2)]
}

#代理
def getProxy():
    proxy=['112.87.68.95:9999','163.204.244.124:9999',
           '111.226.211.11:8118','113.120.37.128:9999',
           '182.138.204.63:8118'
           ]
    # proxy=['120.83.107.154:9999','60.13.42.104:9999']
    #每次随机获取一个代理
    return {'http':'http://'+random.choice(proxy)}

########################################################################################################################
###################################################获取用户基本信息#####################################################
#获取b站up主的个人基础信息
#传入data，浏览器标识获取到用户的基础信息1
def getUserInfo1(data,headers,proxies):
    url='https://api.bilibili.com/x/space/acc/info?'+urlencode(data)
    response=requests.get(url,headers=headers,proxies=proxies)
    try:
        if response.status_code==200:
            return response.text
        print("uid="+str(data.get("mid"))+"....状态码" + str(response.status_code))
    except RequestException:
        print("uid=" + str(data.get("mid")) + "....状态码" + str(response.status_code))

#传入data，浏览器标识获取到用户的基础信息2
def getUserInfo2(data,headers,proxies):
    url='https://api.bilibili.com/x/relation/stat?v'+urlencode(data)
    response=requests.get(url,headers=headers,proxies=proxies)
    try:
        if response.status_code==200:
            return response.text
        print("uid=" + str(data.get("mid")) + "....状态码" + str(response.status_code))
    except RequestException:
        print("uid=" + str(data.get("mid")) + "....状态码" + str(response.status_code))

#传入data，浏览器标识获取到用户的基础信息3
def getUserInfo3(data,headers,proxies):
    url='https://api.bilibili.com/x/space/navnum?'+urlencode(data)
    response=requests.get(url,headers=headers,proxies=proxies)
    try:
        if response.status_code==200:
            return response.text
        print("uid=" + str(data.get("mid")) + "....状态码" + str(response.status_code))
    except RequestException:
        print("uid=" + str(data.get("mid")) + "....状态码" + str(response.status_code))

#传入data，浏览器标识获取到用户的基础信息4
def getUserInfo4(data,headers,proxies):
    url='https://api.bilibili.com/x/space/upstat?'+urlencode(data)

    # req=urllib.request.Request(url)
    # req.add_header("User-Agent",headers.get('user-agent'))
    # response=urllib.request.urlopen(req,timeout=10)
    # return response.read()
    response=requests.get(url,headers=headers,proxies=proxies)
    try:
        if response.status_code==200:
            return response.text
        print("uid=" + str(data.get("mid")) + "....状态码" + str(response.status_code))
    except RequestException:
        print("uid=" + str(data.get("mid")) + "....状态码" + str(response.status_code))
########################################################################################################################
#################################################获取用户基本信息结束###################################################


#根据数据库结构新建一个类
class User:
    def __init__(self,UserInfo1,UserInfo2,UserInfo3,UserInfo4):
        self.uid=UserInfo1.get("mid")
        self.name=UserInfo1.get("name")
        self.sex=UserInfo1.get("sex")
        self.sign=UserInfo1.get("sign")
        self.birthday=UserInfo1.get("birthday")
        self.face=UserInfo1.get("face")
        self.vip_type=UserInfo1.get("vip").get("type")
        self.vip_status=UserInfo1.get("vip").get("status")
        self.sub_video=UserInfo3.get("video")
        self.sub_audio=UserInfo3.get("audio")
        self.sub_album=UserInfo3.get("album")
        self.sub_article=UserInfo3.get("article")
        self.archive_view=UserInfo4.get("archive").get("view")
        self.article_view=UserInfo4.get("article").get("view")
        self.following=UserInfo2.get("following")
        self.follower=UserInfo2.get("follower")
        self.level=UserInfo1.get("level")

#获取单个用户全部信息
def getUserInfo(uid):
    data={
        'mid': uid,
        'jsonp': 'jsonp'
    }
    proxies=getProxy();
    #将得到的json数据转化为字典
    UserInfo1=json.loads(getUserInfo1(data,headers,proxies)).get("data")
    UserInfo2=json.loads(getUserInfo2(data,headers,proxies)).get("data")
    UserInfo3=json.loads(getUserInfo3(data,headers,proxies)).get("data")
    UserInfo4=json.loads(getUserInfo4(data,headers,proxies)).get("data")
    #生成一个user对象，然后返回user对象
    user=User(UserInfo1,UserInfo2,UserInfo3,UserInfo4)
    return user


#每轮获取10000个用户存到数据库中
def getUserInfoTenThousand(i):
    print("第"+str(i)+"-"+str((i+10000))+"用户")
    sleep(2)
    #建立数据库链接
    db = pymysql.connect(host="localhost", user="root", password="root", db="bilibili_user_info", port=3306)
    cur = db.cursor()
    try:
        for j in range(i, i + 10000):
            try:
                values=j+1
                # 获取uid为values的user对象
                user = getUserInfo(values)
                sleep(0.1)
                insertSql="INSERT INTO `bilibili_user_info`.`users_info` (`uid`,`name`,`sex`,`sign`,`birthday`,`face`,`vip_type`,`vip_status`,`sub_video`,`sub_audio`,`sub_album`,`sub_article`,`archive_view`,`article_view`,`following`,`follower`,`level`) VALUES (" + str(user.uid) + ",\'" + user.name + "\',\'" + user.sex + "\',\'" + user.sign + "\',\'0000-" + user.birthday + "\',\'" + user.face + "\'," + str(user.vip_type) + "," + str(user.vip_status) + "," + str(user.sub_video) + "," + str(user.sub_audio) + "," + str(user.sub_album) + "," + str(user.sub_article) + "," + str(user.archive_view) + "," + str(user.article_view) + "," + str(user.following) + "," + str(user.follower) + "," + str(user.level) + ") ;"
                #打印一下sql语句
                print(insertSql)
                cur.execute(insertSql)
            except Exception:
                pass
    except Exception:
        pass
    finally:
        #每爬取一万个用户开关一次数据库
        db.close()


def main():
    # getUserInfoTenThousand(0)
    #建立一个多线程池
    pool=Pool()
    #先爬取前100万用户
    pool.map(getUserInfoTenThousand,[i*10000 for i in range(0,100)])

###########################################
###这是一个代理IP测试方法
def ipTest():
    proxies={'http':'http://123.169.35.7:9999'}
    url = 'http://httpbin.org/get'
    response = requests.get(url, headers=headers,proxies=proxies)
    print(response.status_code)
    try:
        if response.status_code == 200:
            print(response.text)
    except RequestException:
        pass
#################################################




if __name__ == '__main__':
    main()
    # getProxy()
    # getUserInfoTenThousand(0)
    # ipTest()
    # getTest(0)

    # getUserInfo(1)
    # data = {
    #     'mid': 2,
    #     'jsonp': 'jsonp'
    # }
    # proxies=getProxy();
    # print(getUserInfo0(data,headers))













