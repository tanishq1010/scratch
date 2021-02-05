import requests
import string
import random
import json
import time


def generate_random_string(len):
    return ''.join(random.choices(string.ascii_lowercase +
                                  string.digits, k=len))




def getOtp(email):
    url = f"http://10.141.10.177:5000/otp/get/{email}"

    payload = {}
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["otp"]


def signUp(host):
    for i in range(2):
        try:
            headers = {
                'Connection': 'keep-alive',
                'Origin': 'https://staging-fiber-web.embibe.com',
                'Content-Type': 'application/json'
            }

            if host == "https://fiberdemoms.embibe.com":
                headers["Origin"] = "https://fiber-demo-web.embibe.com"

            payload = {"first_name": generate_random_string(5),
                       "email": "test-" + generate_random_string(7) + "@embibe.com", "password": "embibe1234",
                       "profile_pic": "https://imagin8ors-temp-dump.s3-ap-southeast-1.amazonaws.com/subject/avatar/ic_avatar1.png",
                       "connected_response": False}
            email_id = payload["email"]
            url = f"{host}/user_auth_ms/sign-up"
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            # user_id=response.json()['data']['user_details']['id']
            # print(response.json())
            # # print(user_id)

            if response.status_code == 201:
                otp = getOtp(email_id)

                otp_token = response.headers["otp-token"]
                embibe_token = response.headers["embibe-token"]

                headers["otp-token"] = otp_token
                payload = {"otp": otp}
                verify_otp_response = requests.request("POST", f"{host}/user_auth_ms/verifyOtp", headers=headers,
                                                       data=json.dumps(payload))

                del headers["otp-token"]
                headers['embibe-token'] = embibe_token

                if verify_otp_response.status_code == 200:
                    payload = {"first_name": "test_child", "primary_goal": "kve97670", "primary_exam": "kve97915",
                               "profile_pic": "https://imagin8ors-temp-dump.s3-ap-southeast-1.amazonaws.com/subject/avatar/ic_avatar1.png",
                               "dreamSelected": [None, None]}
                    add_profile_response = requests.request("POST", f"{host}/user_auth_ms/add_profile", headers=headers,
                                                            data=json.dumps(payload))


                    if add_profile_response.status_code == 200:
                        # print(add_profile_response.json())
                        user_id=add_profile_response.json()['data']['id']
                        embibe_token=add_profile_response.json()['data']['embibe_token']
                        return {"Email": email_id, "Password": "embibe1234", "embibe-token": embibe_token,"user_id":user_id}

            time.sleep(5)

        except Exception as e:
            raise e

    return {"Email": None, "Password": None, "embibe-token": None,'user_id':None}


def signIn(host, email, password):
    for i in range(2):
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://staging-fiber-web.embibe.com',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        if host == "https://fiberdemoms.embibe.com":
            headers["Origin"] = "https://fiber-demo-web.embibe.com"

        payload = {"email": email, "password": password, "device_id": "1611312548234"}
        url = f"{host}/user_auth_ms/sign-in"
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.headers["embibe-token"]

        time.sleep(5)

    return None


# print(signUp("https://preprodms.embibe.com"))