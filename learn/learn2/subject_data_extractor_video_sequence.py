import requests
import pandas as pd
import json
from openpyxl import Workbook, load_workbook
# from miscellaneous import *


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method, token):
        self.headers['embibe-token'] = token
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, child_id, board, grade, exam, goal, embibe_token, subject, home_data):
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade,
            "onlyPractise": "false",
            # "fetch_all_content":"true"
        }
        response1 = self.callAPI(
            f"/fiber_ms/v1/home/{subject}",
            json.dumps(payload),
            'POST', embibe_token)
        df=pd.read_csv('video_sequence.csv')
        for item in response1.json():
            # home_data = [child_id, exam, goal, grade]
            l=item["content_section_type"]
            l2='EMBIBEEXPLAINERSVIDEOS'
            if l.find(l2) == 0:
                i=0
                for data in item["content"]:
                    home= []
                    title = data['title']
                    home.append(child_id)
                    home.append(exam)
                    home.append(goal)
                    home.append(title)
                    ID=data['id']
                    subject_tagged=data['subject']
                    home.append(subject_tagged)
                    print(home)
                    # print(home_data)
                    df.loc[len(df)] = [child_id, exam, goal, title,ID,subject_tagged]
                    df.to_csv('video_sequence.csv',index=False)
                    i+=1
                    if subject=="Science":
                        if i>=15:
                            break
                    else:
                      if i>=5:
                        break

            



def subject_data_extractor(child_id, board, grade, exam, goal, embibe_token, subject, home_data):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token, subject, home_data)

# subject_data_extractor("", "", "", "", "",
#                        "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag",
#                        "Science")
