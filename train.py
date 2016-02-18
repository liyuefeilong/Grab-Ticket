#!/usr/bin/python
# -*- coding:utf8 -*-
from splinter.browser import Browser
from time import sleep

# 登录、购票等网址
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
config_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

# b = Browser(driver_name="chrome")

# b.visit(url)

# 用户名，密码
username = "liyuefeilong"
passwd = "peng968"
# cookies
# "%u4E0A%u6D77%2CSHH" 上海
# "%u6DF1%u5733%u5317%2CIOQ" 深圳北
# "%u666E%u5B81%2CPEQ" 普宁
starts = "%u6DF1%u5733%u5317%2CIOQ"
ends = "%u666E%u5B81%2CPEQ"

# 乘车时间
dtime = "2016-01-18"

# 选择查询列表中的车次，默认为0，从上到下依次点击
order = 0

# 乘客名
pa = u"黄佳楠(常用联系人)"

# 车次类型
ttype="GC-高铁/城际"

def login():
    b.find_by_text(u"登录").click()
    sleep(3)
    b.fill("loginUserDTO.user_name",username)
    sleep(0.1)
    b.fill("userDTO.password",passwd)
    sleep(0.1)
    b.execute_script('alert("请自行输入验证码")')
    print(u"等待验证码，自行输入...")
    sleep(10)

            
def check():
    global b
    b = Browser(driver_name="chrome")
    b.visit(ticket_url)
    b.execute_script('alert("开始刷票")')
    sleep(2)
    b.get_alert().dismiss()
    
    while b.is_text_present(u"登录"):
        sleep(1)
        login()
        if b.url == initmy_url:
            break
      
    try:
        # 跳回购票页面
        b.visit(ticket_url)
        
        # 加载车票查询信息
        b.cookies.add({"_jc_save_fromStation":starts})
        b.cookies.add({"_jc_save_toStation":ends})
        b.cookies.add({"_jc_save_fromDate":dtime})
        b.reload()
        i = 1        
        
        # 循环点击预订
        if order != 0:
            while b.url == ticket_url:
                sleep(3)
                b.find_by_text(u"查询").click()
#                b.find_by_text(ttype).click()
                
                if b.find_by_text(u"预订"):
                    sleep(0.3)
                    b.find_by_text(u"预订")[order - 1].click()
                    print(b.url)
                    
                    if b.is_text_present(u"证件号码",wait_time = 0.5):
#                        print [ i.text for i in b.find_by_text(pa) ]
                        b.find_by_text(pa)[1].click()
                        
                else:
                    b.execute_script('alert("没有可预订选项")')
                    b.get_alert().dismiss()
                    pass
                 
        else:
            while b.url == ticket_url:
                sleep(3)
                b.find_by_text(u"查询").click()
                if b.find_by_text(u"预订"):
                    sleep(0.3)
                    for i in b.find_by_text(u"预订"):                 
                        i.click()
                        sleep(0.1)
                        if b.is_text_present(u"证件号码"):
                            b.find_by_text(pa)[1].click()
                                                        
                    else:
                        b.execute_script('alert("似乎没有可预订选项")')
                        b.get_alert().dismiss()
                        pass
                     
        b.execute_script('alert("能做的都做了")')
        b.get_alert().dismiss()
        
        print(u"能做的都做了.....不再对浏览器进行任何操作")
        
    except Exception:
        print(u"出错了....")

if __name__ == "__main__":
    check()
