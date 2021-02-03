import pandas as pd
from API_call_method import callAPI
from new_user_generator import signUp
import json

df = pd.read_csv('testfile2.csv')
host = 'https://preprodms.embibe.com'
dictionary = signUp(host)
df1 = pd.DataFrame(
    columns=['Goal', 'Exam', 'Section', 'Title', 'Description', 'Duration', 'Thumbnail', 'Currency', 'ID', 'Subject'])
for ind in df.index:
    goal = df['Goal'][ind]
    exam = df['Exam_name'][ind]
    grade = df['Grade'][ind]
    print(goal, "--", exam)
    payload = {
        "board": goal,
        "child_id": dictionary['user_id'],
        "exam": exam,
        "exam_name": exam,
        "goal": goal,
        "grade": grade,
        "fetch_all_content": True
    }

    # embibe_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjb3VudHJ5IjoxLCJ1c2VyX3R5cGUiOjEsInBhcmVudF91c2VyX2lkIjoxNTAwMDA2MzQ0LCJjcmVhdGVkIjoxNjEyMjcwNTI0LCJvcmdhbml6YXRpb25faWQiOiIxIiwiaWQiOjE1MDAwMDYzNDUsImV4cCI6MTYxMzQ4MDEyNCwiZGV2aWNlSWQiOiIxNjExODU2NDMwMDY4IiwibW9iaWxlX3ZlcmlmaWNhdGlvbl9zdGF0dXMiOmZhbHNlLCJlbWFpbF92ZXJpZmljYXRpb25fc3RhdHVzIjpmYWxzZSwiZW1haWwiOiIxNTAwMDA2MzQ0XzE1Mjg5OTE3OTAwMzcxNDA0QGVtYmliZS11c2VyLmNvbSJ9.zaIn_Q18tJVGpoOxjPYQs1td1HRq_wamuhLOaZ0LxbwS5gSQGqkcKPaWCmZ-Drsm4a_p_-BpVH6_Vt_JSJe-eA'
    embibe_token=dictionary['embibe-token']
    try:
        response = callAPI('POST', host, '/fiber_ms/v1/home/', embibe_token, json.dumps(payload))
        for item in response.json():
            if item['contentType'] == 'Video':
                section_name = item['section_name']
                for item in item['content']:
                    try:
                        title = item['title']
                    except:
                        title = None
                    try:
                        description = item['description']
                    except:
                        description = None
                    try:
                        duration = item['length']
                    except:
                        duration = None
                    try:
                        ID = item['id']
                    except:
                        ID = None
                    try:
                        thumbnail = item['thumb']
                    except:
                        thumbnail = None
                    try:
                        currency = item['currency']
                    except:
                        currency = None
                    try:
                        subject = item['subject']
                    except:
                        subject = None
                    df1.loc[len(df1)] = [goal, exam, section_name, title, description, duration, thumbnail, currency, ID,
                                         subject]
    except:
        df1.loc[len(df1)] = [goal, exam,'', '', '', '', '', '', '',
                             response.text]


    # break
df1.drop_duplicates(inplace=True)
df1.to_csv('test.csv')
