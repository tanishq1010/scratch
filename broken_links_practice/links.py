import os
import csv
import json
import string
import random
import requests
import sys
import traceback

import pandas as pd
from openpyxl import Workbook, load_workbook


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json',
        }
        # self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method):
        self.headers[
            "embibe-token"] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJjb3VudHJ5IjoxLCJ1c2VyX3R5cGUiOjEsImNyZWF0ZWQiOjE2MDk4NjAzOTYsIm9yZ2FuaXphdGlvbl9pZCI6IjEiLCJpZCI6MTUwMDAwMTMwNCwiZXhwIjoxNjExMDY5OTk2LCJtb2JpbGVfdmVyaWZpY2F0aW9uX3N0YXR1cyI6ZmFsc2UsImVtYWlsX3ZlcmlmaWNhdGlvbl9zdGF0dXMiOmZhbHNlLCJlbWFpbCI6IjUwNTQ1ODVfMTA5NjgwNjkzNDA0MDE2OTBAZW1iaWJlLXVzZXIuY29tIn0.bJRRZyF4eh_N7AhbjRf4SeGvKEmjObVSoTzR7SvofNJFh-BYtWROWNxi8kZaXs2LmFw7StQsg2eMc3iX0ipb4Q'
        response = requests.request(method, url, headers=self.headers, data=payload)

        # if response.status_code != 200:
        #     print(url + ' - ' + str(response.content))
        #     r
        return response

    def main(self, df):
        df1 = pd.read_csv("broken links.csv")
        for ind in df.index:
            learnmap_id = df["Learnmap_id"][ind]
            learnpath_name = df["Learnpath_name"][ind]
            grade = df["Grade"][ind]
            goal=df["Goal"][ind]
            exam=df["Exam"][ind]
            subject=df["Subject"][ind]
            print("----------------new-----------------")
            print("------------------------------------")
            print(learnmap_id)
            # print(exam)
            print(exam)
            print(subject)
            print("\n")

            response1 = self.callAPI(
                f"https://preprodms.embibe.com/fiber_ms/search/books?learn_path={learnpath_name}&query={subject}&section=books&source=Practice%20Page%20Summary&user_id=1500001304",
                '{}', 'GET')

            try:
                print("books available :" ,response1.status_code)

                if response1.status_code == 200:
                    books = True
                else:
                    books = False

            except Exception as e:
                print(traceback.format_exc())
                books = False

            
            response2 = self.callAPI(
                f"https://preprodms.embibe.com/fiber_ms/chapters/recommended-learning-objects?&learnMapId={learnmap_id}&contentTypes=Video",
                '{}', 'GET')
            # print(response2)
            try:
                print("recommended learinig :", response2.status_code)
                if response2.status_code == 200:
                    recommended_learning = True
                else:
                    recommended_learning = False
            except Exception as e:
                print(traceback.format_exc())
                recommended_learning = False

            payload3 = {
    "learnmap_id": learnmap_id,
    "subject": subject
}

            response3 = self.callAPI(
                "https://preprodms.embibe.com/fiber_ms/chapterPractices",
                json.dumps(payload3), 'POST')
            print(response3.status_code)
            try:
                print("topic for practice :", response3.status_code)
                if response3.status_code == 200:
                    topics_practice = True
                else:
                    topics_practice = False
            except Exception as e:
                print(traceback.format_exc())
                topics_practice = False

            payload4 = {
    "board": goal,
    "chapter_name": df['Chapter'][ind],
    "child_id": int(1500001304),
    "exam": exam,
    "goal": goal,
    "grade": str(grade)
}
            response4 = self.callAPI(
                "https://preprodms.embibe.com/fiber_ms/home/filter-test",
                json.dumps(payload4), 'POST')

            try:
                print("all tests :", response4.status_code)
                if response4.status_code == 200:
                    test = True
                else:
                    test = False
            except Exception as e:
                print(traceback.format_exc())
                test = False

            payload5 = {
    "learn_path": learnpath_name,
    "query": "",
    "section": "bookmarked questions",
    "source": "Practice Page Summary",
    "user_id": 1500001304
}
            response5 = self.callAPI(
                "https://preprodms.embibe.com/fiber_ms/search/practice/chapter/bookmarked/questions",
                json.dumps(payload5), 'POST')
            try:
                print("bookmark :", response5.status_code)
                if response5.status_code == 200:
                    bookmark = True
                else:
                    bookmark = False
            except Exception as e:
                print(traceback.format_exc())
                bookmark = False

            response6=self.callAPI(
                f"https://preprodms.embibe.com/fiber_ms/concept_sequence/coverage?&format_reference={df['Format_refrence'][ind]}&learnpath_name={learnpath_name}&test_code=",
                '{}', 'GET')
            response7=self.callAPI(
                f"https://preprodms.embibe.com/fiber_ms/sincerity_score?format_reference={df['Format_refrence'][ind]}&learnpath_format=goal--exam--subject--unit--chapter--topic&learnpath_name={learnpath_name}&type=practice",
                '{}', 'GET')
            response8=self.callAPI(
                f"https://preprodms.embibe.com/fiber_ms/attempt_quality?&format_reference={df['Format_refrence'][ind]}&learnpath_format=goal--exam--subject--unit--chapter--topic&learnpath_name={learnpath_name}&type=practice",
                '{}', 'GET')
            try:
                print("about your progress :", response6.status_code,response7.status_code,response8.status_code)
                if response6.status_code == 200 and response7.status_code == 200 and response8.status_code == 200  :
                    about_your_progress = True
                else:
                    about_your_progress = False
            except Exception as e:
                print(traceback.format_exc())
                about_your_progress = False



            df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind], df["Grade"][ind],
                                 df["Title"][ind], df["Type"][ind], df["Format_refrence"][ind], df["Section_name"][ind],
                                 df["Subject"][ind], df["Subject_tagged"][ind], df["Learnpath_name"][ind],
                                 df["Learnmap_id"][ind], df["Chapter"][ind], books, recommended_learning, topics_practice, test,
                                 bookmark,about_your_progress]
        df1.to_csv("broken links.csv",index=False)


def broken_link(df):
    src = Source()
    return src.main(df)

# goal_exam_grade_extractor()
