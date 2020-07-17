# -*- coding:utf-8 -*-
# @time   :2020/6/23  15:11
# @Author :feiou
# @Email  :1006290526@qq.com
# @File   :http_request.py

#发送http请求
import requests
#注册 、登录、充值、提现为一个函数

def http_request(url,data,token=None,method='post'):#注册与登录函数
    header = {'X-Lemonban-Media-Type': 'lemonban.v2',
                'Authorization':token}  # 充值的请求头
    if method=='get':#根据get、post请求来处理
        result = requests.get(url, json=data, headers=header)
        print(result.json())
    elif method=='post':
        result = requests.post(url,json=data,headers=header) #post请求方式，返回的结果存起来
        print(result.json())
    # print(result.json())#.json就是看到他的结果值、输出内容到控制台
    return result.json() #返回指定的结果  拿到这一步的return返回值，是为了做下一步用

# if __name__ == '__main__': # 只有你在当前文件夹下面才可以执行这个数据  避免在其他地方调用的时候打印两次
reg_url = "http://120.78.128.25:8766/futureloan/member/register"  # 注册URL
log_url = "http://120.78.128.25:8766/futureloan/member/login"  # 登录URL
rec_url="http://120.78.128.25:8766/futureloan/member/recharge" #充值的URL
with_url="http://120.78.128.25:8766/futureloan/member/withdraw" #充值的URL

# header = {'X-Lemonban-Media-Type': 'lemonban.v2'}  # 注册的请求头、头部数据是固定的可以放在函数里面
reg_data = {'mobile_phone': 13214741914, 'pwd': '123456789'}  # 注册、登录的json数据

http_request(reg_url,reg_data) #注册
response=http_request(log_url,reg_data) #登录、登录返回的json结果存到这里

#充值时会用到登录函数里面返回的token值
#如果下一个请求需要上一个请求的结果时，就利用返回值return来实现
token = response['data']['token_info']['token']
member_id=response['data']['id']
rec_data={'member_id':member_id,'amount':1000} #充值数据

http_request(rec_url,rec_data,"Bearer "+token) #充值
http_request(with_url,rec_data,"Bearer "+token) #提现
