import string
import time
import pandas as pd

import requests
import pandas as pd
import json
import random


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        # self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method, token):
        self.headers[
            'embibe-token'] = token
        response = requests.request(method, url, headers=self.headers, data=payload)
        # if response.status_code != 200:
        #     print(url + ' - ' + str(response.content))
        #     return None
        return response


def API_call(url, payload, method, token,i):
    src = Source()
    response = src.callAPI(url, json.dumps(payload), method, token)
    # print(response.status_code)
    if response.status_code == 200:
        # print(response.json())
        # print(response.status_code,"__________")
        status_code = response.status_code
        # print(response.json())
        # response.json()
        # print(response)
        return response
    else:
        i=i+1
        time.sleep(2)
        # print(i)
        if i<=10:
            response = API_call(url, payload, method, token,i)
        else :
            print("Exit because tries exceeded")
            return response



