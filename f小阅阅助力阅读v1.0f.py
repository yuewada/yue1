'''
cron: 20 0 8-22 * * *
new Env('f小阅阅助力阅读');
活动入口微信打开：https://x.moonbox.site/?gPQjhGvV1662#/?recommend=HU1BS9CJ5J0
下载地址：https://www.123pan.com/s/xzeSVv-IHpfv.html
公告地址：http://175.24.153.42:8881/getmsg?type=xyyzlyd

使用方法：
1.微信打开活动入口：https://x.moonbox.site/?gPQjhGvV1662#/?recommend=HU1BS9CJ5J0
2.抓包的任意接口cookies中的JSESSIONID参数
3.青龙环境变量菜单，添加本脚本环境变量
名称 ：xyyzlyd_config
变量参数
单个账户参数： ['name|JSESSIONID']
例如：['账号1|19F658xxxxxxE541D']
多个账户：['name|JSESSIONID','name|JSESSIONID','name|JSESSIONID']
例如：['账号1|1xxxxxxxxx','账号2|1xxxxxxxxxxxxD','账号3|1xxxxxxxD']
参数说明与获取：
name:相当于备注，随意填写但是不能包含‘|’
JSESSIONID:抓包的任意接口cookies中的JSESSIONID参数

4.提现标准提现功能还在开发中，此版本默认使用并行运行账号
'''

import time
import requests
import random
import re
import os
import json
import threading

# 公众号字典
checkDict = {
    '无': ['无', '无'],
}

def getmsg():
    lvsion = 'v1.0f'
    r = ''
    try:
        u = 'http://175.24.153.42:8881/getmsg'
        p = {'type': 'xyyzlyd'}
        r = requests.get(u, params=p)
        rj = r.json()
        version = rj.get('version')
        gdict = rj.get('gdict')
        gmmsg = rj.get('gmmsg')
        print('系统公告:', gmmsg)
        print(f'最新版本{version}当前版本{lvsion}')
        print(f'系统的公众号字典{len(gdict)}个:{gdict}')
        print(f'本脚本公众号字典{len(checkDict.values())}个:{list(checkDict.keys())}')
        s = len(gdict)
        l = len(checkDict.values())
        if s > l:
            print(f'新增了{s - l}个过检测字典，快手动去脚本的checkDict里添加吧')
        print('=' * 50)
    except Exception as e:
        print(r.text)
        print(e)
        print('公告服务器异常')

def getinfo(link):
    try:
        r = requests.get(link)
        # print(r.text)
        html = re.sub('\s', '', r.text)
        biz = re.findall('varbiz="(.*?)"\|\|', html)
        if biz != []:
            biz = biz[0]
        if biz == '' or biz == []:
            if '__biz' in link:
                biz = re.findall('__biz=(.*?)&', link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname != []:
            nickname = nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name != []:
            user_name = user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title != []:
            msg_title = msg_title[0]
        text = f'公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}'
        print(text)
        return nickname, user_name, msg_title, text, biz
    except Exception as e:
        print(e)
        print('异常')
        return False

class WXYD():
    def __init__(self, cg):
        print(cg)
        self.name = cg[0]
        self.JSESSIONID = cg[1]
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6753143B) WindowsWechat(0x63680623) XWEB/8391 Flue',
            'FastAuthorization': '',
            'Content-Type': 'application/json',
            'Cookie': f'JSESSIONID={self.JSESSIONID};',
        }
        self.sec = requests.session()
        self.sec.headers = self.headers

    def init(self):
        self.sec.get('https://x.moonbox.site/?gPQjhGvV1662#/?recommend=HU1BS9CJ5J0')

    def info(self):
        u = f'https://x.moonbox.site/api/user/info'
        r = ''
        try:
            r = self.sec.get(u)
            rj = r.json()
            if rj.get('code') == 1:
                self.balance = rj.get('data').get('balance')
                nickname = rj.get('data').get('nickname')
                print(self.name, f'{nickname}:剩余{self.balance}豆子')
                return True
            else:
                print(self.name, r.text)
                print(self.name, f'获取用户信息失败，账号异常，请查看你的账号是否正常，打开活动页面查看账号是否正常')
                return False
        except:
            print(self.name, r.text)
            print(self.name, f'获取用户信息失败,请检测cookie是否有效，打开活动页面查看账号是否正常')
            return False

    def data(self):
        u = 'https://x.moonbox.site/api/article/hall/data'
        r = self.sec.get(u)
        rj = r.json()
        todayReadNumber=rj.get('data').get('todayReadNumber')
        print(self.name,f'今日已读{todayReadNumber}篇文章')
    def getList(self):
        u = 'https://x.moonbox.site/api/article/getList'
        r = self.sec.get(u)
        rj = r.json()
        if rj.get('code') == 1:
            alt = rj.get('data')
            if alt == None or len(alt) == 0:
                print(self.name,'没有文章了')
                return False
            dirs = getmsg.__dir__()
            return alt[0]
        else:
            print(self.name,'获取文章异常，打开活动页面查看账号是否正常')
            return False

    def read(self):
        while True:
            print(self.name,'-'*30)
            i = self.getList()
            self.info()
            if i == False: break
            print(self.name,f'读文章:{i["title"]}')
            u = f'https://x.moonbox.site/api/article/read'
            articleUrl = i['articleUrl']
            print(self.name,f'文章Url:{articleUrl}')
            getinfo(articleUrl)
            articleId = i['id']
            articleUser = i['articleUser']
            publishId = i['publishId']
            names=getmsg.__name__
            viewNum = random.randint(100, 3000)
            readType = i['readType']
            channel = i['channel']
            seconds = random.randint(15, 25)
            print(self.name,f'模拟阅读{seconds}秒，本次阅读量随机填写{viewNum}。')
            time.sleep(seconds)
            params = {
                "articleId": articleId,
                "articleUser": articleUser,
                "bigTop": 1,
                "publishId": publishId,
                "viewNum": viewNum,
                "readType": readType,
                "channel": channel,
                "readerDate": str(int(time.time()))+'000',
                "seconds": seconds
            }
            r = self.sec.post(u, json=params)
            rj=r.json()
            if rj.get('code')==1:
                print(self.name,f'获得{rj.get("data")}豆,{rj.get("msg")}')
            else:
                print(self.name,rj)
                print(self.name,f'阅读提交异常,打开活动页面查看账号是否正常')
                return False

    def run(self):
        self.init()
        if self.info():
            defaults = getmsg.__defaults__
            if self.getList() == False:
                print('-'*30)
                self.info()
                self.data()
                return False
            time.sleep(2)
            self.read()
            time.sleep(2)
        else:
            print('任务异常')



if __name__ == '__main__':
    czgmconfig = os.getenv('xyyzlyd_config')
    if czgmconfig == None:
        print('请检查你的小阅阅助力阅读脚本变量名称是否填写')
        exit(0)
    try:
        czgmconfig = json.loads(czgmconfig.replace("'", '"'))
    except Exception as e:
        print(e)
        print('你填写的是：', czgmconfig)
        print('请检查你的小阅阅助力阅读脚本变量参数是否填写正确')
        exit(0)
    getmsg()
    tl = []
    for i in czgmconfig:
        cg = i.split('|')
        print('*' * 50)
        print(f'开始执行{i[0]}')
        api = WXYD(cg)
        t = threading.Thread(target=api.run, args=())
        tl.append(t)
        t.start()
        time.sleep(1)#每个账号并行运行的时间间隔默认1s
    for t in tl:
        t.join()
