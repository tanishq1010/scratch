import time
import requests


def callAPI(method, host, url, token, payload):
    headers = {'Connection': 'keep-alive', 'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': token,'embibe-token':token}
    response = requests.request(method, host + url, headers=headers, data=payload)
    return response
