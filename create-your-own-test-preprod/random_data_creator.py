import requests
import pandas as pd
import json
import random
import traceback
from goal_exam_extractor import goal_exam_grade_extractor


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method):
        self.headers[
            'embibe-token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTExLTE3IDExOjM3OjM0IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.xAKYAszvYPOTEWHzdTbfSROvr-mi5yxK28EpFceaWCvfYhMaawTce2vTMlaIGRTi48tLhzvQ__CgUgeN79vdnQ'
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def callAPI2(self, url, payload, method, token):
        self.headers['Authorization'] = token
        response = requests.request(method, url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, goal, exam):
        print("\n\n")
        print(goal, exam)
        try:
            exam = exam.lower()
            goal=goal.lower()
            # payload1 = {
            #     "exam_name": exam,
            #     "learnt_embibe": "false",
            #     "namespace": "namespace",
            #     "type": "subject",
            #     "version": "2.0"
            # }
            payload1={
    "version": "2.0",
    "type": "subject",
    "namespace": "embibe",
    "exam_name": exam,
    "goal_name": goal
}

            response1 = self.callAPI(
                f"/fiber_ms/home/exam_config",
                json.dumps(payload1),
                'POST')
            LIST = []
            for item in response1.json()['subject_data']:
                LIST.append(item['name'])
            # print(LIST)

            random_number = random.randint(1, len(LIST))
            LIST11 = []
            for i in range(0, random_number):
                var = random.choice(LIST)
                LIST11.append(random.choice(LIST))
                LIST.remove(var)

            LIST11 = [item.lower() for item in LIST11]
            LIST11 = list(dict.fromkeys(LIST11))

            # print(LIST11)
            dict_exc = {}
            for subject in LIST11:
                # print(subject)
                for item in response1.json()['subject_data']:
                    if item['name'] == subject:
                        dict_exc[subject] = item

            length_of_subject_exam_config = len(response1.json()['subject_data'])

            section_data = (dict_exc)
            LIST = list(dict_exc.keys())
            print(LIST)

            payload2 = {
                "exam_name": exam,
                "learnt_embibe": "false",
                "goal_name":goal,
                "namespace": "namespace",
                "type": "chapter",
                "version": "2.0"
            }

            response2 = self.callAPI(
                f"/fiber_ms/home/exam_config",
                json.dumps(payload2),
                'POST')
            # print(response2.json())
            integer_value = len(response2.json()['chapter_data']) // length_of_subject_exam_config
            dict_2 = {}
            number_of_subjects = len(LIST)
            for subject in LIST:
                print(subject)
                z = random.randint(1, integer_value)
                # z=20
                print(z)
                try:
                    LIST22 = []
                    for item in response2.json()['chapter_data']:
                        if item['subject_name'] == subject:
                            LIST22.append(item)

                    for i in range(0, z):
                        # print(i)
                        var = random.choice(LIST22)
                        # print(var)
                        chapter_name = var['chapter_name']
                        chapter_name = chapter_name.lower()
                        # del var['display_name']
                        del var['chapter_name']
                        # print(chapter_name)
                        dict_2[chapter_name] = var
                        LIST22.remove(var)

                except Exception as e:
                    print(e)
                    LIST22 = []
                    for item in response2.json()['chapter_data']:
                        if item['subject_name'] == subject:
                            LIST22.append(item)
                    # print(len(LIST22))
                    # print(LIST22)
                    z = 1
                    for i in range(0, z):
                        # print(i)
                        var = random.choice(LIST22)
                        # print(var)
                        chapter_name = var['chapter_name']
                        chapter_name=chapter_name.lower()
                        # del var['display_name']
                        del var['chapter_name']
                        # print(var)

                        # print(chapter_name)
                        dict_2[chapter_name] = var
                        LIST22.remove(var)

            # print(len(dict_2))

            chapter_data = (dict_2)
            print("chapter_data--------", chapter_data)
            print("section_data---------", section_data)
            dict_3 = {}
            for i in range(0, len(LIST)):
                subject = LIST[i]
                # print(subject)
                var = dict_exc[subject]['entity_codes'][0]
                var = var['question_count']
                # var= section_data[subject]['question_count']
                dict_3[subject] = var
            # print(dict_3)
            subject_question_count = (dict_3)
            print("subject_question_count--------", subject_question_count)

            try:
                response3 = self.callAPI("/fiber_ms/exam/configurations", "{}", "GET")
                print(response3.json())
                time_list = response3.json()['duration']
                incorrect_marks_list = response3.json()['incorrect_marks']
                correct_marks_list = response3.json()['correct_marks']
                difficulty_list = response3.json()['difficulty_level']
            except Exception as e:
                print(e)
                print("EXAM CONFIGURATION API GAVE ERROR SO TAKING FIXED VALUES ")
                time_list = [int(45)]
                incorrect_marks_list = [int(0)]
                correct_marks_list = [int(4)]
                difficulty_list = ["Easy"]

            return random.choice(time_list), random.choice(incorrect_marks_list), random.choice(
                correct_marks_list), random.choice(
                difficulty_list), section_data, chapter_data, number_of_subjects, subject_question_count, LIST
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            time_list = [int(45)]
            incorrect_marks_list = [int(0)]
            correct_marks_list = [int(4)]
            difficulty_list = ["Easy"]
            # print("sjdbsajkd")
            return random.choice(time_list), random.choice(incorrect_marks_list), random.choice(
                correct_marks_list), random.choice(
                difficulty_list), "NA", "NA", "NA", "NA", "NA"


def Exam_data_creator(exam, goal):
    src = Source()

    # for i in range(0,9):
    return (src.main(goal, exam))
    # break

# Exam_data_creator("CTET Paper 1","Teaching")
