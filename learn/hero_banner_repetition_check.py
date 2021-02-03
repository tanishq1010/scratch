import os
import csv
import json
import string
import random
import requests
import sys
import traceback
import multiprocessing
import pandas as pd
import ast


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json',
        }

    def callAPI2(self, url, payload, method,token):
        self.headers['embibe-token']=token
        response = requests.request(method, url, headers=self.headers, data=payload)
        # if response.status_code != 200:######5233290
        #     print(url + ' - ' + str(response.content))
        # return None
        return response

    def getting_hoerobanner(self, exam, exam_code, goal, goal_code, grade,child_id,token):
        df = pd.read_csv("hero_banner_check.csv")
        payload1 = {
            'primary_exam_code': exam_code,
            'primary_goal': goal_code
        }
        response1 = self.callAPI2("https://preprodms.embibe.com/user_profile/edit_profile", json.dumps(payload1), 'PUT',token)
        # print(response1.status_code)
        payload2 = payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade
        }
        response2 = self.callAPI2(
            f"https://preprodms.embibe.com/fiber_ms/v1/home",
            json.dumps(payload2),
            'POST',token)
        home_data = []
        for item in response2.json():
            if item["content_section_type"] == "HEROBANNER":
                for data in item["content"]:
                    for data in data["data"]:
                        title = str(data["title"])
                        home_data.append(exam)
                        home_data.append(goal)
                        home_data.append(title)
                        home_data.append(child_id)
                        break
                    break
                break
        # print(home_data)
        df.loc[len(df)] = [child_id,home_data[0],home_data[1],home_data[2]]
        df.to_csv("hero_banner_check.csv",index=False)


def main(df_new,child_id,token):
    src = Source()

    df = pd.DataFrame(columns=['Child_id','Exam', 'Goal', 'herobanner title'])
    df.to_csv("hero_banner_check.csv", index=False)
    # print(df_new)
    for ind in df_new.index:
        src.getting_hoerobanner(df_new["Exam"][ind], df_new["Exam_code"][ind], df_new["Goal"][ind],
                                df_new["Goal_code"][ind], df_new["Grade"][ind],child_id,token)
    # print(pd.read_csv('hero_banner_check.csv'))


# df_new = pd.read_csv('goal_exam.csv')
# main(df_new,5233290,'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTEwIDE1OjI2OjM1IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjUyMzMyOTAsImVtYWlsIjoidGVzdF91c2VyX281YzFjNWltQGdtYWlsLmNvbSJ9.drZcB8fi0f8tYOpGZjo8WhMaK5rolsFLUUPvKw9x6fKKOaueo1RxISL5ccn5DLs4iQDDrb_dQNEzV25Tymk9iA')
