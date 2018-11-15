# -*- coding: utf-8 -*-
import requests
import hashlib
import time
import json
import random


class Youdao(object):
    def __init__(self, msg):
        self.msg = msg
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.D = "ebSeFb%=XZ%T[KZ)c(sy!"
        self.salt = self.get_salt()
        self.sign = self.get_sign()

    def get_md(self, value):
        """md5加密"""
        m = hashlib.md5()
        # m.update(value)
        m.update(value.encode('utf-8'))
        return m.hexdigest()

    def get_salt(self):
        """根据当前时间戳获取salt参数"""
        s = int(time.time() * 1000) + random.randint(0, 10)
        return str(s)

    def get_sign(self):
        """使用md5函数和其他参数，得到sign参数"""
        s = "fanyideskweb" + self.msg + self.salt + self.D
        return self.get_md(s)

    def get_result(self):
        headers = {
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:51.0) Gecko/20100101 Firefox/51.0',
        }
        data = {
            'i': self.msg,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': self.salt,
            'sign': self.sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CL1CKBUTTON',
            'typoResult': 'true'
        }
        html = requests.post(self.url, data=data, headers=headers).text
        # print(html)
        infos = json.loads(html)
        if 'translateResult' in infos:
            try:
                result = infos['translateResult'][0][0]['tgt']
                print(result)
            except:
                pass


if __name__ == '__main__':
    print("欢迎使用，本程序调用有道词典 API 进行翻译\n--自动检测输入语言--")
    while True:
        word = str(input("请输入(按 q 退出)："))
        if (word == 'q'):
            print("感谢使用")
            break
        y = Youdao(word)
        y.get_result()
