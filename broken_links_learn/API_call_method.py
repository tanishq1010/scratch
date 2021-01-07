import time
import requests


def callAPI(method, host, url, token, payload):
    headers = {'Connection': 'keep-alive', 'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8',
               'Authorization': token,'embibe-token':token}
    c = 1
    response = None

    for i in range(3):
        response = requests.request(method, host + url, headers=headers, data=payload)
        if response.status_code == 200 and response.json()!= None:
            return response

        time.sleep(3)

    return response

    # while True:
    #     if c > 3:
    #         break
    #     try:
    #         response = requests.request(method, host + url, headers=headers, data=payload)
    #         if response.status_code != 200:
    #             raise Exception('calling api again')
    #     except Exception as e:
    #         print(e)
    #         c = c + 1
    #         time.sleep(3)
    #         continue
    #     break
    # return response
