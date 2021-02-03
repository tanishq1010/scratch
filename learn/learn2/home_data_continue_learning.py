import requests
import pandas as pd
import json



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

    def main(self, child_id, board, grade, exam, goal, embibe_token):
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade
        }

        response1 = self.callAPI(
            f"/fiber_ms/v1/home",
            json.dumps(payload),
            'POST', embibe_token)

        df=pd.read_csv("continue_learning.csv")
        for item in response1.json():
            home_data = [child_id, exam, goal,grade]
            if item["content_section_type"] == "CONTINUELEARNING":
                for data in item["content"]:
                    title = data["title"]
                    description = data["description"]
                    id = data["id"]
                    a_string = id
                    split_string = a_string.split("/", 1)
                    id= split_string[0]
                    Type = data["type"]
                    subject_tagged = data["subject"]
                    df.loc[len(df)] = home_data + [Type,id,title,"All Subjects",subject_tagged]
                    df.to_csv("continue_learning.csv",index=False)



def home_data(child_id, board, grade, exam, goal, embibe_token):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token)


# home_data("", "", "", "", "",
#           "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag")
