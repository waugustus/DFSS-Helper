#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import base64

class BaiduUtils:
    def __init__(self, appid, appsecret):
        if not appid or not appsecret:
            print('''
            [x] 请提供appId与appSecret!
            [x] 参考 https://console.bce.baidu.com/ai/\n\n
            ''')
            exit(1)
        self.appid = appid
        self.appsecret = appsecret

    def getAccessToken(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(
        self.appid, self.appsecret)
        response = requests.get(host)
        return response.json()['access_token']
    
    def getValidCode(self, content, token):
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        img = base64.b64encode(content)
        params = {"image": img, "language_type": "ENG",
              "detect_direction": "false", "paragraph": "false"}
        access_token = token
        request_url = url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        return response.json()['words_result'][0]['words'].replace(' ', '')