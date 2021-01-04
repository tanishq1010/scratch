import requests
import pandas as pd
import json
import random
from openpyxl import Workbook, load_workbook
from API_call_method import callAPI
#from goal_exam import goal_exam


def main():
    df = pd.read_csv('test_file2.csv')
    # df=goal_exam()
    df1 = pd.DataFrame(columns=['Goal', 'Exam', 'Subjects in fiber', 'subjects in  cg api', 'do they match'])
    for ind in df.index:
        goal = df['Goal'][ind]

        exam = df['Exam_name'][ind]

        child_id = 1500001304
        grade = df['Grade'][ind]
        print(goal, ",", exam)
        embibe_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjb3VudHJ5IjoxLCJ1c2VyX3R5cGUiOjEsImNyZWF0ZWQiOjE2MDk3NTIyMzcsIm9yZ2FuaXphdGlvbl9pZCI6IjEiLCJpZCI6MTUwMDAwMTMwNCwiZXhwIjoxNjEwOTYxODM3LCJtb2JpbGVfdmVyaWZpY2F0aW9uX3N0YXR1cyI6ZmFsc2UsImVtYWlsX3ZlcmlmaWNhdGlvbl9zdGF0dXMiOmZhbHNlLCJlbWFpbCI6IjUwNTQ1ODVfMTA5NjgwNjkzNDA0MDE2OTBAZW1iaWJlLXVzZXIuY29tIn0.icz7gy8WwkU4VBXuCe29YYloaJcBmyDFxx2B9U1hiq0Ie6mN8LU0BufIomOnAvKZ0WW_gz47eN7onst8Yzlx-Q'
        format_refrence = df['Format_refrence'][ind]
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade
            
        }

        response1 = callAPI('POST', 'https://preprodms.embibe.com', '/fiber_ms/v1/home/practise', embibe_token,
                            json.dumps(payload))
        url = "/fiber_app/learning_maps/filters/" + str(format_refrence) + "/" + str(goal) + "/" + str(exam)
        response2 = callAPI('GET', 'https://content-demo.embibe.com', url,
                            '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D', '{}')
        try:
            LIST1 = []
            for item in response1.json():
                if item["content_section_type"] == "SUBJECTS":
                    for data in item["content"]:
                        if data["subject"] == "All Subjects":
                            continue
                        else:
                            LIST1.append(data['subject'])
            for i in range(len(LIST1)):
                LIST1[i] = LIST1[i].lower()
            LIST1.sort()

            LIST = []
            for item in response2.json()["Subject"]:
                subject = item["name"]
                LIST.append(subject)

            for i in range(len(LIST)):
                LIST[i] = LIST[i].lower()

            LIST.sort()
            print(LIST1, ",", LIST)
            all_subjects_present = False
            if LIST == LIST1:
                all_subjects_present = True
            df1.loc[len(df1)] = [goal, exam, LIST1, LIST, all_subjects_present]
        except:
            df1.loc[len(df1)] = [goal, exam, '', '', '']

    df1.to_csv('subjects_correctly_displaying.csv')

    # break


main()
