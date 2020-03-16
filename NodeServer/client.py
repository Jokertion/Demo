# -*- coding: utf-8 -*-
import requests


url = "http://127.0.0.1:3000/crypto"

data = {
    "user": "jokertion", "password": "1234abcd"
}
req = requests.post(url,data)
print(req.text)
