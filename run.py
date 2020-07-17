# -*- coding:utf-8 -*-
# @time   :2020/6/30  15:54
# @Author :feiou
# @Email  :1006290526@qq.com
# @File   :run.py

#执行文件  哪个文件夹下面的哪个文件调用哪个函数
from R_W_excel import read_data  #从wxl_atuo文件夹里的R_W_excel里导入read_data函数
from http_request import http_request
from R_W_excel import write_data

Token = None #全局变量  初始值设置为None
def run(file_name,sheet_name,c1,c2): #修改全局变量 行根据id走的  c1,c2写入结果和判断结果
    global Token #在这里声明  函数外的Token和函数内的Token是同一个值   必须要声明一下
    all_case = read_data(file_name, sheet_name)# 获取到所有的测试数据
    print("获取到的所有数据是：",all_case)
    for test_data in all_case:  # 长度为4  这个意思是每一行的数据依次传过来，所以第一次传test_data[0]的值是1
        # 在http_request进行请求的时候，判断是否是登录请求
        # print('test_data[6]的值是,',test_data[6])
        # if test_data[0] == 1: #他就是一个登录的用例  获取到登录的，就可以获取到token值
        # if test_data[1] == '登录': #判断两把是否相等  比较运算符
        ip = "http://120.78.128.25:8766" #先进行请求  #Token最初始值是NOne
        #test_data[4] 就是获取Excel表格中第5列的URL地址，每循环一次执行下一行
        response = http_request(ip + test_data[4], eval(test_data[5]), token=Token, method=test_data[3])
        if 'login' in test_data[4]: #成员运算符
            Token = "Bearer " + response['data']['token_info']['token']  # 获取登录token
        print("最后的结果值：{}".format(response))

        #开始写入结果
        write_data(file_name, sheet_name,test_data[0] + 1,c1,str(response))

        actual = {'code':response['code'],'msg':response['msg']}  #实际结果 result
        if test_data[6] == actual:   #test_data[6]指的是期望结果与实际结果是否相等  test_data[6]为expected          write_data('test_data.xlsx', 'recharge', test_data[0] + 1,9, str(response)
            print('测试用例执行通过')
            #写入数据  一步步定位Excel表、表单、行列
            write_data(file_name,sheet_name, test_data[0] + 1, c2, 'PASS') #test_data[0] + 1就是获取它的id，从第二行开始
        else:
            print('测试用例执行不通过')
            write_data(file_name, sheet_name, test_data[0] + 1, c2, 'FAIL')

#调用函数
#执行的充值的接口
run('test_data.xlsx','recharge',8,9)  #要调用函数
#执行提现的接口 设计用例很重要
# run('test_data.xlsx','withdraw',8,9)


