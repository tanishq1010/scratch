import string

import pandas as pd
from goal_exam_extractor import goal_exam_grade_extractor
from random_data_creator import Exam_data_creator
from API_call_method import API_call
import traceback
import requests
import pandas as pd
import json
import random


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'embibe-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTE3IDExOjM3OjM0IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.xAKYAszvYPOTEWHzdTbfSROvr-mi5yxK28EpFceaWCvfYhMaawTce2vTMlaIGRTi48tLhzvQ__CgUgeN79vdnQ',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8'

        }
        self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method):
        # self.headers[
        #     'embibe-token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTE3IDExOjM3OjM0IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.xAKYAszvYPOTEWHzdTbfSROvr-mi5yxK28EpFceaWCvfYhMaawTce2vTMlaIGRTi48tLhzvQ__CgUgeN79vdnQ'
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        # if response.status_code != 200:
        #     print(url + ' - ' + str(response.content))
        #     return None
        return response

    def main(self, atg_id, difficulty, duration, exam_code, name, request_id):
        df = pd.read_csv('Create_test_data.csv')
        print(atg_id, difficulty, duration, exam_code, name, request_id)
        payload = {
            "atg_id": int(atg_id),
            "create_mocktest_data": "",
            "created_at": "",
            "difficulty_level": str(difficulty),
            "duration": "",
            "exam_code": "",
            "exclude_question_restrictions": {
                "atg_ids": [],
                "is_default": "true",
                "previous_year": "false",
                "x_month_tests": "false",
                "x_value": 3
            },
            "ideal_time_level_to_finish": "",
            "language": "",
            "last_modified_at": "",
            "name": "",
            "question_count": "",
            "request_id": str(request_id),
            "resource_type": "test",
            "source": "fiber"
        }
        response1 = API_call("https://preprodms.embibe.com/fiber_ms/v1/atg/progress", payload, "POST",
                             'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTE3IDExOjM3OjM0IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.xAKYAszvYPOTEWHzdTbfSROvr-mi5yxK28EpFceaWCvfYhMaawTce2vTMlaIGRTi48tLhzvQ__CgUgeN79vdnQ',
                             0)
        try:
            # print(response1.json())
            success = response1.json()['success']
            progress = response1.json()['progress']
            print(success, progress)
            return success, progress
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(response1.status_code)
            success = response1.text
            progress = response1.text

            return response1.text, response1.text

        # break


def progress_check(df):
    src = Source()
    # print(df)
    # print(df[['Success']])
    for ind in df.index:
        print(df["Goal"][ind], df["Exam"][ind])
        if df["Atg_id"][ind] == "ATG API FAILED" or df["Atg_id"][ind] == "EXAM CONFIG FAILED/EXAM CONFIGURATION FAILED":
            # continue
            df['Success'][ind] = "False"
            df.to_csv('Create_test_data.csv', index=False)
        else:
            success, progress = src.main(df['Atg_id'][ind], df['Difficulty'][ind], df['Time'][ind],
                                         df['Exam_code'][ind],
                                         df['Name'][ind], df['Request_id'][ind])
            df['Success'][ind] = success
            df['Progress'][ind] = progress
            df.to_csv('Create_test_data.csv', index=False)
        # return progress

    # df.to_csv('Create_test_data.csv',index=False)

# df = pd.read_csv('Create_test_data.csv')
# progress_check(df)
