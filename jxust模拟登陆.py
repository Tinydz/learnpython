# -*- coding:utf-8 -*-
'''
Created on 2016年1月23日
思路：验证码是动态更新的每次打开都不一样，
一般这种验证码和cookie是同步的。其次想
识别验证码肯定是吃力不讨好的事，因此我们
的思路是首先访问验证码页面，保存验证码、
获取cookie用于登录，然后再直接向登录
地址post数据。
@author: AndrewsMJ
'''

import urllib
import http.cookiejar
import re

captchaUrl = "http://jw.jxust.edu.cn/CheckCode.aspx"
PostUrl = "http://jw.jxust.edu.cn/default2.aspx"

# 构建cookie
cj = http.cookiejar.CookieJar()
# 构建httpcookie处理器
httphandler = urllib.request.HTTPCookieProcessor(cj)
# 构建一个opener
opener = urllib.request.build_opener(httphandler)
# 用户名密码
username = '学号'
password = '密码'

PicCode = opener.open(captchaUrl).read()
localPicCode = open('picCode.jpg', 'wb')
localPicCode.write(PicCode)
localPicCode.close()

SecretCode = input('请输入验证码: ')
postData={
    '__VIEWSTATE': 'dDwyODE2NTM0OTg7Oz4lehgYY/JuEnXQKwVOg75pFCIy9A==', #各个学校的不同，是asp特有的
    'txtUserName': username,
    'TextBox2': password,
    'txtSecretCode': SecretCode,
    'RadioButtonList1': '学生',
    'Button1': '',
    'lbLanguage': '',
    'hidPdrs': '',
    'hidsc': '',
    }

# 根据抓包信息 构造表单
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}

# 生成post数据 ?key1=value1&key2=value2的形式
data = urllib.parse.urlencode(postData)

# 解决POST data should be bytes or an iterable of bytes. It cannot be of type str.
data = data.encode('utf-8')

# 构造post请求
req = urllib.request.Request(PostUrl, data, headers)
try:
    response = opener.open(req)
    result = response.read().decode('gb2312')
    pattern = r'<span id="xhxm">(.*)同学</span>'
    sname = re.compile(pattern)
    snamestr = sname.findall(result)[0]
    print('姓名： ', snamestr)
except urllib.request.HTTPError as e:
    print('模拟登陆失败')
    print(e)















































