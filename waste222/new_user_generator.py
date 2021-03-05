import requests
import string
import random
import json
import time


def generate_random_string(len):
    return ''.join(random.choices(string.ascii_lowercase +
                                  string.digits, k=len))




def getOtp(email,host,otp_token):
    # url = f"http://10.141.10.177:5000/otp/get/{email}"
    if host !='https://preprodms.embibe.com':
        url=f"https://preprodms.embibe.com/ondemandautomation/otp/get/{email}"

        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()["otp"]
    else:
        print(otp_token)
        otp_token=otp_token.replace(' ','').replace('\n','')
        print(otp_token)
        url="http://10.141.10.177:8080/ondemandautomation/getotp"
        payload = {}
        headers = {}
        headers['host'] = host
        headers['otp-token'] = otp_token
        
        

        response = requests.get(url, headers=headers, data=payload)
        print(response.text)
        # print(response.json())

        return response.json()['otp']



def signIn(host):
    if host !='https://preprodms.embibe.com':
        for i in range(2):
            try:
                headers = {
                    'Connection': 'keep-alive',
                    'Origin': 'https://staging-fiber-web.embibe.com',
                    'Content-Type': 'application/json'
                }

                if host == "https://fiberdemoms.embibe.com" or host=="https://fiberdemoms-cdn.embibe.com":
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
                    otp = getOtp(email_id,host,'')

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
    else:
        for i in range(2):
            try:
                headers = {
                    'Connection': 'keep-alive',
                    'Origin': 'https://staging-fiber-web.embibe.com',
                    'Content-Type': 'application/json'
                }

                if host == "https://fiberdemoms.embibe.com" or host=="https://fiberdemoms-cdn.embibe.com":
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
                # print(response.headers["otp-token"])
                # # print(user_id)

                if response.status_code == 201:
                    

                    otp_token = response.headers["otp-token"]
                    # print(type(otp_token))
                    # print(otp_token)

                    otp = getOtp(email_id,host,str(otp_token))
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



def signUp(host):
    if host=='https://preprodms.embibe.com':
        email='testing_fiber_checklist_preprod@embibe.com'
        password='embibe1234'
    else:
        email='testing_fiber_checklist@embibe.com'
        password='embibe1234'



    for i in range(2):
            headers = {
                  'Connection': 'keep-alive',
                  'Accept': 'application/json, text/plain, */*',
                  'Content-Type': 'application/json;charset=UTF-8',
                  'Origin': 'https://staging-fiber-web.embibe.com',
                  'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                }

            if host == "https://fiberdemoms.embibe.com" or host == "https://fiberdemoms-cdn.embibe.com":
                headers["Origin"] = "https://fiber-demo-web.embibe.com"
            
            payload = {"email":email,"password":password,"device_id":"1611312548234"}

            url = f"{host}/user_auth_ms/sign-in"
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                _embibe_token = response.headers["embibe-token"]
                headers['embibe-token'] = _embibe_token

                conn_prof_url = f"{host}/user_auth_ms/connected_profiles"
                response = requests.request("GET",conn_prof_url,headers=headers,data={})

                if response.status_code == 200:
                    embibe_token = response.json().get("data",{}).get("embibe_token")
                    userId = response.json().get("data",{}).get("id")
                    email_id = email
                   
                return {"Email": email_id, "Password": "embibe1234", "embibe-token": embibe_token,"user_id":userId}

            time.sleep(5)

    return None


# print(signUp("https://preprodms.embibe.com"))