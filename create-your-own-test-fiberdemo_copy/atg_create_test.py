import string

import pandas as pd
from goal_exam_extractor import goal_exam_grade_extractor
from random_data_creator import Exam_data_creator

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
        self.host = 'https://fiberdemoms-cdn.embibe.com'

    def callAPI(self, url, payload, method):
        self.headers[
            'embibe-token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjb3VudHJ5IjoxLCJ1c2VyX3R5cGUiOjEsInBhcmVudF91c2VyX2lkIjoyMDAxMywiY3JlYXRlZCI6MTYxMzcxNzcxOSwib3JnYW5pemF0aW9uX2lkIjoiMSIsImlkIjoxNTAwMDAwMTc0LCJleHAiOjE2MTQ5MjczMTksImRldmljZUlkIjoiMTYxMzU2MzIxNzUyNSIsIm1vYmlsZV92ZXJpZmljYXRpb25fc3RhdHVzIjpmYWxzZSwiZW1haWxfdmVyaWZpY2F0aW9uX3N0YXR1cyI6ZmFsc2UsImVtYWlsIjoiMjAwMTNfODIxMTA5NTcyMDg4NDA5MkBlbWJpYmUtdXNlci5jb20ifQ.Mipd7Q5rA9pJR5yRWwGv2e_9r8hMQv1KmOuEmYLLNX3LB2by-RBtBwjp2SOjmF8Ws9Tc_gfbmx0Y9ab7gX-vow'
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, goal, exam, exam_code):
        df = pd.read_csv('Create_test_data.csv')

        def get_random_string(length):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str

        for i in range(0, 1):
            name = goal+"_"+exam+"_"+str(get_random_string(4))
            time, incorrect_marks, correct_marks, difficuty, section_data, chapter_data, number_of_subject, subject_question_count, subjects = Exam_data_creator(
                exam, goal)
            if section_data=="NA":
                print('Exam config API FAILED GAVE ERROR SO json COULD NOT BE GENERATED')
                df.loc[len(df)] = [exam, goal, exam_code, time, name, incorrect_marks, correct_marks, difficuty,
                                   section_data, chapter_data, 'EXAM CONFIG FAILED/EXAM CONFIGURATION FAILED', "", "NA", "NA", subjects, "",
                                   'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTE3IDExOjM3OjM0IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.xAKYAszvYPOTEWHzdTbfSROvr-mi5yxK28EpFceaWCvfYhMaawTce2vTMlaIGRTi48tLhzvQ__CgUgeN79vdnQ']
                # break
                df.to_csv('Create_test_data.csv', index=False)
            else:
                # print(time,incorrect_marks,correct_marks,difficuty,section_data,chapter_data)
                payload = {
                    "chapter_data": chapter_data,
                    "created_at": "2020-11-19T12:01:22.197Z",
                    "difficulty_level": difficuty,
                    "duration": time,
                    "exam_code": exam_code,
                    "ideal_time_level_to_finish": "avg",
                    "language": "en",
                    "last_modified_at": "2020-11-19T12:01:22.218Z",
                    "marking_scheme": {
                        "nmarks": incorrect_marks,
                        "partial_marking": "false",
                        "pmarks": correct_marks
                    },
                    "name": name,
                    "question_count": 15,
                    "resource_type": "test",
                    "section_data": section_data,
                    "source": "fiber",
                    "test_config": {
                        "algorithm": "greedy",
                        "avg_difficulty_level": 4.1,
                        "avg_ideal_time": 90,
                        "base_entity": "Chapter",
                        "difficulty_level": "avg",
                        "ignore_previous_year_tests": "True",
                        "maximum_difficulty_level": 8,
                        "maximum_ideal_time": 180,
                        "minimum_difficulty_level": 1,
                        "minimum_ideal_time": 0,
                        "mocktest_bundle": "",
                        "no_of_subjects": number_of_subject,
                        "no_of_tests": 1,
                        "std_difficulty_level": 1.2,
                        "std_ideal_time": 45,
                        "subject_question_count": subject_question_count
                    }
                }
                try:
                    # print(json.dumps(payload))

                    response1 = self.callAPI("/fiber_ms/v1/atg/test", json.dumps(payload), "POST")
                    print(response1.json())
                    dict = {}
                    atg_id = response1.json()['atg_id']
                    request_id = response1.json()['request_id']

                    dict['atg_id'] = atg_id
                    dict['request_id'] = request_id
                    print(dict)
                    # ["Exam", "Goal", "Exam_code", 'Time', 'Incorrect_marks', 'Correct_marks', 'Difficulty', 'Section_data',
                    #  'Chapter_data', 'Atg_id', 'Request_id'])

                    df.loc[len(df)] = [exam, goal, exam_code, time, name, incorrect_marks, correct_marks, difficuty,
                                       section_data, chapter_data, atg_id, request_id, "", "", subjects,json.dumps(payload),'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTE3IDExOjM3OjM0IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.xAKYAszvYPOTEWHzdTbfSROvr-mi5yxK28EpFceaWCvfYhMaawTce2vTMlaIGRTi48tLhzvQ__CgUgeN79vdnQ']
                    # break
                    df.to_csv('Create_test_data.csv', index=False)
                except:
                    print('ATG TEST API FAILED GAVE ERROR SO ATG ID COULD NOT BE GENERATED')
                    df.loc[len(df)] = [exam, goal, exam_code, time, name, incorrect_marks, correct_marks, difficuty,
                                       section_data, chapter_data, 'ATG API FAILED', "", "NA", "NA", subjects,"",'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTE3IDExOjM3OjM0IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.xAKYAszvYPOTEWHzdTbfSROvr-mi5yxK28EpFceaWCvfYhMaawTce2vTMlaIGRTi48tLhzvQ__CgUgeN79vdnQ']
                    # break
                    df.to_csv('Create_test_data.csv', index=False)


def ATG_test(goal, exam, exam_code):
    src = Source()
    src.main(goal, exam, exam_code)
    # for ind in df.index:
    #     main(df["Goal"][ind],df["Exam_name"][ind],df["Exam_code"][ind])

# ATG_test("Engineering","JEE Main","kve383631")
