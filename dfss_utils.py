#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import requests


class DFSSUtils:
    def __init__(self, studentId, password):
        if not studentId or not password:
            print('''
            [x] 请提供账号与密码!\n\n
            ''')
            exit(1)
        self.studentId = studentId
        self.password = password
        self.cookies = {}

    def getValidPNG(self):
        print("[*] 正在获取验证码...\n")
        url = "http://wsyc.dfss.com.cn/validpng.aspx"

        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "image/webp,image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://wsyc.dfss.com.cn/pc-client/wsyc.aspx?stuid=%s" % (self.studentId)
        }


        r = requests.get(url, headers=header, cookies=self.cookies)

        for key in r.cookies.get_dict():
            self.cookies[key] = r.cookies.get_dict()[key]

        return r.content

    def getCookies(self):
        print("[*] 尝试获取Cookies...\n")
        browser = webdriver.Safari()
        browser.get('http://wsyc.dfss.com.cn/login-pc.aspx')

        cookie = browser.get_cookies()

        browser.quit()

        for c in cookie:
            self.cookies[c['name']] = c['value']
        
        return 0

    def login(self, code):
        print("[*] 正在尝试登录...\n")
        url = "http://wsyc.dfss.com.cn/DfssAjax.aspx"

        data = {
            "AjaxMethod": "LOGIN",
            "Account": self.studentId,
            "Pwd": self.password,
            "ValidCode": code
        }

        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://wsyc.dfss.com.cn/login-pc.aspx"
        }

        session = requests.Session()
        r = session.post(url, data=data, headers=header, cookies=self.cookies)

        if r.status_code == 200:
            if r.text != "true":
                print('''
                [x] 登录失败!
                [x] 错误信息: %s\n\n
                '''%(r.text))
                exit(1)
            return r.text
        else:
            print(r.status_code, r.text)
            exit(1)

    def getCarList(self, lessonId, date, start, end, code):
        print("[*] 正在读取%s车辆信息...\n"%(date))
        url = 'http://wsyc.dfss.com.cn/Ajax/StuHdl.ashx?loginType=2&method=loadcarinf&start=%s&end=%s&stuid=%s&carid=&lessonid=%s&changedate=%s&id=1&cartypeid=17&trainsessionid=52&caridfind=&ValidCode=%s' % (
            start, end, self.studentId, lessonId, date, code)
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Referer": "http://wsyc.dfss.com.cn/pc-client/wsyc.aspx?stuid=%s" % (self.studentId)
        }

        r = requests.post(
            url, data={"page": "1", "rows": "1000"}, headers=header, cookies=self.cookies)

        if r.status_code == 200:
            return r.json()
        else:
            print(r.status_code, r.text)
            exit(1)

    def bookCar(self, lessonId, date, start, end, carId, releaseCarId, code):
        print("[*] 尝试预定车辆...\n")
        url = 'http://wsyc.dfss.com.cn/Ajax/StuHdl.ashx?loginType=2&method=yueche&stuid=%s&bmnum=%s&start=%s&end=%s&lessionid=%s&trainpriceid=BD13062400003&lesstypeid=02&date=%s&id=0&carid=%s&ycmethod=03&cartypeid=17&trainsessionid=52&ReleaseCarID=%s&ValidCode=%s' % (
            self.studentId, self.studentId, start, end, lessonId, date, carId, releaseCarId, code)
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Referer": "http://wsyc.dfss.com.cn/pc-client/wsyc.aspx?stuid=%s" % (self.studentId)
        }

        r = requests.post(
            url, headers=header, cookies=self.cookies)

        if r.status_code == 200:
            if r.text != "success":
                print('''
                [x] 约车失败!
                [x] 错误信息: %s\n\n
                '''%(r.text))
                exit(1)
            return r.text
        else:
            print(r.status_code, r.text)
            exit(1)
