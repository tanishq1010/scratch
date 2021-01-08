import requests
import pandas as pd
import json
import random
# from openpyxl import Workbook, load_workbook
from API_call_method import callAPI
# from goal_exam import goal_exam
# from update import *

def _revision():
    # df = goal_exam()
    # df=pd.read_csv('test_file2.csv')
    df1=pd.DataFrame(columns=['Status_code','Response'])

    for i in range(0,1000):
            # child_id = 1500001304
            # embibe_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjb3VudHJ5IjoxLCJ1c2VyX3R5cGUiOjEsImNyZWF0ZWQiOjE2MDk3NTIyMzcsIm9yZ2FuaXphdGlvbl9pZCI6IjEiLCJpZCI6MTUwMDAwMTMwNCwiZXhwIjoxNjEwOTYxODM3LCJtb2JpbGVfdmVyaWZpY2F0aW9uX3N0YXR1cyI6ZmFsc2UsImVtYWlsX3ZlcmlmaWNhdGlvbl9zdGF0dXMiOmZhbHNlLCJlbWFpbCI6IjUwNTQ1ODVfMTA5NjgwNjkzNDA0MDE2OTBAZW1iaWJlLXVzZXIuY29tIn0.icz7gy8WwkU4VBXuCe29YYloaJcBmyDFxx2B9U1hiq0Ie6mN8LU0BufIomOnAvKZ0WW_gz47eN7onst8Yzlx-Q'
            # goal = df['Goal'][ind]
            # exam = df['Exam_name'][ind]
            # print(goal,',',exam)
            # grade = df['Grade'][ind]
            embibe_token='jhadsbhads'
            payload = { 
"user_id":"8317487",
"learnpath_name": "Engineering--JEE Main",
"learnpath_format":"Goal--Exam",
"group_by": "subject",
"offset":0,
"limit":100
}
            LIST=['wasted_attempts','incorrect_attempts','overtime_incorrect_attempts','overtime_correct_attempts']
            response1 = callAPI('POST','https://preprodms.embibe.com',f"/de/jf_analyse/revision-list-question?section_name={random.choice(LIST)}",embibe_token,
                                json.dumps(payload))
            # print(response1.json())
            status_code=response1.status_code
            print(i)
            print(status_code)
                # df1.loc[len(df1)] = [goal, exam, response1.status_code, "", "", "", "", found]
            df1.loc[len(df1)]=[status_code,response1.text]


                # except Exception as e:
                #     df1.loc[len(df1)] = [goal, exam, response1.json(), "", "", "", ""]

        # print(df1)
    df1.to_csv('scratch.csv',index=False)
    # update_sheet('herobanner_home','herobanner_home')



_revision()


        # break

# herobanner_home()