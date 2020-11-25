from locust import task, between, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, WorkerRunner
from locust.contrib.fasthttp import FastHttpUser
from random import randrange
from random import randint
import json
import csv
import string
import random
import logging
import time
import gevent
import resource


all_commands = {}
with open("all_commands.txt") as f:
    for line in f:
        (key, val) = line.split()
        all_commands[key] = val
dev = "Raj"
resource.setrlimit(resource.RLIMIT_NOFILE, (10240, 10240))
host = "https://preprodms.embibe.com"


# functions
email_password = []

with open('email_password_embibe.csv', 'r') as csvfile:
    email_password = list (csv.reader(csvfile, delimiter=','))

class UserBehaviour(FastHttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.body = {}

    wait_time = between(5, 9)
    host = "https://preprodms.embibe.com"
    @task
    def achieve_ms_home(self):
        rnum = randrange(len(email_password)-1)

        self.headers['embibe-token'] = email_password[rnum][3]
        self.body = "{ \"exam\": \"10th CBSE\", \"goal\": \"CBSE\"}"

        response = self.client.post(
           f"/achieve_ms/home",
            name="achieve_ms_home", data=self.body, headers=self.headers)

        uri = host + f"/achieve_ms/home"

        curl = "curl --location --request POST '"+ str(uri)+ "' \n"
        curl +="--header 'accept: application/json' \n"
        if 'embibe-token' in self.headers.keys(): 
            curl += "--header 'embibe-token :" + str(self.headers['embibe-token']) + "'\n"
        curl += "--header 'Content-Type: application/json' \n"
        curl += "--header 'Accept-Encoding':'gzip, deflate, br' \n"
        curl += "--header 'Accept':'*/*' \n"
        curl += "--data-raw ' " + str(self.body) + "'"

        file1 = open("curl.txt","w")
        file1.writelines(curl) 
        file1.close()

        file1 = open("dev_host.txt","w")
        dev_host_name = host + "\n" + dev
        file1.writelines(dev_host_name)
        file1.close()
       
        if (response.status_code != 200):
            # print(response.request.headers)
            # print(f"getHomeData -{host}/fiber_ms_lt/v1/home")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
def checker(environment):
    while not environment.runner.state in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
        time.sleep(1)
        if environment.stats.total.fail_ratio > float(all_commands['limit_fail_ratio']):
            logging.error("Test failed due to failure ratio > " + str(float(all_commands['limit_fail_ratio']) * 100) +"%")
            file2 = open("fail_reason.txt","w") 
            if(environment.stats.total.fail_ratio == 1.0):
                file2.writelines("404")
            else:
                file2.writelines("Test failed due to failure ratio > " + str(float(all_commands['limit_fail_ratio']) * 100)+"%") 
            file2.close()
            environment.runner.quit()
            return
        elif environment.stats.total.avg_response_time > int(all_commands['limit_avg_response_time_in_ms']):
            logging.error("Test failed due to average response time ratio > " + str(all_commands['limit_avg_response_time_in_ms']) +" ms")
            environment.runner.quit()
            file2 = open("fail_reason.txt","w") 
            file2.writelines("Test failed due to average response time ratio > " + str(all_commands['limit_avg_response_time_in_ms']) +" ms") 
            file2.close()
            return
        elif environment.stats.total.get_response_time_percentile(0.95) > int(all_commands['limit_95_percentile_response_time_in_ms']):
            logging.error("Test failed due to 95th percentile response time > " + str(all_commands['limit_95_percentile_response_time_in_ms']) +" ms")
            environment.runner.quit()
            file2 = open("fail_reason.txt","w") 
            file2.writelines("Test failed due to 95th percentile response time > " + str(all_commands['limit_95_percentile_response_time_in_ms']) +" ms") 
            file2.close()
            return


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    if not isinstance(environment.runner, WorkerRunner):
        gevent.spawn(checker, environment)