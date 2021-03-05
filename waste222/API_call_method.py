import time
import requests


def callAPI(method, host, url, token, payload):
    # if 'https://preprodms.embibe.com' in host:
    #     host ='https://fiberdemoms-cdn.embibe.com'

    headers = {'Connection': 'keep-alive', 'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': token,'embibe-token':token}
    c = 1
    response = ''
    while True:
        if c > 3:
            break
        try:
            response = requests.request(method, host + url, headers=headers, data=payload)
            if response.status_code != 200:
                raise Exception('calling api again')
        except Exception as e:
            print(e)
            c = c + 1
            time.sleep(3)
            continue
        break
    return response
